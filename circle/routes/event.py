from datetime import datetime
from io import StringIO

from flask import Blueprint, Response, abort, current_app, jsonify, request
from flask_jwt_extended import jwt_required
from sqlalchemy import and_, or_

from circle.extensions import cache, db, limiter
from circle.models.event import Event, EventTag
from circle.models.lookups import EventStatus, SignupStatus, Tag
from circle.models.signup import Checkin, EventSignup
from circle.schemas import EventCreateSchema, EventFilterSchema, SignupSchema
from utils.helpers import filter_by_university, refresh_public_events_view, resolve_university


events_bp = Blueprint("events", __name__)

STATUS_LABELS = {
    "draft": "Draft",
    "published": "Published",
    "cancelled": "Cancelled",
}

SIGNUP_STATUS_LABELS = {
    "confirmed": "Confirmed",
    "waitlist": "Waitlist",
    "cancelled": "Cancelled",
}


def _get_or_create(model, key, labels):
    instance = model.query.filter_by(key=key).first()
    if not instance:
        instance = model(key=key, label=labels.get(key, key))
        db.session.add(instance)
        db.session.commit()
    return instance


def _get_event_with_university(event_id, university_id):
    event = filter_by_university(Event.query, university_id).filter_by(id=event_id).first()
    if not event:
        abort(404, description="Event not found")
    return event


def _serialize_event(event):
    data = event.as_dict()
    data["tags"] = [tag.tag_id for tag in event.tags]
    return data


@events_bp.before_request
def _ensure_university_header():
    resolve_university()


@events_bp.route("/events", methods=["GET"])
@limiter.limit("60 per minute")
@cache.cached(timeout=30, query_string=True)
def list_events():
    university = resolve_university()
    args = EventFilterSchema().load(request.args)
    published_status = _get_or_create(EventStatus, "published", STATUS_LABELS)

    query = filter_by_university(Event.query, university.id).filter(
        Event.deleted_at.is_(None)
    )
    if args.get("status"):
        status = _get_or_create(EventStatus, args["status"], STATUS_LABELS)
        query = query.filter(Event.status_id == status.id)
    else:
        query = query.filter(Event.status_id == published_status.id)

    if args.get("campus"):
        query = query.join(Event.venue).filter_by(campus_id=args["campus"])
    if args.get("q"):
        pattern = f"%{args['q']}%"
        query = query.filter(or_(Event.title.ilike(pattern), Event.description.ilike(pattern)))
    if args.get("tag"):
        query = query.join(EventTag).join(Tag).filter(Tag.key == args["tag"])
    if args.get("start_from"):
        query = query.filter(Event.start_at >= args["start_from"])
    if args.get("end_to"):
        query = query.filter(Event.end_at <= args["end_to"])

    per_page = args.get("per_page") or current_app.config.get("DEFAULT_PER_PAGE", 20)
    per_page = min(per_page, current_app.config.get("MAX_PER_PAGE", 50))
    pagination = query.order_by(Event.start_at.asc()).paginate(
        page=args.get("page", 1), per_page=per_page, error_out=False
    )
    return jsonify(
        {
            "items": [_serialize_event(event) for event in pagination.items],
            "page": pagination.page,
            "per_page": pagination.per_page,
            "total": pagination.total,
        }
    )


@events_bp.route("/events/<event_id>", methods=["GET"])
def get_event(event_id):
    university = resolve_university()
    event = _get_event_with_university(event_id, university.id)
    return jsonify(_serialize_event(event))


@events_bp.route("/events", methods=["POST"])
@jwt_required()
def create_event():
    university = resolve_university()
    payload = EventCreateSchema().load(request.get_json(force=True))
    draft_status = _get_or_create(EventStatus, "draft", STATUS_LABELS)

    event = Event(
        university_id=university.id,
        club_id=payload.get("club_id"),
        venue_id=payload.get("venue_id"),
        status_id=draft_status.id,
        visibility_type_id=payload.get("visibility_type_id"),
        title=payload.get("title"),
        description=payload.get("description"),
        start_at=payload.get("start_at"),
        end_at=payload.get("end_at"),
        capacity=payload.get("capacity"),
        banner_url=payload.get("banner_url"),
    )
    db.session.add(event)
    db.session.flush()

    tag_ids = payload.get("tag_ids", [])
    for tag_id in tag_ids:
        db.session.add(EventTag(event_id=event.id, tag_id=tag_id))
    db.session.commit()

    return jsonify(_serialize_event(event)), 201


@events_bp.route("/events/<event_id>", methods=["PUT"])
@jwt_required()
def update_event(event_id):
    university = resolve_university()
    event = _get_event_with_university(event_id, university.id)
    payload = EventCreateSchema(partial=True).load(request.get_json(force=True))

    for field in ["title", "description", "capacity", "banner_url", "venue_id", "visibility_type_id", "club_id", "start_at", "end_at"]:
        if field in payload:
            setattr(event, field, payload[field])

    db.session.commit()
    cache.delete_memoized(list_events)
    return jsonify(_serialize_event(event))


@events_bp.route("/events/<event_id>/publish", methods=["POST"])
@jwt_required()
def publish_event(event_id):
    university = resolve_university()
    event = _get_event_with_university(event_id, university.id)
    published_status = _get_or_create(EventStatus, "published", STATUS_LABELS)
    event.status_id = published_status.id
    db.session.commit()
    refresh_public_events_view()
    cache.delete_memoized(list_events)
    return jsonify({"status": "published", "event_id": event.id})


@events_bp.route("/events/<event_id>/cancel", methods=["POST"])
@jwt_required()
def cancel_event(event_id):
    university = resolve_university()
    event = _get_event_with_university(event_id, university.id)
    cancelled_status = _get_or_create(EventStatus, "cancelled", STATUS_LABELS)
    event.status_id = cancelled_status.id
    db.session.commit()
    refresh_public_events_view()
    cache.delete_memoized(list_events)
    return jsonify({"status": "cancelled", "event_id": event.id})


@events_bp.route("/events/<event_id>/signups", methods=["GET"])
@jwt_required()
def export_signups(event_id):
    university = resolve_university()
    event = _get_event_with_university(event_id, university.id)

    output = StringIO()
    output.write("email,status\n")
    for signup in event.signups:
        status = SignupStatus.query.get(signup.status_id)
        status_key = status.key if status else "unknown"
        output.write(f"{signup.email},{status_key}\n")

    return Response(output.getvalue(), mimetype="text/csv")


@events_bp.route("/events/<event_id>/checkin", methods=["POST"])
@jwt_required()
def checkin_attendee(event_id):
    university = resolve_university()
    event = _get_event_with_university(event_id, university.id)
    payload = request.get_json(force=True)
    signup_id = payload.get("signup_id")
    signup = EventSignup.query.filter_by(event_id=event.id, id=signup_id).first()
    if not signup:
        abort(404, description="Signup not found")
    checkin = Checkin(signup_id=signup.id, checked_in_at=datetime.utcnow())
    db.session.add(checkin)
    db.session.commit()
    return jsonify({"checked_in": signup.id})


@events_bp.route("/events/<event_id>/signups", methods=["POST"])
@limiter.limit("10 per minute")
def create_signup(event_id):
    university = resolve_university()
    event = _get_event_with_university(event_id, university.id)
    payload = SignupSchema().load(request.get_json(force=True))

    confirmed_status = _get_or_create(SignupStatus, "confirmed", SIGNUP_STATUS_LABELS)
    waitlist_status = _get_or_create(SignupStatus, "waitlist", SIGNUP_STATUS_LABELS)

    existing = EventSignup.query.filter_by(event_id=event.id, email=payload["email"]).first()
    if existing:
        status = SignupStatus.query.get(existing.status_id)
        return (
            jsonify(
                {
                    "signup_id": existing.id,
                    "status": status.key if status else "unknown",
                    "waitlist_position": existing.waitlist_position,
                }
            ),
            200,
        )

    confirmed_count = EventSignup.query.filter_by(event_id=event.id, status_id=confirmed_status.id).count()
    waitlist_position = None
    signup_status = confirmed_status

    if event.capacity and confirmed_count >= event.capacity:
        signup_status = waitlist_status
        waitlist_position = (
            EventSignup.query.filter_by(event_id=event.id, status_id=waitlist_status.id).count()
            + 1
        )

    signup = EventSignup(
        event_id=event.id,
        user_id=payload.get("user_id"),
        email=payload.get("email"),
        status_id=signup_status.id,
        waitlist_position=waitlist_position,
    )
    db.session.add(signup)
    db.session.commit()

    return jsonify({"signup_id": signup.id, "status": signup_status.key, "waitlist_position": waitlist_position}), 201


@events_bp.route("/signups/<signup_id>/cancel", methods=["POST"])
def cancel_signup(signup_id):
    university = resolve_university()
    signup = (
        EventSignup.query.join(Event)
        .filter(and_(EventSignup.id == signup_id, Event.university_id == university.id))
        .first()
    )
    if not signup:
        abort(404, description="Signup not found")

    cancelled_status = _get_or_create(SignupStatus, "cancelled", SIGNUP_STATUS_LABELS)
    signup.status_id = cancelled_status.id
    db.session.commit()
    return jsonify({"cancelled": signup.id})

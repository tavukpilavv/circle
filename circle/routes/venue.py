from datetime import datetime

from flask import Blueprint, abort, jsonify, request

from datetime import datetime

from flask import Blueprint, abort, jsonify, request
from flask_jwt_extended import jwt_required

from circle.auth import require_roles
from circle.extensions import db, limiter
from circle.models.venue import Venue, VenueBlock
from utils.helpers import filter_by_university, resolve_university


venues_bp = Blueprint("venues", __name__)


@venues_bp.route("/venues", methods=["GET"])
@limiter.limit("30 per minute")
def list_venues():
    university = resolve_university()
    query = filter_by_university(Venue.query, university.id)
    venues = query.filter(Venue.deleted_at.is_(None)).all()
    return jsonify([venue.as_dict() for venue in venues])


@venues_bp.route("/venues", methods=["POST"])
@jwt_required()
@require_roles("org_admin", "venue_admin")
@limiter.limit("15 per minute")
def create_venue():
    university = resolve_university()
    payload = request.get_json(force=True)
    venue = Venue(
        university_id=university.id,
        campus_id=payload.get("campus_id"),
        name=payload.get("name"),
        address=payload.get("address"),
        capacity=payload.get("capacity"),
        venue_type_id=payload.get("venue_type_id"),
    )
    db.session.add(venue)
    db.session.commit()
    return jsonify(venue.as_dict()), 201


@venues_bp.route("/venues/<venue_id>", methods=["PUT"])
@jwt_required()
@require_roles("org_admin", "venue_admin")
@limiter.limit("15 per minute")
def update_venue(venue_id):
    university = resolve_university()
    venue = filter_by_university(Venue.query, university.id).filter_by(id=venue_id).first()
    if not venue:
        abort(404, description="Venue not found")
    payload = request.get_json(force=True)
    for field in ["name", "address", "capacity", "campus_id", "venue_type_id"]:
        if field in payload:
            setattr(venue, field, payload[field])
    db.session.commit()
    return jsonify(venue.as_dict())


@venues_bp.route("/venues/<venue_id>", methods=["DELETE"])
@jwt_required()
@require_roles("org_admin", "venue_admin")
@limiter.limit("10 per minute")
def delete_venue(venue_id):
    university = resolve_university()
    venue = filter_by_university(Venue.query, university.id).filter_by(id=venue_id).first()
    if not venue:
        abort(404, description="Venue not found")
    venue.soft_delete()
    db.session.commit()
    return jsonify({"deleted": venue.id})


@venues_bp.route("/venue-blocks", methods=["POST"])
@jwt_required()
@require_roles("org_admin", "venue_admin")
@limiter.limit("10 per minute")
def create_block():
    payload = request.get_json(force=True)
    venue_id = payload.get("venue_id")
    university = resolve_university()
    venue = filter_by_university(Venue.query, university.id).filter_by(id=venue_id).first()
    if not venue:
        abort(404, description="Venue not found")

    block = VenueBlock(
        venue_id=venue.id,
        start_at=datetime.fromisoformat(payload.get("start_at")),
        end_at=datetime.fromisoformat(payload.get("end_at")),
        reason=payload.get("reason"),
    )
    db.session.add(block)
    db.session.commit()
    return jsonify(block.as_dict()), 201

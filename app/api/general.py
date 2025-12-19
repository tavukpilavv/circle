import os
from urllib.parse import urlparse

from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    verify_jwt_in_request
)

from app import db
from app.models import Community, Event, User, Rating
from app.utils import upload_file

bp = Blueprint("general", __name__)

# -------------------------
# Helpers
# -------------------------
def is_valid_http_url(url: str) -> bool:
    try:
        u = urlparse((url or "").strip())
        return u.scheme in ("http", "https") and bool(u.netloc)
    except Exception:
        return False

def is_super_admin(user: User) -> bool:
    # handle both spellings to avoid breaking your existing DB / logic
    return (user.role or "").lower() in ("super_admin", "superadmin")

def is_admin(user: User) -> bool:
    return (user.role or "").lower() == "admin"


# =========================
# EVENTS
# =========================

@bp.route("/events", methods=["GET"])
def get_events():
    try:
        # optional JWT to set "registered" flag
        verify_jwt_in_request(optional=True)
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id) if current_user_id else None

        q = request.args.get("q")
        query = Event.query
        if q:
            query = query.filter(Event.title.contains(q))

        events = query.all()
        output = []

        for e in events:
            organizer_name = "Unknown"
            community_name = "Genel"

            if e.host_community:
                community_name = e.host_community.name
                organizer_name = e.host_community.university or "Unknown"

            is_registered = False
            is_rated = False
            user_rating = 0
            user_comment = ""

            if current_user:
                if e in current_user.registered_events:
                    is_registered = True

                user_rating_obj = Rating.query.filter_by(
                    user_id=current_user.id,
                    event_id=e.id
                ).first()
                if user_rating_obj:
                    is_rated = True
                    user_rating = user_rating_obj.score or 0
                    user_comment = user_rating_obj.comment or ""

            output.append({
                "id": e.id,
                "name": e.title,
                "title": e.title,
                "date": e.date,
                "time": e.time,
                "location": e.location,
                "image": e.image_url,  # keep frontend compatibility
                "alt": e.title,
                "community_name": community_name,
                "organizer": organizer_name,
                "capacity": e.capacity,
                "description": e.description,
                "registered": is_registered,
                "rating": e.rating or 0,
                "ratingCount": e.rating_count or 0,
                "participant_count": e.participants.count(),
                "is_rated": is_rated,
                "user_rating": user_rating,
                "user_comment": user_comment
            })

        return jsonify(output), 200

    except Exception as e:
        current_app.logger.error(f"Event List Error: {str(e)}")
        return jsonify({"error": "Etkinlikler getirilemedi."}), 500


@bp.route("/events/create", methods=["POST"])
@jwt_required()
def create_event():
    """Etkinlik Oluşturma (Admin Kontrollü)"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "Kullanıcı bulunamadı"}), 404

        target_community_id = None
        club_name = request.form.get("club")

        # admin => only their managed community
        if is_admin(user):
            if user.managed_community:
                target_community_id = user.managed_community.id
            else:
                return jsonify({"error": "Yönettiğiniz bir kulüp yok!"}), 403

        # super_admin => may pick club or community_id
        elif is_super_admin(user):
            if club_name:
                found = Community.query.filter_by(name=club_name).first()
                if found:
                    target_community_id = found.id
            if not target_community_id:
                target_community_id = request.form.get("community_id")

        if not target_community_id:
            return jsonify({"error": "Kulüp seçilmeli."}), 400

        # ✅ already file upload supported (image/file)
        image_url = upload_file(
            request.files.get("file") or request.files.get("image"),
            folder="events"
        )

        title = request.form.get("name") or request.form.get("eventName") or request.form.get("title")

        new_event = Event(
            title=title,
            date=request.form.get("date"),
            time=request.form.get("time"),
            location=request.form.get("location"),
            capacity=request.form.get("capacity"),
            description=request.form.get("description"),
            community_id=target_community_id,
            image_url=image_url
        )

        db.session.add(new_event)
        db.session.commit()
        return jsonify({"message": "Etkinlik oluşturuldu!"}), 201

    except Exception as e:
        current_app.logger.error(f"Event Create Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@bp.route("/events/<int:id>/register", methods=["POST"])
@jwt_required()
def register_event(id):
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        event = Event.query.get(id)

        if not user or not event:
            return jsonify({"error": "Hata"}), 404

        if event in user.registered_events:
            return jsonify({"message": "Zaten kayıtlısınız"}), 400

        user.registered_events.append(event)
        db.session.commit()
        return jsonify({"message": "Kayıt Başarılı!"}), 200

    except Exception as e:
        current_app.logger.error(f"Register Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@bp.route("/events/<int:id>/rate", methods=["POST"])
@jwt_required()
def rate_event(id):
    """Puan Verme (Ekleme veya Güncelleme)"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json() or {}

        rating_val = data.get("rating")
        feedback_text = data.get("feedback")
        is_anonymous = data.get("is_anonymous", False)

        event = Event.query.get(id)
        user = User.query.get(user_id)
        if not event or not user:
            return jsonify({"error": "Hata"}), 404

        existing = Rating.query.filter_by(user_id=user.id, event_id=event.id).first()

        if existing:
            old_score = existing.score or 0
            existing.score = rating_val
            existing.comment = feedback_text
            existing.is_anonymous = is_anonymous

            current_total_score = (event.rating or 0) * (event.rating_count or 0)
            new_total_score = current_total_score - old_score + rating_val
            event.rating = round(new_total_score / (event.rating_count or 1), 1)

            db.session.commit()
            return jsonify({"message": "Puanınız güncellendi.", "new_rating": event.rating}), 200

        # New rating
        new_rating_instance = Rating(
            user_id=user.id,
            event_id=event.id,
            score=rating_val,
            comment=feedback_text,
            is_anonymous=is_anonymous
        )
        db.session.add(new_rating_instance)

        new_count = (event.rating_count or 0) + 1
        new_rating = (((event.rating or 0) * (event.rating_count or 0)) + rating_val) / new_count

        event.rating = round(new_rating, 1)
        event.rating_count = new_count

        db.session.commit()
        return jsonify({"message": "Geri bildiriminiz kaydedildi.", "new_rating": event.rating}), 200

    except Exception as e:
        current_app.logger.error(f"Rating Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@bp.route("/events/<int:id>/participants", methods=["GET"])
@jwt_required()
def get_event_participants(id):
    """Katılımcı Listesi (Admin)"""
    try:
        requester_id = get_jwt_identity()
        requester = User.query.get(requester_id)
        event = Event.query.get(id)

        if not event or not requester:
            return jsonify({"error": "Hata"}), 404

        authorized = False
        if is_super_admin(requester):
            authorized = True
        elif is_admin(requester):
            if event.host_community and event.host_community.admin_id == requester.id:
                authorized = True

        if not authorized:
            return jsonify({"error": "Yetkiniz yok"}), 403

        participants_list = []
        for p in event.participants:
            participants_list.append({
                "first_name": p.first_name,
                "last_name": p.last_name,
                "email": p.email,
                "avatar_url": p.avatar_url
            })

        return jsonify(participants_list), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/events/<int:id>/reviews", methods=["GET"])
def get_event_reviews(id):
    try:
        verify_jwt_in_request(optional=True)
        current_user_id = get_jwt_identity()

        event = Event.query.get(id)
        if not event:
            return jsonify({"error": "Etkinlik bulunamadı"}), 404

        reviews = []
        for r in event.feedbacks:
            user_name = "Incognito User"
            if not r.is_anonymous:
                user = User.query.get(r.user_id)
                if user:
                    user_name = f"{user.first_name} {user.last_name}" if user.first_name else (user.username or "User")

            is_current_user = bool(current_user_id and r.user_id == current_user_id)

            reviews.append({
                "id": r.id,
                "user": user_name,
                "rating": r.score,
                "comment": r.comment,
                "isAnonymous": r.is_anonymous,
                "isCurrentUser": is_current_user,
                "created_at": r.created_at.isoformat() if r.created_at else None
            })

        reviews.sort(key=lambda x: x["created_at"] or "", reverse=True)
        return jsonify(reviews), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/reviews/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_review(id):
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        review = Rating.query.get(id)

        if not review:
            return jsonify({"error": "Yorum bulunamadı"}), 404

        if review.user_id != user_id and not (is_admin(user) or is_super_admin(user)):
            return jsonify({"error": "Yetkiniz yok"}), 403

        event = Event.query.get(review.event_id)

        db.session.delete(review)
        db.session.commit()

        if event:
            ratings = Rating.query.filter_by(event_id=event.id).all()
            count = len(ratings)
            if count > 0:
                total = sum(r.score for r in ratings)
                event.rating = round(total / count, 1)
            else:
                event.rating = 0
            event.rating_count = count
            db.session.commit()

        return jsonify({"message": "Review deleted"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/events/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_event(id):
    event = Event.query.get(id)
    if event:
        db.session.delete(event)
        db.session.commit()
        return jsonify({"message": "Silindi"}), 200
    return jsonify({"error": "Bulunamadı"}), 404


# =========================
# COMMUNITIES
# =========================

@bp.route("/communities", methods=["GET"])
def get_communities():
    try:
        # optional login; community page does not need joined anymore
        verify_jwt_in_request(optional=True)

        comms = Community.query.filter_by(is_approved=True).all()
        output = []

        for c in comms:
            output.append({
                "id": c.id,
                "name": c.name,
                "description": c.description,
                "image_url": c.image_url,
                "website_url": c.external_link,
                "members_count": c.members.count()
            })

        return jsonify(output), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/communities", methods=["POST"])
@jwt_required()
def create_community_multipart():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "Unauthorized"}), 401

        if not (is_admin(user) or is_super_admin(user)):
            return jsonify({"error": "Only admins can create communities"}), 403

        name = (request.form.get("name") or "").strip()
        description = (request.form.get("description") or "").strip()
        website_url = (request.form.get("website_url") or "").strip()

        if not name:
            return jsonify({"error": "name is required"}), 400
        if not description:
            return jsonify({"error": "description is required"}), 400
        if not is_valid_http_url(website_url):
            return jsonify({"error": "website_url must be a valid http(s) URL"}), 400

        image_file = request.files.get("image") or request.files.get("file")
        if not image_file:
            return jsonify({"error": "image file is required"}), 400

        image_url = upload_file(image_file, folder="communities")
        if not image_url:
            return jsonify({"error": "Image upload failed"}), 500

        existing = Community.query.filter_by(name=name).first()
        if existing:
            return jsonify({"error": "Community name already exists"}), 409

        new_c = Community(
            name=name,
            description=description,
            image_url=image_url,
            external_link=website_url,
            is_approved=True,
            admin_id=user.id
        )

        db.session.add(new_c)
        db.session.commit()

        return jsonify({
            "message": "Community created",
            "community": {
                "id": new_c.id,
                "name": new_c.name,
                "description": new_c.description,
                "image_url": new_c.image_url,
                "website_url": new_c.external_link,
                "members_count": new_c.members.count()
            }
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/communities/pending", methods=["GET"])
def get_pending_communities():
    try:
        comms = Community.query.filter_by(is_approved=False).all()
        output = []
        for c in comms:
            output.append({
                "id": c.id,
                "name": c.name,
                "university": c.university,
                "description": c.description,
                "short_description": c.short_description,
                "image": c.image_url,
                "joined": False,
                "member_count": c.members.count()
            })
        return jsonify(output), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# KEEP OLD JSON CREATE ENDPOINT (so old frontend doesn’t break)
@bp.route("/communities/create", methods=["POST"])
@jwt_required()
def create_community():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return jsonify({"error": "Unauthorized"}), 401

        if not (is_admin(user) or is_super_admin(user)):
            return jsonify({"error": "Only admins can create communities"}), 403

        data = request.get_json() or {}
        file_url = data.get("clubImage")

        new_c = Community(
            name=data.get("clubName"),
            university=data.get("university"),
            category=data.get("category"),
            short_description=data.get("shortDescription"),
            description=data.get("description"),
            contact_person=data.get("contactName"),
            contact_email=data.get("email"),
            instagram_link=data.get("instagram"),
            external_link=data.get("otherLink"),
            image_url=file_url,
            proof_document_url=file_url,
            is_approved=True,
            admin_id=user.id
        )

        db.session.add(new_c)
        db.session.commit()

        # Admin auto join (optional)
        user.joined_communities.append(new_c)
        db.session.commit()

        return jsonify({"message": "Community created"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/communities/<int:id>/join", methods=["POST"])
@jwt_required()
def join_community(id):
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        comm = Community.query.get(id)

        if not user or not comm:
            return jsonify({"error": "Hata"}), 404

        if comm in user.joined_communities:
            return jsonify({"message": "Zaten üyesiniz"}), 400

        user.joined_communities.append(comm)
        db.session.commit()
        return jsonify({"message": "Katılım Başarılı!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/communities/applications", methods=["GET"])
@jwt_required()
def get_applications():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        # allow both spellings
        if not user or not is_super_admin(user):
            return jsonify({"error": "Yetkiniz yok"}), 403

        pending = Community.query.filter_by(is_approved=False).all()
        output = [{
            "id": c.id,
            "name": c.name,
            "proof_document": c.proof_document_url,
            "contact_person": c.contact_person
        } for c in pending]

        return jsonify(output), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/communities/approve", methods=["POST"])
@jwt_required()
def approve_community():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        data = request.get_json() or {}
        cid = data.get("id")

        if not user or not is_super_admin(user):
            return jsonify({"error": "Yetkiniz yok"}), 403

        comm = Community.query.get(cid)
        if not comm:
            return jsonify({"error": "Bulunamadı"}), 404

        comm.is_approved = True

        # promote admin of that community (keep your logic)
        admin_user = User.query.get(comm.admin_id)
        if admin_user:
            admin_user.role = "admin"

        db.session.commit()
        return jsonify({"success": True, "message": "Onaylandı"}), 200

    except Exception as e:
        current_app.logger.error(f"approve_community error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@bp.route("/communities/apply", methods=["POST"])
@jwt_required()
def apply_community():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "Unauthorized"}), 401

        data = request.get_json() or {}

        existing = Community.query.filter_by(name=data.get("clubName")).first()
        if existing:
            return jsonify({"error": "Community name already exists"}), 409

        new_c = Community(
            name=data.get("clubName"),
            university=data.get("university"),
            category=data.get("category"),
            short_description=data.get("shortDescription"),
            description=data.get("description"),
            contact_person=data.get("contactName"),
            contact_email=data.get("email"),
            instagram_link=data.get("instagram"),
            external_link=data.get("otherLink"),
            image_url=data.get("clubImage"),
            proof_document_url=data.get("clubImage"),
            is_approved=False,
            admin_id=user.id
        )

        db.session.add(new_c)
        db.session.commit()

        return jsonify({"message": "Application submitted"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

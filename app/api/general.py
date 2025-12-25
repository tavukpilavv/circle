import os
from urllib.parse import urlparse
from datetime import datetime, timedelta # timedelta eklendi

from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    verify_jwt_in_request
)

from app import db
from app.models import Community, Event, User, Rating
from app.utils import upload_file
from app.services.image_service import upload_image
from sqlalchemy import func

bp = Blueprint("general", __name__)


# =========================
# HELPERS
# =========================
def is_valid_http_url(url: str) -> bool:
    try:
        u = urlparse((url or "").strip())
        return u.scheme in ("http", "https") and bool(u.netloc)
    except Exception:
        return False


def role_lower(user: User) -> str:
    return (user.role or "").lower()


def is_super_admin(user: User) -> bool:
    return role_lower(user) in ("super_admin", "superadmin")


def is_admin(user: User) -> bool:
    return role_lower(user) == "admin"


def _is_multipart_request() -> bool:
    ct = (request.content_type or "").lower()
    return "multipart/form-data" in ct

# --- YENİ HELPER: TÜRKİYE SAATİ ---
def get_turkey_time():
    # Render sunucusu UTC çalışır. Türkiye UTC+3'tür.
    return datetime.utcnow() + timedelta(hours=3)


# =========================
# EVENTS
# =========================
@bp.route("/events", methods=["GET"])
def get_events():
    try:
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
                "image": e.image_url,     
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
                "user_comment": user_comment,
                "community_id": e.community_id
            })

        return jsonify(output), 200

    except Exception as e:
        current_app.logger.error(f"Event List Error: {str(e)}")
        return jsonify({"error": "Etkinlikler getirilemedi."}), 500


@bp.route("/events/create", methods=["POST"])
@jwt_required()
def create_event():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "Kullanıcı bulunamadı"}), 404

        target_community_id = None
        r = role_lower(user)

        if r == "admin":
            if user.managed_community:
                target_community_id = user.managed_community.id
            else:
                return jsonify({"error": "Yönettiğiniz bir kulüp yok!"}), 403
        elif r in ("super_admin", "superadmin"):
            target_community_id = request.form.get("community_id")
        else:
            return jsonify({"error": "Yetkiniz yok"}), 403

        if not target_community_id:
            return jsonify({"error": "Kulüp seçilmeli."}), 400

        image_file = request.files.get("image")
        image_url = None
        
        if image_file:
            try:
                image_url = upload_image(image_file, folder="circle_events")
            except Exception as e:
                return jsonify({"error": f"Resim yüklenemedi: {str(e)}"}), 400

        title = request.form.get("title") or request.form.get("name")
        date = request.form.get("date")
        time = request.form.get("time")
        location = request.form.get("location")
        description = request.form.get("description")
        capacity = request.form.get("capacity")

        if not title:
            return jsonify({"error": "Etkinlik başlığı gereklidir."}), 400

        new_event = Event(
            title=title,
            date=date,
            time=time,
            location=location,
            capacity=int(capacity) if capacity and capacity.isdigit() else 0,
            description=description,
            community_id=target_community_id,
            image_url=image_url
        )

        db.session.add(new_event)
        db.session.commit()
        return jsonify({"message": "Etkinlik başarıyla oluşturuldu!"}), 201

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
    
@bp.route("/events/<int:id>/unregister", methods=["POST"])
@jwt_required()
def unregister_event(id):
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        event = Event.query.get(id)

        if not user or not event:
            return jsonify({"error": "Not found"}), 404

        if event not in user.registered_events:
            return jsonify({"message": "Not registered"}), 400

        user.registered_events.remove(event)
        db.session.commit()

        return jsonify({"message": "Unregistered successfully"}), 200

    except Exception as e:
        current_app.logger.error(f"Unregister Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@bp.route("/events/<int:id>/rate", methods=["POST"])
@jwt_required()
def rate_event(id):
    """Add/Update rating"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json() or {}

        rating_val = data.get("rating")
        feedback_text = data.get("feedback")
        is_anonymous = data.get("is_anonymous", False)

        event = Event.query.get(id)
        user = User.query.get(user_id)
        
        if not event or not user:
            return jsonify({"error": "Hata: Etkinlik veya kullanıcı bulunamadı."}), 404

        # 1. SIKI KATILIM KONTROLÜ
        if event not in user.registered_events:
             return jsonify({"error": "Sadece etkinliğe kayıtlı katılımcılar yorum yapabilir."}), 403

        # 2. TARİH VE SAAT KONTROLÜ (TÜRKİYE SAATİ FİX)
        if event.date:
            try:
                event_time = event.time if event.time else "00:00"
                event_dt_str = f"{event.date} {event_time}"
                event_dt_obj = datetime.strptime(event_dt_str, "%Y-%m-%d %H:%M")
                
                # Render (UTC) vs Türkiye (UTC+3) farkını düzeltiyoruz
                current_tr_time = get_turkey_time()
                
                if current_tr_time < event_dt_obj:
                     return jsonify({"error": "Etkinlik henüz bitmediği için yorum yapamazsınız."}), 400
            except ValueError:
                pass

        # 3. GÜNCELLEME MANTIĞI
        existing = Rating.query.filter_by(user_id=user.id, event_id=event.id).first()

        if existing:
            old_score = existing.score or 0
            existing.score = rating_val
            existing.comment = feedback_text
            existing.is_anonymous = is_anonymous

            current_total = (event.rating or 0) * (event.rating_count or 0)
            new_total = current_total - old_score + rating_val
            
            count = event.rating_count if event.rating_count > 0 else 1
            event.rating = round(new_total / count, 1)

            db.session.commit()
            return jsonify({"message": "Yorumunuz güncellendi.", "new_rating": event.rating}), 200

        # Yeni Yorum Ekleme
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
        return jsonify({"message": "Yorumunuz kaydedildi.", "new_rating": event.rating}), 200

    except Exception as e:
        current_app.logger.error(f"Rating Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@bp.route("/events/<int:id>/participants", methods=["GET"])
@jwt_required()
def get_event_participants(id):
    """Participants list (Fixed & Safer Query)"""
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

        # --- DÜZELTİLEN KISIM: .any() SORGUSU ---
        # "registered_events" listesinin içinde ID'si bu event olan var mı?
        # Bu yöntem en hatasız çalışan yöntemdir.
        participants = User.query.filter(User.registered_events.any(id=id)).all()

        participants_list = []
        for p in participants:
            participants_list.append({
                "first_name": p.first_name,
                "last_name": p.last_name,
                "email": p.email,
                "avatar_url": p.avatar_url
            })

        return jsonify(participants_list), 200

    except Exception as e:
        # Hata detayını terminale yazdıralım ki Render loglarında görebilesin
        print(f"DEBUG: Participants Error: {str(e)}") 
        return jsonify({"error": str(e)}), 500


@bp.route("/events/<int:id>/reviews", methods=["GET"])
@jwt_required()
def get_event_reviews(id):
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id) 

        if not (is_admin(user) or is_super_admin(user)):
             return jsonify({"error": "Yorumları görüntüleme yetkiniz yok."}), 403
        
        event = Event.query.get(id)
        if not event:
            return jsonify({"error": "Etkinlik bulunamadı"}), 404

        reviews = []
        for r in event.feedbacks:
            user_name = "Incognito User"
            if not r.is_anonymous:
                u = User.query.get(r.user_id)
                if u:
                    user_name = f"{u.first_name} {u.last_name}" if u.first_name else (u.username or "User")

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
            return jsonify({"error": "Club name is required"}), 400
        if not description:
            return jsonify({"error": "Description is required"}), 400

        image_file = request.files.get("image") or request.files.get("file")
        image_url = None
        
        if image_file:
            try:
                image_url = upload_image(image_file, folder="communities")
            except Exception as e:
                print(f"Resim yükleme hatası: {e}")
                return jsonify({"error": "Resim yüklenirken hata oluştu."}), 500

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

        try:
            new_c.members.append(user)
            db.session.commit()
        except:
            pass

        return jsonify({
            "message": "Community created successfully",
            "community": {
                "id": new_c.id,
                "name": new_c.name,
                "image_url": new_c.image_url,
                "website_url": new_c.external_link
            }
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/communities/options", methods=["GET"])
@jwt_required()
def communities_options_for_event():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Unauthorized"}), 401

    r = role_lower(user)

    if r in ("super_admin", "superadmin"):
        comms = Community.query.filter_by(is_approved=True).all()
        return jsonify([{"id": c.id, "name": c.name} for c in comms]), 200

    if r == "admin":
        if not user.managed_community:
            return jsonify([]), 200
        c = user.managed_community
        return jsonify([{"id": c.id, "name": c.name}]), 200

    return jsonify([]), 200


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


@bp.route("/communities/create", methods=["POST"])
@jwt_required()
def create_community_legacy_json():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "Unauthorized"}), 401

        if not (is_admin(user) or is_super_admin(user)):
            return jsonify({"error": "Only admins can create communities"}), 403

        data = request.get_json() or {}

        file_url = data.get("clubImage")

        website_url = (data.get("website_url") or data.get("otherLink") or "").strip()

        new_c = Community(
            name=data.get("clubName"),
            university=data.get("university"),
            category=data.get("category"),
            short_description=data.get("shortDescription"),
            description=data.get("description"),
            contact_person=data.get("contactName"),
            contact_email=data.get("email"),
            instagram_link=data.get("instagram"),
            external_link=website_url,
            image_url=file_url,
            proof_document_url=file_url,
            is_approved=True,
            admin_id=user.id
        )

        db.session.add(new_c)
        db.session.commit()

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

        club_name = (request.form.get("clubName") or request.form.get("name") or "").strip()
        description = (request.form.get("description") or "").strip()
        website_url = (request.form.get("website_url") or request.form.get("websiteUrl") or "").strip()
        
        university = (request.form.get("university") or "").strip()
        category = (request.form.get("category") or "").strip()
        contact_name = (request.form.get("contactName") or "").strip()
        email = (request.form.get("email") or "").strip()

        if not club_name:
            return jsonify({"error": "Club name is required"}), 400

        existing = Community.query.filter_by(name=club_name).first()
        if existing:
            return jsonify({"error": "Community name already exists"}), 409

        image_file = request.files.get("clubImage") or request.files.get("image") or request.files.get("file")
        image_url = None

        if image_file:
            try:
                image_url = upload_image(image_file, folder="community_applications")
            except Exception as e:
                print(f"Başvuru resmi yüklenemedi: {e}")

        new_c = Community(
            name=club_name,
            university=university,
            category=category,
            description=description,
            contact_person=contact_name,
            contact_email=email,
            external_link=website_url,
            image_url=image_url,
            proof_document_url=image_url, 
            is_approved=False,            
            admin_id=user.id
        )

        db.session.add(new_c)
        db.session.commit()

        return jsonify({"message": "Application submitted successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route("/events/<int:id>", methods=["PUT"])
@jwt_required()
def update_event(id):
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        event = Event.query.get(id)

        if not event or not user:
            return jsonify({"error": "Event or User not found"}), 404

        authorized = False
        if is_super_admin(user):
            authorized = True
        else:
            if event.community_id:
                comm = Community.query.get(event.community_id)
                if comm and comm.admin_id == user.id:
                    authorized = True

        if not authorized:
            return jsonify({"error": "You are not authorized to edit this event"}), 403
        
        title = request.form.get("title") or request.form.get("name")
        if title:
            event.title = title
        date = request.form.get("date")
        if date:
            event.date = date
        description = request.form.get("description")
        if description:
            event.description = description
        new_time = request.form.get("time")
        if new_time and new_time.strip():
            event.time = new_time.strip()
        location = request.form.get("location")
        if location:
            event.location = location
        
        capacity = request.form.get("capacity")
        if capacity is not None and capacity != "":
            try:
                event.capacity = int(capacity)
            except ValueError:
                pass
        new_community_id = request.form.get("community_id")
        if new_community_id:
            try:
                target_comm = Community.query.get(new_community_id)
                if target_comm:
                    event.community_id = int(new_community_id)
            except:
                pass 

        image_file = request.files.get("image") or request.files.get("file")
        if image_file and image_file.filename != '':
            new_url = upload_file(image_file, folder="events")
            if new_url:
                event.image_url = new_url

        db.session.commit()
        return jsonify({"message": "Event updated successfully", "id": event.id}), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"FATAL ERROR: {str(e)}")
        print(f"DEBUG BACKEND HATA: {str(e)}")
        return jsonify({"error": "Sunucu hatası oluştu, terminali kontrol edin."}), 500

@bp.route("/stats", methods=["GET"])
def get_home_stats():
    try:
        uni_count = db.session.query(func.count(func.distinct(Community.university)))\
            .filter(Community.university != None)\
            .filter(Community.university != "")\
            .filter(Community.is_approved == True)\
            .scalar() or 0

        if uni_count == 0:
            uni_count = 1

        club_count = Community.query.filter_by(is_approved=True).count()
        student_count = User.query.count()
        event_count = Event.query.count()

        return jsonify({
            "universities": uni_count,
            "clubs": club_count,
            "students": student_count,
            "events": event_count
        }), 200

    except Exception as e:
        print(f"Stats Error: {e}")
        return jsonify({"error": str(e)}), 500

@bp.route("/communities/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_community(id):
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        comm = Community.query.get(id)

        if not comm:
            return jsonify({"error": "Community not found"}), 404

        is_authorized = is_super_admin(user) or (comm.admin_id == user.id)
        if not is_authorized:
            return jsonify({"error": "Unauthorized delete request"}), 403

        db.session.delete(comm)
        db.session.commit()
        return jsonify({"message": "Community deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@bp.route("/communities/<int:id>", methods=["PUT"])
@jwt_required()
def update_community(id):
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        comm = Community.query.get(id)

        if not user or not comm:
            return jsonify({"error": "Community or user not found"}), 404

        if not (is_super_admin(user) or comm.admin_id == user.id):
            return jsonify({"error": "Unauthorized"}), 403

        name = request.form.get("name")
        description = request.form.get("description")
        website_url = request.form.get("website_url")

        if name and name.strip():
            existing = Community.query.filter(
                Community.name == name.strip(),
                Community.id != comm.id
            ).first()
            if existing:
                return jsonify({"error": "Community name already exists"}), 409
            comm.name = name.strip()

        if description is not None:
            comm.description = description.strip()

        if website_url is not None:
            comm.external_link = website_url.strip()

        image_file = request.files.get("image")
        if image_file and image_file.filename:
            new_image_url = upload_image(image_file, folder="communities")
            comm.image_url = new_image_url

        db.session.commit()
        return jsonify({"message": "Community updated successfully"}), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(str(e))
        return jsonify({"error": "Failed to update community"}), 500

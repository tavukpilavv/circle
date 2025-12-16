import os
from flask import Blueprint, jsonify, request, current_app
from app.models import Community, Event, User, Rating
from app import db
from app.utils import upload_file
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from flask_jwt_extended import decode_token

bp = Blueprint('general', __name__)

# ================= EVENTS =================

@bp.route('/events', methods=['GET'])
def get_events():
    try:
        # Opsiyonel JWT kontrolü (Giriş yapmışsa registered bilgisini doğru verelim)
        verify_jwt_in_request(optional=True)
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id) if current_user_id else None

        q = request.args.get('q')
        query = Event.query
        if q: query = query.filter(Event.title.contains(q))
        
        events = query.all()
        output = []
        for e in events:
            # Frontend Uyumlu Veri Yapısı (name, image, organizer)
            organizer_name = "Unknown"
            community_name = "Genel"
            
            if e.host_community:
                community_name = e.host_community.name
                organizer_name = e.host_community.university

            is_registered = False
            is_rated = False
            user_rating = 0
            user_comment = ""

            if current_user:
                if e in current_user.registered_events:
                    is_registered = True
                
                # Kullanıcının bu etkinliğe verdiği puanı bul
                user_rating_obj = Rating.query.filter_by(user_id=current_user.id, event_id=e.id).first()
                if user_rating_obj:
                    is_rated = True
                    user_rating = user_rating_obj.score
                    user_comment = user_rating_obj.comment

            output.append({
                'id': e.id,
                'name': e.title,
                'title': e.title,
                'date': e.date,
                'time': e.time,
                'location': e.location,
                'image': e.image_url,
                'alt': e.title,
                'community_name': community_name,
                'organizer': organizer_name,
                'capacity': e.capacity,
                'description': e.description,
                'registered': is_registered,
                'rating': e.rating or 0,
                'ratingCount': e.rating_count or 0,
                'participant_count': e.participants.count(),
                'is_rated': is_rated,
                'user_rating': user_rating,
                'user_comment': user_comment
            })
        return jsonify(output), 200
    except Exception as e:
        current_app.logger.error(f"Event List Error: {str(e)}")
        return jsonify({'error': 'Etkinlikler getirilemedi.'}), 500

@bp.route('/events/create', methods=['POST'])
@jwt_required()
def create_event():
    """Etkinlik Oluşturma (Admin Kontrollü)"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user: return jsonify({'error': 'Kullanıcı bulunamadı'}), 404

        target_community_id = None
        club_name = request.form.get('club')

        if user.role == 'admin':
            if user.managed_community: target_community_id = user.managed_community.id
            else: return jsonify({'error': 'Yönettiğiniz bir kulüp yok!'}), 403
        elif user.role == 'super_admin':
            if club_name:
                found = Community.query.filter_by(name=club_name).first()
                if found: target_community_id = found.id
            if not target_community_id: target_community_id = request.form.get('community_id')

        if not target_community_id: return jsonify({'error': 'Kulüp seçilmeli.'}), 400

        image_url = upload_file(request.files.get('file') or request.files.get('image'), folder="events")
        title = request.form.get('name') or request.form.get('eventName') or request.form.get('title')

        new_event = Event(
            title=title,
            date=request.form.get('date'),
            time=request.form.get('time'),
            location=request.form.get('location'),
            capacity=request.form.get('capacity'),
            description=request.form.get('description'),
            community_id=target_community_id,
            image_url=image_url
        )
        db.session.add(new_event)
        db.session.commit()
        return jsonify({'message': 'Etkinlik oluşturuldu!'}), 201
    except Exception as e:
        current_app.logger.error(f"Event Create Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/events/<int:id>/register', methods=['POST'])
@jwt_required()
def register_event(id):
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        event = Event.query.get(id)
        
        if not user or not event: return jsonify({'error': 'Hata'}), 404
        if event in user.registered_events: return jsonify({'message': 'Zaten kayıtlısınız'}), 400
        
        user.registered_events.append(event)
        db.session.commit()
        return jsonify({'message': 'Kayıt Başarılı!'}), 200
    except Exception as e:
        current_app.logger.error(f"Register Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/events/<int:id>/rate', methods=['POST'])
@jwt_required()
def rate_event(id):
    """Puan Verme (Ekleme veya Güncelleme)"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        rating_val = data.get('rating')
        feedback_text = data.get('feedback')
        is_anonymous = data.get('is_anonymous', False)
        
        event = Event.query.get(id)
        user = User.query.get(user_id)
        
        if not event or not user: return jsonify({'error': 'Hata'}), 404

        existing = Rating.query.filter_by(user_id=user.id, event_id=event.id).first()
        
        if existing:
            # Güncelleme Mantığı
            old_score = existing.score
            existing.score = rating_val
            existing.comment = feedback_text
            existing.is_anonymous = is_anonymous
            
            # Ortalamayı yeniden hesapla
            current_total_score = (event.rating or 0) * (event.rating_count or 0)
            new_total_score = current_total_score - old_score + rating_val
            event.rating = round(new_total_score / event.rating_count, 1)
            
            db.session.commit()
            return jsonify({'message': 'Puanınız güncellendi.', 'new_rating': event.rating}), 200
        else:
            # Yeni Rating Kaydı
            new_rating_instance = Rating(
                user_id=user.id, event_id=event.id, score=rating_val,
                comment=feedback_text, is_anonymous=is_anonymous
            )
            db.session.add(new_rating_instance)
            
            # Ortalama Puanı Güncelle
            new_count = (event.rating_count or 0) + 1
            new_rating = (((event.rating or 0) * (event.rating_count or 0)) + rating_val) / new_count
            
            event.rating = round(new_rating, 1)
            event.rating_count = new_count
            
            db.session.commit()
            return jsonify({'message': 'Geri bildiriminiz kaydedildi.', 'new_rating': event.rating}), 200
    except Exception as e:
        current_app.logger.error(f"Rating Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/events/<int:id>/participants', methods=['GET'])
@jwt_required()
def get_event_participants(id):
    """Katılımcı Listesi (Admin)"""
    try:
        requester_id = get_jwt_identity()
        requester = User.query.get(requester_id)
        event = Event.query.get(id)
        
        if not event or not requester: return jsonify({'error': 'Hata'}), 404
            
        is_authorized = False
        if requester.role == 'superadmin': is_authorized = True
        elif requester.role == 'admin':
            if event.host_community and event.host_community.admin_id == requester.id:
                is_authorized = True
        
        if not is_authorized: return jsonify({'error': 'Yetkiniz yok'}), 403
            
        participants_list = []
        for p in event.participants:
            participants_list.append({
                'first_name': p.first_name,
                'last_name': p.last_name,
                'email': p.email,
                'avatar_url': p.avatar_url
            })
        return jsonify(participants_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/events/<int:id>/reviews', methods=['GET'])
def get_event_reviews(id):
    try:
        # Opsiyonel JWT kontrolü (current user'ı belirlemek için)
        verify_jwt_in_request(optional=True)
        current_user_id = get_jwt_identity()
        
        event = Event.query.get(id)
        if not event: return jsonify({'error': 'Etkinlik bulunamadı'}), 404
        
        reviews = []
        for r in event.feedbacks:
            user_name = "Incognito User"
            if not r.is_anonymous:
                user = User.query.get(r.user_id)
                if user:
                    user_name = f"{user.first_name} {user.last_name}" if user.first_name else user.username
            
            is_current_user = False
            if current_user_id and r.user_id == current_user_id:
                is_current_user = True
                
            reviews.append({
                'id': r.id,
                'user': user_name,
                'rating': r.score,
                'comment': r.comment,
                'isAnonymous': r.is_anonymous,
                'isCurrentUser': is_current_user,
                'created_at': r.created_at.isoformat() if r.created_at else None
            })
            
        # Sort by date (newest first)
        reviews.sort(key=lambda x: x['created_at'] or '', reverse=True)
        
        return jsonify(reviews), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/reviews/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_review(id):
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        review = Rating.query.get(id)
        
        if not review: return jsonify({'error': 'Yorum bulunamadı'}), 404
        
        # Yetki Kontrolü: Sadece yorum sahibi veya admin silebilir
        if review.user_id != user_id and user.role not in ['admin', 'superadmin']:
            return jsonify({'error': 'Yetkiniz yok'}), 403
            
        # Event rating güncellemesi gerekiyor mu? 
        # Evet, ortalamayı yeniden hesaplamalıyız.
        event = Event.query.get(review.event_id)
        
        db.session.delete(review)
        db.session.commit()
        
        # Ortalamayı güncelle
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
            
        return jsonify({'message': 'Review deleted'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/events/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_event(id):
    # Basit bir yetki kontrolü eklenebilir
    event = Event.query.get(id)
    if event:
        db.session.delete(event)
        db.session.commit()
        return jsonify({'message': 'Silindi'}), 200
    return jsonify({'error': 'Bulunamadı'}), 404

# ================= COMMUNITIES =================

@bp.route('/communities', methods=['GET'])
def get_communities():
    print("test communities")
    try:
        verify_jwt_in_request(optional=True)
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id) if current_user_id else None

        comms = Community.query.filter_by(is_approved=True).all()
        output = []
        for c in comms:
            is_joined = False
            if current_user and c in current_user.joined_communities:
                is_joined = True

            output.append({
                'id': c.id,
                'name': c.name,
                'university': c.university,
                'description': c.description,
                'short_description': c.short_description,
                'image': c.image_url, 
                'joined': is_joined,
                'member_count': c.members.count()
            })
        return jsonify(output), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@bp.route('/communities/pending', methods=['GET'])
def get_pending_communities():
    try:
        comms = Community.query.filter_by(is_approved=False).all()
        output = []
        for c in comms:
            output.append({
                'id': c.id,
                'name': c.name,
                'university': c.university,
                'description': c.description,
                'short_description': c.short_description,
                'image': c.image_url, 
                'joined': False,
                'member_count': c.members.count()
            })
        return jsonify(output), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/communities/create', methods=['POST'])
@jwt_required()
def create_community():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return jsonify({'error': 'Unauthorized'}), 401

        # 🔒 ADMIN-ONLY
        if user.role not in ['admin', 'super_admin']:
            return jsonify({'error': 'Only admins can create communities'}), 403

        data = request.get_json()

        file_url = data.get("clubImage")

        new_c = Community(
            name=data.get('clubName'),
            university=data.get('university'),
            category=data.get('category'),
            short_description=data.get('shortDescription'),
            description=data.get('description'),
            contact_person=data.get('contactName'),
            contact_email=data.get('email'),
            instagram_link=data.get("instagram"),
            external_link=data.get("otherLink"),
            image_url=file_url,
            proof_document_url=file_url,
            is_approved=True,     # admins create approved communities
            admin_id=user.id
        )

        db.session.add(new_c)
        db.session.commit()

        # Admin automatically joins
        user.joined_communities.append(new_c)
        db.session.commit()

        return jsonify({'message': 'Community created'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/communities/<int:id>/join', methods=['POST'])
@jwt_required()
def join_community(id):
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        comm = Community.query.get(id)
        if comm in user.joined_communities: return jsonify({'message': 'Zaten üyesiniz'}), 400
        user.joined_communities.append(comm)
        db.session.commit()
        return jsonify({'message': 'Katılım Başarılı!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/communities/applications', methods=['GET'])
@jwt_required()
def get_applications():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.role != 'superadmin': return jsonify({'error': 'Yetkiniz yok'}), 403
        
        pending = Community.query.filter_by(is_approved=False).all()
        output = [{
            'id': c.id, 
            'name': c.name, 
            'proof_document': c.proof_document_url,
            'contact_person': c.contact_person
        } for c in pending]
        return jsonify(output), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/communities/approve', methods=['POST'])
@jwt_required()
def approve_community():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        data = request.get_json()
        id = data.get('id') 
        if not user or user.role != 'super_admin': return jsonify({'error': 'Yetkiniz yok'}), 403
        
        comm = Community.query.get(id)
        if comm:
            comm.is_approved = True
            User.query.get(comm.admin_id).role = 'admin'
            db.session.commit()
            return jsonify({'success': True, 'message': 'Onaylandı'}), 200
        return jsonify({'error': 'Bulunamadı'}), 404
    except Exception as e:
        print("\n🔥 COMMUNITY CREATE ERROR ↓↓↓↓↓")
        print(str(e))
        import traceback
        traceback.print_exc()
        print("🔥 END ERROR ↑↑↑↑↑\n")
        return jsonify({'error': str(e)}), 500

@bp.route('/communities/apply', methods=['POST'])
@jwt_required()
def apply_community():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()

    # Prevent duplicate names
    existing = Community.query.filter_by(name=data.get('clubName')).first()
    if existing:
        return jsonify({'error': 'Community name already exists'}), 409

    new_c = Community(
        name=data.get('clubName'),
        university=data.get('university'),
        category=data.get('category'),
        short_description=data.get('shortDescription'),
        description=data.get('description'),
        contact_person=data.get('contactName'),
        contact_email=data.get('email'),
        instagram_link=data.get("instagram"),
        external_link=data.get("otherLink"),
        image_url=data.get("clubImage"),
        proof_document_url=data.get("clubImage"),
        is_approved=False,              # 🔑 IMPORTANT
        admin_id=user.id                # applicant
    )

    db.session.add(new_c)
    db.session.commit()

    return jsonify({'message': 'Application submitted'}), 201




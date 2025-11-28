from flask import Blueprint, jsonify, request
from app.models import Community, Event, User
from app import db
from app.utils import upload_file # YENİ YARDIMCIN

bp = Blueprint('general', __name__)

# --- EVENTS ---

@bp.route('/events', methods=['GET'])
def get_events():
    q = request.args.get('q')
    query = Event.query
    if q: query = query.filter(Event.title.contains(q))
    
    events = query.all()
    output = []
    for e in events:
        output.append({
            'id': e.id,
            'title': e.title,
            'date': e.date,
            'time': e.time,
            'location': e.location,
            'capacity': e.capacity,
            'image_url': e.image_url,
            'community_name': e.host_community.name if e.host_community else "Genel",
            'participant_count': e.participants.count()
        })
    return jsonify(output), 200

@bp.route('/events/create', methods=['POST'])
def create_event():
    try:
        # 1. Yetki Kontrolleri (Aynı kalıyor)
        user_id = request.form.get('user_id')
        user = User.query.get(user_id)
        if not user: return jsonify({'error': 'Kullanıcı bulunamadı'}), 404

        target_community_id = None
        if user.role == 'superadmin':
            target_community_id = request.form.get('community_id')
        elif user.role == 'admin':
            if user.managed_community:
                target_community_id = user.managed_community.id
            else:
                return jsonify({'error': 'Kulübünüz yok!'}), 403
        else:
            return jsonify({'error': 'Yetkiniz yok'}), 403

        # 2. CLOUDINARY YÜKLEMESİ (Değişen Kısım)
        # Frontend'den gelen 'file' veya 'image' dosyasını al
        image_file = request.files.get('file') or request.files.get('image')
        # Utils'deki fonksiyonu kullan
        image_url = upload_file(image_file, folder="events")

        # 3. Kayıt
        new_event = Event(
            title=request.form.get('eventName') or request.form.get('title'),
            date=request.form.get('date'),
            time=request.form.get('time'),
            location=request.form.get('location'),
            capacity=request.form.get('capacity'),
            description=request.form.get('description'),
            community_id=target_community_id,
            image_url=image_url # Artık Cloudinary linki
        )
        db.session.add(new_event)
        db.session.commit()
        return jsonify({'message': 'Etkinlik oluşturuldu!'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ... (Diğer register, delete metodları aynı kalabilir) ...
@bp.route('/events/<int:id>/register', methods=['POST'])
def register_event(id):
    data = request.get_json()
    user = User.query.get(data.get('user_id'))
    event = Event.query.get(id)
    if event in user.registered_events: return jsonify({'message': 'Zaten kayıtlısınız'}), 400
    user.registered_events.append(event)
    db.session.commit()
    return jsonify({'message': 'Kayıt Başarılı!'}), 200

@bp.route('/events/<int:id>', methods=['DELETE'])
def delete_event(id):
    event = Event.query.get(id)
    if event:
        db.session.delete(event)
        db.session.commit()
        return jsonify({'message': 'Silindi'}), 200
    return jsonify({'error': 'Bulunamadı'}), 404

# --- COMMUNITIES ---

@bp.route('/communities/create', methods=['POST'])
def create_community():
    try:
        # CLOUDINARY YÜKLEMESİ
        file_url = upload_file(request.files.get('file'), folder="communities")
        
        new_c = Community(
            name=request.form.get('name'),
            university=request.form.get('university'),
            category=request.form.get('category'),
            short_description=request.form.get('shortDescription'),
            description=request.form.get('description'),
            contact_person=request.form.get('contactPerson'),
            contact_email=request.form.get('contactEmail'),
            image_url=file_url,
            proof_document_url=file_url
        )
        db.session.add(new_c)
        db.session.commit()
        return jsonify({'message': 'Kulüp başvurusu alındı!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/communities', methods=['GET'])
def get_communities():
    comms = Community.query.all()
    output = []
    for c in comms:
        output.append({
            'id': c.id,
            'name': c.name,
            'university': c.university,
            'short_description': c.short_description,
            'image_url': c.image_url,
            'member_count': c.members.count()
        })
    return jsonify(output), 200

@bp.route('/communities/<int:id>/join', methods=['POST'])
def join_community(id):
    data = request.get_json()
    user = User.query.get(data.get('user_id'))
    comm = Community.query.get(id)
    if comm in user.joined_communities: return jsonify({'message': 'Zaten üyesiniz'}), 400
    user.joined_communities.append(comm)
    db.session.commit()
    return jsonify({'message': 'Katılım Başarılı!'}), 200

# --- USER ---

@bp.route('/users/<int:id>/dashboard', methods=['GET'])
def get_dashboard(id):
    user = User.query.get(id)
    if not user: return jsonify({'error': 'Kullanıcı yok'}), 404
    return jsonify({
        'user': {'first_name': user.first_name, 'avatar_url': user.avatar_url, 'role': user.role},
        'my_events': [{'id': e.id, 'title': e.title, 'date': e.date, 'image_url': e.image_url} for e in user.registered_events],
        'my_communities': [{'id': c.id, 'name': c.name, 'image_url': c.image_url} for c in user.joined_communities]
    }), 200

@bp.route('/users/<int:id>/update', methods=['POST'])
def update_profile(id):
    user = User.query.get(id)
    user.first_name = request.form.get('first_name') or user.first_name
    
    # CLOUDINARY YÜKLEMESİ
    avatar = request.files.get('avatar')
    if avatar:
        user.avatar_url = upload_file(avatar, folder="avatars")
        
    db.session.commit()
    return jsonify({'message': 'Güncellendi', 'avatar_url': user.avatar_url}), 200

@bp.route('/support', methods=['POST'])
def contact_support():
    return jsonify({'message': 'Alındı'}), 200
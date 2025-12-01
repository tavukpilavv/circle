import os
from flask import Blueprint, jsonify, request, current_app
from app.models import Community, Event, User
from app import db
from app.utils import upload_file

bp = Blueprint('general', __name__)

# ================= EVENTS =================

@bp.route('/events', methods=['GET'])
def get_events():
    try:
        q = request.args.get('q')
        query = Event.query
        if q: query = query.filter(Event.title.contains(q))
        
        events = query.all()
        output = []
        for e in events:
            # Frontend Uyumlu Veri Yapısı
            organizer_name = "Unknown"
            community_name = "Genel"
            if e.host_community:
                community_name = e.host_community.name
                organizer_name = e.host_community.university

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
                'registered': False,
                'rating': e.rating or 0,
                'ratingCount': e.rating_count or 0,
                'participant_count': e.participants.count()
            })
        return jsonify(output), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/events/create', methods=['POST'])
def create_event():
    try:
        user_id = request.form.get('user_id')
        user = User.query.get(user_id)
        if not user: return jsonify({'error': 'Kullanıcı bulunamadı'}), 404

        target_community_id = None
        club_name = request.form.get('club')

        if user.role == 'admin':
            if user.managed_community: target_community_id = user.managed_community.id
            else: return jsonify({'error': 'Yönettiğiniz bir kulüp yok!'}), 403
        elif user.role == 'superadmin':
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
        return jsonify({'error': str(e)}), 500

@bp.route('/events/<int:id>/register', methods=['POST'])
def register_event(id):
    try:
        data = request.get_json()
        user = User.query.get(data.get('user_id'))
        event = Event.query.get(id)
        
        if not user or not event: return jsonify({'error': 'Hata'}), 404
        if event in user.registered_events: return jsonify({'message': 'Zaten kayıtlısınız'}), 400
        
        user.registered_events.append(event)
        db.session.commit()
        return jsonify({'message': 'Kayıt Başarılı!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/events/<int:id>/rate', methods=['POST'])
def rate_event(id):
    try:
        data = request.get_json()
        rating_val = data.get('rating')
        event = Event.query.get(id)
        if not event: return jsonify({'error': 'Bulunamadı'}), 404
        
        curr_rating = event.rating or 0
        curr_count = event.rating_count or 0
        new_count = curr_count + 1
        new_rating = ((curr_rating * curr_count) + rating_val) / new_count
        
        event.rating = round(new_rating, 1)
        event.rating_count = new_count
        db.session.commit()
        return jsonify({'message': 'Puan kaydedildi', 'rating': event.rating}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/events/<int:id>/participants', methods=['GET'])
def get_event_participants(id):
    try:
        requester_id = request.args.get('user_id')
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

@bp.route('/events/<int:id>', methods=['DELETE'])
def delete_event(id):
    event = Event.query.get(id)
    if event:
        db.session.delete(event)
        db.session.commit()
        return jsonify({'message': 'Silindi'}), 200
    return jsonify({'error': 'Bulunamadı'}), 404

# ================= COMMUNITIES =================

@bp.route('/communities', methods=['GET'])
def get_communities():
    try:
        # Sadece onaylılar
        comms = Community.query.filter_by(is_approved=True).all()
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
def create_community():
    try:
        # 1. Başvuranı Bul
        user_id = request.form.get('user_id')
        user = User.query.get(user_id)
        if not user: return jsonify({'error': 'Giriş yapmalısınız'}), 401
        
        if user.managed_community:
             return jsonify({'error': 'Zaten bir kulübünüz var!'}), 400

        # 2. Dosya Yükle
        file_url = upload_file(request.files.get('file'), folder="communities")
        
        # 3. Kulübü Kur (Otomatik Onaylı + Admin Atamalı)
        new_c = Community(
            name=request.form.get('name'),
            university=request.form.get('university'),
            category=request.form.get('category'),
            short_description=request.form.get('shortDescription'),
            description=request.form.get('description'),
            contact_person=request.form.get('contactPerson'),
            contact_email=request.form.get('contactEmail'),
            image_url=file_url,
            proof_document_url=file_url,
            is_approved=True, # Otomatik Onay
            admin_id=user.id  # Tapuyu kullanıcıya ver
        )
        
        # 4. Kullanıcıyı Admin Yap
        if user.role == 'student':
            user.role = 'admin'
        
        user.joined_communities.append(new_c)

        db.session.add(new_c)
        db.session.commit()
        return jsonify({'message': 'Kulübünüz kuruldu! Yönetim paneli açıldı.'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/communities/<int:id>/join', methods=['POST'])
def join_community(id):
    try:
        data = request.get_json()
        user = User.query.get(data.get('user_id'))
        comm = Community.query.get(id)
        if comm in user.joined_communities: return jsonify({'message': 'Zaten üyesiniz'}), 400
        user.joined_communities.append(comm)
        db.session.commit()
        return jsonify({'message': 'Katılım Başarılı!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ================= USER / DASHBOARD =================

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
    avatar = request.files.get('avatar')
    if avatar:
        user.avatar_url = upload_file(avatar, folder="avatars")
    db.session.commit()
    return jsonify({'message': 'Güncellendi', 'avatar_url': user.avatar_url}), 200

@bp.route('/support', methods=['POST'])
def contact_support():
    return jsonify({'message': 'Alındı'}), 200

# ================= DATABASE SEED (RENDER İÇİN) =================

@bp.route('/admin/seed', methods=['POST'])
def seed_database():
    """
    Render'da veritabanını seed verilerle doldurur.
    Güvenlik: X-Seed-Secret header'ı kontrol edilir
    """
    # Basit güvenlik kontrolü
    secret = request.headers.get('X-Seed-Secret')
    if secret != 'CIRCLE_SEED_2025_SECRET':  # ⚠️ Bunu değiştirin!
        return jsonify({"error": "Unauthorized - Invalid secret"}), 401
    
    try:
        print("💣 Veritabanı SIFIRLANIYOR...")
        
        db.session.remove()
        db.drop_all()
        db.create_all()
        
        print("✅ Tablolar yeniden oluşturuldu.")

        # ================= KULLANICILAR =================
        super_admin = User(
            first_name="Super", last_name="Admin", 
            email="super@circle.com", username="superadmin",
            role="superadmin", major="System Admin", 
            avatar_url="https://cdn-icons-png.flaticon.com/512/147/147144.png"
        )
        super_admin.set_password("123456")

        club_admin = User(
            first_name="Kulüp", last_name="Başkanı", 
            email="admin@circle.com", username="clubadmin",
            role="admin", major="Theater Arts",
            avatar_url="https://cdn-icons-png.flaticon.com/512/147/147142.png"
        )
        club_admin.set_password("123456")

        student = User(
            first_name="Ali", last_name="Yılmaz", 
            email="ali@ogrenci.com", username="aliy",
            role="student", major="Computer Science",
            avatar_url="https://cdn-icons-png.flaticon.com/512/147/147140.png"
        )
        student.set_password("123456")

        db.session.add_all([super_admin, club_admin, student])
        db.session.commit()

        # ================= TOPLULUKLAR =================
        c1 = Community(
            name="AYBU Tiyatro Kulübü",
            university="AYBU",
            category="Art & Culture",
            short_description="Sahne tozunu yutmak isteyenler buraya!",
            description="Tiyatro kulübümüz, sahne sanatlarına ilgi duyan öğrencileri bir araya getirir.",
            contact_person="Ahmet Demir",
            contact_email="tiyatro@aybu.edu.tr",
            image_url="https://images.unsplash.com/photo-1460723237483-7a6dc9d0b212",
            admin=club_admin,
            is_approved=True 
        )

        c2 = Community(
            name="Computer Science Club",
            university="ODTÜ",
            category="Science & Tech",
            short_description="Yazılım ve Teknoloji tutkunları.",
            description="Coding workshops, hackathonlar ve teknoloji sohbetleri.",
            contact_person="Ayşe Yılmaz",
            contact_email="cs@odtu.edu.tr",
            image_url="https://images.unsplash.com/photo-1531482615713-2afd69097998",
            is_approved=True
        )

        c3 = Community(
            name="Engineering Society",
            university="Bilkent",
            category="Science & Tech",
            short_description="Geleceği inşa ediyoruz.",
            description="Mühendislik öğrencileri için network ve proje geliştirme.",
            contact_person="Mehmet Çelik",
            contact_email="eng@bilkent.edu.tr",
            image_url="https://images.unsplash.com/photo-1550751827-4bd374c3f58b",
            is_approved=True
        )

        db.session.add_all([c1, c2, c3])
        db.session.commit()

        # ================= ETKİNLİKLER =================
        e1 = Event(
            title="Seramik Boyama",
            date="2025-11-29",
            time="14:00",
            location="Cleopatra Ayrancı Atelier",
            capacity=20,
            description="Yaratıcılığınızı keşfedin!",
            image_url="https://images.unsplash.com/photo-1517976487492-5750f3195933",
            community_id=c1.id,
            rating=4.8,
            rating_count=124
        )

        e2 = Event(
            title="Game Jam 2025",
            date="2025-11-07",
            time="09:00",
            location="ODTÜ Teknokent",
            capacity=100,
            description="48 saat sürecek oyun geliştirme maratonu.",
            image_url="https://images.unsplash.com/photo-1552820728-8b83bb6b773f",
            community_id=c2.id,
            rating=4.5,
            rating_count=89
        )

        e3 = Event(
            title="Coffee Meetup",
            date="2025-10-12",
            time="14:00",
            location="Coffee Up, Bahçelievler",
            capacity=50,
            description="Tanışma toplantısı.",
            image_url="https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4",
            community_id=c1.id,
            rating=4.2,
            rating_count=30
        )

        db.session.add_all([e1, e2, e3])
        
        # Öğrenciyi üye yapalım
        c2.members.append(student)
        e1.participants.append(student)

        db.session.commit()
        
        print("🎉 İŞLEM TAMAM! Veritabanı etkinliklerle doldu.")
        
        return jsonify({
            "message": "🎉 Database seeded successfully!",
            "users": 3,
            "communities": 3,
            "events": 3
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ HATA: {str(e)}")
        return jsonify({"error": str(e)}), 500
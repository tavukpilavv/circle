from app import create_app, db
from app.models import User, Community, Event

app = create_app()

with app.app_context():
    print("🧹 Veritabanı temizleniyor...")
    db.session.remove()
    db.drop_all()
    db.create_all()

    # ================= KULLANICILAR =================
    print("👤 Kullanıcılar oluşturuluyor...")
    
    super_admin = User(
        first_name="Super", last_name="Admin", email="super@circle.com", username="superadmin",
        role="superadmin", major="System Admin", 
        avatar_url="https://cdn-icons-png.flaticon.com/512/147/147144.png"
    )
    super_admin.set_password("123456")

    club_admin = User(
        first_name="Kulüp", last_name="Başkanı", email="admin@circle.com", username="clubadmin",
        role="admin", major="Theater Arts",
        avatar_url="https://cdn-icons-png.flaticon.com/512/147/147142.png"
    )
    club_admin.set_password("123456")

    student = User(
        first_name="Ali", last_name="Yılmaz", email="ali@ogrenci.com", username="aliy",
        role="student", major="Computer Science",
        avatar_url="https://cdn-icons-png.flaticon.com/512/147/147140.png"
    )
    student.set_password("123456")

    db.session.add_all([super_admin, club_admin, student])
    db.session.commit()

    # ================= TOPLULUKLAR =================
    print("camp Communities oluşturuluyor...")

    c1 = Community(
        name="AYBU Tiyatro Kulübü",
        university="AYBU",
        category="Art & Culture",
        short_description="Sahne tozunu yutmak isteyenler buraya!",
        description="...",
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
        description="...",
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
        description="...",
        contact_person="Mehmet Çelik",
        contact_email="eng@bilkent.edu.tr",
        image_url="https://images.unsplash.com/photo-1550751827-4bd374c3f58b",
        is_approved=True
    )

    db.session.add_all([c1, c2, c3])
    db.session.commit()

    # ================= ETKİNLİKLER =================
    print("📅 Etkinlikler oluşturuluyor...")

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
        description="48 saat sürecek maraton.",
        image_url="https://images.unsplash.com/photo-1552820728-8b83bb6b773f",
        community_id=c2.id,
        rating=4.5,
        rating_count=89
    )

    db.session.add_all([e1, e2])
    
    c2.members.append(student)
    e1.participants.append(student)

    db.session.commit()
    print("✅ VERİTABANI BAŞARIYLA DOLDURULDU!")
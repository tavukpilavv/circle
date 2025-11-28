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
    
    # 1. Super Admin
    super_admin = User(
        first_name="Super", 
        last_name="Admin", 
        email="super@circle.com", 
        role="superadmin",
        avatar_url="https://cdn-icons-png.flaticon.com/512/147/147144.png"
    )
    super_admin.set_password("123456")

    # 2. Kulüp Başkanı (Admin)
    club_admin = User(
        first_name="Kulüp", 
        last_name="Başkanı", 
        email="admin@circle.com", 
        role="admin",
        avatar_url="https://cdn-icons-png.flaticon.com/512/147/147142.png"
    )
    club_admin.set_password("123456")

    # 3. Öğrenci
    student = User(
        first_name="Ali", 
        last_name="Yılmaz", 
        email="ali@ogrenci.com", 
        role="student",
        avatar_url="https://cdn-icons-png.flaticon.com/512/147/147140.png"
    )
    student.set_password("123456")

    db.session.add_all([super_admin, club_admin, student])
    db.session.commit()

    # ================= TOPLULUKLAR =================
    print("camp Communities oluşturuluyor...")

    c1 = Community(
        name="AYBU Tiyatro Kulübü",
        university="Ankara Yıldırım Beyazıt Üniversitesi",
        category="Art & Culture",
        short_description="Sahne tozunu yutmak isteyenler buraya!",
        description="Tiyatro kulübümüz, sahne sanatlarına ilgi duyan öğrencileri bir araya getirerek oyunlar sergilemeyi amaçlar. Haftalık provalar ve dönem sonu gösterileri yapıyoruz.",
        contact_person="Ahmet Demir",
        contact_email="tiyatro@aybu.edu.tr",
        instagram_link="https://instagram.com/aybutiyatro",
        image_url="https://images.unsplash.com/photo-1460723237483-7a6dc9d0b212",
        # Bu kulübün başkanı "club_admin" olsun
        admin=club_admin 
    )

    c2 = Community(
        name="BİLTEK",
        university="Ankara Yıldırım Beyazıt Üniversitesi",
        category="Science & Tech",
        short_description="Yazılım ve Teknoloji tutkunlarının buluşma noktası.",
        description="Coding workshops, hackathonlar ve teknoloji sohbetleri. Geleceği kodluyoruz.",
        contact_person="Ayşe Yılmaz",
        contact_email="biltek@aybu.edu.tr",
        image_url="https://images.unsplash.com/photo-1531482615713-2afd69097998"
        # Bunun başkanı yok (Superadmin yönetebilir)
    )

    c3 = Community(
        name="ASEC AYBU",
        university="Ankara Yıldırım Beyazıt Üniversitesi",
        category="Science & Tech",
        short_description="Siber güvenlik ve yazılım geliştirme.",
        description="Siber güvenlik dünyasına adım atın. CTF yarışmaları ve eğitimler.",
        contact_person="Mehmet Çelik",
        contact_email="asec@aybu.edu.tr",
        image_url="https://images.unsplash.com/photo-1550751827-4bd374c3f58b"
    )

    db.session.add_all([c1, c2, c3])
    db.session.commit()

    # ================= ETKİNLİKLER =================
    print("📅 Etkinlikler oluşturuluyor...")

    e1 = Event(
        title="Seramik Boyama Etkinliği",
        date="2025-11-29",
        time="14:00",
        location="Cleopatra Ayrancı Atelier",
        capacity=20,
        description="Hayal gücünün zanaatkarlıkla buluştuğu rahat ve destekleyici bir ortamda yaratıcılığınızı keşfedin!",
        image_url="https://images.unsplash.com/photo-1517976487492-5750f3195933",
        community_id=c2.id # BİLTEK düzenliyor
    )

    e2 = Event(
        title="Game Jam 2025",
        date="2025-11-07",
        time="09:00",
        location="AYBU Kampüs",
        capacity=100,
        description="48 saat sürecek oyun geliştirme maratonuna hazır mısın? Takımını kur gel!",
        image_url="https://images.unsplash.com/photo-1552820728-8b83bb6b773f",
        community_id=c3.id # ASEC düzenliyor
    )

    e3 = Event(
        title="Coffee Meetup",
        date="2025-10-12",
        time="14:00",
        location="Coffee Up, Bahçelievler",
        capacity=50,
        description="Sadece bizimle kahve içmeye ihtiyacın var. Tanışma toplantısı.",
        image_url="https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4",
        community_id=c1.id # Tiyatro kulübü düzenliyor
    )

    db.session.add_all([e1, e2, e3])
    
    # Öğrenciyi bir kulübe üye yapalım ve etkinliğe kaydettirelim (Test için)
    c2.members.append(student) # BİLTEK'e üye oldu
    e1.participants.append(student) # Seramik boyamaya kaydoldu

    db.session.commit()
    
    print("✅ VERİTABANI BAŞARIYLA DOLDURULDU!")
    print("------------------------------------------")
    print(f"SuperAdmin: super@circle.com / 123456")
    print(f"Kulüp Admini: admin@circle.com / 123456 (Yönettiği Kulüp: {c1.name})")
    print(f"Öğrenci: ali@ogrenci.com / 123456")
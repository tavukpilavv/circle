from app import create_app, db
from app.models import User, Community, Event

app = create_app()

with app.app_context():
    print("💣 Veritabanı SIFIRLANIYOR...")
    
    # İşte sihirli komutlar burası:
    db.session.remove()
    db.drop_all()   # Tüm tabloları sil
    db.create_all() # Tüm tabloları yeniden oluştur (512 karakterlik yeni haliyle)
    
    print("✅ Tablolar yeniden oluşturuldu.")

    # ================= KULLANICILAR =================
    print("👤 Kullanıcılar ekleniyor...")
    
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

    # ... (Buraya Kulüpler ve Etkinlikler gelecek - Önceki kodunun aynısı) ...
    # Kısa olsun diye burayı kestim ama sen önceki seed.py dosyanın tamamını kullan,
    # Sadece en üste db.drop_all() ve db.create_all() eklemiş olduk.
    
    print("🎉 İŞLEM TAMAM! Veritabanı tertemiz oldu.")
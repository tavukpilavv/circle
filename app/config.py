import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Güvenlik Anahtarı
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cok-gizli-anahtar-123'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or SECRET_KEY
    
    # --- VERİTABANI AYARLARI ---
    # Render'da DATABASE_URL ortam değişkeni kullanılır, localde SQLite
    database_url = os.environ.get('DATABASE_URL')
    
    # Render'ın verdiği postgres:// linkini düzeltiyoruz
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = database_url or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- CLOUDINARY AYARLARI ---
    CLOUDINARY_CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME')
    CLOUDINARY_API_KEY = os.environ.get('CLOUDINARY_API_KEY')
    CLOUDINARY_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET')

    # --- DOSYA YÜKLEME AYARLARI ---
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
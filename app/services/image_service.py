import os
import cloudinary
import cloudinary.uploader

# Cloudinary Ayarları
# Bu bilgileri Render'da environment variable olarak gireceğiz.
# Localde çalışırken bilgisayarındaki .env dosyasından okur.
cloudinary.config(
    cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key = os.environ.get('CLOUDINARY_API_KEY'),
    api_secret = os.environ.get('CLOUDINARY_API_SECRET'),
    secure = True
)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    """Dosya uzantısı izin verilenler listesinde mi kontrol eder."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_image(file_storage, folder="circle_events"):
    """
    Dosyayı alır, uzantısını kontrol eder ve Cloudinary'ye yükler.
    Geriye resmin URL'ini döndürür.
    """
    if not file_storage:
        return None
    
    if not allowed_file(file_storage.filename):
        raise ValueError("Bu dosya formatı desteklenmiyor. (Sadece resim dosyaları: png, jpg, jpeg, gif, webp)")

    try:
        # Dosyayı direkt Cloudinary'ye gönder
        upload_result = cloudinary.uploader.upload(
            file_storage, 
            folder=folder,
            resource_type="image"
        )
        return upload_result.get('secure_url')
    except Exception as e:
        print(f"Cloudinary hatası: {e}")
        raise e
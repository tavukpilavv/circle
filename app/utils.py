import cloudinary
import cloudinary.uploader
from flask import current_app

def upload_file(file, folder="uploads"):
    """
    Dosyayı Cloudinary'ye yükler ve güvenli HTTPS linkini döndürür.
    Eğer Cloudinary ayarlı değilse None döner.
    """
    if not file:
        return None

    # Cloudinary ayarları var mı kontrol et
    cloud_name = current_app.config.get('CLOUDINARY_CLOUD_NAME')
    if not cloud_name:
        print("UYARI: Cloudinary ayarları eksik!")
        return None

    # Cloudinary'yi başlat
    cloudinary.config(
        cloud_name = cloud_name,
        api_key = current_app.config.get('CLOUDINARY_API_KEY'),
        api_secret = current_app.config.get('CLOUDINARY_API_SECRET')
    )

    try:
        # Yükleme işlemi
        result = cloudinary.uploader.upload(
            file,
            folder=f"circle_app/{folder}", # Cloudinary'de düzenli klasörleme
            resource_type="auto" # Resim, PDF, Video otomatik algıla
        )
        return result['secure_url']
    
    except Exception as e:
        print(f"Cloudinary Yükleme Hatası: {e}")
        return None
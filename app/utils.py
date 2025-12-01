import cloudinary
import cloudinary.uploader
from flask import current_app

def upload_file(file, folder="uploads"):
    """
    Dosyayı Cloudinary'ye yükler ve güvenli HTTPS linkini döndürür.
    Frontend'den gelen FormData objesini işler.
    """
    if not file:
        return None

    cloud_name = current_app.config.get('CLOUDINARY_CLOUD_NAME')
    if not cloud_name:
        # Localhost'ta test yapılıyorsa Cloudinary'yi atla
        return None 

    # Cloudinary'yi başlat
    cloudinary.config(
        cloud_name = cloud_name,
        api_key = current_app.config.get('CLOUDINARY_API_KEY'),
        api_secret = current_app.config.get('CLOUDINARY_API_SECRET')
    )

    try:
        # Yükleme işlemi
        upload_result = cloudinary.uploader.upload(
            file,
            folder=f"circle_app/{folder}", # Cloudinary'de düzenli klasörleme
            resource_type="auto"
        )
        return upload_result['secure_url']
    
    except Exception as e:
        current_app.logger.error(f"Cloudinary Yükleme Hatası: {e}")
        return None
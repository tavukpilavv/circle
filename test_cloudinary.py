import requests
import os

# Backend'imizin adresi (Çalışıyor olması lazım!)
url = "http://127.0.0.1:5000/api/general/events/create"

# Göndereceğimiz test verileri
# (Seed dosyasındaki SuperAdmin ID'si genelde 1 olur)
payload = {
    "user_id": "1", 
    "title": "Cloudinary Test Etkinligi",
    "date": "2025-01-01",
    "time": "12:00",
    "location": "Test Sunucusu",
    "capacity": "50",
    "description": "Bu etkinlik Cloudinary entegrasyonunu doğrulamak için oluşturulmuştur.",
    "community_id": "2" # BİLTEK ID'si (Seed ile geldiyse)
}

# Dosya yolu
file_path = "test.jpg"

print(f"📡 İstek gönderiliyor: {url}...")

if not os.path.exists(file_path):
    print(f"❌ HATA: '{file_path}' dosyası bulunamadı! Lütfen klasöre bir resim koy.")
else:
    # Dosyayı ve verileri paketleyip gönderiyoruz
    with open(file_path, "rb") as f:
        files = {"file": f}
        try:
            response = requests.post(url, data=payload, files=files)
            
            print(f"Durum Kodu: {response.status_code}")
            print("Cevap:", response.json())
            
            if response.status_code == 201:
                print("\n✅ BAŞARILI! Etkinlik oluşturuldu.")
                print("Lütfen Cloudinary paneline gidip 'Media Library' kısmını kontrol et.")
                print("Resmin orada görünüyorsa işlem tamamdır! ☁️")
            else:
                print("\n❌ BİR SORUN VAR. Hata mesajını kontrol et.")
                
        except Exception as e:
            print(f"❌ Bağlantı hatası: {e}")
            print("Sunucunun (run.py) açık olduğundan emin misin?")
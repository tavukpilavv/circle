# Codex Handoff – Multi-University Events Platform (Flask + PostgreSQL)

Bu rehber, Flask tabanlı uygulamamızı **model-odaklı**, **çok-üniversiteli (multi-tenant)**, **onaysız akış** mimarisine taşımak için adım adım yapılacakları anlatır.

---

## 1) Pakette ne var?
- **aybu_multi_uni_schema.sql** → PostgreSQL DDL: uzantılar, tablolar, indeksler, EXCLUDE çakışma kuralı, materialized view, seed’ler.
- **Bu README** → Dosya düzeni, bağımlılıklar, migration notları, endpoint checklist.

---

## 2) Hedef klasör yapısı (mevcut yapıyı koru, eksikleri ekle)
circle/
init.py # app factory
extensions.py # db, migrate, jwt, limiter
config.py # Base/Dev/Prod
models/
init.py # register_models()
base.py # BaseModel: id, created_at, updated_at, deleted_at
lookups.py # Role, VisibilityType, EventStatus, SignupStatus, VenueType, Tag
university.py # University, Campus
user.py # User, UserRole
club.py # Club, ClubMembership
venue.py # Venue, VenueBlock
event.py # Event, EventTag
signup.py # EventSignup, WaitlistPromotion, Checkin
media.py # Media, EmailLog, AuditEvent
routes/
init.py # register_routes()
auth.py
user.py
club.py
venue.py
event.py # list/create/publish/cancel/signups
upload.py
services/
init.py
events.py # (opsiyonel) kapasite, waitlist, e-posta tetikleyicileri
utils/
init.py
helpers.py # resolve_university(), ortak yardımcılar
app.py # entrypoint

from flask import Flask, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.config import Config
from sqlalchemy import MetaData
import logging
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended.exceptions import NoAuthorizationError
from flask_jwt_extended.exceptions import (
    NoAuthorizationError,
    InvalidHeaderError,
    JWTDecodeError,
    CSRFError
)

# Logging'i aktif edin
logging.basicConfig(level=logging.DEBUG)



# --- OTOMATİK İSİMLENDİRME KURALI (SQLite Fix) ---
convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)
# ----------------------------------------------------------

migrate = Migrate()
jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(
        __name__,
        static_folder="static",
        template_folder="templates",
        static_url_path=""
    )

    app.config.from_object(config_class)
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False
    app.config['JWT_CSRF_CHECK_FORM'] = False
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    app.config['JWT_HEADER_NAME'] = 'Authorization'
    app.config['JWT_HEADER_TYPE'] = 'Bearer'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False    
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    jwt.init_app(app)


    @app.before_request
    def log_request_info():
        print("\n=== INCOMING REQUEST ===")
        print(f"Method: {request.method}")
        print(f"URL: {request.url}")
        print(f"Headers: {dict(request.headers)}")
        print(f"Content-Type: {request.content_type}")
        
        # Body'yi oku (dikkat: bir kere okunabilir)
        if request.is_json:
            print(f"JSON Data: {request.get_json()}")
        else:
            print(f"Form Data: {request.form}")
            print(f"Raw Data: {request.get_data()}")
        print("=====================\n")
    @app.errorhandler(Exception)
    def handle_all_exceptions(e):
        import traceback
        print("\n!!! EXCEPTION CAUGHT !!!")
        print(f"Type: {type(e).__name__}")
        print(f"Message: {str(e)}")
        print("Traceback:")
        traceback.print_exc()
        print("!!!!!!!!!!!!!!!!!!!!!\n")
        return {"error": str(e), "type": type(e).__name__}, 500

    @app.errorhandler(422)
    def handle_422(e):
        import traceback
        print("\n!!! 422 ERROR !!!")
        print(f"Error: {e}")
        traceback.print_exc()
        print("!!!!!!!!!!!!!!!\n")
        return {"error": str(e)}, 422

    @app.errorhandler(NoAuthorizationError)
    def handle_no_auth(e):
        print(f"JWT Error: {e}")
        return {"msg": str(e)}, 401  # 422 yerine 401 dönsün




    @app.errorhandler(NoAuthorizationError)
    def handle_no_auth_error(e):
        print(f"NoAuthorizationError: {e}")
        return {"msg": "Missing Authorization Header"}, 401

    @app.errorhandler(InvalidHeaderError)
    def handle_invalid_header_error(e):
        print(f"InvalidHeaderError: {e}")
        return {"msg": "Invalid Authorization Header"}, 422

    @app.errorhandler(JWTDecodeError)
    def handle_jwt_decode_error(e):
        print(f"JWTDecodeError: {e}")
        return {"msg": "Token decode failed"}, 422

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        print(f"CSRFError: {e}")
        return {"msg": "CSRF token missing or invalid"}, 422

    # Tüm hataları yakala
    @app.errorhandler(Exception)
    def handle_all_exceptions(e):
        import traceback
        print(f"\n!!! EXCEPTION: {type(e).__name__} !!!")
        print(f"Message: {str(e)}")
        traceback.print_exc()
        print("!!!!!!!!!!!!!!!\n")
        return {"msg": str(e), "type": type(e).__name__}, 500


    # CORS
    CORS(
        app,
        resources={r"/api/*": {
            "origins": [
                "http://localhost:5173",
                "http://localhost:5000",
                "https://new2-dusky.vercel.app",
                "https://circleevent.app",
                "https://www.circleevent.app"
            ]
        }},
        supports_credentials=True
    )

    # API Blueprints
    from app.api.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    from app.api.general import bp as general_bp
    app.register_blueprint(general_bp, url_prefix="/api/general")

    # SPA Route
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def spa(path):
        if path.startswith("api/"):
            abort(404)
        return render_template("index.html")

    # Health Check
    @app.route("/health")
    def health():
        return {"status": "healthy"}, 200

    # --- SÜPER ADMIN KONTROLÜ (DOĞRU YER: return'den önce!) ---
    # --- GÜNCELLENMİŞ SÜPER ADMIN TOHUMLAMA ---
    with app.app_context():
        db.create_all()
        
        # User modelini import et
        from app.models import User 
        
        # 1. Önce superadmin var mı diye bakalım
        admin = User.query.filter_by(username='superadmin').first()
        
        # 2. Yoksa sıfırdan oluşturalım
        if not admin:
            print("--- Creating Super Admin... ---")

            admin = User(
                username='superadmin',
                email='admin@circle.app',
                first_name='Super',
                last_name='Admin',
                major='Management'
            )
            
            db.session.add(admin)
        
        # 3. VARSA DA YOKSA DA ŞUNLARI GÜNCELLE (ZORLA YAP)
        # Bu satırlar sayesinde eski hatalı rolü düzeltiyoruz!
        admin.role = 'superadmin' 
        admin.set_password('123456') # Şifreyi de garantiye alalım
        
        db.session.commit()
        print(f"--- Super Admin Role Updated to: {admin.role} ---")
    # -----------------------------------------------------------

    return app  # TEK VE SON return BU OLMALI

from app import models
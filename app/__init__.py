import logging
import os
from flask import Flask, render_template, abort, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from app.config import Config
from sqlalchemy import MetaData
from flask_jwt_extended.exceptions import (
    NoAuthorizationError,
    InvalidHeaderError,
    JWTDecodeError,
    CSRFError
)

# Logging Ayarı
logging.basicConfig(level=logging.DEBUG)

# --- OTOMATİK İSİMLENDİRME KURALI ---
convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
metadata = MetaData(naming_convention=convention)

# 1. db nesnesini EN BAŞTA tanımlıyoruz ki diğer dosyalar bunu import edebilsin
db = SQLAlchemy(metadata=metadata)
migrate = Migrate()
jwt = JWTManager()
mail = Mail()

def create_app(config_class=Config):
    app = Flask(
        __name__,
        static_folder="static",
        template_folder="templates",
        static_url_path=""
    )

    # Config yükle
    app.config.from_object(config_class)

    # Render/Prod ortamı için DB URL override
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        app.config["SQLALCHEMY_DATABASE_URI"] = db_url.replace("postgres://", "postgresql://")

    # JWT Config
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False
    app.config['JWT_CSRF_CHECK_FORM'] = False
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    app.config['JWT_HEADER_NAME'] = 'Authorization'
    app.config['JWT_HEADER_TYPE'] = 'Bearer'
    
    # Eklentileri başlat
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    jwt.init_app(app)
    mail.init_app(app)

    # CORS Ayarı
    CORS(app, supports_credentials=True) 

    # Security Headers (TC_11)
    @app.after_request
    def add_security_headers(response):
        response.headers['Strict-Transport-Security'] = 'max-age=0'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['Content-Security-Policy'] = "default-src * 'unsafe-inline' 'unsafe-eval' data: blob:;"
        return response

    # Request Logger
    @app.before_request
    def log_request_info():
        if "/health" in request.url:
            return
        print("\n=== INCOMING REQUEST ===")
        print(f"Method: {request.method}")
        print(f"URL: {request.url}")
        # print(f"Headers: {dict(request.headers)}") # Log kirliliği yapmasın diye kapattım
        if request.is_json:
            print(f"JSON Data: {request.get_json()}")
        print("=====================\n")

    # --- ERROR HANDLERS ---
    @app.errorhandler(NoAuthorizationError)
    def handle_auth_error(e):
        return {"msg": "Missing Authorization Header"}, 401

    @app.errorhandler(InvalidHeaderError)
    def handle_invalid_header_error(e):
        return {"msg": "Invalid Authorization Header"}, 422

    @app.errorhandler(JWTDecodeError)
    def handle_jwt_decode_error(e):
        return {"msg": "Token decode failed"}, 422

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return {"msg": "CSRF token missing or invalid"}, 422

    @app.errorhandler(422)
    def handle_422(e):
        return {"error": str(e)}, 422

    @app.errorhandler(Exception)
    def handle_all_exceptions(e):
        import traceback
        print(f"\n!!! EXCEPTION: {type(e).__name__} !!!")
        print(f"Message: {str(e)}")
        traceback.print_exc()
        return {"msg": str(e), "type": type(e).__name__}, 500

    # --- BLUEPRINTS ---
    # KRİTİK NOKTA: Blueprint importlarını BURADA (fonksiyon içinde) yapıyoruz.
    # Böylece 'db' nesnesi çoktan oluşmuş oluyor ve Circular Import hatası almıyoruz.
    
    from app.api.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    from app.api.general import bp as general_bp
    app.register_blueprint(general_bp, url_prefix="/api/general")

    from app.api.user import bp as user_bp
    app.register_blueprint(user_bp, url_prefix="/api/user")

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

    # --- FIXED SÜPER ADMIN SEEDING ---
    with app.app_context():
        db.create_all()
        from app.models import User 
        
        try:
            # We check by email or username to see if the admin exists
            admin = User.query.filter_by(username='superadmin').first()
            
            if not admin:
                print("--- Initializing Super Admin for the first time... ---")
                
                # Pull the password from Render Environment Variables
                # Default to a temporary string if you haven't set the Render variable yet
                initial_pw = os.environ.get("INITIAL_ADMIN_PASSWORD", "CircleAdmin2026!")
                
                admin = User(
                    username='superadmin',
                    email='admin@circle.app',
                    first_name='Super',
                    last_name='Admin',
                    major='Management',
                    role='super_admin'
                )
                
                # Hash the password only once during creation
                admin.set_password(initial_pw)
                
                db.session.add(admin)
                db.session.commit()
                print("--- Super Admin created and hashed. ---")
            else:
                # If the user is found, we do NOT run set_password. 
                # This protects your 'Forgot Password' changes from being reset
                print(f"--- Admin {admin.username} already exists. Persistent password maintained. ---")
                
        except Exception as e:
            print(f"Seeding Error (Ignored): {e}")
    return app

# Modelleri en sonda import ediyoruz ki migrate algılasın
from app import models
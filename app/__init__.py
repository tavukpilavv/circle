from flask import Flask, render_template, abort, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from app.config import Config
from sqlalchemy import MetaData
import logging
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
mail = Mail()

def create_app(config_class=Config):
    app = Flask(
        __name__,
        static_folder="static",
        template_folder="templates",
        static_url_path=""
    )

    # Load base config
    app.config.from_object(config_class)

    # Override DB from env (Render / prod)
    import os
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        app.config["SQLALCHEMY_DATABASE_URI"] = db_url

    # JWT Config
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False
    app.config['JWT_CSRF_CHECK_FORM'] = False
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    app.config['JWT_HEADER_NAME'] = 'Authorization'
    app.config['JWT_HEADER_TYPE'] = 'Bearer'
    
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    jwt.init_app(app)
    mail.init_app(app)

    # --- GLOBAL CORS AYARI (EN ÖNEMLİ KISIM) ---
    # Resources kısmını kaldırdım, tüm route'lara her yerden izin veriyoruz.
    # Development aşamasında en sorunsuz yöntem budur.
    CORS(app, supports_credentials=True) 

    @app.before_request
    def log_request_info():
        # Sağlık kontrolü loglarını kirletmemesi için filtreleyebilirsin
        if "/health" in request.url:
            return
        print("\n=== INCOMING REQUEST ===")
        print(f"Method: {request.method}")
        print(f"URL: {request.url}")
        print(f"Headers: {dict(request.headers)}")
        if request.is_json:
            print(f"JSON Data: {request.get_json()}")
        print("=====================\n")

    # --- ERROR HANDLERS (Tekrar edenleri temizledim) ---

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
    # Dikkat: URL Prefixleri '/api/...' şeklinde ayarlı.
    
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

    # --- SÜPER ADMIN SEEDING ---
    with app.app_context():
        db.create_all()
        from app.models import User 
        
        admin = User.query.filter_by(username='superadmin').first()
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
        
        # Rolü ve şifreyi güncelle
        admin.role = 'super_admin'
        admin.set_password('123456')
        db.session.commit()
        print(f"--- Super Admin Check: {admin.username} is ready ---")

    return app

from app import models
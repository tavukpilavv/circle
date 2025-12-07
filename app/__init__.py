from flask import Flask, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.config import Config
from sqlalchemy import MetaData

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

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    jwt.init_app(app)

    # CORS
    CORS(
        app,
        resources={r"/api/*": {
            "origins": [
                "http://localhost:5173",
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
        admin.role = 'super_admin' 
        admin.set_password('123456') # Şifreyi de garantiye alalım
        
        db.session.commit()
        print(f"--- Super Admin Role Updated to: {admin.role} ---")
    # -----------------------------------------------------------

    return app  # TEK VE SON return BU OLMALI

from app import models
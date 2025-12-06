from flask import Flask, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.config import Config
from sqlalchemy import MetaData  # SQLite Hata Çözümü İçin

# --- YENİ: OTOMATİK İSİMLENDİRME KURALI (SQLite Fix) ---
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
        template_folder="templates"
    )

    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    jwt.init_app(app)

    # CORS – şu anda zorunlu değil ama dursun
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

    # 🔵 SPA ana sayfa route'u
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def spa(path):
        # /api/* isteklerini SPA'ya yönlendirme
        if path.startswith("api/"):
            abort(404)
        return render_template("index.html")

    # Health Check Endpoint
    @app.route("/health")
    def health():
        return {"status": "healthy"}, 200

    return app


from app import models


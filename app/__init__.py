import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from app.config import Config
from sqlalchemy import MetaData # <--- YENİ EKLENDİ

# --- YENİ: OTOMATİK İSİMLENDİRME KURALI ---
# Bu kural, SQLite hatalarını sonsuza dek çözer.
convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata) # Metadata'yı buraya ekledik
# ------------------------------------------

migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    # render_as_batch=True ayarını buraya da ekleyelim, garanti olsun
    migrate.init_app(app, db, render_as_batch=True)
    
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    from app.api.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    from app.api.general import bp as general_bp
    app.register_blueprint(general_bp, url_prefix='/api/general')
    
    @app.route('/health')
    def health():
        return {'status': 'healthy'}, 200

    return app

from app import models
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    
    # CORS Ayarı (Tüm domainlere izin ver - Geliştirme için en rahatı)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    from app.api.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    from app.api.general import bp as general_bp
    app.register_blueprint(general_bp, url_prefix='/api/general')
    
    # Health Check (Render için lazım olacak)
    @app.route('/health')
    def health():
        return {'status': 'healthy'}, 200

    return app

from app import models
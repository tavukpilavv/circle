from circle.routes.auth import auth_bp
from circle.routes.event import events_bp
from circle.routes.venue import venues_bp


def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix="/api")
    app.register_blueprint(events_bp, url_prefix="/api")
    app.register_blueprint(venues_bp, url_prefix="/api")


__all__ = ["register_routes"]

from flask import Flask, g, request

from circle.config import get_config
from circle.errors import register_error_handlers
from circle.extensions import init_extensions, jwt
from circle.models import register_models
from circle.routes import register_routes
from circle.routes.auth import token_blocklist
from utils.helpers import resolve_university


def create_app(config_object=None):
    app = Flask(__name__)
    app.config.from_object(config_object or get_config())

    init_extensions(app)
    register_models()
    register_routes(app)
    register_error_handlers(app)

    @jwt.token_in_blocklist_loader
    def is_token_revoked(jwt_header, jwt_payload):
        return jwt_payload.get("jti") in token_blocklist

    @app.before_request
    def enforce_university_header():
        if request.path.startswith("/api"):
            university = resolve_university()
            g.university_id = university.id

    @app.after_request
    def add_security_headers(response):
        for header, value in app.config.get("SECURITY_HEADERS", {}).items():
            response.headers.setdefault(header, value)
        return response

    @app.route("/health")
    def healthcheck():
        return {"status": "ok"}

    return app


__all__ = ["create_app"]

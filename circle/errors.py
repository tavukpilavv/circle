from flask import jsonify
from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException


def _format_error(code: str, message: str, status: int = 400, details=None):
    payload = {"code": code, "message": message}
    if details:
        payload["details"] = details
    response = jsonify(payload)
    response.status_code = status
    return response


def register_error_handlers(app):
    @app.errorhandler(HTTPException)
    def handle_http_exception(err: HTTPException):
        return _format_error(
            code=err.name.replace(" ", "_"),
            message=err.description,
            status=err.code or 500,
        )

    @app.errorhandler(ValidationError)
    def handle_validation_error(err: ValidationError):
        return _format_error(
            "validation_error", "Invalid request", 422, err.messages
        )

    @app.errorhandler(Exception)
    def handle_generic_error(err: Exception):
        app.logger.exception(err)
        return _format_error("internal_error", "Unexpected error", 500)


__all__ = ["register_error_handlers"]

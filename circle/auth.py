from functools import wraps

from flask import abort, g
from flask_jwt_extended import get_jwt, verify_jwt_in_request


def require_roles(*roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            token_roles = claims.get("roles", [])
            if not any(role in token_roles for role in roles):
                abort(403, description="Forbidden")
            if g.get("university_id") and claims.get("university_id") != g.get("university_id"):
                abort(403, description="Cross-tenant access denied")
            return fn(*args, **kwargs)

        return wrapper

    return decorator


__all__ = ["require_roles"]

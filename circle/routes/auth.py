from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    jwt_required,
)

from circle.models.user import User
from circle.schemas import LoginSchema
from utils.helpers import resolve_university


auth_bp = Blueprint("auth", __name__)
token_blocklist: set[str] = set()


@auth_bp.route("/auth/login", methods=["POST"])
def login():
    university = resolve_university()
    payload = LoginSchema().load(request.get_json(force=True))
    user = User.query.filter_by(
        university_id=university.id, email=payload["email"]
    ).first()
    if not user or not user.check_password(payload["password"]):
        return (
            jsonify(
                {
                    "code": "invalid_credentials",
                    "message": "Invalid email or password",
                }
            ),
            401,
        )

    role_keys = [ur.role.key for ur in user.roles if ur.role]
    claims = {"roles": role_keys, "university_id": university.id}
    access = create_access_token(identity=user.id, additional_claims=claims)
    refresh = create_refresh_token(identity=user.id, additional_claims=claims)
    return jsonify({"access_token": access, "refresh_token": refresh})


@auth_bp.route("/auth/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    claims = get_jwt()
    identity = claims.get("sub")
    new_access = create_access_token(
        identity=identity,
        additional_claims={
            "roles": claims.get("roles", []),
            "university_id": claims.get("university_id"),
        },
    )
    return jsonify({"access_token": new_access})


@auth_bp.route("/auth/logout", methods=["POST"])
@jwt_required(verify_type=False)
def logout():
    jti = get_jwt().get("jti")
    token_blocklist.add(jti)
    return jsonify({"status": "logged_out"})


__all__ = ["auth_bp", "token_blocklist"]

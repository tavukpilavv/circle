from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import User
from werkzeug.security import generate_password_hash

bp = Blueprint('user', __name__)

@bp.route('/profile', methods=['GET'])
@jwt_required()
def get_user_profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
        
    # Construct full name from first and last name
    full_name = f"{user.first_name} {user.last_name}".strip()
    
    return jsonify({
        "name": full_name,
        "email": user.email,
        "avatar_url": user.avatar_url,
        "username": user.username # Adding username just in case, though not explicitly requested in JSON it's often useful
    }), 200

@bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_user_profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
        
    data = request.get_json()
    
    if 'name' in data:
        # Split name into first and last name
        parts = data['name'].strip().split(' ', 1)
        user.first_name = parts[0]
        user.last_name = parts[1] if len(parts) > 1 else ''
    
    if 'avatar_url' in data:
        user.avatar_url = data['avatar_url']
        
    try:
        db.session.commit()
        
        full_name = f"{user.first_name} {user.last_name}".strip()
        return jsonify({
            "message": "Profile updated successfully",
            "user": {
                "name": full_name,
                "avatar_url": user.avatar_url,
                 "email": user.email
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
         return jsonify({"error": "User not found"}), 404
         
    data = request.get_json()
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    
    if not current_password or not new_password:
        return jsonify({"error": "Both current and new passwords are required"}), 400
        
    # Verify old password
    if not user.check_password(current_password):
        return jsonify({"error": "Incorrect current password"}), 401
    
    # Update to new password
    user.set_password(new_password)
    
    try:
        db.session.commit()
        return jsonify({"message": "Password changed successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to update password"}), 500

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart  # <--- BU EKSİKTİ, EKLENDİ!
from email.header import Header
from datetime import timedelta
from flask import Blueprint, jsonify, request, current_app
from app import db
from app.models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, decode_token
from dotenv import load_dotenv
from sqlalchemy import or_

load_dotenv()

bp = Blueprint('auth', __name__)

# ===========================
# 1. REGISTER
# ===========================
@bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        if User.query.filter_by(email=data.get('email')).first():
            return jsonify({'error': 'Email is already in use.'}), 400
        
        if data.get('username') and User.query.filter_by(username=data.get('username')).first():
            return jsonify({'error': 'Username is already taken.'}), 400
        
        user = User(
            first_name=data.get('firstName'),
            last_name=data.get('lastName'),
            email=data.get('email'),
            username=data.get('username'),
            major=data.get('major')
        )
        user.set_password(data.get('password'))
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({'message': 'Registration successful!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===========================
# 2. LOGIN (Smart Login)
# ===========================
@bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        login_input = data.get('username') or data.get('email')
        password = data.get('password')

        if not login_input or not password:
            return jsonify({'error': 'Username/Email and password are required.'}), 400

        user = User.query.filter(
            or_(User.username == login_input, User.email == login_input)
        ).first()
        
        if user and user.check_password(password):
            access_token = create_access_token(identity=str(user.id))
            return jsonify({
                'message': 'Login successful.',
                'access_token': access_token,
                'user': {
                    'id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'username': user.username,
                    'major': user.major,
                    'role': 'super_admin' if user.role == 'superadmin' else user.role,
                    'avatar_url': user.avatar_url,
                    'managed_community_id': user.managed_community.id if user.managed_community else None
                }
            }), 200
            
        return jsonify({'error': 'Invalid username/email or password.'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===========================
# 3. FORGOT PASSWORD (HELP KODUYLA GÜNCELLENDİ ✅)
# ===========================
@bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    try:
        data = request.get_json()
        email = data.get('email')
        
        if not email:
            return jsonify({'error': 'Email address is required.'}), 400

        user = User.query.filter_by(email=email).first()
        
        if not user:
            # Güvenlik için kullanıcı yoksa bile başarılı gibi dönüyoruz
            return jsonify({'message': 'If your email is registered, you will receive a reset link.'}), 200

        # Token Oluşturma
        reset_token = create_access_token(
            identity=str(user.id),
            expires_delta=timedelta(minutes=15),
            additional_claims={"type": "reset"}
        )
        
        # Link Oluşturma
        frontend_url = os.environ.get('FRONTEND_URL', 'http://localhost:5173')
        reset_link = f"{frontend_url}/#/reset-password?token={reset_token}"
        
        print(f"\n=== PASSWORD RESET LINK ({email}) ===\n{reset_link}\n=====================================\n")

        # --- BURASI GENERAL.PY'DEN ALINAN ÇALIŞAN KOD YAPISI ---
        try:
            sender_email = os.environ.get('MAIL_USER')
            sender_password = os.environ.get('MAIL_PASS')

            if not sender_email or not sender_password:
                print("MAIL CONFIG ERROR: MAIL_USER or MAIL_PASS eksik.")
                # Hata dönmüyoruz ki frontend akışı bozulmasın
                return jsonify({'message': 'If your email is registered, you will receive a reset link.'}), 200

            # 1. MIMEMultipart kullanımı (Daha güvenli)
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = user.email
            
            subject = "Circle App - Password Reset Request"
            msg['Subject'] = Header(subject, 'utf-8')

            body = f"""
Hello {user.first_name},

You requested to reset your password. Click the link below (valid for 15 minutes):

{reset_link}

If you did not request this, please ignore this email.

Best,
Circle App Team
            """
            
            # 2. UTF-8 Kodlamasıyla Ekleme
            msg.attach(MIMEText(body, 'plain', 'utf-8'))

            # 3. Bağlantı ve Gönderim (General.py ile aynı)
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg) # Modern yöntem
            server.quit()
            
            print(f"✅ Mail başarıyla gönderildi: {user.email}")
            
        except Exception as mail_error:
            print(f"❌ MAIL HATASI: {str(mail_error)}")
            # Mail hatası olsa bile kullanıcıya başarılı diyoruz (Güvenlik standardı)
        
        return jsonify({'message': 'If your email is registered, you will receive a reset link.'}), 200

    except Exception as e:
        print(f"ERROR in forgot_password: {str(e)}")
        return jsonify({'error': 'An error occurred.'}), 500

# ===========================
# 4. RESET PASSWORD
# ===========================
@bp.route('/reset-password', methods=['POST'])
def reset_password():
    try:
        data = request.get_json()
        token = data.get('token')
        new_password = data.get('new_password')
        
        if not token or not new_password:
            return jsonify({'error': 'Token and new password are required.'}), 400
            
        try:
            decoded_token = decode_token(token)
            
            if decoded_token.get("type") != "reset":
                return jsonify({'error': 'Invalid token type.'}), 400
                
            user_id = decoded_token.get("sub")
            user = User.query.get(user_id)
            
            if not user:
                return jsonify({'error': 'User not found.'}), 404
                
            user.set_password(new_password)
            db.session.commit()
            
            return jsonify({'message': 'Password has been reset successfully. You can login now.'}), 200
            
        except Exception as token_error:
            print(f"TOKEN ERROR: {str(token_error)}")
            return jsonify({'error': 'Invalid or expired link.'}), 400
        
    except Exception as e:
        print(f"ERROR in reset_password: {str(e)}")
        return jsonify({'error': 'An error occurred.'}), 500

# ===========================
# 5. PROFILE & CHANGE PASSWORD
# ===========================
@bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found.'}), 404
            
        data = request.get_json()
        
        if 'avatar' in data:
            user.avatar_url = data['avatar']
            
        if 'name' in data:
            full_name = data['name'].strip()
            if full_name:
                parts = full_name.split(' ', 1)
                user.first_name = parts[0]
                user.last_name = parts[1] if len(parts) > 1 else ''
                
        db.session.commit()
        
        return jsonify({
            'message': 'Profile updated successfully.',
            'user': {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'username': user.username,
                'major': user.major,
                'role': 'super_admin' if user.role == 'superadmin' else user.role,
                'avatar_url': user.avatar_url,
                'managed_community_id': user.managed_community.id if user.managed_community else None
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'An error occurred while updating profile.'}), 500

@bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'User not found.'}), 404
            
        data = request.get_json()
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        
        if not current_password or not new_password:
            return jsonify({'error': 'Current password and new password are required.'}), 400
            
        if not user.check_password(current_password):
            return jsonify({'error': 'Incorrect current password.'}), 401
            
        user.set_password(new_password)
        db.session.commit()
        
        return jsonify({'message': 'Password changed successfully.'}), 200
        
    except Exception as e:
        return jsonify({'error': 'An error occurred while changing password.'}), 500
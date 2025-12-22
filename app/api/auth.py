from flask import Blueprint, jsonify, request, current_app
from app import db, mail
from app.models import User
from flask import Blueprint, jsonify, request, current_app
from app import db, mail
from app.models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        if User.query.filter_by(email=data.get('email')).first():
            return jsonify({'error': 'Bu email zaten kullanılıyor.'}), 400
        
        if data.get('username') and User.query.filter_by(username=data.get('username')).first():
            return jsonify({'error': 'Bu kullanıcı adı zaten alınmış.'}), 400
        
        # Yeni Kullanıcı (Username ve Major eklendi)
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
        
        return jsonify({'message': 'Kayıt Başarılı!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')

        if not password:
            return jsonify({'error': 'Email/Kullanıcı adı ve şifre gereklidir'}), 400

        user = None
        if email:
            user = User.query.filter_by(email=email).first()
        elif username:
            user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            access_token = create_access_token(identity=str(user.id))
            return jsonify({
                'message': 'Giriş Başarılı',
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
            
        return jsonify({'error': 'Email veya şifre hatalı'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    try:
        data = request.get_json()
        email = data.get('email')
        
        if not email:
            return jsonify({'error': 'Email adresi gereklidir.'}), 400

        user = User.query.filter_by(email=email).first()
        
        # Güvenlik: Kullanıcı bulunamasa bile 200 dönüyoruz (User Enumeration Attack önlemi)
        # Amaç: Kötü niyetli kişilerin hangi emaillerin kayıtlı olduğunu öğrenmesini engellemek
        if not user:
            print(f"DEBUG: Forgot password request for non-existent email: {email}")
            return jsonify({'message': 'Şifre sıfırlama bağlantısı gönderildi.'}), 200

        # Token Oluşturma
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        token = s.dumps(user.email, salt=current_app.config['SECURITY_PASSWORD_SALT'])
        
        # Link Oluşturma
        # Frontend URL'i config'den alıyoruz (yoksa varsayılan localhost:5173)
        frontend_url = current_app.config.get('FRONTEND_URL', 'http://localhost:5173')
        reset_link = f"{frontend_url}/#/reset-password?token={token}"
        
        print(f"\n=== PASSWORD RESET LINK ({email}) ===\n{reset_link}\n=====================================\n")

        # Email Gönderme
        try:
            msg = Message(
                subject='Circle App - Şifre Sıfırlama İsteği',
                recipients=[user.email],
                body=f"Şifrenizi sıfırlamak için aşağıdaki bağlantıya tıklayın:\n\n{reset_link}\n\nBu bağlantı 1 saat süreyle geçerlidir.",
                sender=current_app.config.get('MAIL_DEFAULT_SENDER', 'noreply@circle.app')
            )
            mail.send(msg)
        except Exception as mail_error:
            print(f"MAIL ERROR: {str(mail_error)}")
            # Email hatası olsa bile kullanıcıya başarılı döndük (security reasons + user experience)
            # Loglardan linki görebilirsiniz.
        
        return jsonify({'message': 'Şifre sıfırlama bağlantısı gönderildi.'}), 200

    except Exception as e:
        print(f"ERROR in forgot_password: {str(e)}")
        return jsonify({'error': 'Bir hata oluştu.'}), 500

@bp.route('/reset-password', methods=['POST'])
def reset_password():
    try:
        data = request.get_json()
        token = data.get('token')
        new_password = data.get('new_password')
        
        if not token or not new_password:
            return jsonify({'error': 'Token ve yeni şifre gereklidir.'}), 400
            
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        
        try:
            # Token geçerlilik süresi: 3600 saniye (1 saat)
            email = s.loads(token, salt=current_app.config['SECURITY_PASSWORD_SALT'], max_age=3600)
        except SignatureExpired:
            return jsonify({'error': 'Sıfırlama bağlantısının süresi dolmuş.'}), 400
        except BadSignature:
            return jsonify({'error': 'Geçersiz sıfırlama bağlantısı.'}), 400
            
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({'error': 'Kullanıcı bulunamadı.'}), 404
            
        user.set_password(new_password)
        db.session.commit()
        
        return jsonify({'message': 'Şifreniz başarıyla güncellendi.'}), 200
        
    except Exception as e:
        print(f"ERROR in reset_password: {str(e)}")
        return jsonify({'error': 'Bir hata oluştu.'}), 500

@bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'Kullanıcı bulunamadı.'}), 404
            
        data = request.get_json()
        
        # Avatar güncelleme
        if 'avatar' in data:
            user.avatar_url = data['avatar']
            
        # İsim güncelleme (Ad Soyad ayrıştırma)
        if 'name' in data:
            full_name = data['name'].strip()
            if full_name:
                parts = full_name.split(' ', 1)
                user.first_name = parts[0]
                user.last_name = parts[1] if len(parts) > 1 else ''
                
        db.session.commit()
        
        return jsonify({
            'message': 'Profil başarıyla güncellendi',
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
        print(f"ERROR in update_profile: {str(e)}")
        return jsonify({'error': 'Profil güncellenirken bir hata oluştu.'}), 500

@bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'Kullanıcı bulunamadı.'}), 404
            
        data = request.get_json()
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        
        if not current_password or not new_password:
            return jsonify({'error': 'Mevcut şifre ve yeni şifre gereklidir.'}), 400
            
        if not user.check_password(current_password):
            return jsonify({'error': 'Mevcut şifreniz hatalı.'}), 401
            
        user.set_password(new_password)
        db.session.commit()
        
        return jsonify({'message': 'Şifreniz başarıyla değiştirildi.'}), 200
        
    except Exception as e:
        print(f"ERROR in change_password: {str(e)}")
        return jsonify({'error': 'Şifre değiştirilirken bir hata oluştu.'}), 500
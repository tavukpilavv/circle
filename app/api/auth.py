from flask import Blueprint, jsonify, request
from app import db
from app.models import User
from flask_jwt_extended import create_access_token

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
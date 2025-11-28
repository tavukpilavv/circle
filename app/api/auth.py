from flask import Blueprint, jsonify, request
from app import db
from app.models import User

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(email=data.get('email')).first():
        return jsonify({'error': 'Bu email zaten kullanılıyor.'}), 400
    
    user = User(
        first_name=data.get('firstName'),
        last_name=data.get('lastName'),
        email=data.get('email')
    )
    user.set_password(data.get('password'))
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'Kayıt Başarılı!'}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data.get('email')).first()
    
    if user and user.check_password(data.get('password')):
        return jsonify({
            'message': 'Giriş Başarılı',
            'user': {
                'id': user.id,
                'first_name': user.first_name,
                'role': user.role,
                'avatar_url': user.avatar_url,
                # Eğer adminse yönettiği kulübün ID'sini de gönderelim
                'managed_community_id': user.managed_community.id if user.managed_community else None
            }
        }), 200
        
    return jsonify({'error': 'Email veya şifre hatalı'}), 401
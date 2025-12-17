from app import db
from datetime import datetime

# --- ARA TABLOLAR ---
user_community = db.Table('user_community',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('community_id', db.Integer, db.ForeignKey('community.id'))
)

user_event = db.Table('user_event',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'))
)

# --- ANA MODELLER ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(256))
    
    # Signup Formu Alanları
    username = db.Column(db.String(64), unique=True)
    major = db.Column(db.String(100))

    role = db.Column(db.String(20), default='student')
    avatar_url = db.Column(db.String(255))

    joined_communities = db.relationship('Community', secondary=user_community, backref=db.backref('members', lazy='dynamic'))
    registered_events = db.relationship('Event', secondary=user_event, backref=db.backref('participants', lazy='dynamic'))

    def set_password(self, password):
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        from werkzeug.security import check_password_hash
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

class Community(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    
    university = db.Column(db.String(100))
    category = db.Column(db.String(50))
    short_description = db.Column(db.String(255))
    description = db.Column(db.Text)

    contact_email = db.Column(db.String(120))
    contact_person = db.Column(db.String(100))
    instagram_link = db.Column(db.String(255))
    external_link = db.Column(db.String(255))

    image_url = db.Column(db.String, nullable=True)
    proof_document_url = db.Column(db.String, nullable=True)

    is_approved = db.Column(db.Boolean, default=False) # Onay Durumu

    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    admin = db.relationship('User', backref=db.backref('managed_community', uselist=False))

    events = db.relationship('Event', backref='host_community', lazy='dynamic')

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    date = db.Column(db.String(20))
    time = db.Column(db.String(20))
    location = db.Column(db.String(100))
    capacity = db.Column(db.Integer)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    
    # Puanlama
    rating = db.Column(db.Float, default=0.0)
    rating_count = db.Column(db.Integer, default=0)
    feedbacks = db.relationship('Rating', backref='rated_event', lazy='dynamic')
    
    community_id = db.Column(db.Integer, db.ForeignKey('community.id'))

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    
    score = db.Column(db.Integer)  # 1'den 5'e kadar puan
    comment = db.Column(db.Text)
    is_anonymous = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('user_id', 'event_id', name='uq_user_event_rating'),)
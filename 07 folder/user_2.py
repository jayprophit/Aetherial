from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
import uuid

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    
    # Profile information
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    phone_number = db.Column(db.String(20), nullable=True)
    avatar_url = db.Column(db.String(255), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    
    # Account status
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)
    is_kyc_verified = db.Column(db.Boolean, default=False, nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    is_moderator = db.Column(db.Boolean, default=False, nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login = db.Column(db.DateTime, nullable=True)
    
    # Email verification
    email_verification_token = db.Column(db.String(100), nullable=True)
    email_verification_sent_at = db.Column(db.DateTime, nullable=True)
    
    # Password reset
    password_reset_token = db.Column(db.String(100), nullable=True)
    password_reset_sent_at = db.Column(db.DateTime, nullable=True)
    
    # Privacy settings
    privacy_level = db.Column(db.String(20), default='public', nullable=False)  # public, friends, private
    allow_messaging = db.Column(db.Boolean, default=True, nullable=False)
    show_age = db.Column(db.Boolean, default=False, nullable=False)
    
    # Digital assets (for minors)
    digital_assets_locked = db.Column(db.Boolean, default=False, nullable=False)
    
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if not self.public_id:
            self.public_id = str(uuid.uuid4())

    def set_password(self, password):
        """Hash and set the user's password"""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Check if the provided password matches the user's password"""
        return bcrypt.check_password_hash(self.password_hash, password)

    def generate_verification_token(self):
        """Generate a new email verification token"""
        self.email_verification_token = str(uuid.uuid4())
        self.email_verification_sent_at = datetime.utcnow()
        return self.email_verification_token

    def generate_reset_token(self):
        """Generate a new password reset token"""
        self.password_reset_token = str(uuid.uuid4())
        self.password_reset_sent_at = datetime.utcnow()
        return self.password_reset_token

    def is_verification_token_valid(self):
        """Check if the email verification token is still valid (24 hours)"""
        if not self.email_verification_sent_at:
            return False
        return datetime.utcnow() - self.email_verification_sent_at < timedelta(hours=24)

    def is_reset_token_valid(self):
        """Check if the password reset token is still valid (1 hour)"""
        if not self.password_reset_sent_at:
            return False
        return datetime.utcnow() - self.password_reset_sent_at < timedelta(hours=1)

    def get_age(self):
        """Calculate user's age from date of birth"""
        if not self.date_of_birth:
            return None
        today = datetime.now().date()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

    def is_minor(self):
        """Check if user is under 18"""
        age = self.get_age()
        return age is not None and age < 18

    def can_access_chat(self):
        """Check if user can access chat features (13+)"""
        age = self.get_age()
        return age is None or age >= 13

    def update_last_login(self):
        """Update the last login timestamp"""
        self.last_login = datetime.utcnow()

    def to_dict(self, include_sensitive=False):
        """Convert user to dictionary for JSON serialization"""
        data = {
            'id': self.public_id,
            'username': self.username,
            'email': self.email if include_sensitive else None,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'avatar_url': self.avatar_url,
            'bio': self.bio,
            'is_verified': self.is_verified,
            'is_kyc_verified': self.is_kyc_verified,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'privacy_level': self.privacy_level,
            'allow_messaging': self.allow_messaging,
            'age': self.get_age() if self.show_age else None,
            'is_minor': self.is_minor(),
            'can_access_chat': self.can_access_chat(),
            'digital_assets_locked': self.digital_assets_locked
        }
        
        if include_sensitive:
            data.update({
                'phone_number': self.phone_number,
                'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
                'is_active': self.is_active,
                'is_admin': self.is_admin,
                'is_moderator': self.is_moderator,
                'show_age': self.show_age
            })
        
        return data

    def __repr__(self):
        return f'<User {self.username}>'


class UserSession(db.Model):
    __tablename__ = 'user_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    session_token = db.Column(db.String(255), unique=True, nullable=False)
    device_info = db.Column(db.String(255), nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    user = db.relationship('User', backref=db.backref('sessions', lazy=True))
    
    def __init__(self, user_id, device_info=None, ip_address=None, expires_in_days=30):
        self.user_id = user_id
        self.session_token = str(uuid.uuid4())
        self.device_info = device_info
        self.ip_address = ip_address
        self.expires_at = datetime.utcnow() + timedelta(days=expires_in_days)
    
    def is_valid(self):
        """Check if the session is still valid"""
        return self.is_active and datetime.utcnow() < self.expires_at
    
    def to_dict(self):
        return {
            'id': self.id,
            'session_token': self.session_token,
            'device_info': self.device_info,
            'ip_address': self.ip_address,
            'created_at': self.created_at.isoformat(),
            'expires_at': self.expires_at.isoformat(),
            'is_active': self.is_active
        }


class LoginAttempt(db.Model):
    __tablename__ = 'login_attempts'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    ip_address = db.Column(db.String(45), nullable=True)
    success = db.Column(db.Boolean, nullable=False)
    attempted_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_agent = db.Column(db.String(255), nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'ip_address': self.ip_address,
            'success': self.success,
            'attempted_at': self.attempted_at.isoformat(),
            'user_agent': self.user_agent
        }


from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from src.models.user import db, User
import jwt
import datetime
import re

auth_bp = Blueprint('auth', __name__)

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    # At least 8 characters, one uppercase, one lowercase, one digit
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    return True

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['email', 'password', 'firstName', 'lastName']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        email = data['email'].lower().strip()
        password = data['password']
        first_name = data['firstName'].strip()
        last_name = data['lastName'].strip()
        company = data.get('company', '').strip()
        phone = data.get('phone', '').strip()
        registration_type = data.get('registrationType', 'basic')  # basic, kyc_individual, kyc_business
        
        # Validate email format
        if not validate_email(email):
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Validate password strength
        if not validate_password(password):
            return jsonify({'error': 'Password must be at least 8 characters with uppercase, lowercase, and number'}), 400
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'error': 'User with this email already exists'}), 409
        
        # Determine access level based on registration type
        access_level = 'basic'  # Default
        verification_status = 'email_pending'
        
        if registration_type == 'kyc_individual':
            access_level = 'basic'  # Will upgrade after KYC completion
            verification_status = 'kyc_required'
        elif registration_type == 'kyc_business':
            access_level = 'basic'  # Will upgrade after KYC completion
            verification_status = 'kyc_business_required'
        
        # Create new user
        hashed_password = generate_password_hash(password)
        new_user = User(
            email=email,
            password_hash=hashed_password,
            first_name=first_name,
            last_name=last_name,
            company=company,
            phone=phone,
            is_active=True,
            access_level=access_level,
            verification_status=verification_status,
            registration_type=registration_type,
            created_at=datetime.datetime.utcnow()
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        # Generate JWT token
        token = jwt.encode({
            'user_id': new_user.id,
            'email': new_user.email,
            'access_level': new_user.access_level,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)
        }, 'asdf#FGSgvasgf$5$WGT', algorithm='HS256')
        
        # Determine next steps based on registration type
        next_steps = []
        if registration_type in ['kyc_individual', 'kyc_business']:
            next_steps.append('complete_kyc_verification')
        else:
            next_steps.append('verify_email')
        
        return jsonify({
            'message': 'User registered successfully',
            'token': token,
            'user': {
                'id': new_user.id,
                'email': new_user.email,
                'firstName': new_user.first_name,
                'lastName': new_user.last_name,
                'company': new_user.company,
                'phone': new_user.phone,
                'accessLevel': new_user.access_level,
                'verificationStatus': new_user.verification_status,
                'registrationType': new_user.registration_type
            },
            'next_steps': next_steps,
            'access_info': get_access_level_info(new_user.access_level)
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Registration failed', 'details': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400
        
        email = data['email'].lower().strip()
        password = data['password']
        
        # Find user by email
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Check password
        if not check_password_hash(user.password_hash, password):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Check if user is active
        if not user.is_active:
            return jsonify({'error': 'Account is deactivated'}), 401
        
        # Update last login
        user.last_login = datetime.datetime.utcnow()
        db.session.commit()
        
        # Generate JWT token
        token = jwt.encode({
            'user_id': user.id,
            'email': user.email,
            'access_level': user.access_level,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)
        }, 'asdf#FGSgvasgf$5$WGT', algorithm='HS256')
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': {
                'id': user.id,
                'email': user.email,
                'firstName': user.first_name,
                'lastName': user.last_name,
                'company': user.company,
                'phone': user.phone,
                'accessLevel': user.access_level,
                'verificationStatus': user.verification_status,
                'registrationType': user.registration_type,
                'lastLogin': user.last_login.isoformat() if user.last_login else None
            },
            'access_info': get_access_level_info(user.access_level)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Login failed', 'details': str(e)}), 500

@auth_bp.route('/guest-access', methods=['POST'])
def create_guest_session():
    """Create a temporary guest session for browsing"""
    try:
        guest_session = {
            'session_id': f"guest_{datetime.datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            'access_level': 'guest',
            'created_at': datetime.datetime.utcnow().isoformat(),
            'expires_at': (datetime.datetime.utcnow() + datetime.timedelta(hours=24)).isoformat(),
            'features_available': [
                'Browse social media content',
                'View educational content',
                'Browse marketplace products',
                'Watch demo videos',
                'Use basic tools'
            ]
        }
        
        return jsonify({
            'message': 'Guest session created',
            'guest_session': guest_session,
            'access_info': get_access_level_info('guest')
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to create guest session', 'details': str(e)}), 500

@auth_bp.route('/verify', methods=['POST'])
def verify_token():
    try:
        data = request.get_json()
        token = data.get('token')
        
        if not token:
            return jsonify({'error': 'Token is required'}), 400
        
        # Decode JWT token
        payload = jwt.decode(token, 'asdf#FGSgvasgf$5$WGT', algorithms=['HS256'])
        user_id = payload['user_id']
        
        # Find user
        user = User.query.get(user_id)
        if not user or not user.is_active:
            return jsonify({'error': 'Invalid token'}), 401
        
        return jsonify({
            'valid': True,
            'user': {
                'id': user.id,
                'email': user.email,
                'firstName': user.first_name,
                'lastName': user.last_name,
                'company': user.company,
                'phone': user.phone,
                'accessLevel': user.access_level,
                'verificationStatus': user.verification_status,
                'registrationType': user.registration_type
            },
            'access_info': get_access_level_info(user.access_level)
        }), 200
        
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401
    except Exception as e:
        return jsonify({'error': 'Token verification failed', 'details': str(e)}), 500

@auth_bp.route('/upgrade-access', methods=['POST'])
def upgrade_access_level():
    """Upgrade user access level after verification"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        target_level = data.get('target_level')
        verification_data = data.get('verification_data', {})
        
        if not all([user_id, target_level]):
            return jsonify({'error': 'User ID and target level are required'}), 400
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Validate upgrade path
        valid_upgrades = {
            'basic': ['verified'],
            'verified': ['kyc_individual', 'kyc_business'],
            'kyc_individual': ['kyc_business']
        }
        
        current_level = user.access_level
        if target_level not in valid_upgrades.get(current_level, []):
            return jsonify({'error': 'Invalid upgrade path'}), 400
        
        # Update user access level
        user.access_level = target_level
        user.verification_status = 'verified'
        user.verified_at = datetime.datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Access level upgraded successfully',
            'user': {
                'id': user.id,
                'accessLevel': user.access_level,
                'verificationStatus': user.verification_status
            },
            'new_features': get_access_level_info(target_level)['features']
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to upgrade access level', 'details': str(e)}), 500

def get_access_level_info(access_level):
    """Get information about an access level"""
    access_info = {
        'guest': {
            'name': 'Guest Access',
            'features': ['Browse content', 'View demos', 'Use basic tools'],
            'limitations': ['Cannot save data', 'Limited features', 'No personalization']
        },
        'basic': {
            'name': 'Basic User',
            'features': ['Create profile', 'Post content', 'Save preferences', 'Basic messaging'],
            'limitations': ['Limited transactions', 'No business features', 'Basic support']
        },
        'verified': {
            'name': 'Verified User',
            'features': ['Higher limits', 'Premium features', 'Advanced tools', 'Priority support'],
            'limitations': ['Limited business features', 'Restricted blockchain access']
        },
        'kyc_individual': {
            'name': 'KYC Individual',
            'features': ['Full blockchain access', 'Financial services', 'Advanced AI', 'API access'],
            'limitations': ['Cannot create business accounts']
        },
        'kyc_business': {
            'name': 'KYC Business',
            'features': ['All features', 'Business tools', 'Enterprise support', 'Custom integrations'],
            'limitations': []
        }
    }
    
    return access_info.get(access_level, access_info['guest'])

# ... (rest of the existing auth routes remain the same)
@auth_bp.route('/logout', methods=['POST'])
def logout():
    # For JWT tokens, logout is handled client-side by removing the token
    return jsonify({'message': 'Logout successful'}), 200

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    try:
        data = request.get_json()
        email = data.get('email', '').lower().strip()
        
        if not email or not validate_email(email):
            return jsonify({'error': 'Valid email is required'}), 400
        
        user = User.query.filter_by(email=email).first()
        if not user:
            # Don't reveal if email exists or not for security
            return jsonify({'message': 'If the email exists, a reset link has been sent'}), 200
        
        # Generate password reset token
        reset_token = jwt.encode({
            'user_id': user.id,
            'purpose': 'password_reset',
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, 'asdf#FGSgvasgf$5$WGT', algorithm='HS256')
        
        # In a real application, you would send this token via email
        # For demo purposes, we'll return it in the response
        return jsonify({
            'message': 'Password reset token generated',
            'resetToken': reset_token  # Remove this in production
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Password reset failed', 'details': str(e)}), 500

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    try:
        data = request.get_json()
        token = data.get('token')
        new_password = data.get('password')
        
        if not token or not new_password:
            return jsonify({'error': 'Token and new password are required'}), 400
        
        if not validate_password(new_password):
            return jsonify({'error': 'Password must be at least 8 characters with uppercase, lowercase, and number'}), 400
        
        # Decode reset token
        payload = jwt.decode(token, 'asdf#FGSgvasgf$5$WGT', algorithms=['HS256'])
        
        if payload.get('purpose') != 'password_reset':
            return jsonify({'error': 'Invalid reset token'}), 401
        
        user_id = payload['user_id']
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Update password
        user.password_hash = generate_password_hash(new_password)
        db.session.commit()
        
        return jsonify({'message': 'Password reset successful'}), 200
        
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Reset token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid reset token'}), 401
    except Exception as e:
        return jsonify({'error': 'Password reset failed', 'details': str(e)}), 500


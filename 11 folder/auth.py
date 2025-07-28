"""
Authentication routes for Unified Platform
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import bcrypt
import uuid
import re
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__)

# In-memory storage for demo (in production, use a proper database)
users_db = {}
verification_codes = {}
reset_tokens = {}

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    return True, "Password is valid"

@auth_bp.route('/register', methods=['POST'])
def register():
    """User registration"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['email', 'password', 'first_name', 'last_name']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400
        
        email = data['email'].lower().strip()
        password = data['password']
        first_name = data['first_name'].strip()
        last_name = data['last_name'].strip()
        
        # Validate email
        if not validate_email(email):
            return jsonify({'success': False, 'error': 'Invalid email format'}), 400
        
        # Check if user already exists
        if email in users_db:
            return jsonify({'success': False, 'error': 'User already exists'}), 409
        
        # Validate password
        is_valid, message = validate_password(password)
        if not is_valid:
            return jsonify({'success': False, 'error': message}), 400
        
        # Hash password
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Create user
        user_id = str(uuid.uuid4())
        verification_code = str(uuid.uuid4())[:8].upper()
        
        user = {
            'id': user_id,
            'email': email,
            'password_hash': password_hash,
            'first_name': first_name,
            'last_name': last_name,
            'is_verified': False,
            'is_active': True,
            'created_at': datetime.utcnow().isoformat(),
            'last_login': None,
            'profile': {
                'phone': data.get('phone', ''),
                'country': data.get('country', ''),
                'timezone': data.get('timezone', 'UTC'),
                'preferences': {
                    'notifications': True,
                    'marketing_emails': data.get('marketing_emails', False),
                    'two_factor_auth': False
                }
            }
        }
        
        users_db[email] = user
        verification_codes[email] = {
            'code': verification_code,
            'expires_at': datetime.utcnow() + timedelta(hours=24)
        }
        
        return jsonify({
            'success': True,
            'message': 'User registered successfully',
            'user_id': user_id,
            'verification_required': True,
            'verification_code': verification_code  # In production, send via email
        }), 201
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """User login"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'email' not in data or 'password' not in data:
            return jsonify({'success': False, 'error': 'Email and password are required'}), 400
        
        email = data['email'].lower().strip()
        password = data['password']
        
        # Check if user exists
        if email not in users_db:
            return jsonify({'success': False, 'error': 'Invalid credentials'}), 401
        
        user = users_db[email]
        
        # Check if user is active
        if not user['is_active']:
            return jsonify({'success': False, 'error': 'Account is deactivated'}), 401
        
        # Verify password
        if not bcrypt.checkpw(password.encode('utf-8'), user['password_hash']):
            return jsonify({'success': False, 'error': 'Invalid credentials'}), 401
        
        # Update last login
        user['last_login'] = datetime.utcnow().isoformat()
        
        # Create access token
        access_token = create_access_token(
            identity=user['id'],
            additional_claims={
                'email': user['email'],
                'first_name': user['first_name'],
                'last_name': user['last_name'],
                'is_verified': user['is_verified']
            }
        )
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'access_token': access_token,
            'user': {
                'id': user['id'],
                'email': user['email'],
                'first_name': user['first_name'],
                'last_name': user['last_name'],
                'is_verified': user['is_verified'],
                'last_login': user['last_login']
            }
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@auth_bp.route('/verify', methods=['POST'])
def verify_email():
    """Verify email address"""
    try:
        data = request.get_json()
        
        if 'email' not in data or 'code' not in data:
            return jsonify({'success': False, 'error': 'Email and verification code are required'}), 400
        
        email = data['email'].lower().strip()
        code = data['code'].upper().strip()
        
        # Check if verification code exists
        if email not in verification_codes:
            return jsonify({'success': False, 'error': 'No verification code found'}), 404
        
        verification_data = verification_codes[email]
        
        # Check if code has expired
        if datetime.utcnow() > verification_data['expires_at']:
            del verification_codes[email]
            return jsonify({'success': False, 'error': 'Verification code has expired'}), 400
        
        # Check if code matches
        if code != verification_data['code']:
            return jsonify({'success': False, 'error': 'Invalid verification code'}), 400
        
        # Verify user
        if email in users_db:
            users_db[email]['is_verified'] = True
            del verification_codes[email]
            
            return jsonify({
                'success': True,
                'message': 'Email verified successfully'
            }), 200
        else:
            return jsonify({'success': False, 'error': 'User not found'}), 404
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    """Request password reset"""
    try:
        data = request.get_json()
        
        if 'email' not in data:
            return jsonify({'success': False, 'error': 'Email is required'}), 400
        
        email = data['email'].lower().strip()
        
        # Check if user exists
        if email not in users_db:
            # Don't reveal if email exists or not
            return jsonify({
                'success': True,
                'message': 'If the email exists, a reset token has been sent'
            }), 200
        
        # Generate reset token
        reset_token = str(uuid.uuid4())
        reset_tokens[email] = {
            'token': reset_token,
            'expires_at': datetime.utcnow() + timedelta(hours=1)
        }
        
        return jsonify({
            'success': True,
            'message': 'Password reset token sent',
            'reset_token': reset_token  # In production, send via email
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    """Reset password with token"""
    try:
        data = request.get_json()
        
        required_fields = ['email', 'token', 'new_password']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400
        
        email = data['email'].lower().strip()
        token = data['token']
        new_password = data['new_password']
        
        # Check if reset token exists
        if email not in reset_tokens:
            return jsonify({'success': False, 'error': 'Invalid or expired reset token'}), 400
        
        reset_data = reset_tokens[email]
        
        # Check if token has expired
        if datetime.utcnow() > reset_data['expires_at']:
            del reset_tokens[email]
            return jsonify({'success': False, 'error': 'Reset token has expired'}), 400
        
        # Check if token matches
        if token != reset_data['token']:
            return jsonify({'success': False, 'error': 'Invalid reset token'}), 400
        
        # Validate new password
        is_valid, message = validate_password(new_password)
        if not is_valid:
            return jsonify({'success': False, 'error': message}), 400
        
        # Update password
        if email in users_db:
            password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            users_db[email]['password_hash'] = password_hash
            del reset_tokens[email]
            
            return jsonify({
                'success': True,
                'message': 'Password reset successfully'
            }), 200
        else:
            return jsonify({'success': False, 'error': 'User not found'}), 404
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get user profile"""
    try:
        user_id = get_jwt_identity()
        
        # Find user by ID
        user = None
        for email, user_data in users_db.items():
            if user_data['id'] == user_id:
                user = user_data
                break
        
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404
        
        return jsonify({
            'success': True,
            'user': {
                'id': user['id'],
                'email': user['email'],
                'first_name': user['first_name'],
                'last_name': user['last_name'],
                'is_verified': user['is_verified'],
                'is_active': user['is_active'],
                'created_at': user['created_at'],
                'last_login': user['last_login'],
                'profile': user['profile']
            }
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update user profile"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Find user by ID
        user = None
        user_email = None
        for email, user_data in users_db.items():
            if user_data['id'] == user_id:
                user = user_data
                user_email = email
                break
        
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404
        
        # Update allowed fields
        allowed_fields = ['first_name', 'last_name', 'phone', 'country', 'timezone']
        for field in allowed_fields:
            if field in data:
                if field in ['first_name', 'last_name']:
                    user[field] = data[field].strip()
                else:
                    user['profile'][field] = data[field]
        
        # Update preferences
        if 'preferences' in data:
            user['profile']['preferences'].update(data['preferences'])
        
        return jsonify({
            'success': True,
            'message': 'Profile updated successfully',
            'user': {
                'id': user['id'],
                'email': user['email'],
                'first_name': user['first_name'],
                'last_name': user['last_name'],
                'profile': user['profile']
            }
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """Change user password"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        required_fields = ['current_password', 'new_password']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400
        
        current_password = data['current_password']
        new_password = data['new_password']
        
        # Find user by ID
        user = None
        for email, user_data in users_db.items():
            if user_data['id'] == user_id:
                user = user_data
                break
        
        if not user:
            return jsonify({'success': False, 'error': 'User not found'}), 404
        
        # Verify current password
        if not bcrypt.checkpw(current_password.encode('utf-8'), user['password_hash']):
            return jsonify({'success': False, 'error': 'Current password is incorrect'}), 400
        
        # Validate new password
        is_valid, message = validate_password(new_password)
        if not is_valid:
            return jsonify({'success': False, 'error': message}), 400
        
        # Update password
        password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        user['password_hash'] = password_hash
        
        return jsonify({
            'success': True,
            'message': 'Password changed successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """User logout"""
    try:
        # In a real application, you would invalidate the token
        # For this demo, we'll just return success
        return jsonify({
            'success': True,
            'message': 'Logged out successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


from flask import Blueprint, request, jsonify, session
import hashlib
import secrets
import datetime

auth_bp = Blueprint('auth', __name__)

# Simple in-memory user store for demo purposes
users_db = {
    'admin': {
        'password_hash': hashlib.sha256('admin123'.encode()).hexdigest(),
        'role': 'admin',
        'permissions': ['all']
    },
    'user': {
        'password_hash': hashlib.sha256('user123'.encode()).hexdigest(),
        'role': 'user',
        'permissions': ['read', 'write']
    }
}

# Active sessions store
active_sessions = {}

@auth_bp.route('/login', methods=['POST'])
def login():
    """User login endpoint"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({
                'success': False,
                'message': 'Username and password required'
            }), 400
        
        # Check user credentials
        if username in users_db:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            if users_db[username]['password_hash'] == password_hash:
                # Create session
                session_token = secrets.token_urlsafe(32)
                session_data = {
                    'username': username,
                    'role': users_db[username]['role'],
                    'permissions': users_db[username]['permissions'],
                    'login_time': datetime.datetime.utcnow().isoformat(),
                    'expires_at': (datetime.datetime.utcnow() + datetime.timedelta(hours=24)).isoformat()
                }
                
                active_sessions[session_token] = session_data
                session['user'] = username
                session['token'] = session_token
                
                return jsonify({
                    'success': True,
                    'message': 'Login successful',
                    'token': session_token,
                    'user': {
                        'username': username,
                        'role': users_db[username]['role'],
                        'permissions': users_db[username]['permissions']
                    },
                    'platform_access': {
                        'quantum_virtual_assistant': True,
                        'social_network_hub': True,
                        'ecommerce_marketplace': True,
                        'education_hub': True,
                        'rdlab_community': True,
                        'iot_manufacturing': True,
                        'developer_tools': True,
                        'metaverse_module': True
                    }
                })
            
        return jsonify({
            'success': False,
            'message': 'Invalid credentials'
        }), 401
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Login failed',
            'error': str(e)
        }), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """User logout endpoint"""
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        if token in active_sessions:
            del active_sessions[token]
        
        session.clear()
        
        return jsonify({
            'success': True,
            'message': 'Logout successful'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Logout failed',
            'error': str(e)
        }), 500

@auth_bp.route('/verify', methods=['GET'])
def verify_token():
    """Verify authentication token"""
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        if token in active_sessions:
            session_data = active_sessions[token]
            expires_at = datetime.datetime.fromisoformat(session_data['expires_at'])
            
            if datetime.datetime.utcnow() < expires_at:
                return jsonify({
                    'success': True,
                    'valid': True,
                    'user': {
                        'username': session_data['username'],
                        'role': session_data['role'],
                        'permissions': session_data['permissions']
                    },
                    'session_info': {
                        'login_time': session_data['login_time'],
                        'expires_at': session_data['expires_at']
                    }
                })
            else:
                # Token expired
                del active_sessions[token]
                return jsonify({
                    'success': False,
                    'valid': False,
                    'message': 'Token expired'
                }), 401
        
        return jsonify({
            'success': False,
            'valid': False,
            'message': 'Invalid token'
        }), 401
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Token verification failed',
            'error': str(e)
        }), 500

@auth_bp.route('/register', methods=['POST'])
def register():
    """User registration endpoint"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        
        if not username or not password:
            return jsonify({
                'success': False,
                'message': 'Username and password required'
            }), 400
        
        if username in users_db:
            return jsonify({
                'success': False,
                'message': 'Username already exists'
            }), 409
        
        # Create new user
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        users_db[username] = {
            'password_hash': password_hash,
            'role': 'user',
            'permissions': ['read', 'write'],
            'email': email,
            'created_at': datetime.datetime.utcnow().isoformat()
        }
        
        return jsonify({
            'success': True,
            'message': 'Registration successful',
            'user': {
                'username': username,
                'role': 'user',
                'email': email
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Registration failed',
            'error': str(e)
        }), 500

@auth_bp.route('/profile', methods=['GET'])
def get_profile():
    """Get user profile information"""
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        if token in active_sessions:
            session_data = active_sessions[token]
            username = session_data['username']
            
            if username in users_db:
                user_data = users_db[username].copy()
                user_data.pop('password_hash', None)  # Remove sensitive data
                
                return jsonify({
                    'success': True,
                    'profile': {
                        'username': username,
                        'role': user_data['role'],
                        'permissions': user_data['permissions'],
                        'email': user_data.get('email', ''),
                        'created_at': user_data.get('created_at', ''),
                        'platform_access': {
                            'quantum_virtual_assistant': True,
                            'social_network_hub': True,
                            'ecommerce_marketplace': True,
                            'education_hub': True,
                            'rdlab_community': True,
                            'iot_manufacturing': True,
                            'developer_tools': True,
                            'metaverse_module': True,
                            'biometric_security': True,
                            'quantum_computing': True,
                            'consciousness_level_ai': True
                        }
                    }
                })
        
        return jsonify({
            'success': False,
            'message': 'Authentication required'
        }), 401
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Profile retrieval failed',
            'error': str(e)
        }), 500

@auth_bp.route('/biometric/enroll', methods=['POST'])
def enroll_biometric():
    """Enroll biometric authentication"""
    try:
        data = request.get_json()
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        biometric_type = data.get('biometric_type')
        biometric_data = data.get('biometric_data')
        
        if token not in active_sessions:
            return jsonify({
                'success': False,
                'message': 'Authentication required'
            }), 401
        
        # Simulate biometric enrollment
        return jsonify({
            'success': True,
            'message': f'{biometric_type} biometric enrolled successfully',
            'biometric_id': secrets.token_urlsafe(16),
            'accuracy': '99.99%',
            'quantum_signature': secrets.token_urlsafe(32)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Biometric enrollment failed',
            'error': str(e)
        }), 500

@auth_bp.route('/quantum/authenticate', methods=['POST'])
def quantum_authenticate():
    """Quantum-level authentication"""
    try:
        data = request.get_json()
        quantum_signature = data.get('quantum_signature')
        consciousness_level = data.get('consciousness_level', 1)
        
        # Simulate quantum authentication
        return jsonify({
            'success': True,
            'message': 'Quantum authentication successful',
            'quantum_verified': True,
            'consciousness_level': consciousness_level,
            'quantum_entanglement_id': secrets.token_urlsafe(32),
            'security_clearance': 'cosmic_top_secret',
            'access_granted': {
                'private_repository': True,
                'quantum_computing': True,
                'consciousness_interface': True,
                'interdimensional_systems': True,
                'biometric_core': True
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Quantum authentication failed',
            'error': str(e)
        }), 500


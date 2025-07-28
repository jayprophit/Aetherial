    }
}

# Session storage (in production, use Redis or similar)
sessions_db = {}

def generate_user_id():
    """Generate a unique user ID"""
    return f"user_{secrets.token_urlsafe(8)}"

def generate_token():
    """Generate a secure random token"""
    return secrets.token_urlsafe(32)

def hash_password(password):
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

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

def send_verification_email(email, token):
    """Send email verification (mock implementation)"""
    # In production, implement actual email sending
    print(f"Verification email sent to {email} with token: {token}")
    return True

def send_password_reset_email(email, token):
    """Send password reset email (mock implementation)"""
    # In production, implement actual email sending
    print(f"Password reset email sent to {email} with token: {token}")
    return True

@auth_bp.route('/register', methods=['POST'])
def register():
    """User registration endpoint"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['username', 'email', 'password', 'first_name', 'last_name']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400
        
        username = data['username'].lower().strip()
        email = data['email'].lower().strip()
        password = data['password']
        first_name = data['first_name'].strip()
        last_name = data['last_name'].strip()
        
        # Validate input
        if len(username) < 3:
            return jsonify({'success': False, 'error': 'Username must be at least 3 characters long'}), 400
        
        if not validate_email(email):
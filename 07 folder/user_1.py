from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import User, db
from datetime import datetime

user_bp = Blueprint('user', __name__)

@user_bp.route('/', methods=['GET'])
@jwt_required()
def get_users():
    """Get list of users (admin only or public profiles)"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.filter_by(public_id=current_user_id).first()
        
        if not current_user:
            return jsonify({'error': 'Invalid user'}), 401
        
        # Build query based on user permissions
        query = User.query.filter_by(is_active=True)
        
        # Non-admin users can only see public profiles
        if not current_user.is_admin:
            query = query.filter_by(privacy_level='public')
        
        # Pagination
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)
        
        # Search functionality
        search = request.args.get('search', '').strip()
        if search:
            query = query.filter(
                db.or_(
                    User.username.ilike(f'%{search}%'),
                    User.first_name.ilike(f'%{search}%'),
                    User.last_name.ilike(f'%{search}%')
                )
            )
        
        # Age filter for appropriate content
        min_age = request.args.get('min_age', type=int)
        if min_age:
            # Calculate birth date for minimum age
            from datetime import date, timedelta
            max_birth_date = date.today() - timedelta(days=min_age * 365.25)
            query = query.filter(User.date_of_birth <= max_birth_date)
        
        users = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        return jsonify({
            'users': [user.to_dict() for user in users.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': users.total,
                'pages': users.pages,
                'has_next': users.has_next,
                'has_prev': users.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get users', 'details': str(e)}), 500

@user_bp.route('/', methods=['POST'])
@jwt_required()
def create_user():
    """Create new user (admin only)"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.filter_by(public_id=current_user_id).first()
        
        if not current_user or not current_user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['username', 'email', 'password', 'first_name', 'last_name']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Check if user already exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 409
        
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already taken'}), 409
        
        # Create new user
        user = User(
            username=data['username'],
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            phone_number=data.get('phone_number'),
            bio=data.get('bio', ''),
            is_admin=data.get('is_admin', False),
            is_moderator=data.get('is_moderator', False),
            is_verified=data.get('is_verified', False),
            privacy_level=data.get('privacy_level', 'public')
        )
        
        user.set_password(data['password'])
        
        # Handle date of birth if provided
        if data.get('date_of_birth'):
            try:
                user.date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
                if user.is_minor():
                    user.digital_assets_locked = True
            except ValueError:
                return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'User created successfully',
            'user': user.to_dict(include_sensitive=True)
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'User creation failed', 'details': str(e)}), 500

@user_bp.route('/<user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """Get specific user by ID"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.filter_by(public_id=current_user_id).first()
        
        if not current_user:
            return jsonify({'error': 'Invalid user'}), 401
        
        # Find target user
        user = User.query.filter_by(public_id=user_id).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Check privacy permissions
        include_sensitive = False
        if (current_user.public_id == user_id or 
            current_user.is_admin or 
            user.privacy_level == 'public'):
            include_sensitive = current_user.public_id == user_id or current_user.is_admin
            
            return jsonify({
                'user': user.to_dict(include_sensitive=include_sensitive)
            }), 200
        else:
            return jsonify({'error': 'Access denied'}), 403
            
    except Exception as e:
        return jsonify({'error': 'Failed to get user', 'details': str(e)}), 500

@user_bp.route('/<user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    """Update user (self or admin only)"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.filter_by(public_id=current_user_id).first()
        
        if not current_user:
            return jsonify({'error': 'Invalid user'}), 401
        
        # Find target user
        user = User.query.filter_by(public_id=user_id).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Check permissions
        if current_user.public_id != user_id and not current_user.is_admin:
            return jsonify({'error': 'Access denied'}), 403
        
        data = request.get_json()
        
        # Update allowed fields
        if current_user.is_admin:
            # Admin can update all fields
            admin_fields = [
                'username', 'email', 'first_name', 'last_name', 'phone_number',
                'bio', 'is_admin', 'is_moderator', 'is_verified', 'is_kyc_verified',
                'is_active', 'privacy_level', 'allow_messaging', 'show_age'
            ]
            for field in admin_fields:
                if field in data:
                    if field == 'username' and data[field] != user.username:
                        if User.query.filter_by(username=data[field]).first():
                            return jsonify({'error': 'Username already taken'}), 409
                    elif field == 'email' and data[field] != user.email:
                        if User.query.filter_by(email=data[field]).first():
                            return jsonify({'error': 'Email already registered'}), 409
                    setattr(user, field, data[field])
        else:
            # Regular users can only update their own profile fields
            user_fields = [
                'first_name', 'last_name', 'phone_number', 'bio',
                'privacy_level', 'allow_messaging', 'show_age', 'avatar_url'
            ]
            for field in user_fields:
                if field in data:
                    setattr(user, field, data[field])
            
            # Handle username update for self
            if 'username' in data and data['username'] != user.username:
                if User.query.filter_by(username=data['username']).first():
                    return jsonify({'error': 'Username already taken'}), 409
                user.username = data['username']
        
        # Handle date of birth update
        if 'date_of_birth' in data and data['date_of_birth']:
            try:
                user.date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
                # Update digital asset locking for minors
                if user.is_minor():
                    user.digital_assets_locked = True
                else:
                    user.digital_assets_locked = False
            except ValueError:
                return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'User updated successfully',
            'user': user.to_dict(include_sensitive=current_user.public_id == user_id or current_user.is_admin)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'User update failed', 'details': str(e)}), 500

@user_bp.route('/<user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    """Delete user (admin only)"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.filter_by(public_id=current_user_id).first()
        
        if not current_user or not current_user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403
        
        user = User.query.filter_by(public_id=user_id).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Prevent admin from deleting themselves
        if current_user.public_id == user_id:
            return jsonify({'error': 'Cannot delete your own account'}), 400
        
        # Soft delete - deactivate instead of hard delete
        user.is_active = False
        user.updated_at = datetime.utcnow()
        
        # Deactivate all user sessions
        from src.models.user import UserSession
        UserSession.query.filter_by(user_id=user.id).update({'is_active': False})
        
        db.session.commit()
        
        return jsonify({'message': 'User deactivated successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'User deletion failed', 'details': str(e)}), 500

@user_bp.route('/<user_id>/verify-kyc', methods=['POST'])
@jwt_required()
def verify_kyc(user_id):
    """Verify user's KYC status (admin/moderator only)"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.filter_by(public_id=current_user_id).first()
        
        if not current_user or not (current_user.is_admin or current_user.is_moderator):
            return jsonify({'error': 'Admin or moderator access required'}), 403
        
        user = User.query.filter_by(public_id=user_id).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        kyc_verified = data.get('kyc_verified', True)
        
        user.is_kyc_verified = kyc_verified
        user.updated_at = datetime.utcnow()
        
        # If user is now KYC verified and is an adult, unlock digital assets
        if kyc_verified and not user.is_minor():
            user.digital_assets_locked = False
        
        db.session.commit()
        
        return jsonify({
            'message': f'KYC status {"verified" if kyc_verified else "unverified"} successfully',
            'user': user.to_dict(include_sensitive=True)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'KYC verification failed', 'details': str(e)}), 500

@user_bp.route('/<user_id>/toggle-assets', methods=['POST'])
@jwt_required()
def toggle_digital_assets(user_id):
    """Toggle digital asset locking (admin only)"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.filter_by(public_id=current_user_id).first()
        
        if not current_user or not current_user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403
        
        user = User.query.filter_by(public_id=user_id).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        lock_assets = data.get('lock_assets', not user.digital_assets_locked)
        
        # Prevent unlocking assets for minors unless they're KYC verified
        if not lock_assets and user.is_minor() and not user.is_kyc_verified:
            return jsonify({'error': 'Cannot unlock digital assets for unverified minors'}), 400
        
        user.digital_assets_locked = lock_assets
        user.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'message': f'Digital assets {"locked" if lock_assets else "unlocked"} successfully',
            'user': user.to_dict(include_sensitive=True)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Digital asset toggle failed', 'details': str(e)}), 500

@user_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_user_stats():
    """Get user statistics (admin only)"""
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.filter_by(public_id=current_user_id).first()
        
        if not current_user or not current_user.is_admin:
            return jsonify({'error': 'Admin access required'}), 403
        
        # Calculate statistics
        total_users = User.query.count()
        active_users = User.query.filter_by(is_active=True).count()
        verified_users = User.query.filter_by(is_verified=True).count()
        kyc_verified_users = User.query.filter_by(is_kyc_verified=True).count()
        
        # Age-based statistics
        from datetime import date, timedelta
        today = date.today()
        minor_cutoff = today - timedelta(days=18 * 365.25)
        teen_cutoff = today - timedelta(days=13 * 365.25)
        
        minors = User.query.filter(User.date_of_birth > minor_cutoff).count()
        teens = User.query.filter(
            User.date_of_birth <= minor_cutoff,
            User.date_of_birth > teen_cutoff
        ).count()
        
        # Recent registrations (last 30 days)
        recent_cutoff = datetime.utcnow() - timedelta(days=30)
        recent_registrations = User.query.filter(User.created_at >= recent_cutoff).count()
        
        return jsonify({
            'total_users': total_users,
            'active_users': active_users,
            'verified_users': verified_users,
            'kyc_verified_users': kyc_verified_users,
            'minors': minors,
            'teens': teens,
            'recent_registrations': recent_registrations,
            'verification_rate': round((verified_users / total_users * 100) if total_users > 0 else 0, 2),
            'kyc_rate': round((kyc_verified_users / total_users * 100) if total_users > 0 else 0, 2)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get user statistics', 'details': str(e)}), 500


from flask import Blueprint, request, jsonify, session
from src.models.user import db
from datetime import datetime

notifications_bp = Blueprint('notifications', __name__)

# For now, we'll use mock notifications since we don't have a full notification system
# In a real implementation, you'd have a Notification model and real-time notification system

def require_auth():
    """Check if user is authenticated"""
    if 'user_id' not in session:
        return False, jsonify({'error': 'Authentication required'}), 401
    return True, None, None

@notifications_bp.route('/', methods=['GET'])
def get_notifications():
    """Get user notifications"""
    is_auth, error_response, status_code = require_auth()
    if not is_auth:
        return error_response, status_code
    
    try:
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 50)
        unread_only = request.args.get('unread_only', 'false').lower() == 'true'
        
        # Mock notifications for demonstration
        # In a real implementation, these would come from a database
        mock_notifications = [
            {
                'id': 1,
                'type': 'like',
                'title': 'New Like',
                'message': 'Sarah Johnson liked your post about AI Revolution',
                'user': {
                    'id': 2,
                    'username': 'sarah_j',
                    'full_name': 'Sarah Johnson',
                    'avatar_url': 'https://images.unsplash.com/photo-1494790108755-2616b612b786?w=150'
                },
                'post_id': 123,
                'is_read': False,
                'created_at': '2024-01-15T10:30:00Z'
            },
            {
                'id': 2,
                'type': 'comment',
                'title': 'New Comment',
                'message': 'John Doe commented on your post: "Great insights on quantum computing!"',
                'user': {
                    'id': 3,
                    'username': 'john_doe',
                    'full_name': 'John Doe',
                    'avatar_url': 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150'
                },
                'post_id': 124,
                'is_read': False,
                'created_at': '2024-01-15T09:15:00Z'
            },
            {
                'id': 3,
                'type': 'follow',
                'title': 'New Follower',
                'message': 'Alex Chen started following you',
                'user': {
                    'id': 4,
                    'username': 'alex_chen',
                    'full_name': 'Alex Chen',
                    'avatar_url': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150'
                },
                'is_read': True,
                'created_at': '2024-01-15T08:45:00Z'
            },
            {
                'id': 4,
                'type': 'share',
                'title': 'Post Shared',
                'message': 'Maria Garcia shared your post about blockchain technology',
                'user': {
                    'id': 5,
                    'username': 'maria_g',
                    'full_name': 'Maria Garcia',
                    'avatar_url': 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=150'
                },
                'post_id': 125,
                'is_read': True,
                'created_at': '2024-01-15T07:20:00Z'
            },
            {
                'id': 5,
                'type': 'mention',
                'title': 'You were mentioned',
                'message': 'David Kim mentioned you in a post about robotics',
                'user': {
                    'id': 6,
                    'username': 'david_kim',
                    'full_name': 'David Kim',
                    'avatar_url': 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150'
                },
                'post_id': 126,
                'is_read': False,
                'created_at': '2024-01-14T22:10:00Z'
            },
            {
                'id': 6,
                'type': 'system',
                'title': 'Welcome to the Platform!',
                'message': 'Welcome to our unified social platform! Start by following some users and creating your first post.',
                'is_read': True,
                'created_at': '2024-01-14T20:00:00Z'
            }
        ]
        
        # Filter unread if requested
        if unread_only:
            mock_notifications = [n for n in mock_notifications if not n['is_read']]
        
        # Simulate pagination
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_notifications = mock_notifications[start_idx:end_idx]
        
        total_notifications = len(mock_notifications)
        total_pages = (total_notifications + per_page - 1) // per_page
        
        return jsonify({
            'notifications': paginated_notifications,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total_notifications,
                'pages': total_pages,
                'has_next': page < total_pages,
                'has_prev': page > 1
            },
            'unread_count': len([n for n in mock_notifications if not n['is_read']])
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch notifications', 'details': str(e)}), 500

@notifications_bp.route('/<int:notification_id>/read', methods=['POST'])
def mark_notification_read(notification_id):
    """Mark a notification as read"""
    is_auth, error_response, status_code = require_auth()
    if not is_auth:
        return error_response, status_code
    
    try:
        # In a real implementation, you would update the notification in the database
        # For now, we'll just return success
        
        return jsonify({
            'message': 'Notification marked as read',
            'notification_id': notification_id
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to mark notification as read', 'details': str(e)}), 500

@notifications_bp.route('/mark-all-read', methods=['POST'])
def mark_all_notifications_read():
    """Mark all notifications as read"""
    is_auth, error_response, status_code = require_auth()
    if not is_auth:
        return error_response, status_code
    
    try:
        # In a real implementation, you would update all user's notifications in the database
        
        return jsonify({
            'message': 'All notifications marked as read'
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to mark all notifications as read', 'details': str(e)}), 500

@notifications_bp.route('/unread-count', methods=['GET'])
def get_unread_count():
    """Get count of unread notifications"""
    is_auth, error_response, status_code = require_auth()
    if not is_auth:
        return error_response, status_code
    
    try:
        # Mock unread count
        # In a real implementation, this would query the database
        unread_count = 3
        
        return jsonify({
            'unread_count': unread_count
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get unread count', 'details': str(e)}), 500

@notifications_bp.route('/settings', methods=['GET'])
def get_notification_settings():
    """Get user notification preferences"""
    is_auth, error_response, status_code = require_auth()
    if not is_auth:
        return error_response, status_code
    
    try:
        # Mock notification settings
        # In a real implementation, these would be stored in user preferences
        settings = {
            'email_notifications': True,
            'push_notifications': True,
            'notification_types': {
                'likes': True,
                'comments': True,
                'follows': True,
                'shares': True,
                'mentions': True,
                'messages': True,
                'system': True
            },
            'quiet_hours': {
                'enabled': False,
                'start_time': '22:00',
                'end_time': '08:00'
            }
        }
        
        return jsonify({
            'settings': settings
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get notification settings', 'details': str(e)}), 500

@notifications_bp.route('/settings', methods=['POST'])
def update_notification_settings():
    """Update user notification preferences"""
    is_auth, error_response, status_code = require_auth()
    if not is_auth:
        return error_response, status_code
    
    try:
        data = request.get_json()
        
        # In a real implementation, you would validate and save these settings
        # For now, we'll just return success
        
        return jsonify({
            'message': 'Notification settings updated successfully',
            'settings': data
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to update notification settings', 'details': str(e)}), 500

@notifications_bp.route('/test', methods=['POST'])
def send_test_notification():
    """Send a test notification (for development)"""
    is_auth, error_response, status_code = require_auth()
    if not is_auth:
        return error_response, status_code
    
    try:
        data = request.get_json()
        notification_type = data.get('type', 'test')
        message = data.get('message', 'This is a test notification')
        
        # In a real implementation, you would create and send a real notification
        test_notification = {
            'id': 999,
            'type': notification_type,
            'title': 'Test Notification',
            'message': message,
            'is_read': False,
            'created_at': datetime.utcnow().isoformat()
        }
        
        return jsonify({
            'message': 'Test notification sent',
            'notification': test_notification
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to send test notification', 'details': str(e)}), 500


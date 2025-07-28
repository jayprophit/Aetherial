from flask import Blueprint, request, jsonify, session
from src.models.user import db, User, Follow
from datetime import datetime

social_bp = Blueprint('social', __name__)

def require_auth():
    """Check if user is authenticated"""
    if 'user_id' not in session:
        return False, jsonify({'error': 'Authentication required'}), 401
    return True, None, None

@social_bp.route('/follow/<int:user_id>', methods=['POST'])
def follow_user(user_id):
    """Follow a user"""
    is_auth, error_response, status_code = require_auth()
    if not is_auth:
        return error_response, status_code
    
    try:
        current_user_id = session['user_id']
        
        # Can't follow yourself
        if current_user_id == user_id:
            return jsonify({'error': 'Cannot follow yourself'}), 400
        
        # Check if target user exists
        target_user = User.query.get_or_404(user_id)
        
        # Check if already following
        existing_follow = Follow.query.filter_by(
            follower_id=current_user_id,
            following_id=user_id
        ).first()
        
        if existing_follow:
            return jsonify({'error': 'Already following this user'}), 400
        
        # Create follow relationship
        new_follow = Follow(
            follower_id=current_user_id,
            following_id=user_id,
            created_at=datetime.utcnow()
        )
        
        db.session.add(new_follow)
        
        # Update follower counts
        current_user = User.query.get(current_user_id)
        current_user.following_count += 1
        target_user.followers_count += 1
        
        db.session.commit()
        
        return jsonify({
            'message': f'Now following {target_user.username}',
            'following': True
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to follow user', 'details': str(e)}), 500

@social_bp.route('/unfollow/<int:user_id>', methods=['POST'])
def unfollow_user(user_id):
    """Unfollow a user"""
    is_auth, error_response, status_code = require_auth()
    if not is_auth:
        return error_response, status_code
    
    try:
        current_user_id = session['user_id']
        
        # Find the follow relationship
        follow = Follow.query.filter_by(
            follower_id=current_user_id,
            following_id=user_id
        ).first()
        
        if not follow:
            return jsonify({'error': 'Not following this user'}), 400
        
        # Remove follow relationship
        db.session.delete(follow)
        
        # Update follower counts
        current_user = User.query.get(current_user_id)
        target_user = User.query.get(user_id)
        
        current_user.following_count = max(0, current_user.following_count - 1)
        target_user.followers_count = max(0, target_user.followers_count - 1)
        
        db.session.commit()
        
        return jsonify({
            'message': f'Unfollowed {target_user.username}',
            'following': False
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to unfollow user', 'details': str(e)}), 500

@social_bp.route('/followers/<int:user_id>', methods=['GET'])
def get_followers(user_id):
    """Get user's followers"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 50)
        
        # Check if user exists
        user = User.query.get_or_404(user_id)
        
        # Get followers
        followers_query = db.session.query(User).join(
            Follow, User.id == Follow.follower_id
        ).filter(Follow.following_id == user_id)
        
        followers = followers_query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'followers': [user.to_public_dict() for user in followers.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': followers.total,
                'pages': followers.pages,
                'has_next': followers.has_next,
                'has_prev': followers.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch followers', 'details': str(e)}), 500

@social_bp.route('/following/<int:user_id>', methods=['GET'])
def get_following(user_id):
    """Get users that this user is following"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 50)
        
        # Check if user exists
        user = User.query.get_or_404(user_id)
        
        # Get following
        following_query = db.session.query(User).join(
            Follow, User.id == Follow.following_id
        ).filter(Follow.follower_id == user_id)
        
        following = following_query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'following': [user.to_public_dict() for user in following.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': following.total,
                'pages': following.pages,
                'has_next': following.has_next,
                'has_prev': following.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch following', 'details': str(e)}), 500

@social_bp.route('/follow-status/<int:user_id>', methods=['GET'])
def get_follow_status(user_id):
    """Check if current user is following another user"""
    is_auth, error_response, status_code = require_auth()
    if not is_auth:
        return error_response, status_code
    
    try:
        current_user_id = session['user_id']
        
        # Check if following
        follow = Follow.query.filter_by(
            follower_id=current_user_id,
            following_id=user_id
        ).first()
        
        # Check if followed by (mutual follow)
        followed_by = Follow.query.filter_by(
            follower_id=user_id,
            following_id=current_user_id
        ).first()
        
        return jsonify({
            'following': follow is not None,
            'followed_by': followed_by is not None,
            'mutual': follow is not None and followed_by is not None
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to check follow status', 'details': str(e)}), 500

@social_bp.route('/suggested-users', methods=['GET'])
def get_suggested_users():
    """Get suggested users to follow"""
    is_auth, error_response, status_code = require_auth()
    if not is_auth:
        return error_response, status_code
    
    try:
        current_user_id = session['user_id']
        limit = min(request.args.get('limit', 10, type=int), 20)
        
        # Get users that current user is not following
        following_ids = db.session.query(Follow.following_id).filter_by(
            follower_id=current_user_id
        ).subquery()
        
        suggested_users = User.query.filter(
            User.id != current_user_id,
            ~User.id.in_(following_ids),
            User.is_active == True
        ).order_by(User.followers_count.desc()).limit(limit).all()
        
        return jsonify({
            'suggested_users': [user.to_public_dict() for user in suggested_users]
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch suggested users', 'details': str(e)}), 500

@social_bp.route('/mutual-friends/<int:user_id>', methods=['GET'])
def get_mutual_friends(user_id):
    """Get mutual friends between current user and another user"""
    is_auth, error_response, status_code = require_auth()
    if not is_auth:
        return error_response, status_code
    
    try:
        current_user_id = session['user_id']
        
        # Get users that both current user and target user are following
        current_user_following = db.session.query(Follow.following_id).filter_by(
            follower_id=current_user_id
        ).subquery()
        
        target_user_following = db.session.query(Follow.following_id).filter_by(
            follower_id=user_id
        ).subquery()
        
        mutual_friends = User.query.filter(
            User.id.in_(current_user_following),
            User.id.in_(target_user_following)
        ).all()
        
        return jsonify({
            'mutual_friends': [user.to_public_dict() for user in mutual_friends],
            'count': len(mutual_friends)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch mutual friends', 'details': str(e)}), 500

@social_bp.route('/activity-feed', methods=['GET'])
def get_activity_feed():
    """Get personalized activity feed for current user"""
    is_auth, error_response, status_code = require_auth()
    if not is_auth:
        return error_response, status_code
    
    try:
        current_user_id = session['user_id']
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 50)
        
        # Get posts from users that current user is following
        following_ids = db.session.query(Follow.following_id).filter_by(
            follower_id=current_user_id
        ).subquery()
        
        from src.models.user import Post
        feed_posts = Post.query.filter(
            Post.user_id.in_(following_ids),
            Post.is_public == True
        ).order_by(Post.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'posts': [post.to_dict() for post in feed_posts.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': feed_posts.total,
                'pages': feed_posts.pages,
                'has_next': feed_posts.has_next,
                'has_prev': feed_posts.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch activity feed', 'details': str(e)}), 500


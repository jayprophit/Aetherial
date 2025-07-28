from flask import Blueprint, request, jsonify, session
from src.models.user import db, User, Post, Comment, Like
from datetime import datetime
import re

posts_bp = Blueprint('posts', __name__)

def require_auth():
    """Check if user is authenticated"""
    if 'user_id' not in session:
        return False, jsonify({'error': 'Authentication required'}), 401
    return True, None, None

@posts_bp.route('/', methods=['GET'])
def get_posts():
    """Get posts feed with pagination"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        user_id = request.args.get('user_id', type=int)
        
        # Limit per_page to prevent abuse
        per_page = min(per_page, 50)
        
        query = Post.query
        
        # Filter by user if specified
        if user_id:
            query = query.filter_by(user_id=user_id)
        
        # Only show public posts for non-authenticated users
        if 'user_id' not in session:
            query = query.filter_by(is_public=True)
        
        # Order by creation date (newest first)
        posts = query.order_by(Post.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'posts': [post.to_dict() for post in posts.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': posts.total,
                'pages': posts.pages,
                'has_next': posts.has_next,
                'has_prev': posts.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch posts', 'details': str(e)}), 500

@posts_bp.route('/', methods=['POST'])
def create_post():
    """Create a new post"""
    is_auth, error_response, status_code = require_auth()
    if not is_auth:
        return error_response, status_code
    
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('content'):
            return jsonify({'error': 'Content is required'}), 400
        
        content = data['content'].strip()
        if len(content) > 5000:
            return jsonify({'error': 'Content too long (max 5000 characters)'}), 400
        
        # Create new post
        new_post = Post(
            user_id=session['user_id'],
            content=content,
            image_url=data.get('image_url'),
            video_url=data.get('video_url'),
            post_type=data.get('post_type', 'text'),
            is_public=data.get('is_public', True),
            created_at=datetime.utcnow()
        )
        
        db.session.add(new_post)
        
        # Update user's post count
        user = User.query.get(session['user_id'])
        user.posts_count += 1
        
        db.session.commit()
        
        return jsonify({
            'message': 'Post created successfully',
            'post': new_post.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create post', 'details': str(e)}), 500

@posts_bp.route('/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """Get a specific post with comments"""
    try:
        post = Post.query.get_or_404(post_id)
        
        # Check if post is public or user is authenticated
        if not post.is_public and 'user_id' not in session:
            return jsonify({'error': 'Post not found'}), 404
        
        # Get comments for the post
        comments = Comment.query.filter_by(post_id=post_id, parent_id=None).order_by(Comment.created_at.asc()).all()
        
        return jsonify({
            'post': post.to_dict(),
            'comments': [comment.to_dict() for comment in comments]
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch post', 'details': str(e)}), 500

@posts_bp.route('/<int:post_id>/like', methods=['POST'])
def like_post(post_id):
    """Like or unlike a post"""
    is_auth, error_response, status_code = require_auth()
    if not is_auth:
        return error_response, status_code
    
    try:
        post = Post.query.get_or_404(post_id)
        user_id = session['user_id']
        
        # Check if user already liked this post
        existing_like = Like.query.filter_by(user_id=user_id, post_id=post_id).first()
        
        if existing_like:
            # Unlike the post
            db.session.delete(existing_like)
            post.likes_count = max(0, post.likes_count - 1)
            action = 'unliked'
        else:
            # Like the post
            new_like = Like(
                user_id=user_id,
                post_id=post_id,
                like_type=request.get_json().get('like_type', 'like') if request.get_json() else 'like',
                created_at=datetime.utcnow()
            )
            db.session.add(new_like)
            post.likes_count += 1
            action = 'liked'
        
        db.session.commit()
        
        return jsonify({
            'message': f'Post {action} successfully',
            'likes_count': post.likes_count,
            'action': action
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to like post', 'details': str(e)}), 500

@posts_bp.route('/<int:post_id>/comments', methods=['POST'])
def create_comment(post_id):
    """Create a comment on a post"""
    is_auth, error_response, status_code = require_auth()
    if not is_auth:
        return error_response, status_code
    
    try:
        post = Post.query.get_or_404(post_id)
        data = request.get_json()
        
        # Validate required fields
        if not data.get('content'):
            return jsonify({'error': 'Content is required'}), 400
        
        content = data['content'].strip()
        if len(content) > 1000:
            return jsonify({'error': 'Comment too long (max 1000 characters)'}), 400
        
        # Create new comment
        new_comment = Comment(
            post_id=post_id,
            user_id=session['user_id'],
            content=content,
            parent_id=data.get('parent_id'),
            created_at=datetime.utcnow()
        )
        
        db.session.add(new_comment)
        
        # Update post's comment count
        post.comments_count += 1
        
        db.session.commit()
        
        return jsonify({
            'message': 'Comment created successfully',
            'comment': new_comment.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create comment', 'details': str(e)}), 500

@posts_bp.route('/<int:post_id>/share', methods=['POST'])
def share_post(post_id):
    """Share a post"""
    is_auth, error_response, status_code = require_auth()
    if not is_auth:
        return error_response, status_code
    
    try:
        post = Post.query.get_or_404(post_id)
        
        # Update share count
        post.shares_count += 1
        db.session.commit()
        
        return jsonify({
            'message': 'Post shared successfully',
            'shares_count': post.shares_count
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to share post', 'details': str(e)}), 500

@posts_bp.route('/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    """Delete a post (only by author)"""
    is_auth, error_response, status_code = require_auth()
    if not is_auth:
        return error_response, status_code
    
    try:
        post = Post.query.get_or_404(post_id)
        
        # Check if user is the author
        if post.user_id != session['user_id']:
            return jsonify({'error': 'Permission denied'}), 403
        
        # Update user's post count
        user = User.query.get(session['user_id'])
        user.posts_count = max(0, user.posts_count - 1)
        
        # Delete the post (cascades to comments and likes)
        db.session.delete(post)
        db.session.commit()
        
        return jsonify({'message': 'Post deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete post', 'details': str(e)}), 500

@posts_bp.route('/trending', methods=['GET'])
def get_trending_posts():
    """Get trending posts based on engagement"""
    try:
        # Get posts with high engagement in the last 24 hours
        from datetime import datetime, timedelta
        yesterday = datetime.utcnow() - timedelta(days=1)
        
        trending_posts = Post.query.filter(
            Post.created_at >= yesterday,
            Post.is_public == True
        ).order_by(
            (Post.likes_count + Post.comments_count + Post.shares_count).desc()
        ).limit(20).all()
        
        return jsonify({
            'trending_posts': [post.to_dict() for post in trending_posts]
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch trending posts', 'details': str(e)}), 500


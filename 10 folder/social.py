"""
Social Media Routes for Unified Platform
Comprehensive social networking functionality
"""

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any
import uuid

logger = logging.getLogger(__name__)

# Create social blueprint
social_bp = Blueprint('social', __name__, url_prefix='/api/social')

# Mock database (in production, use actual database)
posts_db = {}
comments_db = {}
likes_db = {}
follows_db = {}
users_db = {}

@social_bp.route('/status', methods=['GET'])
def get_social_status():
    """Get social media service status"""
    try:
        return jsonify({
            'status': 'healthy',
            'service': 'social_media',
            'version': '1.0.0',
            'features': [
                'posts', 'comments', 'likes', 'follows', 'feeds',
                'hashtags', 'mentions', 'media_sharing', 'stories'
            ],
            'statistics': {
                'total_posts': len(posts_db),
                'total_comments': len(comments_db),
                'total_likes': len(likes_db),
                'total_follows': len(follows_db)
            },
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Social status error: {str(e)}")
        return jsonify({'error': 'Failed to get social status'}), 500

@social_bp.route('/posts', methods=['POST'])
@jwt_required()
def create_post():
    """Create a new post"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        if 'content' not in data:
            return jsonify({'error': 'Content is required'}), 400
        
        content = data['content']
        media_urls = data.get('media_urls', [])
        hashtags = data.get('hashtags', [])
        mentions = data.get('mentions', [])
        privacy = data.get('privacy', 'public')  # public, friends, private
        location = data.get('location')
        
        # Create post
        post_id = str(uuid.uuid4())
        post = {
            'post_id': post_id,
            'user_id': user_id,
            'content': content,
            'media_urls': media_urls,
            'hashtags': hashtags,
            'mentions': mentions,
            'privacy': privacy,
            'location': location,
            'likes_count': 0,
            'comments_count': 0,
            'shares_count': 0,
            'views_count': 0,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'is_active': True
        }
        
        # Store post
        posts_db[post_id] = post
        
        logger.info(f"Post created: {post_id} by user {user_id}")
        
        return jsonify({
            'post_id': post_id,
            'message': 'Post created successfully',
            'post': {
                'post_id': post['post_id'],
                'content': post['content'],
                'media_urls': post['media_urls'],
                'hashtags': post['hashtags'],
                'mentions': post['mentions'],
                'privacy': post['privacy'],
                'location': post['location'],
                'likes_count': post['likes_count'],
                'comments_count': post['comments_count'],
                'shares_count': post['shares_count'],
                'created_at': post['created_at'].isoformat()
            }
        }), 201
        
    except Exception as e:
        logger.error(f"Create post error: {str(e)}")
        return jsonify({'error': 'Failed to create post'}), 500

@social_bp.route('/posts', methods=['GET'])
@jwt_required()
def get_posts():
    """Get posts (feed)"""
    try:
        user_id = get_jwt_identity()
        
        # Query parameters
        page = int(request.args.get('page', 1))
        per_page = min(int(request.args.get('per_page', 20)), 100)
        feed_type = request.args.get('feed_type', 'timeline')  # timeline, following, trending
        hashtag = request.args.get('hashtag')
        user_filter = request.args.get('user')
        
        # Filter posts
        filtered_posts = []
        
        for post in posts_db.values():
            if not post['is_active']:
                continue
                
            # Privacy filter
            if post['privacy'] == 'private' and post['user_id'] != user_id:
                continue
            elif post['privacy'] == 'friends':
                # Check if users are friends (simplified)
                if post['user_id'] != user_id and not _are_friends(user_id, post['user_id']):
                    continue
            
            # Hashtag filter
            if hashtag and hashtag not in post['hashtags']:
                continue
            
            # User filter
            if user_filter and post['user_id'] != user_filter:
                continue
            
            filtered_posts.append(post)
        
        # Sort posts
        if feed_type == 'trending':
            # Sort by engagement (likes + comments + shares)
            filtered_posts.sort(
                key=lambda p: p['likes_count'] + p['comments_count'] + p['shares_count'],
                reverse=True
            )
        else:
            # Sort by creation time (newest first)
            filtered_posts.sort(key=lambda p: p['created_at'], reverse=True)
        
        # Pagination
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_posts = filtered_posts[start_idx:end_idx]
        
        # Format posts for response
        formatted_posts = []
        for post in paginated_posts:
            formatted_post = {
                'post_id': post['post_id'],
                'user_id': post['user_id'],
                'content': post['content'],
                'media_urls': post['media_urls'],
                'hashtags': post['hashtags'],
                'mentions': post['mentions'],
                'privacy': post['privacy'],
                'location': post['location'],
                'likes_count': post['likes_count'],
                'comments_count': post['comments_count'],
                'shares_count': post['shares_count'],
                'views_count': post['views_count'],
                'created_at': post['created_at'].isoformat(),
                'is_liked': _is_post_liked(post['post_id'], user_id),
                'user_info': _get_user_info(post['user_id'])
            }
            formatted_posts.append(formatted_post)
        
        return jsonify({
            'posts': formatted_posts,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total_posts': len(filtered_posts),
                'total_pages': (len(filtered_posts) + per_page - 1) // per_page,
                'has_next': end_idx < len(filtered_posts),
                'has_prev': page > 1
            },
            'feed_type': feed_type
        }), 200
        
    except Exception as e:
        logger.error(f"Get posts error: {str(e)}")
        return jsonify({'error': 'Failed to get posts'}), 500

@social_bp.route('/posts/<post_id>', methods=['GET'])
@jwt_required()
def get_post(post_id):
    """Get a specific post"""
    try:
        user_id = get_jwt_identity()
        
        if post_id not in posts_db:
            return jsonify({'error': 'Post not found'}), 404
        
        post = posts_db[post_id]
        
        # Check privacy
        if post['privacy'] == 'private' and post['user_id'] != user_id:
            return jsonify({'error': 'Post not accessible'}), 403
        elif post['privacy'] == 'friends' and post['user_id'] != user_id:
            if not _are_friends(user_id, post['user_id']):
                return jsonify({'error': 'Post not accessible'}), 403
        
        # Increment view count
        post['views_count'] += 1
        
        # Get comments
        post_comments = [
            comment for comment in comments_db.values()
            if comment['post_id'] == post_id and comment['is_active']
        ]
        post_comments.sort(key=lambda c: c['created_at'])
        
        formatted_comments = []
        for comment in post_comments[:10]:  # Limit to 10 comments
            formatted_comments.append({
                'comment_id': comment['comment_id'],
                'user_id': comment['user_id'],
                'content': comment['content'],
                'likes_count': comment['likes_count'],
                'created_at': comment['created_at'].isoformat(),
                'user_info': _get_user_info(comment['user_id'])
            })
        
        return jsonify({
            'post': {
                'post_id': post['post_id'],
                'user_id': post['user_id'],
                'content': post['content'],
                'media_urls': post['media_urls'],
                'hashtags': post['hashtags'],
                'mentions': post['mentions'],
                'privacy': post['privacy'],
                'location': post['location'],
                'likes_count': post['likes_count'],
                'comments_count': post['comments_count'],
                'shares_count': post['shares_count'],
                'views_count': post['views_count'],
                'created_at': post['created_at'].isoformat(),
                'updated_at': post['updated_at'].isoformat(),
                'is_liked': _is_post_liked(post_id, user_id),
                'user_info': _get_user_info(post['user_id'])
            },
            'comments': formatted_comments,
            'total_comments': len(post_comments)
        }), 200
        
    except Exception as e:
        logger.error(f"Get post error: {str(e)}")
        return jsonify({'error': 'Failed to get post'}), 500

@social_bp.route('/posts/<post_id>', methods=['PUT'])
@jwt_required()
def update_post(post_id):
    """Update a post"""
    try:
        user_id = get_jwt_identity()
        
        if post_id not in posts_db:
            return jsonify({'error': 'Post not found'}), 404
        
        post = posts_db[post_id]
        
        # Check ownership
        if post['user_id'] != user_id:
            return jsonify({'error': 'Not authorized to update this post'}), 403
        
        data = request.get_json()
        
        # Update allowed fields
        if 'content' in data:
            post['content'] = data['content']
        if 'hashtags' in data:
            post['hashtags'] = data['hashtags']
        if 'privacy' in data:
            post['privacy'] = data['privacy']
        if 'location' in data:
            post['location'] = data['location']
        
        post['updated_at'] = datetime.utcnow()
        
        logger.info(f"Post updated: {post_id} by user {user_id}")
        
        return jsonify({
            'message': 'Post updated successfully',
            'post': {
                'post_id': post['post_id'],
                'content': post['content'],
                'hashtags': post['hashtags'],
                'privacy': post['privacy'],
                'location': post['location'],
                'updated_at': post['updated_at'].isoformat()
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Update post error: {str(e)}")
        return jsonify({'error': 'Failed to update post'}), 500

@social_bp.route('/posts/<post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    """Delete a post"""
    try:
        user_id = get_jwt_identity()
        
        if post_id not in posts_db:
            return jsonify({'error': 'Post not found'}), 404
        
        post = posts_db[post_id]
        
        # Check ownership
        if post['user_id'] != user_id:
            return jsonify({'error': 'Not authorized to delete this post'}), 403
        
        # Soft delete
        post['is_active'] = False
        post['updated_at'] = datetime.utcnow()
        
        logger.info(f"Post deleted: {post_id} by user {user_id}")
        
        return jsonify({'message': 'Post deleted successfully'}), 200
        
    except Exception as e:
        logger.error(f"Delete post error: {str(e)}")
        return jsonify({'error': 'Failed to delete post'}), 500

@social_bp.route('/posts/<post_id>/like', methods=['POST'])
@jwt_required()
def like_post(post_id):
    """Like or unlike a post"""
    try:
        user_id = get_jwt_identity()
        
        if post_id not in posts_db:
            return jsonify({'error': 'Post not found'}), 404
        
        post = posts_db[post_id]
        
        # Check if already liked
        like_key = f"{user_id}:{post_id}"
        
        if like_key in likes_db:
            # Unlike
            del likes_db[like_key]
            post['likes_count'] = max(0, post['likes_count'] - 1)
            action = 'unliked'
        else:
            # Like
            likes_db[like_key] = {
                'user_id': user_id,
                'post_id': post_id,
                'created_at': datetime.utcnow()
            }
            post['likes_count'] += 1
            action = 'liked'
        
        return jsonify({
            'message': f'Post {action} successfully',
            'action': action,
            'likes_count': post['likes_count']
        }), 200
        
    except Exception as e:
        logger.error(f"Like post error: {str(e)}")
        return jsonify({'error': 'Failed to like post'}), 500

@social_bp.route('/posts/<post_id>/comments', methods=['POST'])
@jwt_required()
def create_comment():
    """Create a comment on a post"""
    try:
        user_id = get_jwt_identity()
        post_id = request.view_args['post_id']
        data = request.get_json()
        
        if post_id not in posts_db:
            return jsonify({'error': 'Post not found'}), 404
        
        if 'content' not in data:
            return jsonify({'error': 'Content is required'}), 400
        
        content = data['content']
        parent_comment_id = data.get('parent_comment_id')  # For nested comments
        
        # Create comment
        comment_id = str(uuid.uuid4())
        comment = {
            'comment_id': comment_id,
            'post_id': post_id,
            'user_id': user_id,
            'content': content,
            'parent_comment_id': parent_comment_id,
            'likes_count': 0,
            'replies_count': 0,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'is_active': True
        }
        
        # Store comment
        comments_db[comment_id] = comment
        
        # Update post comment count
        posts_db[post_id]['comments_count'] += 1
        
        # Update parent comment reply count
        if parent_comment_id and parent_comment_id in comments_db:
            comments_db[parent_comment_id]['replies_count'] += 1
        
        logger.info(f"Comment created: {comment_id} on post {post_id} by user {user_id}")
        
        return jsonify({
            'comment_id': comment_id,
            'message': 'Comment created successfully',
            'comment': {
                'comment_id': comment['comment_id'],
                'content': comment['content'],
                'parent_comment_id': comment['parent_comment_id'],
                'likes_count': comment['likes_count'],
                'replies_count': comment['replies_count'],
                'created_at': comment['created_at'].isoformat(),
                'user_info': _get_user_info(user_id)
            }
        }), 201
        
    except Exception as e:
        logger.error(f"Create comment error: {str(e)}")
        return jsonify({'error': 'Failed to create comment'}), 500

@social_bp.route('/posts/<post_id>/comments', methods=['GET'])
@jwt_required()
def get_comments(post_id):
    """Get comments for a post"""
 
(Content truncated due to size limit. Use line ranges to read in chunks)
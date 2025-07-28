from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from src.models.user import db, User, Post

social_bp = Blueprint('social', __name__)

@social_bp.route('/feed', methods=['GET'])
@jwt_required()
def get_feed():
    try:
        current_user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Sample feed data
        feed_posts = [
            {
                'id': '1',
                'author': {
                    'id': 'user1',
                    'username': 'rustdev_sarah',
                    'name': 'Sarah Chen',
                    'avatar': '/api/placeholder/50/50',
                    'verified': True
                },
                'content': 'Just released a new Rust crate for async HTTP clients! 🦀 Check it out on crates.io. The performance improvements are incredible - 40% faster than the previous version.',
                'media_urls': ['/api/placeholder/600/400'],
                'post_type': 'text_with_image',
                'created_at': '2024-01-20T10:30:00Z',
                'likes_count': 156,
                'comments_count': 23,
                'shares_count': 12,
                'is_liked': False,
                'is_shared': False,
                'tags': ['#Rust', '#AsyncProgramming', '#OpenSource'],
                'engagement': {
                    'reactions': {
                        'like': 120,
                        'love': 25,
                        'wow': 11
                    }
                }
            },
            {
                'id': '2',
                'author': {
                    'id': 'user2',
                    'username': 'gopher_mike',
                    'name': 'Mike Johnson',
                    'avatar': '/api/placeholder/50/50',
                    'verified': False
                },
                'content': 'Working on a new microservices architecture with Go and Kubernetes. The scalability we\'re achieving is mind-blowing! 🚀\n\nKey learnings:\n• Service mesh is a game-changer\n• Proper monitoring is crucial\n• Don\'t over-engineer from day one',
                'media_urls': [],
                'post_type': 'text',
                'created_at': '2024-01-20T09:15:00Z',
                'likes_count': 89,
                'comments_count': 15,
                'shares_count': 8,
                'is_liked': True,
                'is_shared': False,
                'tags': ['#Go', '#Kubernetes', '#Microservices', '#DevOps'],
                'engagement': {
                    'reactions': {
                        'like': 65,
                        'love': 15,
                        'wow': 9
                    }
                }
            },
            {
                'id': '3',
                'author': {
                    'id': 'user3',
                    'username': 'ts_emma',
                    'name': 'Emma Rodriguez',
                    'avatar': '/api/placeholder/50/50',
                    'verified': True
                },
                'content': 'TypeScript 5.3 features are amazing! The new import attributes and resolution improvements make development so much smoother. Here\'s a quick demo of the new features:',
                'media_urls': ['/api/placeholder/600/300'],
                'post_type': 'code_snippet',
                'created_at': '2024-01-20T08:45:00Z',
                'likes_count': 234,
                'comments_count': 45,
                'shares_count': 28,
                'is_liked': True,
                'is_shared': False,
                'tags': ['#TypeScript', '#WebDevelopment', '#JavaScript'],
                'code_snippet': {
                    'language': 'typescript',
                    'code': '''// New import attributes in TypeScript 5.3
import data from "./data.json" with { type: "json" };
import styles from "./styles.css" with { type: "css" };

// Improved type inference
const processData = <T extends Record<string, unknown>>(data: T) => {
  return Object.entries(data).map(([key, value]) => ({
    key,
    value,
    type: typeof value
  }));
};'''
                },
                'engagement': {
                    'reactions': {
                        'like': 180,
                        'love': 35,
                        'wow': 19
                    }
                }
            },
            {
                'id': '4',
                'author': {
                    'id': 'user4',
                    'username': 'julia_scientist',
                    'name': 'Dr. David Kim',
                    'avatar': '/api/placeholder/50/50',
                    'verified': True
                },
                'content': 'Published a new research paper on high-performance computing with Julia! The results show 10x performance improvement over traditional Python implementations for scientific computing tasks.',
                'media_urls': ['/api/placeholder/600/400'],
                'post_type': 'research',
                'created_at': '2024-01-20T07:20:00Z',
                'likes_count': 67,
                'comments_count': 12,
                'shares_count': 15,
                'is_liked': False,
                'is_shared': False,
                'tags': ['#Julia', '#ScientificComputing', '#Research', '#HPC'],
                'research_paper': {
                    'title': 'High-Performance Scientific Computing with Julia: A Comparative Study',
                    'doi': '10.1000/xyz123',
                    'journal': 'Journal of Computational Science'
                },
                'engagement': {
                    'reactions': {
                        'like': 45,
                        'love': 12,
                        'wow': 10
                    }
                }
            }
        ]
        
        return jsonify({
            'posts': feed_posts,
            'total': len(feed_posts),
            'page': page,
            'per_page': per_page,
            'has_more': False
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get feed: {str(e)}'}), 500

@social_bp.route('/posts', methods=['POST'])
@jwt_required()
def create_post():
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        content = data.get('content')
        media_urls = data.get('media_urls', [])
        post_type = data.get('post_type', 'text')
        privacy_level = data.get('privacy_level', 'public')
        
        if not content:
            return jsonify({'error': 'Content is required'}), 400
        
        # In a real application, create the post in the database
        new_post = {
            'id': str(datetime.utcnow().timestamp()),
            'content': content,
            'media_urls': media_urls,
            'post_type': post_type,
            'privacy_level': privacy_level,
            'created_at': datetime.utcnow().isoformat(),
            'likes_count': 0,
            'comments_count': 0,
            'shares_count': 0
        }
        
        return jsonify({
            'message': 'Post created successfully',
            'post': new_post
        }), 201
        
    except Exception as e:
        return jsonify({'error': f'Failed to create post: {str(e)}'}), 500

@social_bp.route('/posts/<post_id>/like', methods=['POST'])
@jwt_required()
def like_post(post_id):
    try:
        current_user_id = get_jwt_identity()
        
        # In a real application, toggle like status in database
        
        return jsonify({
            'message': 'Post liked successfully',
            'post_id': post_id,
            'is_liked': True
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to like post: {str(e)}'}), 500

@social_bp.route('/posts/<post_id>/comments', methods=['GET'])
def get_post_comments(post_id):
    try:
        # Sample comments data
        comments = [
            {
                'id': '1',
                'author': {
                    'id': 'user5',
                    'username': 'dev_alex',
                    'name': 'Alex Thompson',
                    'avatar': '/api/placeholder/40/40'
                },
                'content': 'This is exactly what I needed for my project! Thanks for sharing.',
                'created_at': '2024-01-20T11:00:00Z',
                'likes_count': 5,
                'is_liked': False,
                'replies': [
                    {
                        'id': '2',
                        'author': {
                            'id': 'user1',
                            'username': 'rustdev_sarah',
                            'name': 'Sarah Chen',
                            'avatar': '/api/placeholder/40/40'
                        },
                        'content': 'Glad it helps! Let me know if you need any assistance.',
                        'created_at': '2024-01-20T11:15:00Z',
                        'likes_count': 2,
                        'is_liked': False
                    }
                ]
            }
        ]
        
        return jsonify({'comments': comments}), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get comments: {str(e)}'}), 500

@social_bp.route('/posts/<post_id>/comments', methods=['POST'])
@jwt_required()
def add_comment(post_id):
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        content = data.get('content')
        parent_comment_id = data.get('parent_comment_id')
        
        if not content:
            return jsonify({'error': 'Comment content is required'}), 400
        
        new_comment = {
            'id': str(datetime.utcnow().timestamp()),
            'content': content,
            'parent_comment_id': parent_comment_id,
            'created_at': datetime.utcnow().isoformat(),
            'likes_count': 0,
            'is_liked': False
        }
        
        return jsonify({
            'message': 'Comment added successfully',
            'comment': new_comment
        }), 201
        
    except Exception as e:
        return jsonify({'error': f'Failed to add comment: {str(e)}'}), 500

@social_bp.route('/communities', methods=['GET'])
def get_communities():
    try:
        # Sample communities data
        communities = [
            {
                'id': '1',
                'name': 'Rust Developers',
                'description': 'Community for Rust programming language enthusiasts',
                'member_count': 15420,
                'avatar': '/api/placeholder/100/100',
                'cover_image': '/api/placeholder/800/200',
                'is_member': True,
                'category': 'Programming',
                'privacy': 'public',
                'recent_activity': '2 hours ago'
            },
            {
                'id': '2',
                'name': 'Go Gophers',
                'description': 'Everything about Go programming and cloud-native development',
                'member_count': 12800,
                'avatar': '/api/placeholder/100/100',
                'cover_image': '/api/placeholder/800/200',
                'is_member': False,
                'category': 'Programming',
                'privacy': 'public',
                'recent_activity': '1 hour ago'
            },
            {
                'id': '3',
                'name': 'TypeScript Masters',
                'description': 'Advanced TypeScript techniques and best practices',
                'member_count': 9650,
                'avatar': '/api/placeholder/100/100',
                'cover_image': '/api/placeholder/800/200',
                'is_member': True,
                'category': 'Web Development',
                'privacy': 'public',
                'recent_activity': '30 minutes ago'
            },
            {
                'id': '4',
                'name': 'Julia Scientific Computing',
                'description': 'High-performance computing and data science with Julia',
                'member_count': 3200,
                'avatar': '/api/placeholder/100/100',
                'cover_image': '/api/placeholder/800/200',
                'is_member': False,
                'category': 'Data Science',
                'privacy': 'public',
                'recent_activity': '4 hours ago'
            }
        ]
        
        return jsonify({'communities': communities}), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get communities: {str(e)}'}), 500

@social_bp.route('/chat/rooms', methods=['GET'])
@jwt_required()
def get_chat_rooms():
    try:
        current_user_id = get_jwt_identity()
        
        # Sample chat rooms data
        chat_rooms = [
            {
                'id': '1',
                'name': 'Rust General Discussion',
                'description': 'General chat about Rust programming',
                'member_count': 234,
                'is_active': True,
                'last_message': {
                    'content': 'Anyone working with async Rust lately?',
                    'author': 'dev_mike',
                    'timestamp': '2024-01-20T12:30:00Z'
                },
                'age_restricted': False
            },
            {
                'id': '2',
                'name': 'Go Microservices',
                'description': 'Discussing microservices architecture with Go',
                'member_count': 156,
                'is_active': True,
                'last_message': {
                    'content': 'Check out this new gRPC implementation',
                    'author': 'cloud_sarah',
                    'timestamp': '2024-01-20T12:15:00Z'
                },
                'age_restricted': False
            },
            {
                'id': '3',
                'name': 'TypeScript Tips & Tricks',
                'description': 'Share your TypeScript knowledge',
                'member_count': 189,
                'is_active': True,
                'last_message': {
                    'content': 'New utility types in TS 5.3 are amazing!',
                    'author': 'ts_expert',
                    'timestamp': '2024-01-20T11:45:00Z'
                },
                'age_restricted': False
            }
        ]
        
        return jsonify({'chat_rooms': chat_rooms}), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get chat rooms: {str(e)}'}), 500

@social_bp.route('/chat/rooms/<room_id>/messages', methods=['GET'])
@jwt_required()
def get_chat_messages(room_id):
    try:
        current_user_id = get_jwt_identity()
        
        # Check age restriction for chat access
        user = User.query.get(current_user_id)
        if user and not user.can_access_chat:
            return jsonify({'error': 'Chat access restricted for users under 13'}), 403
        
        # Sample chat messages
        messages = [
            {
                'id': '1',
                'author': {
                    'id': 'user1',
                    'username': 'rustdev_sarah',
                    'name': 'Sarah Chen',
                    'avatar': '/api/placeholder/30/30'
                },
                'content': 'Anyone working with async Rust lately? I\'m having some issues with tokio.',
                'timestamp': '2024-01-20T12:30:00Z',
                'message_type': 'text'
            },
            {
                'id': '2',
                'author': {
                    'id': 'user2',
                    'username': 'async_expert',
                    'name': 'Mike Johnson',
                    'avatar': '/api/placeholder/30/30'
                },
                'content': 'What specific issues are you facing? I might be able to help.',
     
(Content truncated due to size limit. Use line ranges to read in chunks)
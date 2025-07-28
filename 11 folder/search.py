from flask import Blueprint, request, jsonify
from src.models.user import db, User, Post
from sqlalchemy import or_, and_

search_bp = Blueprint('search', __name__)

@search_bp.route('/users', methods=['GET'])
def search_users():
    """Search for users by username, full name, or bio"""
    try:
        query = request.args.get('q', '').strip()
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 50)
        
        if not query:
            return jsonify({'error': 'Search query is required'}), 400
        
        if len(query) < 2:
            return jsonify({'error': 'Search query must be at least 2 characters'}), 400
        
        # Search in username, full_name, and bio
        search_pattern = f'%{query}%'
        users = User.query.filter(
            and_(
                User.is_active == True,
                or_(
                    User.username.ilike(search_pattern),
                    User.full_name.ilike(search_pattern),
                    User.bio.ilike(search_pattern)
                )
            )
        ).order_by(
            User.followers_count.desc(),  # Popular users first
            User.username.asc()
        ).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'users': [user.to_public_dict() for user in users.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': users.total,
                'pages': users.pages,
                'has_next': users.has_next,
                'has_prev': users.has_prev
            },
            'query': query
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Search failed', 'details': str(e)}), 500

@search_bp.route('/posts', methods=['GET'])
def search_posts():
    """Search for posts by content"""
    try:
        query = request.args.get('q', '').strip()
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 50)
        
        if not query:
            return jsonify({'error': 'Search query is required'}), 400
        
        if len(query) < 2:
            return jsonify({'error': 'Search query must be at least 2 characters'}), 400
        
        # Search in post content
        search_pattern = f'%{query}%'
        posts = Post.query.filter(
            and_(
                Post.is_public == True,
                Post.content.ilike(search_pattern)
            )
        ).order_by(
            (Post.likes_count + Post.comments_count + Post.shares_count).desc(),  # Popular posts first
            Post.created_at.desc()
        ).paginate(
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
            },
            'query': query
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Search failed', 'details': str(e)}), 500

@search_bp.route('/all', methods=['GET'])
def search_all():
    """Search across users and posts"""
    try:
        query = request.args.get('q', '').strip()
        
        if not query:
            return jsonify({'error': 'Search query is required'}), 400
        
        if len(query) < 2:
            return jsonify({'error': 'Search query must be at least 2 characters'}), 400
        
        search_pattern = f'%{query}%'
        
        # Search users (limit to top 10)
        users = User.query.filter(
            and_(
                User.is_active == True,
                or_(
                    User.username.ilike(search_pattern),
                    User.full_name.ilike(search_pattern),
                    User.bio.ilike(search_pattern)
                )
            )
        ).order_by(
            User.followers_count.desc(),
            User.username.asc()
        ).limit(10).all()
        
        # Search posts (limit to top 10)
        posts = Post.query.filter(
            and_(
                Post.is_public == True,
                Post.content.ilike(search_pattern)
            )
        ).order_by(
            (Post.likes_count + Post.comments_count + Post.shares_count).desc(),
            Post.created_at.desc()
        ).limit(10).all()
        
        return jsonify({
            'users': [user.to_public_dict() for user in users],
            'posts': [post.to_dict() for post in posts],
            'query': query,
            'total_results': len(users) + len(posts)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Search failed', 'details': str(e)}), 500

@search_bp.route('/trending', methods=['GET'])
def get_trending_searches():
    """Get trending search terms (mock data for now)"""
    try:
        # In a real implementation, this would track actual search queries
        trending_searches = [
            {'term': 'AI Revolution', 'count': 15200},
            {'term': 'Text2Robot', 'count': 8900},
            {'term': 'DeFi Protocols', 'count': 6100},
            {'term': 'Quantum Computing', 'count': 4500},
            {'term': 'Blockchain Technology', 'count': 3800},
            {'term': 'Machine Learning', 'count': 3200},
            {'term': 'Cryptocurrency', 'count': 2900},
            {'term': 'Virtual Reality', 'count': 2400},
            {'term': 'Robotics Engineering', 'count': 2100},
            {'term': 'Data Science', 'count': 1800}
        ]
        
        return jsonify({
            'trending_searches': trending_searches
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch trending searches', 'details': str(e)}), 500

@search_bp.route('/hashtags', methods=['GET'])
def search_hashtags():
    """Search for hashtags in posts"""
    try:
        query = request.args.get('q', '').strip()
        
        if not query:
            return jsonify({'error': 'Search query is required'}), 400
        
        # Remove # if present
        if query.startswith('#'):
            query = query[1:]
        
        if len(query) < 2:
            return jsonify({'error': 'Hashtag must be at least 2 characters'}), 400
        
        # Search for hashtags in post content
        hashtag_pattern = f'%#{query}%'
        posts = Post.query.filter(
            and_(
                Post.is_public == True,
                Post.content.ilike(hashtag_pattern)
            )
        ).order_by(
            Post.created_at.desc()
        ).limit(50).all()
        
        # Extract hashtags from posts (simplified)
        hashtags = {}
        for post in posts:
            import re
            found_hashtags = re.findall(r'#(\w+)', post.content.lower())
            for hashtag in found_hashtags:
                if query.lower() in hashtag:
                    if hashtag not in hashtags:
                        hashtags[hashtag] = {'count': 0, 'posts': []}
                    hashtags[hashtag]['count'] += 1
                    if len(hashtags[hashtag]['posts']) < 5:  # Limit posts per hashtag
                        hashtags[hashtag]['posts'].append(post.to_dict())
        
        # Sort by count
        sorted_hashtags = sorted(hashtags.items(), key=lambda x: x[1]['count'], reverse=True)
        
        return jsonify({
            'hashtags': [
                {
                    'tag': tag,
                    'count': data['count'],
                    'recent_posts': data['posts']
                }
                for tag, data in sorted_hashtags[:20]  # Top 20 hashtags
            ],
            'query': f'#{query}'
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Hashtag search failed', 'details': str(e)}), 500

@search_bp.route('/suggestions', methods=['GET'])
def get_search_suggestions():
    """Get search suggestions based on partial query"""
    try:
        query = request.args.get('q', '').strip()
        
        if not query or len(query) < 2:
            return jsonify({'suggestions': []}), 200
        
        search_pattern = f'{query}%'
        
        # Get username suggestions
        user_suggestions = db.session.query(User.username).filter(
            and_(
                User.is_active == True,
                User.username.ilike(search_pattern)
            )
        ).limit(5).all()
        
        # Get full name suggestions
        name_suggestions = db.session.query(User.full_name).filter(
            and_(
                User.is_active == True,
                User.full_name.ilike(search_pattern)
            )
        ).limit(5).all()
        
        suggestions = []
        suggestions.extend([username[0] for username in user_suggestions])
        suggestions.extend([name[0] for name in name_suggestions])
        
        # Remove duplicates and limit
        suggestions = list(set(suggestions))[:10]
        
        return jsonify({
            'suggestions': suggestions,
            'query': query
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get suggestions', 'details': str(e)}), 500


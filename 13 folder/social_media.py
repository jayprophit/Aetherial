"""
Social Media Platform API - Facebook-like Features
Complete social networking with posts, communities, messaging, and interactions
"""

from flask import Blueprint, request, jsonify
import random
import time
from datetime import datetime, timedelta

social_media_bp = Blueprint('social_media', __name__)

# Mock data for demonstration
USERS_DATABASE = {
    "user001": {
        "user_id": "user001",
        "username": "john_doe",
        "display_name": "John Doe",
        "email": "john@example.com",
        "profile_picture": "/images/profiles/john.jpg",
        "cover_photo": "/images/covers/john_cover.jpg",
        "bio": "Software engineer passionate about AI and technology",
        "location": "San Francisco, CA",
        "joined_date": "2023-01-15",
        "followers_count": 1250,
        "following_count": 890,
        "posts_count": 156,
        "verified": True,
        "privacy_settings": {
            "profile_visibility": "public",
            "post_visibility": "friends",
            "message_permissions": "everyone"
        }
    },
    "user002": {
        "user_id": "user002",
        "username": "sarah_tech",
        "display_name": "Sarah Johnson",
        "email": "sarah@example.com",
        "profile_picture": "/images/profiles/sarah.jpg",
        "cover_photo": "/images/covers/sarah_cover.jpg",
        "bio": "Tech entrepreneur and AI researcher",
        "location": "New York, NY",
        "joined_date": "2023-03-20",
        "followers_count": 2100,
        "following_count": 450,
        "posts_count": 89,
        "verified": True,
        "privacy_settings": {
            "profile_visibility": "public",
            "post_visibility": "public",
            "message_permissions": "friends"
        }
    }
}

POSTS_DATABASE = [
    {
        "post_id": "post001",
        "user_id": "user001",
        "content": "Just finished implementing a new AI algorithm for supply chain optimization! The results are incredible - 25% cost reduction and 40% faster delivery times. #AI #SupplyChain #Innovation",
        "media": [
            {"type": "image", "url": "/images/posts/ai_algorithm.jpg", "alt": "AI Algorithm Visualization"}
        ],
        "timestamp": "2024-01-27T10:30:00Z",
        "likes_count": 45,
        "comments_count": 12,
        "shares_count": 8,
        "visibility": "public",
        "location": "San Francisco, CA",
        "tags": ["AI", "SupplyChain", "Innovation"],
        "reactions": {
            "like": 30,
            "love": 10,
            "wow": 3,
            "laugh": 1,
            "angry": 0,
            "sad": 1
        }
    },
    {
        "post_id": "post002",
        "user_id": "user002",
        "content": "Excited to announce our new robotics platform! We're revolutionizing how robots assist in construction and underwater operations. The future is here! 🤖🚀",
        "media": [
            {"type": "video", "url": "/videos/posts/robotics_demo.mp4", "thumbnail": "/images/posts/robotics_thumb.jpg"},
            {"type": "image", "url": "/images/posts/robot_construction.jpg", "alt": "Robot in Construction Site"}
        ],
        "timestamp": "2024-01-27T08:15:00Z",
        "likes_count": 78,
        "comments_count": 23,
        "shares_count": 15,
        "visibility": "public",
        "location": "New York, NY",
        "tags": ["Robotics", "Construction", "Innovation", "Future"],
        "reactions": {
            "like": 45,
            "love": 20,
            "wow": 10,
            "laugh": 2,
            "angry": 0,
            "sad": 1
        }
    }
]

COMMUNITIES_DATABASE = [
    {
        "community_id": "comm001",
        "name": "AI & Machine Learning",
        "description": "A community for AI enthusiasts, researchers, and professionals to share knowledge and discuss the latest developments in artificial intelligence.",
        "cover_image": "/images/communities/ai_ml_cover.jpg",
        "category": "Technology",
        "privacy": "public",
        "members_count": 15420,
        "posts_count": 2340,
        "created_date": "2023-01-01",
        "admin_ids": ["user001", "user002"],
        "moderator_ids": ["user003", "user004"],
        "rules": [
            "Be respectful and professional",
            "Share relevant AI/ML content only",
            "No spam or self-promotion without permission",
            "Use appropriate tags for posts"
        ],
        "tags": ["AI", "MachineLearning", "DeepLearning", "NeuralNetworks"]
    },
    {
        "community_id": "comm002",
        "name": "Supply Chain Innovation",
        "description": "Connecting supply chain professionals, discussing automation, optimization, and future technologies in logistics.",
        "cover_image": "/images/communities/supply_chain_cover.jpg",
        "category": "Business",
        "privacy": "public",
        "members_count": 8750,
        "posts_count": 1560,
        "created_date": "2023-02-15",
        "admin_ids": ["user001"],
        "moderator_ids": ["user005"],
        "rules": [
            "Focus on supply chain topics",
            "Share industry insights and experiences",
            "No competitor bashing",
            "Constructive discussions only"
        ],
        "tags": ["SupplyChain", "Logistics", "Automation", "Innovation"]
    }
]

@social_media_bp.route('/api/social/posts/feed', methods=['GET'])
def get_news_feed():
    """
    Get personalized news feed with AI-powered content ranking
    """
    user_id = request.args.get('user_id', 'user001')
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    
    # AI-powered feed algorithm (simplified)
    # In real implementation, this would consider user interests, engagement history, etc.
    
    # Get posts from followed users and communities
    feed_posts = []
    for post in POSTS_DATABASE:
        # Add engagement metrics and user info
        user_info = USERS_DATABASE.get(post['user_id'], {})
        
        feed_post = post.copy()
        feed_post['user_info'] = {
            "username": user_info.get('username'),
            "display_name": user_info.get('display_name'),
            "profile_picture": user_info.get('profile_picture'),
            "verified": user_info.get('verified', False)
        }
        
        # Calculate engagement rate
        total_reactions = sum(post['reactions'].values())
        engagement_rate = (total_reactions + post['comments_count'] + post['shares_count']) / max(user_info.get('followers_count', 1), 1) * 100
        feed_post['engagement_rate'] = round(engagement_rate, 2)
        
        # AI relevance score
        feed_post['ai_relevance_score'] = round(random.uniform(0.7, 0.98), 3)
        
        feed_posts.append(feed_post)
    
    # Sort by AI relevance and recency
    feed_posts.sort(key=lambda x: (x['ai_relevance_score'], x['timestamp']), reverse=True)
    
    # Pagination
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    paginated_posts = feed_posts[start_idx:end_idx]
    
    return jsonify({
        "status": "success",
        "feed": {
            "posts": paginated_posts,
            "pagination": {
                "current_page": page,
                "per_page": limit,
                "total_posts": len(feed_posts),
                "has_next": end_idx < len(feed_posts)
            },
            "ai_insights": {
                "personalization_score": 0.89,
                "content_diversity": 0.76,
                "engagement_prediction": 0.82
            }
        }
    })

@social_media_bp.route('/api/social/posts/create', methods=['POST'])
def create_post():
    """
    Create a new social media post with media support
    """
    data = request.get_json()
    
    user_id = data.get('user_id')
    content = data.get('content', '')
    media = data.get('media', [])
    visibility = data.get('visibility', 'friends')
    location = data.get('location', '')
    tags = data.get('tags', [])
    
    # Generate new post
    post_id = f"post{int(time.time())}"
    new_post = {
        "post_id": post_id,
        "user_id": user_id,
        "content": content,
        "media": media,
        "timestamp": datetime.now().isoformat() + "Z",
        "likes_count": 0,
        "comments_count": 0,
        "shares_count": 0,
        "visibility": visibility,
        "location": location,
        "tags": tags,
        "reactions": {
            "like": 0,
            "love": 0,
            "wow": 0,
            "laugh": 0,
            "angry": 0,
            "sad": 0
        }
    }
    
    # Add to database (in real implementation)
    POSTS_DATABASE.append(new_post)
    
    # AI content analysis
    ai_analysis = {
        "sentiment": random.choice(["positive", "neutral", "negative"]),
        "topics": tags if tags else ["general"],
        "engagement_prediction": round(random.uniform(0.1, 0.9), 2),
        "reach_estimate": random.randint(100, 5000),
        "content_quality_score": round(random.uniform(0.6, 0.95), 2)
    }
    
    return jsonify({
        "status": "success",
        "message": "Post created successfully",
        "post": new_post,
        "ai_analysis": ai_analysis
    })

@social_media_bp.route('/api/social/posts/<post_id>/react', methods=['POST'])
def react_to_post(post_id):
    """
    Add reaction to a post (like, love, wow, etc.)
    """
    data = request.get_json()
    
    user_id = data.get('user_id')
    reaction_type = data.get('reaction_type', 'like')
    
    # Find post
    post = next((p for p in POSTS_DATABASE if p['post_id'] == post_id), None)
    if not post:
        return jsonify({"status": "error", "message": "Post not found"}), 404
    
    # Update reaction count
    if reaction_type in post['reactions']:
        post['reactions'][reaction_type] += 1
        
        # Update total likes count for backward compatibility
        post['likes_count'] = sum(post['reactions'].values())
    
    return jsonify({
        "status": "success",
        "message": f"Reacted with {reaction_type}",
        "post_id": post_id,
        "reactions": post['reactions'],
        "total_reactions": sum(post['reactions'].values())
    })

@social_media_bp.route('/api/social/posts/<post_id>/comments', methods=['GET', 'POST'])
def handle_comments(post_id):
    """
    Get comments for a post or add a new comment
    """
    if request.method == 'GET':
        # Get comments for post
        comments = [
            {
                "comment_id": "comm001",
                "post_id": post_id,
                "user_id": "user002",
                "user_info": {
                    "username": "sarah_tech",
                    "display_name": "Sarah Johnson",
                    "profile_picture": "/images/profiles/sarah.jpg"
                },
                "content": "This is amazing! Can't wait to see the implementation details.",
                "timestamp": "2024-01-27T11:00:00Z",
                "likes_count": 5,
                "replies_count": 2
            },
            {
                "comment_id": "comm002",
                "post_id": post_id,
                "user_id": "user001",
                "user_info": {
                    "username": "john_doe",
                    "display_name": "John Doe",
                    "profile_picture": "/images/profiles/john.jpg"
                },
                "content": "Thanks! I'll be sharing more details in our AI community soon.",
                "timestamp": "2024-01-27T11:15:00Z",
                "likes_count": 3,
                "replies_count": 0
            }
        ]
        
        return jsonify({
            "status": "success",
            "post_id": post_id,
            "comments": comments,
            "total_comments": len(comments)
        })
    
    elif request.method == 'POST':
        # Add new comment
        data = request.get_json()
        
        user_id = data.get('user_id')
        content = data.get('content', '')
        parent_comment_id = data.get('parent_comment_id')  # For replies
        
        comment_id = f"comm{int(time.time())}"
        new_comment = {
            "comment_id": comment_id,
            "post_id": post_id,
            "user_id": user_id,
            "content": content,
            "timestamp": datetime.now().isoformat() + "Z",
            "likes_count": 0,
            "replies_count": 0,
            "parent_comment_id": parent_comment_id
        }
        
        # Update post comment count
        post = next((p for p in POSTS_DATABASE if p['post_id'] == post_id), None)
        if post:
            post['comments_count'] += 1
        
        return jsonify({
            "status": "success",
            "message": "Comment added successfully",
            "comment": new_comment
        })

@social_media_bp.route('/api/social/communities', methods=['GET'])
def get_communities():
    """
    Get list of communities with filtering and search
    """
    category = request.args.get('category', '')
    search = request.args.get('search', '')
    sort_by = request.args.get('sort_by', 'members')  # members, posts, recent
    
    filtered_communities = COMMUNITIES_DATABASE.copy()
    
    # Filter by category
    if category:
        filtered_communities = [c for c in filtered_communities if c['category'].lower() == category.lower()]
    
    # Search by name or description
    if search:
        search_lower = search.lower()
        filtered_communities = [
            c for c in filtered_communities 
            if search_lower in c['name'].lower() or search_lower in c['description'].lower()
        ]
    
    # Sort communities
    if sort_by == 'members':
        filtered_communities.sort(key=lambda x: x['members_count'], reverse=True)
    elif sort_by == 'posts':
        filtered_communities.sort(key=lambda x: x['posts_count'], reverse=True)
    elif sort_by == 'recent':
        filtered_communities.sort(key=lambda x: x['created_date'], reverse=True)
    
    return jsonify({
        "status": "success",
        "communities": filtered_communities,
        "total_count": len(filtered_communities),
        "categories": ["Technology", "Business", "Science", "Arts", "Sports"],
        "popular_tags": ["AI", "MachineLearning", "SupplyChain", "Innovation", "Robotics"]
    })

@social_media_bp.route('/api/social/communities/<community_id>/join', methods=['POST'])
def join_community(community_id):
    """
    Join a community
    """
    data = request.get_json()
    user_id = data.get('user_id')
    
    community = next((c for c in COMMUNITIES_DATABASE if c['community_id'] == community_id), None)
    if not community:
        return jsonify({"status": "error", "message": "Community not found"}), 404
    
    # Update member count
    community['members_count'] += 1
    
    return jsonify({
        "status": "success",
        "message": f"Successfully joined {community['name']}",
        "community": community,
        "membership_status": "active"
    })

@social_media_bp.route('/api/social/messages/conversations', methods=['GET'])
def get_conversations():
    """
    Get user's message conversations
    """
    user_id = request.args.get('user_id', 'user001')
    
    conversations = [
        {
            "conversation_id": "conv001",
            "participants": [
                {
                    "user_id": "user002",
                    "username": "sarah_tech",
                    "display_name": "Sarah Johnson",
                    "profile_picture": "/images/profiles/sarah.jpg",
                    "online_status": "online"
                }
            ],
            "last_message": {
                "message_id": "msg001",
                "sender_id": "user002",
                "content": "Hey! Saw your post about the AI algorithm. Would love to collaborate!",
                "timestamp": "2024-01-27T12:30:00Z",
                "message_type": "text"
            },
            "unread_count": 2,
            "conversation_type": "direct",
            "updated_at": "2024-01-27T12:30:00Z"
        },
        {
            "conversation_id": "conv002",
            "participants": [
                {
                    "user_id": "user003",
                    "username": "alex_dev",
                    "display_name": "Alex Developer",
                    "profile_picture": "/images/profiles/alex.jpg",
                    "online_status": "away"
                }
            ],
            "last_message": {
                "message_id": "msg002",
                "sender_id": "user001",
                "content": "Thanks for the feedback on the robotics project!",
                "timestamp": "2024-01-27T10:45:00Z",
                "message_type": "text"
            },
            "unread_count": 0,
            "conversation_type": "direct",
            "updated_at": "2024-01-27T10:45:00Z"
        }
    ]
    
    return jsonify({
        "status": "success",
        "conversations": conversations,
        "total_conversations": len(conversations),
        "unread_total": sum(c['unread_count'] for c in conversations)
    })

@social_media_bp.route('/api/social/messages/send', methods=['POST'])
def send_message():
    """
    Send a message to a user or group
    """
    data = request.get_json()
    
    sender_id = data.get('sender_id')
    recipient_id = data.get('recipient_id')
    conversation_id = data.get('conversation_id')
    content = data.get('content', '')
    message_type = data.get('message_type', 'text')  # text, image, video, file
    media_url = data.get('media_url', '')
    
    message_id = f"msg{int(time.time())}"
    new_message = {
        "message_id": message_id,
        "conversation_id": conversation_id,
        "sender_id": sender_id,
        "recipient_id": recipient_id,
        "content": content,
        "message_type": message_type,
        "media_url": media_url,
        "timestamp": datetime.now().isoformat() + "Z",
        "read_status": False,
        "delivery_status": "sent"
    }
    
    return jsonify({
        "status": "success",
        "message": "Message sent successfully",
        "message_data": new_message
    })

@social_media_bp.route('/api/social/users/<user_id>/profile', methods=['GET'])
def get_user_profile(user_id):
    """
    Get detailed user profile information
    """
    user = USERS_DATABASE.get(user_id)
    if not user:
        return jsonify({"status": "error", "message": "User not found"}), 404
    
    # Get user's recent posts
    user_posts = [p for p in POSTS_DATABASE if p['user_id'] == user_id]
    user_posts.sort(key=lambda x: x['timestamp'], reverse=True)
    
    # Calculate profile stats
    total_likes = sum(sum(p['reactions'].values()) for p in user_posts)
    total_comments = sum(p['comments_count'] for p in user_posts)
    
    profile_data = user.copy()
    profile_data.update({
        "recent_posts": user_posts[:5],  # Last 5 posts
        "stats": {
            "total_likes_received": total_likes,
            "total_comments_received": total_comments,
            "average_engagement": round((total_likes + total_comments) / max(len(user_posts), 1), 2),
            "profile_views": random.randint(500, 5000),
            "profile_completion": 85
        },
        "badges": ["Early Adopter", "AI Enthusiast", "Top Contributor"],
        "interests": ["Artificial Intelligence", "Machine Learning", "Robotics", "Supply Chain"],
        "activity_status": {
            "last_seen": "2024-01-27T12:45:00Z",
            "online_status": "online"
        }
    })
    
    return jsonify({
        "status": "success",
        "profile": profile_data
    })

@social_media_bp.route('/api/social/analytics/engagement', methods=['GET'])
def get_engagement_analytics():
    """
    Get social media engagement analytics
    """
    user_id = request.args.get('user_id', 'user001')
    timeframe = request.args.get('timeframe', '7d')  # 1d, 7d, 30d, 90d
    
    analytics = {
        "overview": {
            "total_posts": 156,
            "total_likes": 2340,
            "total_comments": 456,
            "total_shares": 123,
            "followers_gained": 45,
            "profile_views": 1250
        },
        "engagement_rate": {
            "current_period": 8.5,
            "previous_period": 7.2,
            "trend": "increasing",
            "benchmark": 6.8
        },
        "top_performing_posts": [
            {
                "post_id": "post001",
                "content_preview": "Just finished implementing a new AI algorithm...",
                "engagement_score": 94.2,
                "reach": 3450,
                "reactions": 45
            }
        ],
        "audience_insights": {
            "demographics": {
                "age_groups": {"18-24": 15, "25-34": 45, "35-44": 30, "45+": 10},
                "locations": {"USA": 60, "Europe": 25, "Asia": 10, "Other": 5}
            },
            "interests": ["AI", "Technology", "Innovation", "Business"],
            "peak_activity_hours": [9, 12, 15, 18, 21]
        },
        "growth_metrics": {
            "follower_growth_rate": 12.5,
            "engagement_growth_rate": 18.3,
            "content_performance_trend": "improving"
        }
    }
    
    return jsonify({
        "status": "success",
        "analytics": analytics,
        "timeframe": timeframe,
        "generated_at": datetime.now().isoformat()
    })


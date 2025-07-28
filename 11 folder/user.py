from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text)
    avatar_url = db.Column(db.String(255))
    cover_photo_url = db.Column(db.String(255))
    location = db.Column(db.String(100))
    website = db.Column(db.String(255))
    birth_date = db.Column(db.Date)
    phone = db.Column(db.String(20))
    
    # Social media links
    facebook_url = db.Column(db.String(255))
    twitter_url = db.Column(db.String(255))
    instagram_url = db.Column(db.String(255))
    linkedin_url = db.Column(db.String(255))
    youtube_url = db.Column(db.String(255))
    tiktok_url = db.Column(db.String(255))
    
    # Account status
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    is_private = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    last_active = db.Column(db.DateTime)
    
    # Statistics
    followers_count = db.Column(db.Integer, default=0)
    following_count = db.Column(db.Integer, default=0)
    posts_count = db.Column(db.Integer, default=0)
    
    # Preferences
    email_notifications = db.Column(db.Boolean, default=True)
    push_notifications = db.Column(db.Boolean, default=True)
    privacy_level = db.Column(db.String(20), default='public')  # public, friends, private
    
    # Relationships
    posts = db.relationship('Post', backref='author', lazy='dynamic', cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='author', lazy='dynamic', cascade='all, delete-orphan')
    likes = db.relationship('Like', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'bio': self.bio,
            'avatar_url': self.avatar_url,
            'cover_photo_url': self.cover_photo_url,
            'location': self.location,
            'website': self.website,
            'is_verified': self.is_verified,
            'is_private': self.is_private,
            'followers_count': self.followers_count,
            'following_count': self.following_count,
            'posts_count': self.posts_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_active': self.last_active.isoformat() if self.last_active else None,
            'social_links': {
                'facebook': self.facebook_url,
                'twitter': self.twitter_url,
                'instagram': self.instagram_url,
                'linkedin': self.linkedin_url,
                'youtube': self.youtube_url,
                'tiktok': self.tiktok_url
            }
        }

    def to_public_dict(self):
        """Public profile information (for non-friends)"""
        return {
            'id': self.id,
            'username': self.username,
            'full_name': self.full_name,
            'bio': self.bio,
            'avatar_url': self.avatar_url,
            'cover_photo_url': self.cover_photo_url,
            'location': self.location if not self.is_private else None,
            'website': self.website,
            'is_verified': self.is_verified,
            'followers_count': self.followers_count,
            'following_count': self.following_count,
            'posts_count': self.posts_count,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255))
    video_url = db.Column(db.String(255))
    post_type = db.Column(db.String(20), default='text')  # text, image, video, link, poll
    
    # Engagement
    likes_count = db.Column(db.Integer, default=0)
    comments_count = db.Column(db.Integer, default=0)
    shares_count = db.Column(db.Integer, default=0)
    
    # Visibility
    is_public = db.Column(db.Boolean, default=True)
    is_pinned = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    comments = db.relationship('Comment', backref='post', lazy='dynamic', cascade='all, delete-orphan')
    likes = db.relationship('Like', backref='post', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'author': self.author.to_public_dict(),
            'content': self.content,
            'image_url': self.image_url,
            'video_url': self.video_url,
            'post_type': self.post_type,
            'likes_count': self.likes_count,
            'comments_count': self.comments_count,
            'shares_count': self.shares_count,
            'is_pinned': self.is_pinned,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'))  # For nested comments
    
    # Engagement
    likes_count = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    replies = db.relationship('Comment', backref=db.backref('parent', remote_side=[id]), lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'post_id': self.post_id,
            'user_id': self.user_id,
            'author': self.author.to_public_dict(),
            'content': self.content,
            'parent_id': self.parent_id,
            'likes_count': self.likes_count,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=True)
    like_type = db.Column(db.String(20), default='like')  # like, love, laugh, angry, sad
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Ensure user can only like a post/comment once
    __table_args__ = (
        db.UniqueConstraint('user_id', 'post_id', name='unique_user_post_like'),
        db.UniqueConstraint('user_id', 'comment_id', name='unique_user_comment_like'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'post_id': self.post_id,
            'comment_id': self.comment_id,
            'like_type': self.like_type,
            'created_at': self.created_at.isoformat()
        }


class Follow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    following_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    follower = db.relationship('User', foreign_keys=[follower_id], backref='following_relationships')
    following = db.relationship('User', foreign_keys=[following_id], backref='follower_relationships')
    
    # Ensure user can't follow the same person twice
    __table_args__ = (
        db.UniqueConstraint('follower_id', 'following_id', name='unique_follow'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'follower_id': self.follower_id,
            'following_id': self.following_id,
            'created_at': self.created_at.isoformat()
        }


"""
Database Models for Unified Platform
Comprehensive database schema with all required models
"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Decimal, JSON, ForeignKey, Index
from sqlalchemy.dialects.mysql import LONGTEXT, MEDIUMTEXT
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

db = SQLAlchemy()

def init_database(app):
    """Initialize database with Flask app"""
    db.init_app(app)
    with app.app_context():
        db.create_all()

# Base model with common fields
class BaseModel(db.Model):
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

# User Management Models
class User(BaseModel):
    __tablename__ = 'users'
    
    user_id = Column(String(36), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    role = Column(String(50), default='user', nullable=False)
    
    # Verification status
    email_verified = Column(Boolean, default=False, nullable=False)
    phone_verified = Column(Boolean, default=False, nullable=False)
    two_factor_enabled = Column(Boolean, default=False, nullable=False)
    
    # Login tracking
    last_login = Column(DateTime, nullable=True)
    login_count = Column(Integer, default=0, nullable=False)
    
    # User preferences and settings
    preferences = Column(JSON, nullable=True)
    settings = Column(JSON, nullable=True)
    
    # Relationships
    wallets = relationship('Wallet', backref='user', lazy='dynamic')
    orders = relationship('Order', backref='user', lazy='dynamic')
    enrollments = relationship('Enrollment', backref='user', lazy='dynamic')
    posts = relationship('Post', backref='author', lazy='dynamic')
    
    def __repr__(self):
        return f'<User {self.email}>'

class UserProfile(BaseModel):
    __tablename__ = 'user_profiles'
    
    profile_id = Column(String(36), unique=True, nullable=False, index=True)
    user_id = Column(String(36), ForeignKey('users.user_id'), nullable=False)
    bio = Column(Text, nullable=True)
    location = Column(String(255), nullable=True)
    website = Column(String(500), nullable=True)
    social_links = Column(JSON, nullable=True)
    skills = Column(JSON, nullable=True)
    interests = Column(JSON, nullable=True)
    
    user = relationship('User', backref='profile')

# Blockchain Models
class Wallet(BaseModel):
    __tablename__ = 'wallets'
    
    wallet_id = Column(String(36), unique=True, nullable=False, index=True)
    user_id = Column(String(36), ForeignKey('users.user_id'), nullable=False)
    name = Column(String(100), nullable=False)
    address = Column(String(255), unique=True, nullable=False, index=True)
    public_key = Column(Text, nullable=False)
    encrypted_private_key = Column(Text, nullable=False)
    wallet_type = Column(String(50), default='standard', nullable=False)
    balance = Column(Decimal(20, 8), default=0, nullable=False)
    
    def __repr__(self):
        return f'<Wallet {self.address}>'

class Block(BaseModel):
    __tablename__ = 'blocks'
    
    block_id = Column(String(36), unique=True, nullable=False, index=True)
    block_number = Column(Integer, unique=True, nullable=False, index=True)
    hash = Column(String(64), unique=True, nullable=False, index=True)
    previous_hash = Column(String(64), nullable=False)
    merkle_root = Column(String(64), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    nonce = Column(String(64), nullable=False)
    difficulty = Column(Integer, nullable=False)
    gas_limit = Column(Integer, nullable=False)
    gas_used = Column(Integer, nullable=False)
    miner_address = Column(String(255), nullable=False)
    reward = Column(Decimal(20, 8), nullable=False)
    transaction_count = Column(Integer, default=0, nullable=False)
    size = Column(Integer, nullable=False)
    
    transactions = relationship('BlockchainTransaction', backref='block', lazy='dynamic')

class BlockchainTransaction(BaseModel):
    __tablename__ = 'blockchain_transactions'
    
    transaction_id = Column(String(36), unique=True, nullable=False, index=True)
    hash = Column(String(64), unique=True, nullable=False, index=True)
    block_id = Column(String(36), ForeignKey('blocks.block_id'), nullable=True)
    block_number = Column(Integer, nullable=True)
    from_address = Column(String(255), nullable=False, index=True)
    to_address = Column(String(255), nullable=False, index=True)
    amount = Column(Decimal(20, 8), nullable=False)
    gas_price = Column(Decimal(20, 8), nullable=False)
    gas_limit = Column(Integer, nullable=False)
    gas_used = Column(Integer, nullable=True)
    nonce = Column(Integer, nullable=False)
    status = Column(String(20), default='pending', nullable=False)
    memo = Column(Text, nullable=True)
    confirmed_at = Column(DateTime, nullable=True)

class SmartContract(BaseModel):
    __tablename__ = 'smart_contracts'
    
    contract_id = Column(String(36), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    address = Column(String(255), unique=True, nullable=False, index=True)
    owner_address = Column(String(255), nullable=False)
    code = Column(LONGTEXT, nullable=False)
    abi = Column(JSON, nullable=False)
    bytecode = Column(LONGTEXT, nullable=False)
    status = Column(String(20), default='deployed', nullable=False)
    deployment_hash = Column(String(64), nullable=True)
    gas_used = Column(Integer, nullable=True)

# E-commerce Models
class Category(BaseModel):
    __tablename__ = 'categories'
    
    category_id = Column(String(36), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    parent_id = Column(String(36), ForeignKey('categories.category_id'), nullable=True)
    image_url = Column(String(500), nullable=True)
    sort_order = Column(Integer, default=0, nullable=False)
    
    parent = relationship('Category', remote_side='Category.category_id', backref='children')
    products = relationship('Product', backref='category', lazy='dynamic')

class Product(BaseModel):
    __tablename__ = 'products'
    
    product_id = Column(String(36), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    short_description = Column(String(500), nullable=True)
    sku = Column(String(100), unique=True, nullable=False, index=True)
    price = Column(Decimal(10, 2), nullable=False)
    sale_price = Column(Decimal(10, 2), nullable=True)
    cost_price = Column(Decimal(10, 2), nullable=True)
    category_id = Column(String(36), ForeignKey('categories.category_id'), nullable=False)
    
    # Inventory
    stock_quantity = Column(Integer, default=0, nullable=False)
    manage_stock = Column(Boolean, default=True, nullable=False)
    stock_status = Column(String(20), default='in_stock', nullable=False)
    
    # Product attributes
    weight = Column(Decimal(8, 2), nullable=True)
    dimensions = Column(JSON, nullable=True)
    images = Column(JSON, nullable=True)
    attributes = Column(JSON, nullable=True)
    
    # SEO
    meta_title = Column(String(255), nullable=True)
    meta_description = Column(String(500), nullable=True)
    
    # Status
    status = Column(String(20), default='published', nullable=False)
    featured = Column(Boolean, default=False, nullable=False)
    
    order_items = relationship('OrderItem', backref='product', lazy='dynamic')
    cart_items = relationship('CartItem', backref='product', lazy='dynamic')

class Cart(BaseModel):
    __tablename__ = 'carts'
    
    cart_id = Column(String(36), unique=True, nullable=False, index=True)
    user_id = Column(String(36), ForeignKey('users.user_id'), nullable=True)
    session_id = Column(String(255), nullable=True, index=True)
    total_amount = Column(Decimal(10, 2), default=0, nullable=False)
    item_count = Column(Integer, default=0, nullable=False)
    
    items = relationship('CartItem', backref='cart', lazy='dynamic', cascade='all, delete-orphan')

class CartItem(BaseModel):
    __tablename__ = 'cart_items'
    
    item_id = Column(String(36), unique=True, nullable=False, index=True)
    cart_id = Column(String(36), ForeignKey('carts.cart_id'), nullable=False)
    product_id = Column(String(36), ForeignKey('products.product_id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Decimal(10, 2), nullable=False)
    total = Column(Decimal(10, 2), nullable=False)

class Order(BaseModel):
    __tablename__ = 'orders'
    
    order_id = Column(String(36), unique=True, nullable=False, index=True)
    order_number = Column(String(50), unique=True, nullable=False, index=True)
    user_id = Column(String(36), ForeignKey('users.user_id'), nullable=False)
    
    # Order totals
    subtotal = Column(Decimal(10, 2), nullable=False)
    tax_amount = Column(Decimal(10, 2), default=0, nullable=False)
    shipping_amount = Column(Decimal(10, 2), default=0, nullable=False)
    discount_amount = Column(Decimal(10, 2), default=0, nullable=False)
    total_amount = Column(Decimal(10, 2), nullable=False)
    
    # Order status
    status = Column(String(20), default='pending', nullable=False)
    payment_status = Column(String(20), default='pending', nullable=False)
    fulfillment_status = Column(String(20), default='unfulfilled', nullable=False)
    
    # Addresses
    billing_address = Column(JSON, nullable=False)
    shipping_address = Column(JSON, nullable=True)
    
    # Payment
    payment_method = Column(String(50), nullable=True)
    payment_reference = Column(String(255), nullable=True)
    
    # Dates
    order_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    shipped_date = Column(DateTime, nullable=True)
    delivered_date = Column(DateTime, nullable=True)
    
    items = relationship('OrderItem', backref='order', lazy='dynamic', cascade='all, delete-orphan')

class OrderItem(BaseModel):
    __tablename__ = 'order_items'
    
    item_id = Column(String(36), unique=True, nullable=False, index=True)
    order_id = Column(String(36), ForeignKey('orders.order_id'), nullable=False)
    product_id = Column(String(36), ForeignKey('products.product_id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Decimal(10, 2), nullable=False)
    total = Column(Decimal(10, 2), nullable=False)

# E-learning Models
class Course(BaseModel):
    __tablename__ = 'courses'
    
    course_id = Column(String(36), unique=True, nullable=False, index=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    short_description = Column(String(500), nullable=True)
    instructor_id = Column(String(36), ForeignKey('users.user_id'), nullable=False)
    
    # Course details
    price = Column(Decimal(10, 2), default=0, nullable=False)
    duration_hours = Column(Integer, nullable=True)
    difficulty_level = Column(String(20), default='beginner', nullable=False)
    language = Column(String(10), default='en', nullable=False)
    
    # Media
    thumbnail_url = Column(String(500), nullable=True)
    preview_video_url = Column(String(500), nullable=True)
    
    # Status
    status = Column(String(20), default='draft', nullable=False)
    featured = Column(Boolean, default=False, nullable=False)
    
    # Stats
    enrollment_count = Column(Integer, default=0, nullable=False)
    rating = Column(Decimal(3, 2), default=0, nullable=False)
    review_count = Column(Integer, default=0, nullable=False)
    
    instructor = relationship('User', backref='courses_taught')
    lessons = relationship('Lesson', backref='course', lazy='dynamic', cascade='all, delete-orphan')
    enrollments = relationship('Enrollment', backref='course', lazy='dynamic')

class Lesson(BaseModel):
    __tablename__ = 'lessons'
    
    lesson_id = Column(String(36), unique=True, nullable=False, index=True)
    course_id = Column(String(36), ForeignKey('courses.course_id'), nullable=False)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    content = Column(LONGTEXT, nullable=True)
    
    # Lesson details
    lesson_type = Column(String(20), default='video', nullable=False)  # video, text, quiz, assignment
    duration_minutes = Column(Integer, nullable=True)
    sort_order = Column(Integer, default=0, nullable=False)
    
    # Media
    video_url = Column(String(500), nullable=True)
    attachments = Column(JSON, nullable=True)
    
    # Status
    is_preview = Column(Boolean, default=False, nullable=False)
    status = Column(String(20), default='published', nullable=False)

class Enrollment(BaseModel):
    __tablename__ = 'enrollments'
    
    enrollment_id = Column(String(36), unique=True, nullable=False, index=True)
    user_id = Column(String(36), ForeignKey('users.user_id'), nullable=False)
    course_id = Column(String(36), ForeignKey('courses.course_id'), nullable=False)
    
    # Enrollment details
    enrollment_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    completion_date = Column(DateTime, nullable=True)
    progress_percentage = Column(Integer, default=0, nullable=False)
    status = Column(String(20), default='active', nullable=False)
    
    # Payment
    amount_paid = Column(Decimal(10, 2), default=0, nullable=False)
    payment_reference = Column(String(255), nullable=True)

# Social Media Models
class Post(BaseModel):
    __tablename__ = 'posts'
    
    post_id = Column(String(36), unique=True, nullable=False, index=True)
    author_id = Column(String(36), ForeignKey('users.user_id'), nullable=False)
    title = Column(String(255), nullable=True)
    content = Column(LONGTEXT, nullable=False)
    post_type = Column(String(20), default='text', nullable=False)  # text, image, video, link
    
    # Media
    media_urls = Column(JSON, nullable=True)
    
    # Engagement
    like_count = Column(Integer, default=0, nullable=False)
    comment_count = Column(Integer, default=0, nullable=False)
    share_count = Column(Integer, default=0, nullable=False)
    
    # Visibility
    visibility = Column(String(20), default='public', nullable=False)  # public, friends, private
    status = Column(String(20), default='published', nullable=False)
    
    comments = relationship('Comment', backref='post', lazy='dynamic', cascade='all, delete-orphan')
    likes = relationship('Like', backref='post', lazy='dynamic', cascade='all, delete-orphan')

class Comment(BaseModel):
    __tablename__ = 'comments'
    
    comment_id = Column(String(36), unique=True, nullable=False, index=True)
    post_id = Column(String(36), ForeignKey('posts.post_id'), nullable=False)
    author_id = Column(String(36), ForeignKey('users.user_id'), nullable=False)
    parent_id = Column(String(36), ForeignKey('comments.comment_id'), nullable=True)
    content = Column(Text, nullable=False)
    
    # Engagement
    like_count = Column(Integer, default=0, nullable=False)
    
    author = relationship('User', backref='comments
(Content truncated due to size limit. Use line ranges to read in chunks)
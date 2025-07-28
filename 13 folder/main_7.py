import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import redis
import logging

# Import models
from src.models.user import db

# Import all route blueprints
from src.routes.user import user_bp
from src.routes.auth import auth_bp
from src.routes.blockchain import blockchain_bp
from src.routes.ai import ai_bp
from src.routes.banking import banking_bp
from src.routes.ecommerce import ecommerce_bp
from src.routes.social import social_bp
from src.routes.legal import legal_bp
from src.routes.insurance import insurance_bp
from src.routes.vpn import vpn_bp
from src.routes.robotics import robotics_bp
from src.routes.knowledge import knowledge_bp
from src.routes.file_processor import file_processor_bp
from src.routes.business import business_bp
from src.routes.crispr import crispr_bp

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Configuration
app.config['SECRET_KEY'] = 'unified-platform-super-secret-key-2024'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-unified-platform-2024'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False  # Tokens don't expire for demo

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
CORS(app, origins="*")  # Allow all origins for development
jwt = JWTManager(app)

# Initialize rate limiter
try:
    redis_client = redis.Redis(host='localhost', port=6379, db=0)
    limiter = Limiter(
        app,
        key_func=get_remote_address,
        storage_uri="redis://localhost:6379",
        default_limits=["1000 per hour"]
    )
except:
    # Fallback to memory storage if Redis is not available
    limiter = Limiter(
        app,
        key_func=get_remote_address,
        default_limits=["1000 per hour"]
    )

# Initialize database
db.init_app(app)
with app.app_context():
    db.create_all()

# Register all blueprints
app.register_blueprint(user_bp, url_prefix='/api/users')
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(blockchain_bp, url_prefix='/api/blockchain')
app.register_blueprint(ai_bp, url_prefix='/api/ai')
app.register_blueprint(banking_bp, url_prefix='/api/banking')
app.register_blueprint(ecommerce_bp, url_prefix='/api/ecommerce')
app.register_blueprint(social_bp, url_prefix='/api/social')
app.register_blueprint(legal_bp, url_prefix='/api/legal')
app.register_blueprint(insurance_bp, url_prefix='/api/insurance')
app.register_blueprint(vpn_bp, url_prefix='/api/vpn')
app.register_blueprint(robotics_bp, url_prefix='/api/robotics')
app.register_blueprint(knowledge_bp, url_prefix='/api/knowledge')
app.register_blueprint(file_processor_bp, url_prefix='/api/files')
app.register_blueprint(business_bp, url_prefix='/api/business')
app.register_blueprint(crispr_bp, url_prefix='/api/crispr')

# Health check endpoint
@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Unified Platform Backend is running',
        'version': '1.0.0',
        'features': [
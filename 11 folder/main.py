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
            'Authentication & Authorization',
            'Blockchain & Cryptocurrency',
            'AI & Machine Learning',
            'Banking & Financial Services',
            'E-commerce Platform',
            'Social Media Features',
            'Legal Services',
            'Insurance Platform',
            'VPN & Privacy Services',
            'Robotics Control',
            'Knowledge Management',
            'Universal File Processing',
            'Business Services',
            'CRISPR Gene Editing'
        ]
    })

# API documentation endpoint
@app.route('/api/docs')
def api_docs():
    """API documentation endpoint"""
    return jsonify({
        'title': 'Unified Platform API',
        'version': '1.0.0',
        'description': 'Comprehensive API for the Unified Platform',
        'endpoints': {
            '/api/health': 'Health check',
            '/api/auth/*': 'Authentication and authorization',
            '/api/users/*': 'User management',
            '/api/blockchain/*': 'Blockchain and cryptocurrency operations',
            '/api/ai/*': 'AI and machine learning services',
            '/api/banking/*': 'Banking and financial services',
            '/api/ecommerce/*': 'E-commerce platform',
            '/api/social/*': 'Social media features',
            '/api/legal/*': 'Legal services and documentation',
            '/api/insurance/*': 'Insurance platform',
            '/api/vpn/*': 'VPN and privacy services',
            '/api/robotics/*': 'Robotics control and automation',
            '/api/knowledge/*': 'Knowledge management system',
            '/api/files/*': 'Universal file processing',
            '/api/business/*': 'Business services and setup',
            '/api/crispr/*': 'CRISPR gene editing services'
        }
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({'error': 'Rate limit exceeded', 'message': str(e.description)}), 429

# Serve frontend
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return jsonify({
                'message': 'Unified Platform Backend API',
                'status': 'running',
                'endpoints': '/api/docs'
            })

if __name__ == '__main__':
    logger.info("Starting Unified Platform Backend...")
    logger.info("Available endpoints: /api/health, /api/docs")
    app.run(host='0.0.0.0', port=5000, debug=True)


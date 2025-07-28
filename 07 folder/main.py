import os
import sys
from datetime import datetime, timedelta
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv

# Import routes (without database for now)
from routes.auth_simple import auth_bp
from routes.blockchain import blockchain_bp
from routes.dev_tools import dev_tools_bp
from routes.settings import settings_bp
from routes.social_links import social_links_bp
from routes.store_builder import store_builder_bp
from routes.page_builder import page_builder_bp

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'unified-platform-secret-key-2024')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-unified-platform')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

# Initialize extensions
CORS(app, origins="*", allow_headers=["Content-Type", "Authorization"])
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(blockchain_bp, url_prefix='/api/blockchain')
app.register_blueprint(dev_tools_bp, url_prefix='/api/dev-tools')
app.register_blueprint(settings_bp, url_prefix='/api/settings')
app.register_blueprint(social_links_bp, url_prefix='/api/social-links')
app.register_blueprint(store_builder_bp, url_prefix='/api/store-builder')
app.register_blueprint(page_builder_bp, url_prefix='/api/page-builder')

# Health check endpoint
@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'Unified Platform API is running',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '2.0.0',
        'features': [
            'Authentication',
            'Education Hub',
            'Job Marketplace', 
            'E-commerce',
            'Social Network',
            'Blockchain Integration',
            'Multi-currency Support',
            'Gamification System',
            'Cloud IDE & Developer Tools',
            'Multi-language Code Execution',
            'Project Templates & Deployment',
            'Theme & Settings Management',
            'Accessibility Features',
            'Store Builder (Shopify-like)',
            'Page Builder (Elementor-like)',
            'Social Links Integration'
        ]
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({'error': 'Token has expired'}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({'error': 'Invalid token'}), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({'error': 'Authorization token is required'}), 401

# Static file serving
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
            return jsonify({'message': 'Unified Platform API', 'status': 'running'}), 200

if __name__ == '__main__':
    print("Starting Unified Platform API on port 5000")
    print(f"Debug mode: {app.debug}")
    app.run(host='0.0.0.0', port=5000, debug=False)


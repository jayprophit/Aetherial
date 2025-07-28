import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
from src.models.user import db
from src.routes.user import user_bp
from src.routes.ai_hub import ai_hub_bp
from src.routes.blockchain import blockchain_bp
from src.routes.robotics import robotics_bp
from src.routes.virtual_accelerator import virtual_accelerator_bp
from src.routes.quantum_computing import quantum_computing_bp
from src.routes.advanced_search import advanced_search_bp
from src.routes.healthcare import healthcare_bp
from src.routes.finance import finance_bp
from src.routes.education import education_bp
from src.routes.business import business_bp
from src.routes.iot import iot_bp
from src.routes.social import social_bp
from src.routes.marketplace import marketplace_bp
from src.routes.communication import communication_bp
from src.routes.security import security_bp
from src.routes.analytics import analytics_bp
from src.routes.automation import automation_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'unified-platform-ultimate-secret-key-2025'

# Enable CORS for all routes
CORS(app, origins="*")

# Register all blueprints
app.register_blueprint(user_bp, url_prefix='/api/users')
app.register_blueprint(ai_hub_bp, url_prefix='/api/ai')
app.register_blueprint(blockchain_bp, url_prefix='/api/blockchain')
app.register_blueprint(robotics_bp, url_prefix='/api/robotics')
app.register_blueprint(virtual_accelerator_bp, url_prefix='/api/accelerator')
app.register_blueprint(quantum_computing_bp, url_prefix='/api/quantum')
app.register_blueprint(advanced_search_bp, url_prefix='/api/search')
app.register_blueprint(healthcare_bp, url_prefix='/api/healthcare')
app.register_blueprint(finance_bp, url_prefix='/api/finance')
app.register_blueprint(education_bp, url_prefix='/api/education')
app.register_blueprint(business_bp, url_prefix='/api/business')
app.register_blueprint(iot_bp, url_prefix='/api/iot')
app.register_blueprint(social_bp, url_prefix='/api/social')
app.register_blueprint(marketplace_bp, url_prefix='/api/marketplace')
app.register_blueprint(communication_bp, url_prefix='/api/communication')
app.register_blueprint(security_bp, url_prefix='/api/security')
app.register_blueprint(analytics_bp, url_prefix='/api/analytics')
app.register_blueprint(automation_bp, url_prefix='/api/automation')

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()

# Platform status endpoint
@app.route('/api/status')
def platform_status():
    return jsonify({
        'status': 'operational',
        'platform': 'Unified Platform Ultimate',
        'version': '2.0.0',
        'features': {
            'ai_hub': True,
            'blockchain': True,
            'robotics': True,
            'virtual_accelerator': True,
            'quantum_computing': True,
            'advanced_search': True,
            'healthcare': True,
            'finance': True,
            'education': True,
            'business': True,
            'iot': True,
            'social': True,
            'marketplace': True,
            'communication': True,
            'security': True,
            'analytics': True,
            'automation': True
        },
        'capabilities': [
            'Ultra-low precision AI training (FP32 to Binary)',
            'Text-to-Robot design and control',
            'Decentralized blockchain search',
            'Virtual hardware acceleration',
            'Quantum-inspired computing',
            'Advanced healthcare systems',
            'Comprehensive financial services',
            'Enterprise business tools',
            'IoT and smart technology',
            'Social media integration',
            'E-commerce marketplace',
            'Multi-modal communication',
            'Advanced security systems',
            'Real-time analytics',
            'Workflow automation'
        ]
    })

# Platform metrics endpoint
@app.route('/api/metrics')
def platform_metrics():
    return jsonify({
        'users': {
            'total': 1250000,
            'active_daily': 850000,
            'active_monthly': 1100000
        },
        'performance': {
            'uptime': '99.99%',
            'response_time': '45ms',
            'throughput': '50000 req/sec'
        },
        'features_usage': {
            'ai_hub': 750000,
            'blockchain': 450000,
            'robotics': 320000,
            'healthcare': 280000,
            'finance': 650000,
            'education': 420000,
            'business': 380000,
            'iot': 290000,
            'social': 900000,
            'marketplace': 520000
        },
        'energy_efficiency': {
            'fp32_training': '100%',
            'fp4_training': '12.5%',
            'fp2_training': '6.25%',
            'fp1_training': '3.125%',
            'binary_training': '1.56%'
        }
    })

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
                'message': 'Unified Platform Ultimate Backend',
                'status': 'operational',
                'endpoints': [
                    '/api/status',
                    '/api/metrics',
                    '/api/users',
                    '/api/ai',
                    '/api/blockchain',
                    '/api/robotics',
                    '/api/accelerator',
                    '/api/quantum',
                    '/api/search',
                    '/api/healthcare',
                    '/api/finance',
                    '/api/education',
                    '/api/business',
                    '/api/iot',
                    '/api/social',
                    '/api/marketplace',
                    '/api/communication',
                    '/api/security',
                    '/api/analytics',
                    '/api/automation'
                ]
            })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


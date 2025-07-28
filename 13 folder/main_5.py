import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
from src.models.user import db
from src.routes.user import user_bp
import random
import time
from datetime import datetime, timedelta
import json

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), '..', 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Enable CORS for all routes
CORS(app)

# Serve the React frontend
@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

# Serve static assets
@app.route('/assets/<path:filename>')
def serve_assets(filename):
    return send_from_directory(os.path.join(app.static_folder, 'assets'), filename)

# Catch-all route for React Router
@app.route('/<path:path>')
def serve_static_files(path):
    # Check if it's a static file first
    if '.' in path:
        try:
            return send_from_directory(app.static_folder, path)
        except:
            pass
    # For React Router, serve index.html for any unmatched routes
    return send_from_directory(app.static_folder, 'index.html')

app.register_blueprint(user_bp, url_prefix='/api')

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()

# Global statistics storage
platform_stats = {
    'total_users': 125420,
    'active_projects': 8934,
    'total_revenue': 4500000,
    'courses_completed': 23456,
    'ai_models_active': 47,
    'blockchain_nodes': 156,
    'iot_devices': 8956,
    'quantum_qubits': 128,
    'last_updated': datetime.now()
}

# Recent activities storage
recent_activities = [
    {
        'id': 'AI',
        'title': 'AI model training completed',
        'description': 'Supply chain optimization model achieved 94.2% accuracy',
        'category': 'AI Hub',
        'timestamp': datetime.now() - timedelta(minutes=15)
    },
    {
        'id': 'BC',
        'title': 'New DeFi protocol launched',
        'description': 'Decentralized search with $4.55B TVL now live',
        'category': 'Blockchain',
        'timestamp': datetime.now() - timedelta(hours=2)
    },
    {
        'id': 'EC',
        'title': 'Marketplace milestone reached',
        'description': '500K+ products now available from 15K sellers',
        'category': 'E-Commerce',
        'timestamp': datetime.now() - timedelta(hours=6)
    }
]

# AI Hub endpoints
@app.route('/api/ai-hub/status')
def ai_hub_status():
    return jsonify({
        'status': 'active',
        'models_running': 47,
        'virtual_accelerator': {
            'status': 'operational',
            'gpu_utilization': random.randint(75, 95),
            'memory_usage': random.randint(60, 85)
        },
        'recent_training': {
            'model': 'Supply Chain Optimizer',
            'accuracy': 94.2,
            'completion_time': '2h 34m'
        }
    })

@app.route('/api/ai-hub/models')
def ai_hub_models():
    models = [
        {'name': 'GPT-4 Turbo', 'status': 'active', 'usage': random.randint(60, 90)},
        {'name': 'Claude-3 Opus', 'status': 'active', 'usage': random.randint(50, 80)},
        {'name': 'Gemini Pro', 'status': 'active', 'usage': random.randint(40, 70)},
        {'name': 'LLaMA 2', 'status': 'active', 'usage': random.randint(30, 60)},
        {'name': 'PaLM 2', 'status': 'active', 'usage': random.randint(25, 55)}
    ]
    return jsonify({'models': models})

# Blockchain endpoints
@app.route('/api/blockchain/status')
def blockchain_status():
    return jsonify({
        'status': 'operational',
        'nodes_active': 156,
        'defi_protocols': {
            'uniswap': {'tvl': 4550000000, 'apy': 15.4},
            'compound': {'tvl': 2800000000, 'apy': 8.2},
            'aave': {'tvl': 6100000000, 'apy': 12.7}
        },
        'nft_marketplace': {
            'total_volume': 2400000,
            'active_listings': 15678,
            'floor_price': 0.05
        }
    })

@app.route('/api/blockchain/defi')
def blockchain_defi():
    return jsonify({
        'protocols': [
            {'name': 'Uniswap V3', 'tvl': 4.55e9, 'apy': 15.4, 'status': 'active'},
            {'name': 'Compound', 'tvl': 2.8e9, 'apy': 8.2, 'status': 'active'},
            {'name': 'Aave', 'tvl': 6.1e9, 'apy': 12.7, 'status': 'active'},
            {'name': 'Curve Finance', 'tvl': 3.9e9, 'apy': 25.1, 'status': 'active'},
            {'name': 'SushiSwap', 'tvl': 1.2e9, 'apy': 18.3, 'status': 'active'}
        ]
    })

# E-Commerce endpoints
@app.route('/api/ecommerce/status')
def ecommerce_status():
    return jsonify({
        'status': 'operational',
        'total_products': 500000,
        'active_sellers': 15000,
        'daily_orders': random.randint(2000, 5000),
        'revenue_today': random.randint(100000, 500000),
        'categories': [
            {'name': 'Electronics', 'count': 125000},
            {'name': 'Fashion', 'count': 98000},
            {'name': 'Home & Garden', 'count': 87000},
            {'name': 'Books', 'count': 65000},
            {'name': 'Sports', 'count': 45000}
        ]
    })

# Healthcare endpoints
@app.route('/api/healthcare/status')
def healthcare_status():
    return jsonify({
        'status': 'operational',
        'ai_diagnostics': {
            'accuracy': 96.8,
            'cases_processed': 12456,
            'active_models': 8
        },
        'telemedicine': {
            'active_sessions': random.randint(50, 200),
            'doctors_online': random.randint(25, 100),
            'patients_waiting': random.randint(5, 30)
        }
    })

# Learning endpoints
@app.route('/api/learning/status')
def learning_status():
    return jsonify({
        'status': 'operational',
        'total_courses': 2456,
        'active_students': 45678,
        'courses_completed': 23456,
        'completion_rate': 78.5,
        'popular_courses': [
            {'title': 'AI & Machine Learning', 'students': 8900, 'rating': 4.8},
            {'title': 'Blockchain Development', 'students': 6700, 'rating': 4.7},
            {'title': 'Data Science', 'students': 5400, 'rating': 4.9},
            {'title': 'Web Development', 'students': 4200, 'rating': 4.6}
        ]
    })

# Robotics endpoints
@app.route('/api/robotics/status')
def robotics_status():
    return jsonify({
        'status': 'operational',
        'text2robot': {
            'models_generated': 1234,
            'success_rate': 89.5,
            'avg_generation_time': '45s'
        },
        'fleet_management': {
            'total_robots': 567,
            'active_robots': 489,
            'maintenance_required': 12,
            'efficiency': 94.2
        }
    })

# Supply Chain endpoints
@app.route('/api/supply-chain/status')
def supply_chain_status():
    return jsonify({
        'status': 'operational',
        'shipments_tracked': 45678,
        'optimization_savings': 2.4e6,
        'delivery_accuracy': 97.8,
        'real_time_tracking': {
            'in_transit': 1234,
            'delivered_today': 567,
            'pending_pickup': 89
        }
    })

# Communication endpoints
@app.route('/api/communication/status')
def communication_status():
    return jsonify({
        'status': 'operational',
        'active_users': random.randint(5000, 15000),
        'messages_today': random.randint(50000, 150000),
        'video_calls_active': random.randint(100, 500),
        'channels': {
            'public': 1234,
            'private': 5678,
            'enterprise': 234
        }
    })

# Business Tools endpoints
@app.route('/api/business/status')
def business_status():
    return jsonify({
        'status': 'operational',
        'active_enterprises': 2345,
        'tools_deployed': 15,
        'productivity_increase': 34.5,
        'cost_savings': 1.2e6,
        'popular_tools': [
            {'name': 'CRM', 'usage': 89},
            {'name': 'Analytics', 'usage': 76},
            {'name': 'Project Management', 'usage': 82},
            {'name': 'HR Management', 'usage': 67}
        ]
    })

# Security & Privacy endpoints
@app.route('/api/security/status')
def security_status():
    return jsonify({
        'status': 'secure',
        'threats_blocked': 12456,
        'security_score': 97.8,
        'privacy_compliance': 99.2,
        'active_protections': [
            {'name': 'DDoS Protection', 'status': 'active'},
            {'name': 'Encryption', 'status': 'active'},
            {'name': 'Access Control', 'status': 'active'},
            {'name': 'Audit Logging', 'status': 'active'}
        ]
    })

# Main dashboard endpoints
@app.route('/api/dashboard/stats')
def dashboard_stats():
    # Simulate real-time updates
    platform_stats['total_users'] += random.randint(1, 10)
    platform_stats['active_projects'] += random.randint(0, 5)
    platform_stats['total_revenue'] += random.randint(1000, 10000)
    platform_stats['courses_completed'] += random.randint(0, 3)
    platform_stats['last_updated'] = datetime.now()
    
    return jsonify(platform_stats)

@app.route('/api/dashboard/activities')
def dashboard_activities():
    return jsonify({'activities': recent_activities})

@app.route('/api/dashboard/modules')
def dashboard_modules():
    modules = [
        {
            'id': 'ai-hub',
            'name': 'AI Hub',
            'description': 'Multi-model AI with virtual accelerator',
            'status': 'active',
            'usage': random.randint(80, 95)
        },
        {
            'id': 'blockchain',
            'name': 'Blockchain',
            'description': 'DeFi, NFTs, and decentralized search',
            'status': 'active',
            'usage': random.randint(70, 90)
        },
        {
            'id': 'robotics',
            'name': 'Robotics',
            'description': 'Text2Robot and fleet management',
            'status': 'active',
            'usage': random.randint(60, 85)
        },
        {
            'id': 'healthcare',
            'name': 'Healthcare',
            'description': 'AI diagnosis and telemedicine',
            'status': 'active',
            'usage': random.randint(75, 90)
        }
    ]
    return jsonify({'modules': modules})

# Import and register new blueprints
from src.routes.courses import courses_bp
from src.routes.products import products_bp
from src.routes.books import books_bp
from src.routes.advanced_features import advanced_features_bp

app.register_blueprint(courses_bp, url_prefix='/api/courses')
app.register_blueprint(products_bp, url_prefix='/api/products')
app.register_blueprint(books_bp, url_prefix='/api/books')
app.register_blueprint(advanced_features_bp, url_prefix='/api/advanced')

# Health check endpoint
@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '2.0.0',
        'services': {
            'ai_hub': 'operational',
            'blockchain': 'operational',
            'ecommerce': 'operational',
            'healthcare': 'operational',
            'learning': 'operational',
            'robotics': 'operational',
            'supply_chain': 'operational',
            'communication': 'operational',
            'business': 'operational',
            'security': 'operational',
            'courses': 'operational',
            'products': 'operational',
            'books': 'operational',
            'advanced_features': 'operational',
            'nanobrain_ai': 'operational',
            'quantum_assistant': 'operational',
            'iot_manufacturing': 'operational',
            'browser_automation': 'operational'
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
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


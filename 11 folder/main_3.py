import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
from src.models.user import db
from src.routes.user import user_bp
import time
import random
import hashlib

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Enable CORS for all routes
CORS(app)

app.register_blueprint(user_bp, url_prefix='/api')

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()

# AI Hub API Endpoints
@app.route('/api/ai/chat', methods=['POST'])
def ai_chat():
    data = request.get_json()
    message = data.get('message', '')
    model = data.get('model', 'gpt-4')
    
    # Simulate AI response
    responses = [
        f"AI ({model}): I understand you're asking about '{message}'. This is a comprehensive unified platform with advanced AI capabilities.",
        f"AI ({model}): Your query about '{message}' is interesting. Our platform integrates quantum computing with traditional AI.",
        f"AI ({model}): Regarding '{message}', our system uses ultra-low precision training for 98.4% energy savings."
    ]
    
    return jsonify({
        'response': random.choice(responses),
        'model': model,
        'timestamp': time.time()
    })

@app.route('/api/ai/models', methods=['GET'])
def get_ai_models():
    return jsonify({
        'models': [
            {'name': 'GPT-4', 'status': 'active', 'accuracy': '94.2%'},
            {'name': 'Claude', 'status': 'active', 'accuracy': '92.8%'},
            {'name': 'DeepSeek', 'status': 'active', 'accuracy': '91.5%'},
            {'name': 'Qwen', 'status': 'active', 'accuracy': '90.3%'},
            {'name': 'Genspark', 'status': 'active', 'accuracy': '89.7%'}
        ]
    })

# Blockchain API Endpoints
@app.route('/api/blockchain/search', methods=['POST'])
def blockchain_search():
    data = request.get_json()
    query = data.get('query', '')
    
    return jsonify({
        'results': [
            {'title': f'Decentralized result for: {query}', 'url': f'https://decentralized.search/{query}', 'reward': 0.05},
            {'title': f'Privacy-focused: {query}', 'url': f'https://private.search/{query}', 'reward': 0.05}
        ],
        'tokens_earned': 0.05,
        'privacy_protected': True
    })

@app.route('/api/blockchain/defi', methods=['GET'])
def get_defi_stats():
    return jsonify({
        'total_value_locked': '$4.55B',
        'monthly_transactions': '2.3M',
        'apy_rate': '12.8%',
        'active_protocols': 156
    })

# Social Media API Endpoints
@app.route('/api/social/posts', methods=['GET'])
def get_social_posts():
    return jsonify({
        'posts': [
            {
                'id': 1,
                'user': 'John Doe',
                'content': 'Just completed the AI course on supply chain optimization! The results are incredible - 25% cost reduction achieved. 🚀',
                'likes': 42,
                'comments': 8,
                'timestamp': '2 hours ago'
            },
            {
                'id': 2,
                'user': 'Sarah Johnson',
                'content': 'Our robotics team just deployed the first Text2Robot system! Natural language to robot design is now reality.',
                'likes': 156,
                'comments': 23,
                'timestamp': '4 hours ago'
            }
        ]
    })

@app.route('/api/social/trending', methods=['GET'])
def get_trending():
    return jsonify({
        'topics': [
            {'tag': '#AIRevolution', 'count': '15.2K'},
            {'tag': '#Text2Robot', 'count': '8.9K'},
            {'tag': '#DeFiProtocols', 'count': '6.1K'}
        ]
    })

# E-Commerce API Endpoints
@app.route('/api/ecommerce/products', methods=['GET'])
def get_products():
    return jsonify({
        'products': [
            {
                'id': 1,
                'name': 'AI-Powered Smart Robot',
                'price': 1299.99,
                'rating': 4.8,
                'image': '/api/placeholder/300/200'
            },
            {
                'id': 2,
                'name': 'Construction Toolkit Pro',
                'price': 899.99,
                'rating': 4.9,
                'image': '/api/placeholder/300/200'
            },
            {
                'id': 3,
                'name': 'Underwater Exploration Drone',
                'price': 2499.99,
                'rating': 4.5,
                'image': '/api/placeholder/300/200'
            },
            {
                'id': 4,
                'name': 'Quantum Computing Kit',
                'price': 4999.99,
                'rating': 4.7,
                'image': '/api/placeholder/300/200'
            }
        ],
        'stats': {
            'total_products': '500K+',
            'sellers': '15K',
            'monthly_revenue': '$2.4M',
            'avg_rating': 4.7
        }
    })

# Healthcare API Endpoints
@app.route('/api/healthcare/diagnosis', methods=['POST'])
def ai_diagnosis():
    data = request.get_json()
    symptoms = data.get('symptoms', [])
    
    return jsonify({
        'diagnosis': 'AI Analysis Complete',
        'accuracy': '94.2%',
        'recommendations': [
            'Consult with a specialist',
            'Schedule follow-up in 2 weeks',
            'Monitor symptoms daily'
        ],
        'risk_level': 'Low'
    })

# E-Learning API Endpoints
@app.route('/api/elearning/courses', methods=['GET'])
def get_courses():
    return jsonify({
        'courses': [
            {
                'id': 1,
                'title': 'AI & Machine Learning Fundamentals',
                'instructor': 'Dr. Sarah Chen',
                'rating': 4.9,
                'students': 12500,
                'price': 99.99
            },
            {
                'id': 2,
                'title': 'Blockchain Development Masterclass',
                'instructor': 'Prof. Michael Rodriguez',
                'rating': 4.8,
                'students': 8900,
                'price': 149.99
            },
            {
                'id': 3,
                'title': 'Quantum Computing Essentials',
                'instructor': 'Dr. Emily Watson',
                'rating': 4.7,
                'students': 5600,
                'price': 199.99
            }
        ]
    })

# Platform Statistics
@app.route('/api/stats', methods=['GET'])
def get_platform_stats():
    return jsonify({
        'total_users': 125420,
        'active_projects': 8934,
        'total_revenue': '$4.5M',
        'courses_completed': 23456,
        'ai_models_available': 15,
        'blockchain_transactions': '2.3M',
        'defi_tvl': '$4.55B'
    })

# Placeholder image endpoint
@app.route('/api/placeholder/<int:width>/<int:height>')
def placeholder_image(width, height):
    return f"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}' viewBox='0 0 {width} {height}'%3E%3Crect width='100%25' height='100%25' fill='%23ddd'/%3E%3Ctext x='50%25' y='50%25' text-anchor='middle' dy='.3em' fill='%23999'%3E{width}x{height}%3C/text%3E%3C/svg%3E"

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


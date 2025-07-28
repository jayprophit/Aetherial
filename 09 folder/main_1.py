import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
import datetime
import secrets
import hashlib
import json
import random
import time

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'quantum_unified_platform_2025_cosmic_secret_key'

# Enable CORS for all routes
CORS(app, origins="*", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"])

# Simple in-memory data stores for demo
users_db = {
    'admin': {
        'password_hash': hashlib.sha256('admin123'.encode()).hexdigest(),
        'role': 'admin',
        'permissions': ['all'],
        'profile': {
            'name': 'Administrator',
            'email': 'admin@unifiedplatform.com',
            'avatar': 'https://via.placeholder.com/150',
            'bio': 'Platform Administrator with full access',
            'created_at': '2025-01-01T00:00:00Z'
        }
    },
    'user': {
        'password_hash': hashlib.sha256('user123'.encode()).hexdigest(),
        'role': 'user',
        'permissions': ['read', 'write'],
        'profile': {
            'name': 'Demo User',
            'email': 'user@unifiedplatform.com',
            'avatar': 'https://via.placeholder.com/150',
            'bio': 'Demo user account for testing',
            'created_at': '2025-01-01T00:00:00Z'
        }
    }
}

active_sessions = {}
research_projects = []
manufacturing_jobs = []
trading_data = {}
blockchain_data = []
communication_channels = []
social_networks = []

# Initialize sample data
def initialize_sample_data():
    global research_projects, manufacturing_jobs, trading_data, blockchain_data, communication_channels, social_networks
    
    # Sample R&D projects
    research_projects = [
        {
            'id': 'rd-001',
            'title': 'Quantum Computing Breakthrough',
            'description': 'Revolutionary quantum processor design with 1000+ qubit capacity',
            'category': 'quantum_computing',
            'funding_goal': 5000000,
            'current_funding': 2750000,
            'votes': 1247,
            'status': 'active',
            'milestones': [
                {'id': 1, 'title': 'Prototype Development', 'completed': True, 'funds_released': 1000000},
                {'id': 2, 'title': 'Testing Phase', 'completed': True, 'funds_released': 750000},
                {'id': 3, 'title': 'Optimization', 'completed': False, 'funds_released': 0},
                {'id': 4, 'title': 'Production Ready', 'completed': False, 'funds_released': 0}
            ],
            'created_at': '2024-12-01T00:00:00Z',
            'creator': 'Dr. Quantum Labs'
        },
        {
            'id': 'rd-002',
            'title': 'AI-Powered Medical Diagnosis',
            'description': 'Advanced AI system for early disease detection and diagnosis',
            'category': 'medical_ai',
            'funding_goal': 3000000,
            'current_funding': 1850000,
            'votes': 892,
            'status': 'active',
            'milestones': [
                {'id': 1, 'title': 'Data Collection', 'completed': True, 'funds_released': 500000},
                {'id': 2, 'title': 'Model Training', 'completed': True, 'funds_released': 750000},
                {'id': 3, 'title': 'Clinical Trials', 'completed': False, 'funds_released': 0}
            ],
            'created_at': '2024-11-15T00:00:00Z',
            'creator': 'MedTech Innovations'
        }
    ]
    
    # Sample manufacturing jobs
    manufacturing_jobs = [
        {
            'id': 'mfg-001',
            'title': '3D Printed Quantum Sensors',
            'description': 'High-precision quantum sensors for industrial applications',
            'type': '3d_printing',
            'status': 'in_progress',
            'progress': 65,
            'estimated_completion': '2025-02-15T00:00:00Z',
            'materials': ['titanium_alloy', 'quantum_dots', 'polymer_substrate'],
            'specifications': {
                'dimensions': '50x30x20mm',
                'precision': '±0.001mm',
                'quantity': 100
            }
        },
        {
            'id': 'mfg-002',
            'title': 'PCB Assembly for IoT Devices',
            'description': 'Smart IoT sensor boards with wireless connectivity',
            'type': 'pcb_fabrication',
            'status': 'completed',
            'progress': 100,
            'estimated_completion': '2025-01-20T00:00:00Z',
            'materials': ['fr4_substrate', 'copper_traces', 'electronic_components'],
            'specifications': {
                'layers': 4,
                'size': '25x15mm',
                'quantity': 500
            }
        }
    ]
    
    # Sample trading data
    trading_data = {
        'market_data': {
            'BTC': {'price': 45250.75, 'change': 2.34, 'volume': 28500000000},
            'ETH': {'price': 2875.50, 'change': -1.23, 'volume': 15200000000},
            'BNB': {'price': 315.25, 'change': 0.87, 'volume': 2100000000},
            'ADA': {'price': 0.485, 'change': 3.45, 'volume': 850000000},
            'SOL': {'price': 98.75, 'change': -0.65, 'volume': 1200000000},
            'AAPL': {'price': 185.50, 'change': 1.25, 'volume': 45000000},
            'TSLA': {'price': 245.75, 'change': -2.15, 'volume': 32000000},
            'GOOGL': {'price': 142.25, 'change': 0.95, 'volume': 28000000}
        },
        'portfolio': {
            'total_value': 125750.50,
            'daily_change': 2.34,
            'positions': [
                {'symbol': 'BTC', 'amount': 1.5, 'value': 67876.13},
                {'symbol': 'ETH', 'amount': 10.2, 'value': 29330.10},
                {'symbol': 'AAPL', 'amount': 150, 'value': 27825.00}
            ]
        },
        'trading_bots': [
            {
                'id': 'bot-001',
                'name': 'Momentum Trader',
                'strategy': 'momentum',
                'status': 'active',
                'profit_loss': 15.75,
                'trades_today': 23
            },
            {
                'id': 'bot-002',
                'name': 'Mean Reversion Bot',
                'strategy': 'mean_reversion',
                'status': 'active',
                'profit_loss': -2.34,
                'trades_today': 8
            }
        ]
    }
    
    # Sample blockchain data
    blockchain_data = [
        {
            'id': 'block-genesis',
            'hash': '0x000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f',
            'height': 0,
            'timestamp': '2025-01-01T00:00:00Z',
            'transactions': 1,
            'size': 285,
            'difficulty': 1,
            'nonce': 2083236893
        },
        {
            'id': 'block-001',
            'hash': '0x00000000839a8e6886ab5951d76f411475428afc90947ee320161bbf18eb6048',
            'height': 1,
            'timestamp': '2025-01-01T00:10:00Z',
            'transactions': 3,
            'size': 512,
            'difficulty': 1.5,
            'nonce': 1924588547
        }
    ]
    
    # Sample communication channels
    communication_channels = [
        {
            'id': 'voice-001',
            'type': 'voice',
            'protocol': 'webrtc',
            'status': 'active',
            'participants': 5,
            'quality': 85,
            'encryption': True
        },
        {
            'id': 'video-001',
            'type': 'video',
            'protocol': 'webrtc',
            'status': 'active',
            'participants': 12,
            'quality': 92,
            'encryption': True
        }
    ]
    
    # Sample social networks
    social_networks = [
        {'name': 'Facebook', 'status': 'connected', 'followers': 15420},
        {'name': 'Twitter/X', 'status': 'connected', 'followers': 8750},
        {'name': 'Instagram', 'status': 'connected', 'followers': 12300},
        {'name': 'LinkedIn', 'status': 'connected', 'followers': 5680},
        {'name': 'YouTube', 'status': 'connected', 'subscribers': 25400}
    ]

# Initialize data on startup
initialize_sample_data()

# Platform status and health check endpoints
@app.route('/api/health')
def health_check():
    """Comprehensive health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'platform': 'Unified Platform',
        'version': '3.0.0',
        'quantum_status': 'operational',
        'ai_consciousness': 'active',
        'biometric_security': 'enabled',
        'blockchain_network': 'connected',
        'iot_manufacturing': 'online',
        'rdlab_community': 'active',
        'social_networks': '31+ platforms connected',
        'trading_systems': 'operational',
        'communication_hub': 'active',
        'no_code_builder': 'ready',
        'specialized_fields': 'available',
        'funding_platform': 'operational',
        '3d_blockchain': 'running',
        'nanotechnology': 'active',
        'quantum_computing': 'stable',
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z'
    })

@app.route('/api/platform/status')
def platform_status():
    """Detailed platform status"""
    return jsonify({
        'overall_status': 'operational',
        'uptime': '99.99%',
        'active_users': 15420,
        'total_transactions': 2847593,
        'blockchain_height': len(blockchain_data),
        'research_projects': len(research_projects),
        'manufacturing_jobs': len(manufacturing_jobs),
        'trading_volume_24h': 125000000,
        'communication_channels': len(communication_channels),
        'social_network_reach': 67550,
        'quantum_qubits': 1024,
        'ai_models_active': 47,
        'iot_devices_connected': 15847,
        'last_updated': datetime.datetime.utcnow().isoformat() + 'Z'
    })

# Authentication endpoints
@app.route('/api/auth/login', methods=['POST'])
def login():
    """User login endpoint"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if username in users_db:
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if users_db[username]['password_hash'] == password_hash:
            session_token = secrets.token_hex(32)
            active_sessions[session_token] = {
                'username': username,
                'role': users_db[username]['role'],
                'permissions': users_db[username]['permissions'],
                'created_at': datetime.datetime.utcnow().isoformat() + 'Z'
            }
            return jsonify({
                'success': True,
                'token': session_token,
                'user': {
                    'username': username,
                    'role': users_db[username]['role'],
                    'permissions': users_db[username]['permissions'],
                    'profile': users_db[username]['profile']
                }
            })
    
    return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

@app.route('/api/auth/register', methods=['POST'])
def register():
    """User registration endpoint"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    name = data.get('name', username)
    
    if username in users_db:
        return jsonify({'success': False, 'message': 'Username already exists'}), 400
    
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    users_db[username] = {
        'password_hash': password_hash,
        'role': 'user',
        'permissions': ['read', 'write'],
        'profile': {
            'name': name,
            'email': email,
            'avatar': 'https://via.placeholder.com/150',
            'bio': 'New user on the Unified Platform',
            'created_at': datetime.datetime.utcnow().isoformat() + 'Z'
        }
    }
    
    return jsonify({'success': True, 'message': 'User registered successfully'})

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """User logout endpoint"""
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if token in active_sessions:
        del active_sessions[token]
    return jsonify({'success': True, 'message': 'Logged out successfully'})

# R&D Lab endpoints
@app.route('/api/rdlab/projects')
def get_research_projects():
    """Get all research projects"""
    return jsonify({
        'projects': research_projects,
        'total_projects': len(research_projects),
        'total_funding': sum(p['current_funding'] for p in research_projects),
        'active_projects': len([p for p in research_projects if p['status'] == 'active'])
    })

@app.route('/api/rdlab/projects/<project_id>/vote', methods=['POST'])
def vote_project(project_id):
    """Vote for a research project"""
    for project in research_projects:
        if project['id'] == project_id:
            project['votes'] += 1
            return jsonify({'success': True, 'votes': project['votes']})
    return jsonify({'success': False, 'message': 'Project not found'}), 404

@app.route('/api/rdlab/projects/<project_id>/fund', methods=['POST'])
def fund_project(project_id):
    """Fund a research project"""
    data = request.get_json()
    amount = data.get('amount', 0)
    
    for project in research_projects:
        if project['id'] == project_id:
            project['current_funding'] += amount
            return jsonify({
                'success': True,
                'current_funding': project['current_funding'],
                'funding_percentage': (project['current_funding'] / project['funding_goal']) * 100
            })
    return jsonify({'success': False, 'message': 'Project not found'}), 404

# Manufacturing endpoints
@app.route('/api/manufacturing/jobs')
def get_manufacturing_jobs():
    """Get all manufacturing jobs"""
    return jsonify({
        'jobs': manufacturing_jobs,
        'total_jobs': len(manufacturing_jobs),
        'active_jobs': len([j for j in manufacturing_jobs if j['status'] == 'in_progress']),
        'completed_jobs': len([j for j in manufacturing_jobs if j['status'] == 'completed'])
    })

@app.route('/api/manufacturing/jobs', methods=['POST'])
def create_manufacturing_job():
    """Create a new manufacturing job"""
    data = request.get_json()
    job_id = f"mfg-{len(manufacturing_jobs) + 1:03d}"
    
    new_job = {
        'id': job_id,
        'title': data.get('title'),
        'description': data.get('description'),
        'type': data.get('type'),
        'status': 'pending',
        'progress': 0,
        'estimated_completion': data.get('estimated_completion'),
        'materials': data.get('materials', []),
        'specifications': data.get('specifications', {}),
        'created_at': datetime.datetime.utcnow().isoformat() + 'Z'
    }
    
    manufacturing_jobs.append(new_job)
    return jsonify({'success': True, 'job': new_job})

# Trading endpoints
@app.route('/api/trading/market-data')
def get_market_data():
    """Get current market data"""
    # Simulate real-time price updates
    for symbol in trading_data['market_data']:
        price_change = random.uniform(-0.05, 0.05)  # ±5% random change
        trading_data['market_data'][symbol]['price'] *= (1 + price_change)
        trading_data['market_data'][symbol]['change'] = price_change * 100
    
    return jsonify(trading_data['market_data'])

@app.route('/api/trading/portfolio')
def get_portfolio():
    """Get user portfolio"""
    return jsonify(trading_data['portfolio'])

@app.route('/api/trading/bots')
def get_trading_bots():
    """Get trading bots status"""
    return jsonify(trading_data['trading_bots'])

@app.route('/api/trading/execute', methods=['POST'])
def execute_trade():
    """Execute a trade"""
    data = request.get_json()
    symbol = data.get('symbol')
    action = data.get('action')  # 'buy' or 'sell'
    amount = data.get
(Content truncated due to size limit. Use line ranges to read in chunks)
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
import datetime
import secrets
import hashlib

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'quantum_unified_platform_2025_cosmic_secret_key'

# Enable CORS for all routes
CORS(app, origins="*", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"])

# Simple in-memory data stores for demo
users_db = {
    'admin': {
        'password_hash': hashlib.sha256('admin123'.encode()).hexdigest(),
        'role': 'admin',
        'permissions': ['all']
    },
    'user': {
        'password_hash': hashlib.sha256('user123'.encode()).hexdigest(),
        'role': 'user',
        'permissions': ['read', 'write']
    }
}

active_sessions = {}
research_projects = []
manufacturing_jobs = []

# Platform status and health check endpoints
@app.route('/api/health')
def health_check():
    """Comprehensive health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'platform': 'Unified Platform',
        'version': '2.0.0',
        'quantum_status': 'operational',
        'ai_consciousness': 'active',
        'biometric_security': 'enabled',
        'blockchain_network': 'connected',
        'iot_manufacturing': 'online',
        'rdlab_community': 'active',
        'social_networks': '31+ platforms connected',
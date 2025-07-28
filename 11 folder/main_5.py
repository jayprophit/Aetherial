import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
from src.models.user import db
from src.routes.user import user_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'unified-platform-secret-key-2024'

# Enable CORS for all routes
CORS(app)

app.register_blueprint(user_bp, url_prefix='/api')

# uncomment if you need to use database
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()

# Comprehensive API endpoints for Unified Platform
@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'Unified Platform API is running!',
        'version': '1.0.0',
        'timestamp': '2024-01-01T00:00:00Z'
    })

@app.route('/api/features')
def get_features():
    return jsonify({
        'blockchain': {
            'name': 'Blockchain & Cryptocurrency',
            'features': [
                '3D Blockchain with Runestones',
                'Multi-Consensus Mechanisms (PoW, PoS, DPoS, PoA, PoH, Quantum)',
                'UBC Native Coin & Q-Tokens',
                'Advanced Mining & Staking (8% APY)',
                'NFT Minting & Marketplace',
                'Flash Loans & DeFi Protocols',
                'Cross-Chain Interoperability',
                'Quantum-Resistant Cryptography'
            ]
        },
        'ai': {
            'name': 'AI & Machine Learning',
            'features': [
                'GPT-4, Claude-3, DALL-E 3 Integration',
                'Advanced Reasoning Frameworks',
                'Multi-Modal Processing',
                'Seven-Node AI Architecture',
                'Quantum AI Enhancement',
                'Real-Time AI Analytics',
                'Custom Model Training',
                'AI-Powered Automation'
            ]
        },
        'banking': {
            'name': 'Banking & Financial Services',
            'features': [
                'Complete Banking Services',
                'Multiple Account Types (Checking, Savings, Business, Investment)',
                'Loan Products (Personal, Auto, Mortgage, Business)',
                'Credit & Debit Card Services',
                'Investment Management',
                'Tax & Capital Gains Calculator',
                'AI Tax Accountant',
                'Offshore Accounts & Trust Funds'
            ]
        },
        'ecommerce': {
            'name': 'E-commerce & Business',
            'features': [
                'Complete E-commerce Platform',
                'Shopping Cart & Checkout',
                'Inventory Management',
                'Payment Processing',
                'Business Formation Services',
                'ERP Systems',
                'Workflow Automation',
                'Supply Chain Management'
            ]
        },
        'legal': {
            'name': 'Legal & Compliance',
            'features': [
                'Legal Consultation Services',
                'Case Management System',
                'Document Generation',
                'LLP Formation',
                'Compliance Monitoring',
                'Legal Research Database',
                'Contract Management',
                'Regulatory Compliance'
            ]
        },
        'privacy': {
            'name': 'Privacy & Security',
            'features': [
                'Global VPN Network',
                'Tor/Onion Router Integration',
                'Military-Grade Encryption',
                'Privacy Analytics',
                'Quantum-Resistant Security',
                'Zero-Logs Policy',
                'Advanced Threat Protection',
                'Secure Communications'
            ]
        },
        'healthcare': {
            'name': 'Healthcare & Life Sciences',
            'features': [
                'Medical AI Diagnostics',
                'Patient Management System',
                'CRISPR Gene Editing Tools',
                'Clinical Decision Support',
                'Drug Discovery Platform',
                'Telemedicine Integration',
                'Health Analytics',
                'Medical Research Database'
            ]
        },
        'knowledge': {
            'name': 'Knowledge & Education',
            'features': [
                'Universal Knowledge Engine',
                'Sociology & Philosophy Databases',
                'Psychology & Spirituality Content',
                'Astrology & Hermetics Systems',
                'Personalized Learning',
                'Research Assistance',
                'Educational Analytics',
                'Skill Assessment'
            ]
        }
    })

@app.route('/api/stats')
def get_stats():
    return jsonify({
        'users': '2.5M+',
        'transactions': '125M+',
        'uptime': '99.99%',
        'countries': '195+',
        'features': '200+',
        'categories': '12',
        'industries': '8+',
        'live_metrics': {
            'active_users': 2547832,
            'daily_transactions': 125847293,
            'system_uptime': 99.99,
            'global_coverage': 195,
            'total_features': 200,
            'major_categories': 12,
            'industry_solutions': 8
        }
    })

@app.route('/api/industries')
def get_industries():
    return jsonify({
        'healthcare': {
            'name': 'Healthcare',
            'description': 'Comprehensive medical platform with AI diagnostics, patient management, and CRISPR gene editing',
            'features': ['AI Diagnostics', 'Patient Management', 'Gene Editing', 'Telemedicine']
        },
        'engineering': {
            'name': 'Engineering',
            'description': 'Complete engineering solutions with CAD integration, materials database, and simulation tools',
            'features': ['CAD Integration', 'Materials Database', 'Simulation Tools', 'Project Management']
        },
        'legal': {
            'name': 'Legal',
            'description': 'Professional legal services with case management, document generation, and compliance monitoring',
            'features': ['Case Management', 'Document Generation', 'Compliance', 'Legal Research']
        },
        'financial': {
            'name': 'Financial',
            'description': 'Advanced financial services with banking, trading, tax optimization, and investment management',
            'features': ['Banking Services', 'Trading Platform', 'Tax Optimization', 'Investment Management']
        },
        'manufacturing': {
            'name': 'Manufacturing',
            'description': 'Smart manufacturing with IoT integration, 3D printing, CNC control, and predictive maintenance',
            'features': ['IoT Integration', '3D Printing', 'CNC Control', 'Predictive Maintenance']
        },
        'enterprise': {
            'name': 'Enterprise',
            'description': 'Complete enterprise solutions with ERP, CRM, workflow automation, and business intelligence',
            'features': ['ERP Systems', 'CRM Platform', 'Workflow Automation', 'Business Intelligence']
        },
        'education': {
            'name': 'Education',
            'description': 'Advanced educational platform with personalized learning, knowledge management, and skill assessment',
            'features': ['Personalized Learning', 'Knowledge Management', 'Skill Assessment', 'Research Tools']
        },
        'technology': {
            'name': 'Technology',
            'description': 'Cutting-edge technology solutions with AI, blockchain, quantum computing, and advanced analytics',
            'features': ['AI Integration', 'Blockchain Technology', 'Quantum Computing', 'Advanced Analytics']
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
    app.run(host='0.0.0.0', port=5000, debug=False)


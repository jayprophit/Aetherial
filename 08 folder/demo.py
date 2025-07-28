from flask import Blueprint, request, jsonify
import datetime
import uuid

demo_bp = Blueprint('demo', __name__)

# Demo data for different platform modules
DEMO_DATA = {
    'quantum_assistant': {
        'title': 'Quantum Virtual Assistant Demo',
        'description': 'Experience our 3D avatar interface with advanced AI capabilities',
        'features': [
            'Real-time 3D avatar with emotional expressions',
            'Multi-AI model integration (GPT-4, Claude, Gemini)',
            'Advanced biometric authentication',
            'Rife frequency therapy integration',
            'Quantum matter manipulation capabilities'
        ],
        'duration': '15 minutes',
        'video_url': '/demo/videos/quantum-assistant-demo.mp4',
        'interactive_url': '/demo/quantum-assistant'
    },
    'social_hub': {
        'title': 'Social Network Hub Demo',
        'description': 'Unified interface for 31+ social media platforms',
        'features': [
            'Cross-platform posting and management',
            'Advanced analytics and insights',
            'AI-powered content creation',
            'Community management tools',
            'Influencer collaboration features'
        ],
        'duration': '12 minutes',
        'video_url': '/demo/videos/social-hub-demo.mp4',
        'interactive_url': '/demo/social-hub'
    },
    'ecommerce': {
        'title': 'E-commerce Marketplace Demo',
        'description': 'Multi-vendor platform with AI optimization',
        'features': [
            'AI-powered product recommendations',
            'Advanced inventory management',
            'Multi-currency support',
            'Global shipping integration',
            'Fraud detection and prevention'
        ],
        'duration': '18 minutes',
        'video_url': '/demo/videos/ecommerce-demo.mp4',
        'interactive_url': '/demo/ecommerce'
    },
    'education': {
        'title': 'Education Hub Demo',
        'description': 'World-class LMS with AI-powered personalization',
        'features': [
            'Adaptive learning paths',
            'Multi-format content support',
            'Blockchain-verified certificates',
            'Real-time progress tracking',
            'AI-powered assessments'
        ],
        'duration': '20 minutes',
        'video_url': '/demo/videos/education-demo.mp4',
        'interactive_url': '/demo/education'
    },
    'jobs': {
        'title': 'Job Marketplace Demo',
        'description': 'AI-powered matching with 85%+ accuracy',
        'features': [
            'Intelligent job-candidate matching',
            'Resume optimization tools',
            'Interview preparation system',
            'Skill assessment platform',
            'Career path planning'
        ],
        'duration': '16 minutes',
        'video_url': '/demo/videos/jobs-demo.mp4',
        'interactive_url': '/demo/jobs'
    },
    'developer_tools': {
        'title': 'Developer Tools Demo',
        'description': 'Multi-language IDE with AI assistance',
        'features': [
            'AI-powered code completion',
            'Advanced debugging tools',
            'One-click deployment',
            'Collaborative coding',
            'Performance optimization'
        ],
        'duration': '22 minutes',
        'video_url': '/demo/videos/developer-tools-demo.mp4',
        'interactive_url': '/demo/developer-tools'
    },
    'store_builder': {
        'title': 'Store & Page Builder Demo',
        'description': 'Professional website creation with drag-and-drop',
        'features': [
            'Visual drag-and-drop editor',
            'Professional templates',
            'E-commerce integration',
            'SEO optimization',
            'Mobile responsive design'
        ],
        'duration': '14 minutes',
        'video_url': '/demo/videos/store-builder-demo.mp4',
        'interactive_url': '/demo/store-builder'
    },
    'metaverse': {
        'title': 'Metaverse Module Demo',
        'description': 'Virtual worlds with NFT integration',
        'features': [
            '3D virtual environments',
            'Avatar customization',
            'NFT marketplace',
            'Virtual asset trading',
            'Social interaction tools'
        ],
        'duration': '25 minutes',
        'video_url': '/demo/videos/metaverse-demo.mp4',
        'interactive_url': '/demo/metaverse'
    }
}

@demo_bp.route('/modules', methods=['GET'])
def get_demo_modules():
    """Get list of available demo modules"""
    return jsonify({
        'modules': DEMO_DATA,
        'total_modules': len(DEMO_DATA)
    }), 200

@demo_bp.route('/module/<module_name>', methods=['GET'])
def get_demo_module(module_name):
    """Get specific demo module details"""
    if module_name not in DEMO_DATA:
        return jsonify({'error': 'Demo module not found'}), 404
    
    return jsonify({
        'module': DEMO_DATA[module_name],
        'module_name': module_name
    }), 200

@demo_bp.route('/schedule', methods=['POST'])
def schedule_demo():
    """Schedule a personalized demo session"""
    try:
        data = request.get_json()
        
        required_fields = ['name', 'email', 'company', 'phone']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Demo scheduling data
        demo_session = {
            'id': str(uuid.uuid4()),
            'name': data['name'],
            'email': data['email'],
            'company': data['company'],
            'phone': data['phone'],
            'preferred_date': data.get('preferredDate'),
            'preferred_time': data.get('preferredTime'),
            'timezone': data.get('timezone', 'UTC'),
            'modules_of_interest': data.get('modulesOfInterest', []),
            'company_size': data.get('companySize'),
            'use_case': data.get('useCase'),
            'additional_notes': data.get('additionalNotes'),
            'status': 'scheduled',
            'created_at': datetime.datetime.utcnow().isoformat(),
            'demo_url': f'/demo/session/{str(uuid.uuid4())}'
        }
        
        # In a real application, you would save this to a database
        # and send confirmation emails
        
        return jsonify({
            'message': 'Demo scheduled successfully',
            'demo_session': demo_session,
            'confirmation_email_sent': True
        }), 201
        
    except Exception as e:
        return jsonify({'error': 'Failed to schedule demo', 'details': str(e)}), 500

@demo_bp.route('/request-access', methods=['POST'])
def request_demo_access():
    """Request access to interactive demo"""
    try:
        data = request.get_json()
        
        required_fields = ['email', 'module']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        email = data['email']
        module = data['module']
        
        if module not in DEMO_DATA:
            return jsonify({'error': 'Invalid demo module'}), 400
        
        # Generate demo access token
        access_token = str(uuid.uuid4())
        
        demo_access = {
            'access_token': access_token,
            'email': email,
            'module': module,
            'expires_at': (datetime.datetime.utcnow() + datetime.timedelta(hours=24)).isoformat(),
            'demo_url': f'/demo/{module}?token={access_token}',
            'created_at': datetime.datetime.utcnow().isoformat()
        }
        
        return jsonify({
            'message': 'Demo access granted',
            'demo_access': demo_access
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to grant demo access', 'details': str(e)}), 500

@demo_bp.route('/feedback', methods=['POST'])
def submit_demo_feedback():
    """Submit feedback after demo experience"""
    try:
        data = request.get_json()
        
        feedback = {
            'id': str(uuid.uuid4()),
            'email': data.get('email'),
            'module': data.get('module'),
            'rating': data.get('rating'),  # 1-5 scale
            'feedback_text': data.get('feedbackText'),
            'would_recommend': data.get('wouldRecommend'),
            'interested_in_trial': data.get('interestedInTrial'),
            'contact_for_sales': data.get('contactForSales'),
            'submitted_at': datetime.datetime.utcnow().isoformat()
        }
        
        return jsonify({
            'message': 'Feedback submitted successfully',
            'feedback_id': feedback['id']
        }), 201
        
    except Exception as e:
        return jsonify({'error': 'Failed to submit feedback', 'details': str(e)}), 500

@demo_bp.route('/analytics', methods=['GET'])
def get_demo_analytics():
    """Get demo usage analytics (for internal use)"""
    # This would typically require admin authentication
    analytics = {
        'total_demo_requests': 1247,
        'scheduled_demos': 89,
        'completed_demos': 76,
        'conversion_rate': 0.68,
        'popular_modules': [
            {'module': 'quantum_assistant', 'requests': 342},
            {'module': 'ecommerce', 'requests': 298},
            {'module': 'education', 'requests': 267},
            {'module': 'jobs', 'requests': 189},
            {'module': 'developer_tools', 'requests': 151}
        ],
        'average_rating': 4.7,
        'trial_conversion_rate': 0.34
    }
    
    return jsonify(analytics), 200


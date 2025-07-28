from flask import Blueprint, request, jsonify
import datetime
import uuid

access_control_bp = Blueprint('access_control', __name__)

# Define access levels and their capabilities
ACCESS_LEVELS = {
    'guest': {
        'level': 0,
        'name': 'Guest Access',
        'description': 'Browse and explore without registration',
        'features': [
            'Browse social media content',
            'View educational content',
            'Browse marketplace products',
            'Watch demo videos',
            'Read articles and blogs',
            'Use basic calculators',
            'View public profiles',
            'Access help documentation'
        ],
        'limitations': [
            'Cannot post or comment',
            'Cannot save preferences',
            'Cannot access personalized content',
            'Limited search results',
            'No customer support'
        ]
    },
    'basic': {
        'level': 1,
        'name': 'Basic User (No-KYC)',
        'description': 'Standard features with email registration only',
        'features': [
            'All guest features',
            'Create and manage profile',
            'Post and comment on social media',
            'Save favorites and preferences',
            'Basic messaging',
            'Join communities',
            'Create basic content',
            'Use standard templates',
            'Access customer support',
            'Participate in forums'
        ],
        'limitations': [
            'Limited transaction amounts',
            'Cannot access business features',
            'No blockchain transactions',
            'No advanced AI features',
            'Limited storage space',
            'Basic analytics only'
        ],
        'requirements': ['email_verification']
    },
    'verified': {
        'level': 2,
        'name': 'Verified User (Partial KYC)',
        'description': 'Enhanced features with phone verification',
        'features': [
            'All basic features',
            'Higher transaction limits',
            'Advanced messaging',
            'Create paid content',
            'Access premium templates',
            'Basic business tools',
            'Enhanced security features',
            'Priority customer support'
        ],
        'limitations': [
            'Limited business features',
            'Restricted blockchain access',
            'Cannot create business accounts',
            'Limited API access'
        ],
        'requirements': ['email_verification', 'phone_verification']
    },
    'kyc_individual': {
        'level': 3,
        'name': 'KYC Individual',
        'description': 'Full individual features with identity verification',
        'features': [
            'All verified features',
            'Full blockchain access',
            'Cryptocurrency transactions',
            'Advanced AI features',
            'Create and sell NFTs',
            'Access financial services',
            'International transactions',
            'Advanced analytics',
            'API access',
            'White-label options'
        ],
        'limitations': [
            'Cannot create business accounts',
            'Limited corporate features',
            'Cannot access enterprise tools'
        ],
        'requirements': ['email_verification', 'phone_verification', 'identity_verification', 'address_verification']
    },
    'kyc_business': {
        'level': 4,
        'name': 'KYC Business',
        'description': 'Full business features with company verification',
        'features': [
            'All individual KYC features',
            'Create business accounts',
            'Access enterprise tools',
            'Advanced business analytics',
            'Multi-user management',
            'Corporate blockchain features',
            'Advanced API access',
            'Custom integrations',
            'Dedicated support',
            'Compliance tools',
            'Advanced security features'
        ],
        'limitations': [],
        'requirements': [
            'email_verification', 
            'phone_verification', 
            'identity_verification', 
            'address_verification',
            'business_registration',
            'business_address_verification',
            'beneficial_ownership_disclosure'
        ]
    }
}

# Feature access matrix
FEATURE_ACCESS = {
    'social_media': {
        'browse': ['guest', 'basic', 'verified', 'kyc_individual', 'kyc_business'],
        'post': ['basic', 'verified', 'kyc_individual', 'kyc_business'],
        'monetize': ['verified', 'kyc_individual', 'kyc_business'],
        'business_pages': ['kyc_business']
    },
    'ecommerce': {
        'browse': ['guest', 'basic', 'verified', 'kyc_individual', 'kyc_business'],
        'purchase_basic': ['basic', 'verified', 'kyc_individual', 'kyc_business'],
        'sell_basic': ['verified', 'kyc_individual', 'kyc_business'],
        'sell_advanced': ['kyc_individual', 'kyc_business'],
        'business_store': ['kyc_business']
    },
    'education': {
        'browse_free': ['guest', 'basic', 'verified', 'kyc_individual', 'kyc_business'],
        'enroll_courses': ['basic', 'verified', 'kyc_individual', 'kyc_business'],
        'create_courses': ['verified', 'kyc_individual', 'kyc_business'],
        'sell_courses': ['kyc_individual', 'kyc_business'],
        'corporate_training': ['kyc_business']
    },
    'blockchain': {
        'view_transactions': ['basic', 'verified', 'kyc_individual', 'kyc_business'],
        'basic_transactions': ['kyc_individual', 'kyc_business'],
        'advanced_features': ['kyc_individual', 'kyc_business'],
        'business_blockchain': ['kyc_business']
    },
    'ai_features': {
        'basic_ai': ['basic', 'verified', 'kyc_individual', 'kyc_business'],
        'advanced_ai': ['kyc_individual', 'kyc_business'],
        'quantum_features': ['kyc_individual', 'kyc_business'],
        'enterprise_ai': ['kyc_business']
    },
    'financial_services': {
        'view_rates': ['guest', 'basic', 'verified', 'kyc_individual', 'kyc_business'],
        'basic_transactions': ['kyc_individual', 'kyc_business'],
        'advanced_trading': ['kyc_individual', 'kyc_business'],
        'business_banking': ['kyc_business']
    }
}

@access_control_bp.route('/levels', methods=['GET'])
def get_access_levels():
    """Get all available access levels"""
    return jsonify({
        'access_levels': ACCESS_LEVELS,
        'feature_access': FEATURE_ACCESS
    }), 200

@access_control_bp.route('/check-access', methods=['POST'])
def check_feature_access():
    """Check if user has access to specific feature"""
    try:
        data = request.get_json()
        user_level = data.get('user_level', 'guest')
        feature = data.get('feature')
        action = data.get('action')
        
        if not feature or not action:
            return jsonify({'error': 'Feature and action are required'}), 400
        
        if feature not in FEATURE_ACCESS:
            return jsonify({'error': 'Invalid feature'}), 400
        
        if action not in FEATURE_ACCESS[feature]:
            return jsonify({'error': 'Invalid action for feature'}), 400
        
        allowed_levels = FEATURE_ACCESS[feature][action]
        has_access = user_level in allowed_levels
        
        response = {
            'has_access': has_access,
            'user_level': user_level,
            'feature': feature,
            'action': action,
            'required_levels': allowed_levels
        }
        
        if not has_access:
            # Suggest upgrade path
            current_level_num = ACCESS_LEVELS.get(user_level, {}).get('level', 0)
            required_level = None
            
            for level_name, level_info in ACCESS_LEVELS.items():
                if (level_name in allowed_levels and 
                    level_info['level'] > current_level_num):
                    if required_level is None or level_info['level'] < ACCESS_LEVELS[required_level]['level']:
                        required_level = level_name
            
            if required_level:
                response['upgrade_suggestion'] = {
                    'target_level': required_level,
                    'level_info': ACCESS_LEVELS[required_level],
                    'requirements': ACCESS_LEVELS[required_level].get('requirements', [])
                }
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({'error': 'Access check failed', 'details': str(e)}), 500

@access_control_bp.route('/upgrade-path', methods=['POST'])
def get_upgrade_path():
    """Get upgrade path from current level to target level"""
    try:
        data = request.get_json()
        current_level = data.get('current_level', 'guest')
        target_level = data.get('target_level')
        
        if target_level not in ACCESS_LEVELS:
            return jsonify({'error': 'Invalid target level'}), 400
        
        current_level_num = ACCESS_LEVELS.get(current_level, {}).get('level', 0)
        target_level_num = ACCESS_LEVELS[target_level]['level']
        
        if target_level_num <= current_level_num:
            return jsonify({'error': 'Target level must be higher than current level'}), 400
        
        # Build upgrade path
        upgrade_steps = []
        for level_name, level_info in ACCESS_LEVELS.items():
            level_num = level_info['level']
            if current_level_num < level_num <= target_level_num:
                upgrade_steps.append({
                    'level': level_name,
                    'level_info': level_info,
                    'requirements': level_info.get('requirements', []),
                    'estimated_time': get_verification_time(level_name)
                })
        
        # Sort by level number
        upgrade_steps.sort(key=lambda x: ACCESS_LEVELS[x['level']]['level'])
        
        return jsonify({
            'current_level': current_level,
            'target_level': target_level,
            'upgrade_steps': upgrade_steps,
            'total_estimated_time': sum(step['estimated_time'] for step in upgrade_steps)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get upgrade path', 'details': str(e)}), 500

def get_verification_time(level):
    """Get estimated verification time for each level"""
    times = {
        'basic': 5,  # 5 minutes
        'verified': 30,  # 30 minutes
        'kyc_individual': 1440,  # 24 hours
        'kyc_business': 4320  # 72 hours
    }
    return times.get(level, 0)

@access_control_bp.route('/guest-features', methods=['GET'])
def get_guest_features():
    """Get features available to guest users"""
    guest_features = {
        'social_media': {
            'browse_feeds': True,
            'view_profiles': True,
            'search_content': True,
            'view_trending': True
        },
        'ecommerce': {
            'browse_products': True,
            'view_product_details': True,
            'search_products': True,
            'view_reviews': True,
            'compare_products': True
        },
        'education': {
            'browse_courses': True,
            'view_free_content': True,
            'watch_preview_videos': True,
            'read_course_descriptions': True
        },
        'content': {
            'read_articles': True,
            'watch_videos': True,
            'view_galleries': True,
            'access_help_docs': True
        },
        'tools': {
            'currency_converter': True,
            'basic_calculators': True,
            'timezone_converter': True,
            'unit_converter': True
        }
    }
    
    return jsonify({
        'guest_features': guest_features,
        'registration_benefits': ACCESS_LEVELS['basic']['features'][:5],
        'call_to_action': 'Register for free to unlock more features!'
    }), 200

@access_control_bp.route('/kyc-requirements', methods=['GET'])
def get_kyc_requirements():
    """Get KYC requirements for different levels"""
    kyc_requirements = {
        'kyc_individual': {
            'documents_required': [
                'Government-issued photo ID (passport, driver\'s license, national ID)',
                'Proof of address (utility bill, bank statement, lease agreement)',
                'Selfie with ID document'
            ],
            'information_required': [
                'Full legal name',
                'Date of birth',
                'Nationality',
                'Current address',
                'Phone number',
                'Email address',
                'Occupation',
                'Source of funds'
            ],
            'verification_process': [
                'Submit required documents',
                'Automated document verification',
                'Manual review if needed',
                'Approval notification'
            ],
            'estimated_time': '1-24 hours',
            'benefits': ACCESS_LEVELS['kyc_individual']['features']
        },
        'kyc_business': {
            'documents_required': [
                'Certificate of incorporation',
                'Business registration documents',
                'Tax identification number',
                'Proof of business address',
                'Director/shareholder information',
                'Beneficial ownership disclosure',
                'Bank account verification'
            ],
            'information_required': [
                'Legal business name',
                'Business registration number',
                'Business address',
                'Industry/business type',
                'Annual revenue',
                'Number of employees',
                'Director/officer details',
                'Beneficial owners (>25% ownership)'
            ],
            'verification_process': [
                'Submit business documents',
                'Verify business registration',
                'Verify directors/officers',
                'Beneficial ownership verification',
                'Business address verification',
                'Final approval'
            ],
            'estimated_time': '2-5 business days',
            'benefits': ACCESS_LEVELS['kyc_business']['features']
        }
    }
    
    return jsonify({
        'kyc_requirements': kyc_requirements,
        'compliance_note': 'KYC verification is required for regulatory compliance and to access advanced financial features.'
    }), 200

@access_control_bp.route('/feature-comparison', methods=['GET'])
def get_feature_comparison():
    """Get feature comparison across all access levels"""
    comparison = {}
    
    for feature_category, actions in FEATURE_ACCESS.items():
        comparison[feature_category] = {}
        for action, allowed_levels in actions.items():
            comparison[feature_category][action] = {
                level: level in allowed_levels 
                for level in ACCESS_LEVELS.keys()
            }
    
    return jsonify({
        'feature_comparison': comparison,
        'access_levels': {
            level: {
                'name': info['name'],
                'level': info['level'],
                'description': info['description']
            }
            for level, info in ACCESS_LEVELS.items()
        }
    }), 200


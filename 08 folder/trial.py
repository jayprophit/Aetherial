from flask import Blueprint, request, jsonify
import datetime
import uuid

trial_bp = Blueprint('trial', __name__)

# Trial plans configuration
TRIAL_PLANS = {
    'basic': {
        'name': 'Basic Trial',
        'duration_days': 14,
        'features': [
            'Access to all core modules',
            'Up to 100 API calls per day',
            'Basic support',
            'Standard templates',
            'Community access'
        ],
        'limitations': {
            'api_calls_per_day': 100,
            'storage_gb': 1,
            'users': 1,
            'projects': 3
        }
    },
    'professional': {
        'name': 'Professional Trial',
        'duration_days': 30,
        'features': [
            'Access to all modules including AI features',
            'Up to 1000 API calls per day',
            'Priority support',
            'Premium templates',
            'Advanced analytics',
            'Custom integrations'
        ],
        'limitations': {
            'api_calls_per_day': 1000,
            'storage_gb': 10,
            'users': 5,
            'projects': 10
        }
    },
    'enterprise': {
        'name': 'Enterprise Trial',
        'duration_days': 45,
        'features': [
            'Full platform access',
            'Unlimited API calls',
            'Dedicated support',
            'Custom templates',
            'Advanced AI features',
            'Quantum computing access',
            'White-label options'
        ],
        'limitations': {
            'api_calls_per_day': -1,  # Unlimited
            'storage_gb': 100,
            'users': 25,
            'projects': -1  # Unlimited
        }
    }
}

@trial_bp.route('/plans', methods=['GET'])
def get_trial_plans():
    """Get available trial plans"""
    return jsonify({
        'plans': TRIAL_PLANS,
        'default_plan': 'professional'
    }), 200

@trial_bp.route('/start', methods=['POST'])
def start_trial():
    """Start a free trial"""
    try:
        data = request.get_json()
        
        required_fields = ['email', 'firstName', 'lastName', 'company']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        plan = data.get('plan', 'professional')
        if plan not in TRIAL_PLANS:
            return jsonify({'error': 'Invalid trial plan'}), 400
        
        trial_config = TRIAL_PLANS[plan]
        
        # Generate trial session
        trial_session = {
            'trial_id': str(uuid.uuid4()),
            'user_info': {
                'email': data['email'],
                'firstName': data['firstName'],
                'lastName': data['lastName'],
                'company': data['company'],
                'phone': data.get('phone'),
                'jobTitle': data.get('jobTitle'),
                'companySize': data.get('companySize'),
                'industry': data.get('industry')
            },
            'plan': plan,
            'plan_details': trial_config,
            'start_date': datetime.datetime.utcnow().isoformat(),
            'end_date': (datetime.datetime.utcnow() + datetime.timedelta(days=trial_config['duration_days'])).isoformat(),
            'status': 'active',
            'usage': {
                'api_calls_today': 0,
                'storage_used_gb': 0,
                'users_created': 1,
                'projects_created': 0
            },
            'access_credentials': {
                'trial_token': str(uuid.uuid4()),
                'dashboard_url': f'/trial/dashboard/{str(uuid.uuid4())}',
                'api_key': f'trial_{str(uuid.uuid4()).replace("-", "")}'
            }
        }
        
        return jsonify({
            'message': 'Trial started successfully',
            'trial_session': trial_session,
            'welcome_email_sent': True
        }), 201
        
    except Exception as e:
        return jsonify({'error': 'Failed to start trial', 'details': str(e)}), 500

@trial_bp.route('/status/<trial_id>', methods=['GET'])
def get_trial_status(trial_id):
    """Get trial status and usage information"""
    try:
        # In a real application, you would fetch this from the database
        # For demo purposes, we'll return mock data
        trial_status = {
            'trial_id': trial_id,
            'status': 'active',
            'plan': 'professional',
            'days_remaining': 23,
            'usage': {
                'api_calls_today': 47,
                'api_calls_limit': 1000,
                'storage_used_gb': 2.3,
                'storage_limit_gb': 10,
                'users_created': 3,
                'users_limit': 5,
                'projects_created': 2,
                'projects_limit': 10
            },
            'features_used': [
                'Quantum Virtual Assistant',
                'E-commerce Marketplace',
                'Education Hub'
            ],
            'upgrade_recommendations': [
                {
                    'plan': 'Professional',
                    'reason': 'Unlimited API calls for your growing usage',
                    'discount': '20% off first 3 months'
                }
            ]
        }
        
        return jsonify(trial_status), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get trial status', 'details': str(e)}), 500

@trial_bp.route('/extend', methods=['POST'])
def extend_trial():
    """Extend trial period"""
    try:
        data = request.get_json()
        trial_id = data.get('trial_id')
        extension_days = data.get('extension_days', 7)
        reason = data.get('reason', 'User request')
        
        if not trial_id:
            return jsonify({'error': 'Trial ID is required'}), 400
        
        # In a real application, you would update the database
        extended_trial = {
            'trial_id': trial_id,
            'original_end_date': '2025-07-27T00:00:00Z',
            'new_end_date': (datetime.datetime.utcnow() + datetime.timedelta(days=extension_days)).isoformat(),
            'extension_days': extension_days,
            'reason': reason,
            'extended_at': datetime.datetime.utcnow().isoformat()
        }
        
        return jsonify({
            'message': 'Trial extended successfully',
            'extension_details': extended_trial
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to extend trial', 'details': str(e)}), 500

@trial_bp.route('/upgrade', methods=['POST'])
def upgrade_trial():
    """Upgrade trial to paid plan"""
    try:
        data = request.get_json()
        trial_id = data.get('trial_id')
        target_plan = data.get('target_plan')
        payment_method = data.get('payment_method')
        
        if not all([trial_id, target_plan, payment_method]):
            return jsonify({'error': 'Trial ID, target plan, and payment method are required'}), 400
        
        # Available paid plans
        paid_plans = {
            'starter': {
                'name': 'Starter Plan',
                'price_monthly': 29,
                'price_yearly': 290,
                'features': ['All trial features', 'Increased limits', 'Email support']
            },
            'professional': {
                'name': 'Professional Plan',
                'price_monthly': 99,
                'price_yearly': 990,
                'features': ['All starter features', 'Advanced AI', 'Priority support', 'Custom integrations']
            },
            'enterprise': {
                'name': 'Enterprise Plan',
                'price_monthly': 299,
                'price_yearly': 2990,
                'features': ['All professional features', 'Unlimited usage', 'Dedicated support', 'Custom development']
            }
        }
        
        if target_plan not in paid_plans:
            return jsonify({'error': 'Invalid target plan'}), 400
        
        upgrade_result = {
            'trial_id': trial_id,
            'upgrade_id': str(uuid.uuid4()),
            'from_plan': 'trial',
            'to_plan': target_plan,
            'plan_details': paid_plans[target_plan],
            'payment_method': payment_method,
            'upgrade_date': datetime.datetime.utcnow().isoformat(),
            'billing_cycle': data.get('billing_cycle', 'monthly'),
            'discount_applied': '20% off first 3 months',
            'next_billing_date': (datetime.datetime.utcnow() + datetime.timedelta(days=30)).isoformat()
        }
        
        return jsonify({
            'message': 'Trial upgraded successfully',
            'upgrade_details': upgrade_result,
            'welcome_to_paid_plan': True
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to upgrade trial', 'details': str(e)}), 500

@trial_bp.route('/cancel', methods=['POST'])
def cancel_trial():
    """Cancel trial"""
    try:
        data = request.get_json()
        trial_id = data.get('trial_id')
        reason = data.get('reason')
        feedback = data.get('feedback')
        
        if not trial_id:
            return jsonify({'error': 'Trial ID is required'}), 400
        
        cancellation = {
            'trial_id': trial_id,
            'cancellation_id': str(uuid.uuid4()),
            'cancelled_at': datetime.datetime.utcnow().isoformat(),
            'reason': reason,
            'feedback': feedback,
            'data_retention_days': 30,
            'reactivation_possible': True
        }
        
        return jsonify({
            'message': 'Trial cancelled successfully',
            'cancellation_details': cancellation,
            'data_retention_notice': 'Your data will be retained for 30 days in case you want to reactivate'
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to cancel trial', 'details': str(e)}), 500

@trial_bp.route('/analytics', methods=['GET'])
def get_trial_analytics():
    """Get trial analytics (for internal use)"""
    analytics = {
        'total_trials_started': 2847,
        'active_trials': 1203,
        'completed_trials': 1644,
        'conversion_rate': 0.42,
        'popular_plans': [
            {'plan': 'professional', 'percentage': 0.65},
            {'plan': 'basic', 'percentage': 0.25},
            {'plan': 'enterprise', 'percentage': 0.10}
        ],
        'average_trial_duration': 18.5,
        'upgrade_rate_by_plan': {
            'basic': 0.28,
            'professional': 0.45,
            'enterprise': 0.67
        },
        'common_cancellation_reasons': [
            {'reason': 'Too complex', 'percentage': 0.23},
            {'reason': 'Price too high', 'percentage': 0.19},
            {'reason': 'Missing features', 'percentage': 0.15},
            {'reason': 'Found alternative', 'percentage': 0.12}
        ]
    }
    
    return jsonify(analytics), 200


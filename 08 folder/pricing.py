from flask import Blueprint, request, jsonify
import datetime
import uuid

pricing_bp = Blueprint('pricing', __name__)

# Pricing structure for business services
PRICING_PLANS = {
    'personal': {
        'name': 'Personal',
        'type': 'personal',
        'monthly_fee': 0,
        'features': {
            'social_media': {
                'posts_per_month': 'unlimited',
                'communities': 'unlimited',
                'messaging': 'basic',
                'advertising': False
            },
            'ecommerce': {
                'can_sell': False,
                'can_buy': True,
                'transaction_fee': 0,
                'listing_fee': 0
            },
            'education': {
                'can_create_courses': False,
                'can_enroll': True,
                'course_fee': 0
            },
            'storage': '1GB',
            'support': 'community'
        }
    },
    'business_starter': {
        'name': 'Business Starter',
        'type': 'business',
        'monthly_fee': 29.99,
        'features': {
            'social_media': {
                'posts_per_month': 'unlimited',
                'communities': 'unlimited',
                'messaging': 'advanced',
                'advertising': True,
                'business_pages': True
            },
            'ecommerce': {
                'can_sell': True,
                'can_buy': True,
                'transaction_fee': 2.9,  # percentage
                'listing_fee': 0.30,  # per listing
                'max_products': 100
            },
            'education': {
                'can_create_courses': True,
                'can_enroll': True,
                'course_fee': 5.0,  # percentage
                'max_courses': 10
            },
            'analytics': 'basic',
            'storage': '10GB',
            'support': 'email'
        }
    },
    'business_professional': {
        'name': 'Business Professional',
        'type': 'business',
        'monthly_fee': 79.99,
        'features': {
            'social_media': {
                'posts_per_month': 'unlimited',
                'communities': 'unlimited',
                'messaging': 'advanced',
                'advertising': True,
                'business_pages': True,
                'advanced_advertising': True
            },
            'ecommerce': {
                'can_sell': True,
                'can_buy': True,
                'transaction_fee': 2.4,  # percentage
                'listing_fee': 0.20,  # per listing
                'max_products': 1000
            },
            'education': {
                'can_create_courses': True,
                'can_enroll': True,
                'course_fee': 3.5,  # percentage
                'max_courses': 50
            },
            'analytics': 'advanced',
            'ai_insights': True,
            'storage': '50GB',
            'support': 'priority_email'
        }
    },
    'business_enterprise': {
        'name': 'Business Enterprise',
        'type': 'business',
        'monthly_fee': 199.99,
        'features': {
            'social_media': {
                'posts_per_month': 'unlimited',
                'communities': 'unlimited',
                'messaging': 'enterprise',
                'advertising': True,
                'business_pages': True,
                'advanced_advertising': True,
                'white_label': True
            },
            'ecommerce': {
                'can_sell': True,
                'can_buy': True,
                'transaction_fee': 1.9,  # percentage
                'listing_fee': 0.10,  # per listing
                'max_products': 'unlimited'
            },
            'education': {
                'can_create_courses': True,
                'can_enroll': True,
                'course_fee': 2.5,  # percentage
                'max_courses': 'unlimited'
            },
            'analytics': 'enterprise',
            'ai_insights': True,
            'custom_integrations': True,
            'api_access': True,
            'storage': '500GB',
            'support': 'dedicated_manager'
        }
    }
}

# Service fees for specific actions
SERVICE_FEES = {
    'ecommerce': {
        'transaction_processing': {
            'starter': 2.9,  # percentage
            'professional': 2.4,
            'enterprise': 1.9
        },
        'listing_fees': {
            'starter': 0.30,  # per listing
            'professional': 0.20,
            'enterprise': 0.10
        },
        'featured_listing': {
            'daily': 2.99,
            'weekly': 14.99,
            'monthly': 49.99
        },
        'promoted_products': {
            'per_click': 0.25,
            'per_impression': 0.02
        }
    },
    'education': {
        'course_sales': {
            'starter': 5.0,  # percentage
            'professional': 3.5,
            'enterprise': 2.5
        },
        'certification_fees': {
            'basic': 9.99,
            'professional': 29.99,
            'enterprise': 99.99
        },
        'live_session_hosting': {
            'per_hour': 4.99,
            'per_participant': 0.99
        }
    },
    'advertising': {
        'social_media_ads': {
            'per_click': 0.50,
            'per_impression': 0.05,
            'per_engagement': 0.25
        },
        'sponsored_content': {
            'daily': 9.99,
            'weekly': 59.99,
            'monthly': 199.99
        },
        'banner_ads': {
            'daily': 19.99,
            'weekly': 119.99,
            'monthly': 399.99
        }
    },
    'premium_features': {
        'ai_analytics': {
            'monthly': 19.99
        },
        'advanced_customization': {
            'monthly': 14.99
        },
        'priority_support': {
            'monthly': 9.99
        },
        'api_access': {
            'monthly': 29.99,
            'per_request': 0.001
        }
    }
}

@pricing_bp.route('/plans', methods=['GET'])
def get_pricing_plans():
    """Get all available pricing plans"""
    return jsonify({
        'pricing_plans': PRICING_PLANS,
        'service_fees': SERVICE_FEES,
        'currency': 'USD'
    }), 200

@pricing_bp.route('/calculate-fees', methods=['POST'])
def calculate_service_fees():
    """Calculate fees for specific services"""
    try:
        data = request.get_json()
        service_type = data.get('service_type')  # ecommerce, education, advertising
        action = data.get('action')  # transaction, listing, course_sale, etc.
        plan_tier = data.get('plan_tier', 'starter')  # starter, professional, enterprise
        amount = data.get('amount', 0)  # transaction amount, course price, etc.
        quantity = data.get('quantity', 1)  # number of listings, participants, etc.
        
        if not service_type or not action:
            return jsonify({'error': 'Service type and action are required'}), 400
        
        fees = calculate_fees(service_type, action, plan_tier, amount, quantity)
        
        return jsonify({
            'service_type': service_type,
            'action': action,
            'plan_tier': plan_tier,
            'amount': amount,
            'quantity': quantity,
            'fees': fees
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Fee calculation failed', 'details': str(e)}), 500

@pricing_bp.route('/subscription/create', methods=['POST'])
def create_subscription():
    """Create a new subscription for a user"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        plan_name = data.get('plan_name')
        billing_cycle = data.get('billing_cycle', 'monthly')  # monthly, yearly
        
        if not all([user_id, plan_name]):
            return jsonify({'error': 'User ID and plan name are required'}), 400
        
        if plan_name not in PRICING_PLANS:
            return jsonify({'error': 'Invalid plan name'}), 400
        
        plan = PRICING_PLANS[plan_name]
        
        # Calculate pricing based on billing cycle
        if billing_cycle == 'yearly':
            monthly_fee = plan['monthly_fee']
            yearly_fee = monthly_fee * 12 * 0.8  # 20% discount for yearly
            total_amount = yearly_fee
        else:
            total_amount = plan['monthly_fee']
        
        subscription = {
            'subscription_id': str(uuid.uuid4()),
            'user_id': user_id,
            'plan_name': plan_name,
            'plan_type': plan['type'],
            'billing_cycle': billing_cycle,
            'monthly_fee': plan['monthly_fee'],
            'total_amount': total_amount,
            'status': 'active',
            'created_at': datetime.datetime.utcnow().isoformat(),
            'next_billing_date': (datetime.datetime.utcnow() + 
                                datetime.timedelta(days=365 if billing_cycle == 'yearly' else 30)).isoformat(),
            'features': plan['features']
        }
        
        return jsonify({
            'message': 'Subscription created successfully',
            'subscription': subscription
        }), 201
        
    except Exception as e:
        return jsonify({'error': 'Subscription creation failed', 'details': str(e)}), 500

@pricing_bp.route('/usage/track', methods=['POST'])
def track_usage():
    """Track usage for billing purposes"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        service_type = data.get('service_type')
        action = data.get('action')
        amount = data.get('amount', 0)
        metadata = data.get('metadata', {})
        
        if not all([user_id, service_type, action]):
            return jsonify({'error': 'User ID, service type, and action are required'}), 400
        
        usage_record = {
            'usage_id': str(uuid.uuid4()),
            'user_id': user_id,
            'service_type': service_type,
            'action': action,
            'amount': amount,
            'metadata': metadata,
            'timestamp': datetime.datetime.utcnow().isoformat(),
            'billing_status': 'pending'
        }
        
        return jsonify({
            'message': 'Usage tracked successfully',
            'usage_record': usage_record
        }), 201
        
    except Exception as e:
        return jsonify({'error': 'Usage tracking failed', 'details': str(e)}), 500

@pricing_bp.route('/invoice/generate', methods=['POST'])
def generate_invoice():
    """Generate invoice for usage and subscription fees"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        billing_period_start = data.get('billing_period_start')
        billing_period_end = data.get('billing_period_end')
        
        if not all([user_id, billing_period_start, billing_period_end]):
            return jsonify({'error': 'User ID and billing period are required'}), 400
        
        # Mock invoice generation
        invoice = {
            'invoice_id': str(uuid.uuid4()),
            'user_id': user_id,
            'billing_period': {
                'start': billing_period_start,
                'end': billing_period_end
            },
            'line_items': [
                {
                    'description': 'Business Professional Plan',
                    'quantity': 1,
                    'unit_price': 79.99,
                    'total': 79.99
                },
                {
                    'description': 'E-commerce Transaction Fees',
                    'quantity': 45,
                    'unit_price': 1.20,
                    'total': 54.00
                },
                {
                    'description': 'Course Sales Commission',
                    'quantity': 12,
                    'unit_price': 8.75,
                    'total': 105.00
                }
            ],
            'subtotal': 238.99,
            'tax': 23.90,
            'total': 262.89,
            'currency': 'USD',
            'status': 'pending',
            'due_date': (datetime.datetime.utcnow() + datetime.timedelta(days=30)).isoformat(),
            'generated_at': datetime.datetime.utcnow().isoformat()
        }
        
        return jsonify({
            'message': 'Invoice generated successfully',
            'invoice': invoice
        }), 201
        
    except Exception as e:
        return jsonify({'error': 'Invoice generation failed', 'details': str(e)}), 500

@pricing_bp.route('/compare-plans', methods=['GET'])
def compare_plans():
    """Get plan comparison data"""
    comparison = {
        'features': [
            'Monthly Fee',
            'Social Media Posts',
            'Can Sell Products',
            'E-commerce Transaction Fee',
            'Can Create Courses',
            'Course Sales Fee',
            'Analytics',
            'AI Insights',
            'Storage',
            'Support Level'
        ],
        'plans': {}
    }
    
    for plan_name, plan_data in PRICING_PLANS.items():
        features = plan_data['features']
        comparison['plans'][plan_name] = {
            'name': plan_data['name'],
            'monthly_fee': f"${plan_data['monthly_fee']}" if plan_data['monthly_fee'] > 0 else 'Free',
            'social_posts': features['social_media']['posts_per_month'],
            'can_sell': features['ecommerce']['can_sell'],
            'transaction_fee': f"{features['ecommerce']['transaction_fee']}%" if features['ecommerce']['transaction_fee'] > 0 else 'N/A',
            'can_create_courses': features['education']['can_create_courses'],
            'course_fee': f"{features['education']['course_fee']}%" if features['education']['course_fee'] > 0 else 'N/A',
            'analytics': features.get('analytics', 'none'),
            'ai_insights': features.get('ai_insights', False),
            'storage': features['storage'],
            'support': features['support']
        }
    
    return jsonify(comparison), 200

def calculate_fees(service_type, action, plan_tier, amount, quantity):
    """Calculate fees based on service type and plan tier"""
    fees = {
        'base_fee': 0,
        'percentage_fee': 0,
        'total_fee': 0,
        'breakdown': []
    }
    
    if service_type == 'ecommerce':
        if action == 'transaction':
            percentage = SERVICE_FEES['ecommerce']['transaction_processing'][plan_tier]
            percentage_fee = (amount * percentage) / 100
            fees['percentage_fee'] = percentage_fee
            fees['total_fee'] = percentage_fee
            fees['breakdown'].append(f"Transaction fee: {percentage}% of ${amount}")
            
        elif action == 'listing':
            base_fee = SERVICE_FEES['ecommerce']['listing_fees'][plan_tier] * quantity
            fees['base_fee'] = base_fee
            fees['total_fee'] = base_fee
            fees['breakdown'].append(f"Listing fee: ${SERVICE_FEES['ecommerce']['listing_fees'][plan_tier]} x {quantity}")
    
    elif service_type == 'education':
        if action == 'course_sale':
            percentage = SERVICE_FEES['education']['course_sales'][plan_tier]
            percentage_fee = (amount * percentage) / 100
            fees['percentage_fee'] = percentage_fee
            fees['total_fee'] = percentage_fee
            fees['breakdown'].append(f"Course sales fee: {percentage}% of ${amount}")
    
    elif service_type == 'advertising':
        if action == 'social_media_ad':
            base_fee = SERVICE_FEES['advertising']['social_media_ads']['per_click'] * quantity
            fees['base_fee'] = base_fee
            fees['total_fee'] = base_fee
            fees['breakdown'].append(f"Ad clicks: ${SERVICE_FEES['advertising']['social_media_ads']['per_click']} x {quantity}")
    
    return fees


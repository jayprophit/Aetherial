"""
Auto Investment Routes for Unified Platform
RESTful API endpoints for automatic investment opportunities
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging
from decimal import Decimal
from datetime import datetime
from ..services.auto_investment_service import AutoInvestmentService

logger = logging.getLogger(__name__)

# Create blueprint
auto_investment_bp = Blueprint('auto_investment', __name__)

# Initialize service
auto_investment_service = AutoInvestmentService()

@auto_investment_bp.route('/register', methods=['POST'])
@jwt_required()
def register_user():
    """Register user for automatic investment opportunities"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json() or {}
        
        # Extract settings
        settings = {
            'max_daily_investment': Decimal(str(data.get('max_daily_investment', 1000))),
            'max_monthly_investment': Decimal(str(data.get('max_monthly_investment', 10000))),
            'risk_tolerance': data.get('risk_tolerance', 'medium'),
            'preferred_currencies': data.get('preferred_currencies', ['ubc', 'qtoken']),
            'diversification_ratio': data.get('diversification_ratio', 0.2),
            'auto_reinvest': data.get('auto_reinvest', True),
            'stop_loss_percentage': data.get('stop_loss_percentage', 0.15),
            'take_profit_percentage': data.get('take_profit_percentage', 0.5)
        }
        
        result = auto_investment_service.register_user_for_auto_investment(user_id, settings)
        
        return jsonify({
            'success': True,
            'data': result,
            'message': 'User registered for auto investment successfully'
        }), 200
        
    except Exception as e:
        logger.error(f"Register user error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to register user for auto investment'
        }), 400

@auto_investment_bp.route('/portfolio', methods=['GET'])
@jwt_required()
def get_portfolio():
    """Get user's investment portfolio"""
    try:
        user_id = get_jwt_identity()
        
        portfolio = auto_investment_service.get_user_portfolio(user_id)
        
        if 'error' in portfolio:
            return jsonify({
                'success': False,
                'error': portfolio['error'],
                'message': 'Failed to get portfolio'
            }), 404
        
        return jsonify({
            'success': True,
            'data': portfolio,
            'message': 'Portfolio retrieved successfully'
        }), 200
        
    except Exception as e:
        logger.error(f"Get portfolio error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to get portfolio'
        }), 500

@auto_investment_bp.route('/opportunities', methods=['GET'])
@jwt_required()
def get_opportunities():
    """Get active investment opportunities"""
    try:
        opportunities = auto_investment_service.get_active_opportunities()
        
        return jsonify({
            'success': True,
            'data': opportunities,
            'count': len(opportunities),
            'message': 'Opportunities retrieved successfully'
        }), 200
        
    except Exception as e:
        logger.error(f"Get opportunities error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to get opportunities'
        }), 500

@auto_investment_bp.route('/opportunities/<opportunity_id>', methods=['GET'])
@jwt_required()
def get_opportunity_details(opportunity_id):
    """Get specific opportunity details"""
    try:
        opportunity = auto_investment_service.active_opportunities.get(opportunity_id)
        
        if not opportunity:
            return jsonify({
                'success': False,
                'error': 'Opportunity not found',
                'message': 'Investment opportunity not found'
            }), 404
        
        # Format opportunity data
        formatted_opportunity = {
            'opportunity_id': opportunity['opportunity_id'],
            'type': opportunity['type'],
            'name': opportunity['name'],
            'description': opportunity['description'],
            'min_investment': str(opportunity['min_investment']),
            'max_investment': str(opportunity['max_investment']),
            'target_raise': str(opportunity['target_raise']),
            'current_raise': str(opportunity['current_raise']),
            'funding_percentage': float(
                (opportunity['current_raise'] / opportunity['target_raise']) * 100
            ),
            'expected_return': opportunity['expected_return'],
            'risk_level': opportunity['risk_level'],
            'duration_days': opportunity['duration_days'],
            'days_remaining': (opportunity['end_date'] - datetime.utcnow()).days,
            'participants_count': len(opportunity['participants']),
            'accepted_currencies': opportunity['accepted_currencies'],
            'auto_entry': opportunity['auto_entry'],
            'requirements': opportunity['requirements'],
            'start_date': opportunity['start_date'].isoformat(),
            'end_date': opportunity['end_date'].isoformat(),
            'status': opportunity['status']
        }
        
        return jsonify({
            'success': True,
            'data': formatted_opportunity,
            'message': 'Opportunity details retrieved successfully'
        }), 200
        
    except Exception as e:
        logger.error(f"Get opportunity details error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to get opportunity details'
        }), 500

@auto_investment_bp.route('/opportunities/<opportunity_id>/enter', methods=['POST'])
@jwt_required()
def manual_enter_opportunity(opportunity_id):
    """Manually enter an investment opportunity"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json() or {}
        
        # Get investment amount
        amount = data.get('amount')
        if not amount:
            return jsonify({
                'success': False,
                'error': 'Investment amount required',
                'message': 'Please specify investment amount'
            }), 400
        
        # Manual entry logic would go here
        # For now, use the auto-entry system
        result = auto_investment_service._auto_enter_opportunity(user_id, opportunity_id)
        
        return jsonify({
            'success': True,
            'data': result,
            'message': 'Successfully entered investment opportunity'
        }), 200
        
    except Exception as e:
        logger.error(f"Manual enter opportunity error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to enter investment opportunity'
        }), 400

@auto_investment_bp.route('/investments', methods=['GET'])
@jwt_required()
def get_user_investments():
    """Get user's investment history"""
    try:
        user_id = get_jwt_identity()
        
        # Get query parameters
        status = request.args.get('status')  # pending, active, completed, failed
        limit = int(request.args.get('limit', 50))
        offset = int(request.args.get('offset', 0))
        
        user_investments = auto_investment_service.user_investments.get(user_id, {})
        investments_list = list(user_investments.values())
        
        # Filter by status if specified
        if status:
            investments_list = [inv for inv in investments_list if inv['status'] == status]
        
        # Sort by entry date (newest first)
        investments_list.sort(key=lambda x: x['entry_date'], reverse=True)
        
        # Apply pagination
        total_count = len(investments_list)
        paginated_investments = investments_list[offset:offset + limit]
        
        # Format investments
        formatted_investments = []
        for investment in paginated_investments:
            current_returns = auto_investment_service._calculate_investment_returns(investment)
            
            formatted_investments.append({
                'investment_id': investment['investment_id'],
                'opportunity_id': investment['opportunity_id'],
                'opportunity_type': investment['opportunity_type'],
                'amount': str(investment['amount']),
                'currency': investment['currency'],
                'status': investment['status'],
                'expected_return': investment['expected_return'],
                'current_returns': str(current_returns),
                'return_percentage': float((current_returns / investment['amount']) * 100),
                'entry_date': investment['entry_date'].isoformat(),
                'auto_entered': investment.get('auto_entered', False),
                'risk_level': investment['risk_level']
            })
        
        return jsonify({
            'success': True,
            'data': formatted_investments,
            'pagination': {
                'total_count': total_count,
                'limit': limit,
                'offset': offset,
                'has_more': offset + limit < total_count
            },
            'message': 'Investments retrieved successfully'
        }), 200
        
    except Exception as e:
        logger.error(f"Get user investments error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to get investments'
        }), 500

@auto_investment_bp.route('/settings', methods=['GET'])
@jwt_required()
def get_settings():
    """Get user's auto investment settings"""
    try:
        user_id = get_jwt_identity()
        
        user_portfolio = auto_investment_service.user_portfolios.get(user_id)
        if not user_portfolio:
            return jsonify({
                'success': False,
                'error': 'User not registered',
                'message': 'User not registered for auto investment'
            }), 404
        
        settings = user_portfolio.get('settings', auto_investment_service.auto_investment_settings)
        
        # Format settings for response
        formatted_settings = {
            'enabled': settings['enabled'],
            'max_daily_investment': str(settings['max_daily_investment']),
            'max_monthly_investment': str(settings['max_monthly_investment']),
            'risk_tolerance': settings['risk_tolerance'],
            'preferred_currencies': settings['preferred_currencies'],
            'diversification_ratio': settings['diversification_ratio'],
            'auto_reinvest': settings['auto_reinvest'],
            'stop_loss_percentage': settings['stop_loss_percentage'],
            'take_profit_percentage': settings['take_profit_percentage']
        }
        
        return jsonify({
            'success': True,
            'data': formatted_settings,
            'message': 'Settings retrieved successfully'
        }), 200
        
    except Exception as e:
        logger.error(f"Get settings error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to get settings'
        }), 500

@auto_investment_bp.route('/settings', methods=['PUT'])
@jwt_required()
def update_settings():
    """Update user's auto investment settings"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json() or {}
        
        user_portfolio = auto_investment_service.user_portfolios.get(user_id)
        if not user_portfolio:
            return jsonify({
                'success': False,
                'error': 'User not registered',
                'message': 'User not registered for auto investment'
            }), 404
        
        # Update settings
        current_settings = user_portfolio.get('settings', auto_investment_service.auto_investment_settings.copy())
        
        # Update only provided fields
        if 'enabled' in data:
            current_settings['enabled'] = data['enabled']
        if 'max_daily_investment' in data:
            current_settings['max_daily_investment'] = Decimal(str(data['max_daily_investment']))
        if 'max_monthly_investment' in data:
            current_settings['max_monthly_investment'] = Decimal(str(data['max_monthly_investment']))
        if 'risk_tolerance' in data:
            current_settings['risk_tolerance'] = data['risk_tolerance']
        if 'preferred_currencies' in data:
            current_settings['preferred_currencies'] = data['preferred_currencies']
        if 'diversification_ratio' in data:
            current_settings['diversification_ratio'] = data['diversification_ratio']
        if 'auto_reinvest' in data:
            current_settings['auto_reinvest'] = data['auto_reinvest']
        if 'stop_loss_percentage' in data:
            current_settings['stop_loss_percentage'] = data['stop_loss_percentage']
        if 'take_profit_percentage' in data:
            current_settings['take_profit_percentage'] = data['take_profit_percentage']
        
        # Save updated settings
        user_portfolio['settings'] = current_settings
        user_portfolio['last_updated'] = datetime.utcnow()
        
        return jsonify({
            'success': True,
            'data': {
                'enabled': current_settings['enabled'],
                'max_daily_investment': str(current_settings['max_daily_investment']),
                'max_monthly_investment': str(current_settings['max_monthly_investment']),
                'risk_tolerance': current_settings['risk_tolerance'],
                'preferred_currencies': current_settings['preferred_currencies'],
                'diversification_ratio': current_settings['diversification_ratio'],
                'auto_reinvest': current_settings['auto_reinvest'],
                'stop_loss_percentage': current_settings['stop_loss_percentage'],
                'take_profit_percentage': current_settings['take_profit_percentage']
            },
            'message': 'Settings updated successfully'
        }), 200
        
    except Exception as e:
        logger.error(f"Update settings error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to update settings'
        }), 400

@auto_investment_bp.route('/metrics', methods=['GET'])
@jwt_required()
def get_metrics():
    """Get auto investment service metrics"""
    try:
        metrics = auto_investment_service.get_service_metrics()
        
        return jsonify({
            'success': True,
            'data': metrics,
            'message': 'Metrics retrieved successfully'
        }), 200
        
    except Exception as e:
        logger.error(f"Get metrics error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to get metrics'
        }), 500

@auto_investment_bp.route('/status', methods=['GET'])
def get_status():
    """Get auto investment service status"""
    try:
        status = auto_investment_service.get_status()
        
        return jsonify({
            'success': True,
            'data': {
                'status': status,
                'timestamp': datetime.utcnow().isoformat()
            },
            'message': 'Status retrieved successfully'
        }), 200
        
    except Exception as e:
        logger.error(f"Get status error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to get status'
        }), 500

@auto_
(Content truncated due to size limit. Use line ranges to read in chunks)
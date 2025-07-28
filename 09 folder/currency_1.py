"""
Currency API Routes
Provides endpoints for currency conversion and multi-currency support
"""

from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import asyncio
from datetime import datetime, timedelta
from decimal import Decimal
import logging
import json
from typing import Dict, Any, Optional

from ..services.currency_service import CurrencyService

# Initialize currency service
currency_service = CurrencyService()

currency_bp = Blueprint('currency', __name__)

def run_async(coro):
    """Helper to run async functions in Flask routes"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()

@currency_bp.route('/api/currency/rates/<from_currency>/<to_currency>', methods=['GET'])
@cross_origin()
def get_exchange_rate(from_currency: str, to_currency: str):
    """Get exchange rate between two currencies"""
    try:
        force_refresh = request.args.get('refresh', 'false').lower() == 'true'
        
        rate = run_async(currency_service.get_exchange_rate(
            from_currency, to_currency, force_refresh
        ))
        
        if not rate:
            return jsonify({
                'error': 'Exchange rate not available',
                'from_currency': from_currency,
                'to_currency': to_currency
            }), 404
        
        return jsonify({
            'from_currency': rate.base_currency,
            'to_currency': rate.target_currency,
            'rate': str(rate.rate),
            'timestamp': rate.timestamp.isoformat(),
            'provider': rate.provider,
            'bid': str(rate.bid) if rate.bid else None,
            'ask': str(rate.ask) if rate.ask else None,
            'spread': str(rate.spread) if rate.spread else None
        })
        
    except Exception as e:
        logging.error(f"Error getting exchange rate: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@currency_bp.route('/api/currency/convert', methods=['POST'])
@cross_origin()
def convert_currency():
    """Convert amount from one currency to another"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        amount = data.get('amount')
        from_currency = data.get('from_currency')
        to_currency = data.get('to_currency')
        user_id = data.get('user_id')
        
        if not all([amount, from_currency, to_currency]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        try:
            amount_decimal = Decimal(str(amount))
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid amount format'}), 400
        
        result = run_async(currency_service.convert_amount(
            amount_decimal, from_currency, to_currency, user_id
        ))
        
        if not result:
            return jsonify({
                'error': 'Conversion not available',
                'from_currency': from_currency,
                'to_currency': to_currency
            }), 404
        
        return jsonify({
            'amount': str(result.amount),
            'from_currency': result.from_currency,
            'to_currency': result.to_currency,
            'converted_amount': str(result.converted_amount),
            'exchange_rate': str(result.exchange_rate),
            'timestamp': result.timestamp.isoformat(),
            'provider': result.provider,
            'fees': str(result.fees) if result.fees else None
        })
        
    except Exception as e:
        logging.error(f"Error converting currency: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@currency_bp.route('/api/currency/supported', methods=['GET'])
@cross_origin()
def get_supported_currencies():
    """Get list of supported currencies"""
    try:
        include_crypto = request.args.get('include_crypto', 'true').lower() == 'true'
        
        currencies = run_async(currency_service.get_supported_currencies(include_crypto))
        
        currency_list = []
        for currency in currencies:
            currency_list.append({
                'code': currency.code,
                'name': currency.name,
                'symbol': currency.symbol,
                'decimal_places': currency.decimal_places,
                'is_crypto': currency.is_crypto,
                'country_codes': currency.country_codes
            })
        
        return jsonify({
            'currencies': currency_list,
            'total': len(currency_list)
        })
        
    except Exception as e:
        logging.error(f"Error getting supported currencies: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@currency_bp.route('/api/currency/popular', methods=['GET'])
@cross_origin()
def get_popular_currencies():
    """Get list of popular currencies"""
    try:
        popular = run_async(currency_service.get_popular_currencies())
        
        return jsonify({
            'currencies': popular
        })
        
    except Exception as e:
        logging.error(f"Error getting popular currencies: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@currency_bp.route('/api/currency/by-country/<country_code>', methods=['GET'])
@cross_origin()
def get_currency_by_country(country_code: str):
    """Get currency for a specific country"""
    try:
        currency = run_async(currency_service.get_currency_by_country(country_code))
        
        if not currency:
            return jsonify({
                'error': 'Currency not found for country',
                'country_code': country_code
            }), 404
        
        return jsonify({
            'code': currency.code,
            'name': currency.name,
            'symbol': currency.symbol,
            'decimal_places': currency.decimal_places,
            'country_codes': currency.country_codes
        })
        
    except Exception as e:
        logging.error(f"Error getting currency by country: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@currency_bp.route('/api/currency/format', methods=['POST'])
@cross_origin()
def format_amount():
    """Format amount with currency symbol/code"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        amount = data.get('amount')
        currency_code = data.get('currency_code')
        format_type = data.get('format_type', 'symbol')
        
        if not all([amount, currency_code]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        try:
            amount_decimal = Decimal(str(amount))
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid amount format'}), 400
        
        formatted = run_async(currency_service.format_amount(
            amount_decimal, currency_code, format_type
        ))
        
        return jsonify({
            'formatted_amount': formatted,
            'amount': str(amount_decimal),
            'currency_code': currency_code,
            'format_type': format_type
        })
        
    except Exception as e:
        logging.error(f"Error formatting amount: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@currency_bp.route('/api/currency/historical/<from_currency>/<to_currency>', methods=['GET'])
@cross_origin()
def get_historical_rates(from_currency: str, to_currency: str):
    """Get historical exchange rates"""
    try:
        days = int(request.args.get('days', 30))
        
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        rates = run_async(currency_service.get_historical_rates(
            from_currency, to_currency, start_date, end_date
        ))
        
        rate_data = []
        for rate in rates:
            rate_data.append({
                'rate': str(rate.rate),
                'timestamp': rate.timestamp.isoformat(),
                'provider': rate.provider,
                'bid': str(rate.bid) if rate.bid else None,
                'ask': str(rate.ask) if rate.ask else None
            })
        
        return jsonify({
            'from_currency': from_currency,
            'to_currency': to_currency,
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
            'rates': rate_data,
            'total_points': len(rate_data)
        })
        
    except Exception as e:
        logging.error(f"Error getting historical rates: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@currency_bp.route('/api/currency/trends/<from_currency>/<to_currency>', methods=['GET'])
@cross_origin()
def get_rate_trends(from_currency: str, to_currency: str):
    """Get rate trends and statistics"""
    try:
        days = int(request.args.get('days', 30))
        
        trends = run_async(currency_service.get_rate_trends(
            from_currency, to_currency, days
        ))
        
        if not trends:
            return jsonify({
                'error': 'Trend data not available',
                'from_currency': from_currency,
                'to_currency': to_currency
            }), 404
        
        return jsonify({
            'from_currency': from_currency,
            'to_currency': to_currency,
            'period_days': days,
            'current_rate': trends.get('current_rate'),
            'min_rate': trends.get('min_rate'),
            'max_rate': trends.get('max_rate'),
            'avg_rate': trends.get('avg_rate'),
            'change_percent': trends.get('change_percent'),
            'volatility': trends.get('volatility'),
            'data_points': trends.get('data_points')
        })
        
    except Exception as e:
        logging.error(f"Error getting rate trends: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@currency_bp.route('/api/currency/user/preferences', methods=['GET', 'POST'])
@cross_origin()
def user_currency_preferences():
    """Get or set user currency preferences"""
    try:
        user_id = request.headers.get('X-User-ID') or request.args.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'User ID required'}), 400
        
        if request.method == 'GET':
            preferences = run_async(currency_service.get_user_currency_preference(user_id))
            
            if not preferences:
                return jsonify({
                    'user_id': user_id,
                    'preferences': None,
                    'default_currency': 'USD'
                })
            
            return jsonify({
                'user_id': user_id,
                'preferences': preferences
            })
        
        elif request.method == 'POST':
            data = request.get_json()
            
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            currency_code = data.get('currency_code')
            display_format = data.get('display_format', 'symbol')
            auto_detect = data.get('auto_detect_location', True)
            
            if not currency_code:
                return jsonify({'error': 'Currency code required'}), 400
            
            run_async(currency_service.set_user_currency_preference(
                user_id, currency_code, display_format, auto_detect
            ))
            
            return jsonify({
                'message': 'Preferences updated successfully',
                'user_id': user_id,
                'currency_code': currency_code,
                'display_format': display_format,
                'auto_detect_location': auto_detect
            })
        
    except Exception as e:
        logging.error(f"Error handling user preferences: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@currency_bp.route('/api/currency/user/history', methods=['GET'])
@cross_origin()
def get_conversion_history():
    """Get user's conversion history"""
    try:
        user_id = request.headers.get('X-User-ID') or request.args.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'User ID required'}), 400
        
        limit = int(request.args.get('limit', 50))
        
        history = run_async(currency_service.get_conversion_history(user_id, limit))
        
        history_data = []
        for conversion in history:
            history_data.append({
                'amount': str(conversion.amount),
                'from_currency': conversion.from_currency,
                'to_currency': conversion.to_currency,
                'converted_amount': str(conversion.converted_amount),
                'exchange_rate': str(conversion.exchange_rate),
                'timestamp': conversion.timestamp.isoformat(),
                'provider': conversion.provider
            })
        
        return jsonify({
            'user_id': user_id,
            'history': history_data,
            'total': len(history_data)
        })
        
    except Exception as e:
        logging.error(f"Error getting conversion history: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@currency_bp.route('/api/currency/bulk-convert', methods=['POST'])
@cross_origin()
def bulk_convert():
    """Convert multiple amounts/currencies at once"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        conversions = data.get('conversions', [])
        user_id = data.get('user_id')
        
        if not conversions:
            return jsonify({'error': 'No conversions provided'}), 400
        
        results = []
        
        for conversion in conversions:
            amount = conversion.get('amount')
            from_currency = conversion.get('from_currency')
            to_currency = conversion.get('to_currency')
            
            if not all([amount, from_currency, to_currency]):
                results.append({
                    'error': 'Missing required fields',
                    'conversion': conversion
                })
                continue
            
            try:
                amount_decimal = Decimal(str(amount))
                result = run_async(currency_service.convert_amount(
                    amount_decimal, from_currency, to_currency, user_id
                ))
                
                if result:
                    results.append({
                        'amount': str(result.amount),
                        'from_currency': result.from_currency,
                        'to_currency': result.to_currency,
                        'converted_amount': str(result.converted_amount),
                        'exchange_rate': str(result.exchange_rate),
                        'timestamp': result.timestamp.isoformat(),
                        'provider': result.provider
                    })
                else:
                    results.append({
                        'error': 'Conversion not available',
                        'conversion': conversion
                    })
                    
            except (ValueError, TypeError):
                results.append({
                    'error': 'Invalid amount format',
                    'conversion': conversion
                })
        
        return jsonify({
            'results': results,
            'total_conversions': len(conversions),
            'successful_conversions': len([r for r in results if 'error' not in r])
        })
        
    except Exception as e:
        logging.error(f"Error in bulk conversion: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@currency_bp.
(Content truncated due to size limit. Use line ranges to read in chunks)
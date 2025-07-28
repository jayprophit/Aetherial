"""
Banking routes for Unified Platform
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import uuid
import random
from datetime import datetime, timedelta

banking_bp = Blueprint('banking', __name__)

# In-memory storage for demo
bank_accounts = {}
bank_transactions = {}
loans = {}
credit_cards = {}
investment_accounts = {}

account_types = {
    'checking': {'name': 'Checking Account', 'min_balance': 0, 'interest_rate': 0.01},
    'savings': {'name': 'Savings Account', 'min_balance': 100, 'interest_rate': 0.045},
    'business': {'name': 'Business Account', 'min_balance': 500, 'interest_rate': 0.02},
    'investment': {'name': 'Investment Account', 'min_balance': 1000, 'interest_rate': 0.06},
    'cd': {'name': 'Certificate of Deposit', 'min_balance': 1000, 'interest_rate': 0.0575},
    'money_market': {'name': 'Money Market Account', 'min_balance': 2500, 'interest_rate': 0.0475}
}

loan_types = {
    'personal': {'name': 'Personal Loan', 'min_amount': 1000, 'max_amount': 50000, 'interest_rate': 0.0699},
    'auto': {'name': 'Auto Loan', 'min_amount': 5000, 'max_amount': 100000, 'interest_rate': 0.0399},
    'mortgage': {'name': 'Mortgage', 'min_amount': 50000, 'max_amount': 2000000, 'interest_rate': 0.0625},
    'business': {'name': 'Business Loan', 'min_amount': 10000, 'max_amount': 500000, 'interest_rate': 0.0549},
    'student': {'name': 'Student Loan', 'min_amount': 1000, 'max_amount': 200000, 'interest_rate': 0.0449}
}

@banking_bp.route('/accounts/create', methods=['POST'])
@jwt_required()
def create_account():
    """Create a new bank account"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        required_fields = ['account_type']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400
        
        account_type = data['account_type']
        
        if account_type not in account_types:
            return jsonify({'success': False, 'error': 'Invalid account type'}), 400
        
        account_info = account_types[account_type]
        account_id = str(uuid.uuid4())
        
        # Generate account number
        account_number = f"UP{random.randint(100000000, 999999999)}"
        routing_number = "123456789"
        
        account = {
            'id': account_id,
            'user_id': user_id,
            'account_number': account_number,
            'routing_number': routing_number,
            'account_type': account_type,
            'account_name': account_info['name'],
            'balance': data.get('initial_deposit', account_info['min_balance']),
            'available_balance': data.get('initial_deposit', account_info['min_balance']),
            'interest_rate': account_info['interest_rate'],
            'min_balance': account_info['min_balance'],
            'status': 'active',
            'opened_date': datetime.utcnow().isoformat(),
            'last_activity': datetime.utcnow().isoformat(),
            'overdraft_protection': data.get('overdraft_protection', False),
            'overdraft_limit': data.get('overdraft_limit', 0),
            'monthly_fee': 0,
            'transaction_limit': data.get('transaction_limit', 1000),
            'metadata': {
                'nickname': data.get('nickname', f'My {account_info["name"]}'),
                'description': data.get('description', ''),
                'alerts_enabled': True
            }
        }
        
        bank_accounts[account_id] = account
        
        return jsonify({
            'success': True,
            'account': {
                'id': account_id,
                'account_number': account_number,
                'routing_number': routing_number,
                'account_type': account_type,
                'account_name': account_info['name'],
                'balance': account['balance'],
                'interest_rate': account['interest_rate'],
                'opened_date': account['opened_date'],
                'metadata': account['metadata']
            }
        }), 201
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@banking_bp.route('/accounts', methods=['GET'])
@jwt_required()
def get_accounts():
    """Get user's bank accounts"""
    try:
        user_id = get_jwt_identity()
        
        user_accounts = []
        total_balance = 0
        
        for account_id, account in bank_accounts.items():
            if account['user_id'] == user_id and account['status'] == 'active':
                user_accounts.append({
                    'id': account_id,
                    'account_number': account['account_number'],
                    'account_type': account['account_type'],
                    'account_name': account['account_name'],
                    'balance': account['balance'],
                    'available_balance': account['available_balance'],
                    'interest_rate': account['interest_rate'],
                    'last_activity': account['last_activity'],
                    'metadata': account['metadata']
                })
                total_balance += account['balance']
        
        return jsonify({
            'success': True,
            'accounts': user_accounts,
            'total_accounts': len(user_accounts),
            'total_balance': round(total_balance, 2)
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@banking_bp.route('/transfer', methods=['POST'])
@jwt_required()
def transfer_funds():
    """Transfer funds between accounts"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        required_fields = ['from_account', 'to_account', 'amount']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400
        
        from_account_id = data['from_account']
        to_account_id = data['to_account']
        amount = float(data['amount'])
        memo = data.get('memo', '')
        
        # Validate accounts
        if from_account_id not in bank_accounts or to_account_id not in bank_accounts:
            return jsonify({'success': False, 'error': 'Account not found'}), 404
        
        from_account = bank_accounts[from_account_id]
        to_account = bank_accounts[to_account_id]
        
        # Check ownership of from_account
        if from_account['user_id'] != user_id:
            return jsonify({'success': False, 'error': 'Unauthorized account access'}), 403
        
        # Check balance
        if from_account['available_balance'] < amount:
            # Check overdraft protection
            if from_account['overdraft_protection'] and (from_account['available_balance'] + from_account['overdraft_limit']) >= amount:
                overdraft_used = amount - from_account['available_balance']
            else:
                return jsonify({'success': False, 'error': 'Insufficient funds'}), 400
        
        # Create transaction
        transaction_id = str(uuid.uuid4())
        transaction = {
            'id': transaction_id,
            'from_account': from_account_id,
            'to_account': to_account_id,
            'amount': amount,
            'type': 'transfer',
            'status': 'completed',
            'timestamp': datetime.utcnow().isoformat(),
            'memo': memo,
            'fee': 0,
            'reference_number': f"TXN{random.randint(100000, 999999)}"
        }
        
        # Update balances
        from_account['balance'] -= amount
        from_account['available_balance'] -= amount
        from_account['last_activity'] = datetime.utcnow().isoformat()
        
        to_account['balance'] += amount
        to_account['available_balance'] += amount
        to_account['last_activity'] = datetime.utcnow().isoformat()
        
        bank_transactions[transaction_id] = transaction
        
        return jsonify({
            'success': True,
            'transaction': transaction,
            'from_account_balance': from_account['balance'],
            'to_account_balance': to_account['balance']
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@banking_bp.route('/transactions', methods=['GET'])
@jwt_required()
def get_transactions():
    """Get user's transaction history"""
    try:
        user_id = get_jwt_identity()
        
        # Get user's account IDs
        user_account_ids = [
            account_id for account_id, account in bank_accounts.items()
            if account['user_id'] == user_id
        ]
        
        # Filter transactions
        user_transactions = []
        for transaction in bank_transactions.values():
            if (transaction['from_account'] in user_account_ids or 
                transaction['to_account'] in user_account_ids):
                user_transactions.append(transaction)
        
        # Sort by timestamp (newest first)
        user_transactions.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return jsonify({
            'success': True,
            'transactions': user_transactions,
            'total_count': len(user_transactions)
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@banking_bp.route('/loans/apply', methods=['POST'])
@jwt_required()
def apply_for_loan():
    """Apply for a loan"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        required_fields = ['loan_type', 'amount', 'purpose', 'annual_income']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400
        
        loan_type = data['loan_type']
        amount = float(data['amount'])
        purpose = data['purpose']
        annual_income = float(data['annual_income'])
        
        if loan_type not in loan_types:
            return jsonify({'success': False, 'error': 'Invalid loan type'}), 400
        
        loan_info = loan_types[loan_type]
        
        # Validate amount
        if amount < loan_info['min_amount'] or amount > loan_info['max_amount']:
            return jsonify({
                'success': False, 
                'error': f'Loan amount must be between ${loan_info["min_amount"]} and ${loan_info["max_amount"]}'
            }), 400
        
        # Simple credit check (in reality, this would be more complex)
        credit_score = random.randint(600, 850)
        debt_to_income = random.uniform(0.1, 0.4)
        
        # Determine approval
        if credit_score >= 650 and debt_to_income <= 0.35 and annual_income >= amount * 0.2:
            status = 'approved'
            interest_rate = loan_info['interest_rate']
        elif credit_score >= 600:
            status = 'conditional'
            interest_rate = loan_info['interest_rate'] + 0.02
        else:
            status = 'denied'
            interest_rate = None
        
        loan_id = str(uuid.uuid4())
        loan_application = {
            'id': loan_id,
            'user_id': user_id,
            'loan_type': loan_type,
            'loan_name': loan_info['name'],
            'amount': amount,
            'purpose': purpose,
            'annual_income': annual_income,
            'interest_rate': interest_rate,
            'term_months': data.get('term_months', 60),
            'status': status,
            'applied_date': datetime.utcnow().isoformat(),
            'credit_score': credit_score,
            'debt_to_income_ratio': round(debt_to_income, 3),
            'monthly_payment': None,
            'total_interest': None,
            'conditions': []
        }
        
        if status in ['approved', 'conditional']:
            # Calculate monthly payment
            monthly_rate = interest_rate / 12
            term_months = loan_application['term_months']
            monthly_payment = amount * (monthly_rate * (1 + monthly_rate)**term_months) / ((1 + monthly_rate)**term_months - 1)
            total_interest = (monthly_payment * term_months) - amount
            
            loan_application['monthly_payment'] = round(monthly_payment, 2)
            loan_application['total_interest'] = round(total_interest, 2)
            
            if status == 'conditional':
                loan_application['conditions'] = [
                    'Provide additional income verification',
                    'Reduce debt-to-income ratio below 30%'
                ]
        
        loans[loan_id] = loan_application
        
        return jsonify({
            'success': True,
            'loan_application': loan_application
        }), 201
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@banking_bp.route('/loans', methods=['GET'])
@jwt_required()
def get_loans():
    """Get user's loans"""
    try:
        user_id = get_jwt_identity()
        
        user_loans = []
        for loan in loans.values():
            if loan['user_id'] == user_id:
                user_loans.append(loan)
        
        # Sort by application date (newest first)
        user_loans.sort(key=lambda x: x['applied_date'], reverse=True)
        
        return jsonify({
            'success': True,
            'loans': user_loans,
            'total_count': len(user_loans),
            'approved_loans': len([l for l in user_loans if l['status'] == 'approved']),
            'total_loan_amount': sum(l['amount'] for l in user_loans if l['status'] == 'approved')
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@banking_bp.route('/cards/issue', methods=['POST'])
@jwt_required()
def issue_card():
    """Issue a debit or credit card"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        required_fields = ['card_type', 'account_id']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400
        
        card_type = data['card_type']  # debit, credit
        account_id = data['account_id']
        
        # Validate account
        if account_id not in bank_accounts:
            return jsonify({'success': False, 'error': 'Account not found'}), 404
        
        account = bank_accounts[account_id]
        if account['user_id'] != user_id:
            return jsonify({'success': False, 'error': 'Unauthorized account access'}), 403
        
        card_id = str(uuid.uuid4())
        
        # Generate card number (simplified)
        card_number = f"4{random.randint(100000000000000, 999999999999999)}"
        cvv = f"{random.randint(100, 999)}"
        expiry_date = (datetime.utcnow() + timedelta(days=1460)).strftime('%m/%y')  # 4 years
        
        card = {
            'id': card_id,
            'user_id': user_id,
            'account_id': account_id,
            'card_number': card_number,
            'card_number_masked': f"****-****-****-{card_number[-4:]}",
            'cvv': cvv,
            'expiry_date': expiry_date,
            'card_type': card_type,
            'status': 'active',
            'issued_date': datetime.utcnow().isoformat(),
            'daily_limit': data.get('daily_limit', 1000),
            'monthly_limit': data.get('monthly_limit', 10000),
            'international_enabled': data.get('international_enabled', False),
            'contactless_enabled': data.get('contactless_enabled', True),
            'pin_set': False,
            'metadata': {
                'nickname': data.get('nickname', f'{card_type.title()} Card'),
                'design': data.get('design', 'classic')
            }
        }
        
        if card_type == 'credit':
            # Add credit-specific fields
            credit_limit = min(data.get('credit_limit', 5000), account['balance'] * 10)
            card.update({
                'credit_limit': credit_limit,
                'available_credit': credit_limit,
                'interest_rate': 0.1899,  # 18.99% APR
                'minimum_payment': 0,
                'statement_balance': 0,
                'payment_due_date': None
            })
        
        credit_cards[card_id] = card
        
        return jsonify({
            'success': True,
            'card': {
                'id': card_id,
                'card_number_masked': card['card_number_masked'],
                'card_type': card_type,
                'expiry_date': expiry_date,
                'status': 'active',
                'daily_limit': card['daily_limit'],
                'monthly_limit': card['monthly_limit'],
                'metadata': card['metadata']
            }
        }), 201
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@banking_bp.route('/cards', methods=['GET'])
@jwt_required()
def get_cards():
    """Get user's cards"""
    try:
        user_id = get_jwt_identity()
        
        user_cards = []
        for card in credit_cards.values():
            if card['user_id'] == user_id:
                card_info = {
                    'id': card['id'],
                    'card_number_masked': card['card_number_masked'],
                    'card_type': card['card_type'],
                    'expiry_date': card['expiry_date'],
                    'status': card['status'],
                    'daily_limit': card['daily_limit'],
                    'monthly_limit': card['monthly_limit'],
                    'international_enabled': card['international_enabled'],
                    'contactless_enabled': card['contactless_enabled'],
                    'metadata': card['metadata']
                }
                
                if card['card_type'] == 'credit':
                    card_info.update({
                        'credit_limit': card['credit_limit'],
                        'available_credit': card['available_credit'],
                        'statement_balance': card['statement_balance']
                    })
                
                user_cards.append(card_info)
        
        return jsonify({
            'success': True,
            'cards': user_cards,
            'total_count': len(user_cards),
            'debit_cards': len([c for c in user_cards if c['card_type'] == 'debit']),
            'credit_cards': len([c for c in user_cards if c['card_type'] == 'credit'])
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@banking_bp.route('/products', methods=['GET'])
def get_banking_products():
    """Get available banking products and rates"""
    try:
        products = {
            'account_types': account_types,
            'loan_types': loan_types,
            'current_rates': {
                'prime_rate': 0.0825,
                'federal_funds_rate': 0.0525,
                'mortgage_rates': {
                    '30_year_fixed': 0.0675,
                    '15_year_fixed': 0.0625,
                    '5_1_arm': 0.0599
                },
                'cd_rates': {
                    '6_months': 0.045,
                    '1_year': 0.0525,
                    '2_years': 0.055,
                    '5_years': 0.0575
                }
            },
            'features': {
                'online_banking': True,
                'mobile_app': True,
                'atm_network': '50,000+ ATMs worldwide',
                'customer_support': '24/7',
                'fdic_insured': True,
                'international_services': True
            }
        }
        
        return jsonify({
            'success': True,
            'products': products
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@banking_bp.route('/credit-score', methods=['GET'])
@jwt_required()
def get_credit_score():
    """Get user's credit score and report"""
    try:
        user_id = get_jwt_identity()
        
        # Simulate credit score (in reality, this would come from credit bureaus)
        credit_score = random.randint(650, 850)
        
        # Determine credit rating
        if credit_score >= 800:
            rating = 'Excellent'
        elif credit_score >= 740:
            rating = 'Very Good'
        elif credit_score >= 670:
            rating = 'Good'
        elif credit_score >= 580:
            rating = 'Fair'
        else:
            rating = 'Poor'
        
        credit_report = {
            'credit_score': credit_score,
            'rating': rating,
            'last_updated': datetime.utcnow().isoformat(),
            'score_range': '300-850',
            'factors': {
                'payment_history': random.randint(80, 100),
                'credit_utilization': random.randint(70, 95),
                'length_of_credit_history': random.randint(75, 90),
                'credit_mix': random.randint(70, 85),
                'new_credit': random.randint(80, 95)
            },
            'recommendations': [
                'Keep credit utilization below 30%',
                'Make all payments on time',
                'Avoid opening too many new accounts',
                'Keep old accounts open to maintain credit history'
            ],
            'accounts': [
                {
                    'account_type': 'Credit Card',
                    'balance': random.randint(500, 5000),
                    'limit': random.randint(5000, 15000),
                    'status': 'Open',
                    'payment_history': 'On Time'
                }
            ]
        }
        
        return jsonify({
            'success': True,
            'credit_report': credit_report
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


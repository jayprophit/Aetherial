from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import sys
import os

# Add the blockchain module to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'blockchain'))

from unified_chain import get_blockchain, TransactionType, InteractionType

blockchain_bp = Blueprint('blockchain', __name__)

@blockchain_bp.route('/wallet/create', methods=['POST'])
@jwt_required()
def create_wallet():
    """Create a new blockchain wallet for the user"""
    try:
        user_id = get_jwt_identity()
        blockchain = get_blockchain()
        
        # Create blockchain account
        address = blockchain.create_account(user_id)
        
        return jsonify({
            'success': True,
            'address': address,
            'balance': blockchain.get_balance(address)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

@blockchain_bp.route('/wallet/balance/<address>', methods=['GET'])
@jwt_required()
def get_wallet_balance(address):
    """Get wallet balance"""
    try:
        blockchain = get_blockchain()
        account = blockchain.get_account(address)
        
        if not account:
            return jsonify({
                'success': False,
                'message': 'Account not found'
            }), 404
        
        return jsonify({
            'success': True,
            'balance': account.balance,
            'staked_amount': account.staked_amount,
            'reputation_score': account.reputation_score,
            'interaction_points': account.interaction_points,
            'skills_verified': account.skills_verified,
            'courses_completed': len(account.courses_completed),
            'jobs_completed': account.jobs_completed,
            'content_created': account.content_created
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

@blockchain_bp.route('/transfer', methods=['POST'])
@jwt_required()
def transfer_tokens():
    """Transfer tokens between accounts"""
    try:
        data = request.get_json()
        blockchain = get_blockchain()
        
        from_address = data.get('from_address')
        to_address = data.get('to_address')
        amount = float(data.get('amount', 0))
        transaction_type = TransactionType(data.get('transaction_type', 'transfer'))
        interaction_type = InteractionType(data.get('interaction_type', 'social'))
        metadata = data.get('metadata', {})
        
        # Validate required fields
        if not all([from_address, to_address, amount > 0]):
            return jsonify({
                'success': False,
                'message': 'Missing required fields'
            }), 400
        
        # Transfer tokens
        transaction_id = blockchain.transfer_tokens(
            from_address, to_address, amount,
            transaction_type, interaction_type, metadata
        )
        
        return jsonify({
            'success': True,
            'transaction_id': transaction_id,
            'message': 'Transfer completed successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

@blockchain_bp.route('/course/complete', methods=['POST'])
@jwt_required()
def complete_course():
    """Record course completion on blockchain"""
    try:
        data = request.get_json()
        blockchain = get_blockchain()
        user_id = get_jwt_identity()
        
        course_id = data.get('course_id')
        student_address = data.get('student_address')
        instructor_address = data.get('instructor_address', 'system_rewards')
        course_price = float(data.get('course_price', 0))
        
        if not all([course_id, student_address]):
            return jsonify({
                'success': False,
                'message': 'Missing required fields'
            }), 400
        
        # Award completion tokens to student
        completion_reward = 50.0  # Base completion reward
        metadata = {
            'course_id': course_id,
            'user_id': user_id,
            'completion_date': data.get('completion_date'),
            'grade': data.get('grade'),
            'certificate_id': data.get('certificate_id')
        }
        
        transaction_id = blockchain.transfer_tokens(
            'system_rewards', student_address, completion_reward,
            TransactionType.COURSE_COMPLETION, InteractionType.LEARNING,
            metadata
        )
        
        # If paid course, transfer payment to instructor
        if course_price > 0 and instructor_address != 'system_rewards':
            payment_id = blockchain.transfer_tokens(
                student_address, instructor_address, course_price,
                TransactionType.TRANSFER, InteractionType.LEARNING,
                {'type': 'course_payment', 'course_id': course_id}
            )
        
        return jsonify({
            'success': True,
            'transaction_id': transaction_id,
            'reward_amount': completion_reward,
            'message': 'Course completion recorded successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

@blockchain_bp.route('/job/apply', methods=['POST'])
@jwt_required()
def apply_for_job():
    """Record job application on blockchain"""
    try:
        data = request.get_json()
        blockchain = get_blockchain()
        user_id = get_jwt_identity()
        
        job_id = data.get('job_id')
        applicant_address = data.get('applicant_address')
        employer_address = data.get('employer_address', 'system_rewards')
        application_fee = float(data.get('application_fee', 5.0))
        
        if not all([job_id, applicant_address]):
            return jsonify({
                'success': False,
                'message': 'Missing required fields'
            }), 400
        
        metadata = {
            'job_id': job_id,
            'user_id': user_id,
            'application_date': data.get('application_date'),
            'cover_letter_hash': data.get('cover_letter_hash'),
            'resume_hash': data.get('resume_hash')
        }
        
        # Charge application fee
        transaction_id = blockchain.transfer_tokens(
            applicant_address, 'system_treasury', application_fee,
            TransactionType.JOB_APPLICATION, InteractionType.EMPLOYMENT,
            metadata
        )
        
        return jsonify({
            'success': True,
            'transaction_id': transaction_id,
            'application_fee': application_fee,
            'message': 'Job application recorded successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

@blockchain_bp.route('/job/complete', methods=['POST'])
@jwt_required()
def complete_job():
    """Record job completion on blockchain"""
    try:
        data = request.get_json()
        blockchain = get_blockchain()
        
        job_id = data.get('job_id')
        worker_address = data.get('worker_address')
        employer_address = data.get('employer_address')
        payment_amount = float(data.get('payment_amount', 0))
        
        if not all([job_id, worker_address, employer_address, payment_amount > 0]):
            return jsonify({
                'success': False,
                'message': 'Missing required fields'
            }), 400
        
        metadata = {
            'job_id': job_id,
            'completion_date': data.get('completion_date'),
            'rating': data.get('rating'),
            'feedback': data.get('feedback'),
            'status': 'completed'
        }
        
        # Transfer payment from employer to worker
        transaction_id = blockchain.transfer_tokens(
            employer_address, worker_address, payment_amount,
            TransactionType.JOB_APPLICATION, InteractionType.EMPLOYMENT,
            metadata
        )
        
        return jsonify({
            'success': True,
            'transaction_id': transaction_id,
            'payment_amount': payment_amount,
            'message': 'Job completion recorded successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

@blockchain_bp.route('/product/purchase', methods=['POST'])
@jwt_required()
def purchase_product():
    """Record product purchase on blockchain"""
    try:
        data = request.get_json()
        blockchain = get_blockchain()
        user_id = get_jwt_identity()
        
        product_id = data.get('product_id')
        buyer_address = data.get('buyer_address')
        seller_address = data.get('seller_address')
        purchase_amount = float(data.get('purchase_amount', 0))
        
        if not all([product_id, buyer_address, seller_address, purchase_amount > 0]):
            return jsonify({
                'success': False,
                'message': 'Missing required fields'
            }), 400
        
        metadata = {
            'product_id': product_id,
            'user_id': user_id,
            'purchase_date': data.get('purchase_date'),
            'quantity': data.get('quantity', 1),
            'shipping_address': data.get('shipping_address'),
            'order_id': data.get('order_id')
        }
        
        # Transfer payment from buyer to seller
        transaction_id = blockchain.transfer_tokens(
            buyer_address, seller_address, purchase_amount,
            TransactionType.PRODUCT_PURCHASE, InteractionType.COMMERCE,
            metadata
        )
        
        return jsonify({
            'success': True,
            'transaction_id': transaction_id,
            'purchase_amount': purchase_amount,
            'message': 'Product purchase recorded successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

@blockchain_bp.route('/content/create', methods=['POST'])
@jwt_required()
def create_content():
    """Record content creation on blockchain"""
    try:
        data = request.get_json()
        blockchain = get_blockchain()
        user_id = get_jwt_identity()
        
        content_id = data.get('content_id')
        creator_address = data.get('creator_address')
        content_type = data.get('content_type')
        
        if not all([content_id, creator_address, content_type]):
            return jsonify({
                'success': False,
                'message': 'Missing required fields'
            }), 400
        
        # Award content creation tokens
        creation_reward = 25.0  # Base creation reward
        metadata = {
            'content_id': content_id,
            'user_id': user_id,
            'content_type': content_type,
            'creation_date': data.get('creation_date'),
            'content_hash': data.get('content_hash'),
            'tags': data.get('tags', [])
        }
        
        transaction_id = blockchain.transfer_tokens(
            'system_rewards', creator_address, creation_reward,
            TransactionType.CONTENT_CREATION, InteractionType.SOCIAL,
            metadata
        )
        
        return jsonify({
            'success': True,
            'transaction_id': transaction_id,
            'reward_amount': creation_reward,
            'message': 'Content creation recorded successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

@blockchain_bp.route('/skill/verify', methods=['POST'])
@jwt_required()
def verify_skill():
    """Record skill verification on blockchain"""
    try:
        data = request.get_json()
        blockchain = get_blockchain()
        user_id = get_jwt_identity()
        
        skill_name = data.get('skill_name')
        user_address = data.get('user_address')
        verifier_address = data.get('verifier_address', 'system_rewards')
        
        if not all([skill_name, user_address]):
            return jsonify({
                'success': False,
                'message': 'Missing required fields'
            }), 400
        
        # Award skill verification tokens
        verification_reward = 100.0  # Base verification reward
        metadata = {
            'skill_name': skill_name,
            'user_id': user_id,
            'verification_date': data.get('verification_date'),
            'verification_method': data.get('verification_method'),
            'certificate_id': data.get('certificate_id'),
            'skill_level': data.get('skill_level', 'intermediate')
        }
        
        transaction_id = blockchain.transfer_tokens(
            'system_rewards', user_address, verification_reward,
            TransactionType.SKILL_VERIFICATION, InteractionType.LEARNING,
            metadata
        )
        
        return jsonify({
            'success': True,
            'transaction_id': transaction_id,
            'reward_amount': verification_reward,
            'message': 'Skill verification recorded successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

@blockchain_bp.route('/stake', methods=['POST'])
@jwt_required()
def stake_tokens():
    """Stake tokens for consensus participation"""
    try:
        data = request.get_json()
        blockchain = get_blockchain()
        
        address = data.get('address')
        amount = float(data.get('amount', 0))
        
        if not all([address, amount > 0]):
            return jsonify({
                'success': False,
                'message': 'Missing required fields'
            }), 400
        
        transaction_id = blockchain.stake_tokens(address, amount)
        
        return jsonify({
            'success': True,
            'transaction_id': transaction_id,
            'staked_amount': amount,
            'message': 'Tokens staked successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

@blockchain_bp.route('/unstake', methods=['POST'])
@jwt_required()
def unstake_tokens():
    """Unstake tokens"""
    try:
        data = request.get_json()
        blockchain = get_blockchain()
        
        address = data.get('address')
        amount = float(data.get('amount', 0))
        
        if not all([address, amount > 0]):
            return jsonify({
                'success': False,
                'message': 'Missing required fields'
            }), 400
        
        transaction_id = blockchain.unstake_tokens(address, amount)
        
        return jsonify({
            'success': True,
            'transaction_id': transaction_id,
            'unstaked_amount': amount,
            'message': 'Tokens unstaked successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

@blockchain_bp.route('/transactions/<address>', methods=['GET'])
@jwt_required()
def get_transaction_history(address):
    """Get transaction history for an address"""
    try:
        blockchain = get_blockchain()
        limit = int(request.args.get('limit', 100))
        
        transactions = blockchain.get_transaction_history(address, limit)
        
        return jsonify({
            'success': True,
            'transactions': transactions,
            'count'
(Content truncated due to size limit. Use line ranges to read in chunks)
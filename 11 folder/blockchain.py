"""
Blockchain routes for Unified Platform
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import uuid
import hashlib
import time
import random
from datetime import datetime, timedelta

blockchain_bp = Blueprint('blockchain', __name__)

# In-memory storage for demo
wallets_db = {}
transactions_db = {}
blocks_db = {}
mining_sessions = {}
staking_pools = {}
nft_collections = {}

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        block_string = f"{self.index}{self.transactions}{self.timestamp}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty):
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()

# Initialize genesis block
genesis_block = Block(0, [], time.time(), "0")
blocks_db[genesis_block.hash] = {
    'index': genesis_block.index,
    'transactions': genesis_block.transactions,
    'timestamp': genesis_block.timestamp,
    'previous_hash': genesis_block.previous_hash,
    'nonce': genesis_block.nonce,
    'hash': genesis_block.hash,
    'miner': 'system',
    'reward': 0,
    'difficulty': 4
}

@blockchain_bp.route('/wallet/create', methods=['POST'])
@jwt_required()
def create_wallet():
    """Create a new blockchain wallet"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json() or {}
        
        wallet_id = str(uuid.uuid4())
        wallet_type = data.get('type', 'standard')  # standard, multisig, hardware
        
        # Generate wallet address (simplified)
        address = f"UBC{hashlib.sha256(wallet_id.encode()).hexdigest()[:32]}"
        
        # Generate private key (in production, use proper cryptography)
        private_key = hashlib.sha256(f"{wallet_id}{time.time()}".encode()).hexdigest()
        
        wallet = {
            'id': wallet_id,
            'user_id': user_id,
            'address': address,
            'private_key': private_key,  # In production, encrypt this
            'type': wallet_type,
            'balance': {
                'UBC': 1000.0,  # Starting balance for demo
                'staked': 0.0,
                'locked': 0.0
            },
            'created_at': datetime.utcnow().isoformat(),
            'is_active': True,
            'transactions': [],
            'metadata': {
                'name': data.get('name', f'Wallet {len(wallets_db) + 1}'),
                'description': data.get('description', ''),
                'tags': data.get('tags', [])
            }
        }
        
        wallets_db[wallet_id] = wallet
        
        return jsonify({
            'success': True,
            'wallet': {
                'id': wallet_id,
                'address': address,
                'type': wallet_type,
                'balance': wallet['balance'],
                'created_at': wallet['created_at'],
                'metadata': wallet['metadata']
            }
        }), 201
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@blockchain_bp.route('/wallets', methods=['GET'])
@jwt_required()
def get_wallets():
    """Get user's wallets"""
    try:
        user_id = get_jwt_identity()
        
        user_wallets = []
        for wallet_id, wallet in wallets_db.items():
            if wallet['user_id'] == user_id and wallet['is_active']:
                user_wallets.append({
                    'id': wallet_id,
                    'address': wallet['address'],
                    'type': wallet['type'],
                    'balance': wallet['balance'],
                    'created_at': wallet['created_at'],
                    'metadata': wallet['metadata'],
                    'transaction_count': len(wallet['transactions'])
                })
        
        return jsonify({
            'success': True,
            'wallets': user_wallets,
            'total_balance': sum(w['balance']['UBC'] for w in user_wallets)
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@blockchain_bp.route('/transaction/send', methods=['POST'])
@jwt_required()
def send_transaction():
    """Send a blockchain transaction"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        required_fields = ['from_wallet', 'to_address', 'amount']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400
        
        from_wallet_id = data['from_wallet']
        to_address = data['to_address']
        amount = float(data['amount'])
        gas_price = data.get('gas_price', 0.001)
        
        # Validate wallet ownership
        if from_wallet_id not in wallets_db:
            return jsonify({'success': False, 'error': 'Wallet not found'}), 404
        
        from_wallet = wallets_db[from_wallet_id]
        if from_wallet['user_id'] != user_id:
            return jsonify({'success': False, 'error': 'Unauthorized wallet access'}), 403
        
        # Check balance
        total_cost = amount + gas_price
        if from_wallet['balance']['UBC'] < total_cost:
            return jsonify({'success': False, 'error': 'Insufficient balance'}), 400
        
        # Create transaction
        transaction_id = str(uuid.uuid4())
        transaction = {
            'id': transaction_id,
            'from_address': from_wallet['address'],
            'to_address': to_address,
            'amount': amount,
            'gas_price': gas_price,
            'status': 'pending',
            'timestamp': datetime.utcnow().isoformat(),
            'block_hash': None,
            'confirmations': 0,
            'metadata': {
                'memo': data.get('memo', ''),
                'type': data.get('type', 'transfer')
            }
        }
        
        # Update balances
        from_wallet['balance']['UBC'] -= total_cost
        from_wallet['transactions'].append(transaction_id)
        
        # Find or create destination wallet
        to_wallet = None
        for wallet_id, wallet in wallets_db.items():
            if wallet['address'] == to_address:
                to_wallet = wallet
                break
        
        if to_wallet:
            to_wallet['balance']['UBC'] += amount
            to_wallet['transactions'].append(transaction_id)
        
        transactions_db[transaction_id] = transaction
        
        # Simulate transaction processing
        transaction['status'] = 'confirmed'
        transaction['confirmations'] = 1
        
        return jsonify({
            'success': True,
            'transaction': transaction,
            'new_balance': from_wallet['balance']['UBC']
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@blockchain_bp.route('/transactions', methods=['GET'])
@jwt_required()
def get_transactions():
    """Get user's transactions"""
    try:
        user_id = get_jwt_identity()
        
        # Get user's wallet addresses
        user_addresses = []
        for wallet in wallets_db.values():
            if wallet['user_id'] == user_id:
                user_addresses.append(wallet['address'])
        
        # Filter transactions
        user_transactions = []
        for transaction in transactions_db.values():
            if (transaction['from_address'] in user_addresses or 
                transaction['to_address'] in user_addresses):
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

@blockchain_bp.route('/mining/start', methods=['POST'])
@jwt_required()
def start_mining():
    """Start mining operation"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json() or {}
        
        wallet_id = data.get('wallet_id')
        if not wallet_id or wallet_id not in wallets_db:
            return jsonify({'success': False, 'error': 'Valid wallet required'}), 400
        
        wallet = wallets_db[wallet_id]
        if wallet['user_id'] != user_id:
            return jsonify({'success': False, 'error': 'Unauthorized wallet access'}), 403
        
        # Check if already mining
        if user_id in mining_sessions:
            return jsonify({'success': False, 'error': 'Already mining'}), 400
        
        mining_power = data.get('power', 'medium')  # low, medium, high
        power_multipliers = {'low': 0.5, 'medium': 1.0, 'high': 2.0}
        
        session_id = str(uuid.uuid4())
        mining_session = {
            'id': session_id,
            'user_id': user_id,
            'wallet_id': wallet_id,
            'wallet_address': wallet['address'],
            'power': mining_power,
            'multiplier': power_multipliers[mining_power],
            'started_at': datetime.utcnow().isoformat(),
            'blocks_mined': 0,
            'total_rewards': 0.0,
            'status': 'active',
            'estimated_daily_reward': 10.0 * power_multipliers[mining_power]
        }
        
        mining_sessions[user_id] = mining_session
        
        return jsonify({
            'success': True,
            'mining_session': mining_session
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@blockchain_bp.route('/mining/status', methods=['GET'])
@jwt_required()
def get_mining_status():
    """Get mining status"""
    try:
        user_id = get_jwt_identity()
        
        if user_id not in mining_sessions:
            return jsonify({
                'success': True,
                'mining': False,
                'message': 'Not currently mining'
            }), 200
        
        session = mining_sessions[user_id]
        
        # Simulate mining progress
        started_time = datetime.fromisoformat(session['started_at'])
        elapsed_hours = (datetime.utcnow() - started_time).total_seconds() / 3600
        
        # Calculate rewards (simplified)
        new_rewards = elapsed_hours * (session['estimated_daily_reward'] / 24)
        session['total_rewards'] = new_rewards
        session['blocks_mined'] = int(elapsed_hours * 2)  # 2 blocks per hour
        
        return jsonify({
            'success': True,
            'mining': True,
            'session': session,
            'elapsed_time': f"{elapsed_hours:.2f} hours"
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@blockchain_bp.route('/mining/stop', methods=['POST'])
@jwt_required()
def stop_mining():
    """Stop mining operation"""
    try:
        user_id = get_jwt_identity()
        
        if user_id not in mining_sessions:
            return jsonify({'success': False, 'error': 'Not currently mining'}), 400
        
        session = mining_sessions[user_id]
        
        # Add rewards to wallet
        wallet = wallets_db[session['wallet_id']]
        wallet['balance']['UBC'] += session['total_rewards']
        
        # Update session
        session['status'] = 'stopped'
        session['stopped_at'] = datetime.utcnow().isoformat()
        
        # Remove from active sessions
        del mining_sessions[user_id]
        
        return jsonify({
            'success': True,
            'message': 'Mining stopped',
            'total_rewards': session['total_rewards'],
            'blocks_mined': session['blocks_mined'],
            'new_balance': wallet['balance']['UBC']
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@blockchain_bp.route('/staking/stake', methods=['POST'])
@jwt_required()
def stake_tokens():
    """Stake tokens for rewards"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        required_fields = ['wallet_id', 'amount', 'duration']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400
        
        wallet_id = data['wallet_id']
        amount = float(data['amount'])
        duration = int(data['duration'])  # days
        
        # Validate wallet
        if wallet_id not in wallets_db:
            return jsonify({'success': False, 'error': 'Wallet not found'}), 404
        
        wallet = wallets_db[wallet_id]
        if wallet['user_id'] != user_id:
            return jsonify({'success': False, 'error': 'Unauthorized wallet access'}), 403
        
        # Check balance
        if wallet['balance']['UBC'] < amount:
            return jsonify({'success': False, 'error': 'Insufficient balance'}), 400
        
        # Calculate rewards
        annual_rate = 0.08  # 8% annual rate
        daily_rate = annual_rate / 365
        estimated_rewards = amount * daily_rate * duration
        
        # Create staking position
        stake_id = str(uuid.uuid4())
        stake = {
            'id': stake_id,
            'user_id': user_id,
            'wallet_id': wallet_id,
            'amount': amount,
            'duration_days': duration,
            'annual_rate': annual_rate,
            'estimated_rewards': estimated_rewards,
            'started_at': datetime.utcnow().isoformat(),
            'ends_at': (datetime.utcnow() + timedelta(days=duration)).isoformat(),
            'status': 'active',
            'rewards_earned': 0.0
        }
        
        # Update wallet balance
        wallet['balance']['UBC'] -= amount
        wallet['balance']['staked'] += amount
        
        staking_pools[stake_id] = stake
        
        return jsonify({
            'success': True,
            'stake': stake,
            'new_balance': wallet['balance']
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@blockchain_bp.route('/staking/positions', methods=['GET'])
@jwt_required()
def get_staking_positions():
    """Get user's staking positions"""
    try:
        user_id = get_jwt_identity()
        
        user_stakes = []
        for stake in staking_pools.values():
            if stake['user_id'] == user_id:
                # Calculate current rewards
                started_time = datetime.fromisoformat(stake['started_at'])
                elapsed_days = (datetime.utcnow() - started_time).days
                daily_reward = stake['amount'] * (stake['annual_rate'] / 365)
                current_rewards = min(daily_reward * elapsed_days, stake['estimated_rewards'])
                
                stake['rewards_earned'] = current_rewards
                user_stakes.append(stake)
        
        return jsonify({
            'success': True,
            'stakes': user_stakes,
            'total_staked': sum(s['amount'] for s in user_stakes),
            'total_rewards': sum(s['rewards_earned'] for s in user_stakes)
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@blockchain_bp.route('/nft/mint', methods=['POST'])
@jwt_required()
def mint_nft():
    """Mint a new NFT"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        required_fields = ['wallet_id', 'name', 'description']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400
        
        wallet_id = data['wallet_id']
        
        # Validate wallet
        if wallet_id not in wallets_db:
            return jsonify({'success': False, 'error': 'Wallet not found'}), 404
        
        wallet = wallets_db[wallet_id]
        if wallet['user_id'] != user_id:
            return jsonify({'success': False, 'error': 'Unauthorized wallet access'}), 403
        
        # Minting cost
        minting_cost = 10.0
        if wallet['balance']['UBC'] < minting_cost:
            return jsonify({'success': False, 'error': 'Insufficient balance for minting'}), 400
        
        # Create NFT
        nft_id = str(uuid.uuid4())
        token_id = len(nft_collections) + 1
        
        nft = {
            'id': nft_id,
            'token_id': token_id,
            'name': data['name'],
            'description': data['description'],
            'image_url': data.get('image_url', ''),
            'attributes': data.get('attributes', []),
            'creator': user_id,
            'owner': user_id,
            'wallet_address': wallet['address'],
            'created_at': datetime.utcnow().isoformat(),
            'metadata': {
                'collection': data.get('collection', 'Default'),
                'rarity': data.get('rarity', 'common'),
                'category': data.get('category', 'art')
            },
            'transaction_history': [],
            'is_listed': False,
            'price': None
        }
        
        # Deduct minting cost
        wallet['balance']['UBC'] -= minting_cost
        
        nft_collections[nft_id] = nft
        
        return jsonify({
            'success': True,
            'nft': nft,
            'minting_cost': minting_cost,
            'new_balance': wallet['balance']['UBC']
        }), 201
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@blockchain_bp.route('/nft/collection', methods=['GET'])
@jwt_required()
def get_nft_collection():
    """Get user's NFT collection"""
    try:
        user_id = get_jwt_identity()
        
        user_nfts = []
        for nft in nft_collections.values():
            if nft['owner'] == user_id:
                user_nfts.append(nft)
        
        # Sort by creation date (newest first)
        user_nfts.sort(key=lambda x: x['created_at'], reverse=True)
        
        return jsonify({
            'success': True,
            'nfts': user_nfts,
            'total_count': len(user_nfts),
            'collections': list(set(nft['metadata']['collection'] for nft in user_nfts))
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@blockchain_bp.route('/network/info', methods=['GET'])
def get_network_info():
    """Get blockchain network information"""
    try:
        total_supply = 21000000  # Total UBC supply
        circulating_supply = sum(
            wallet['balance']['UBC'] + wallet['balance']['staked'] 
            for wallet in wallets_db.values()
        )
        
        network_info = {
            'network_name': 'Unified Blockchain Network',
            'symbol': 'UBC',
            'total_supply': total_supply,
            'circulating_supply': circulating_supply,
            'total_wallets': len(wallets_db),
            'total_transactions': len(transactions_db),
            'total_blocks': len(blocks_db),
            'current_block_height': len(blocks_db) - 1,
            'average_block_time': '10 seconds',
            'network_hashrate': '1.2 TH/s',
            'difficulty': 4,
            'active_miners': len(mining_sessions),
            'total_staked': sum(
                wallet['balance']['staked'] for wallet in wallets_db.values()
            ),
            'staking_apy': '8.0%',
            'transaction_fee': '0.001 UBC',
            'consensus_mechanism': 'Proof of Stake + Proof of Work Hybrid'
        }
        
        return jsonify({
            'success': True,
            'network_info': network_info
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


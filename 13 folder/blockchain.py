from flask import Blueprint, jsonify, request
import json
import random
import time
import hashlib

blockchain_bp = Blueprint('blockchain', __name__)

# Blockchain Search Engine (Presearch/Brave inspired)
class DecentralizedSearchEngine:
    def __init__(self):
        self.search_providers = ['Presearch', 'Brave Search', 'DuckDuckGo', 'Searx']
        self.token_rewards = {'PRE': 0.1, 'BAT': 0.05, 'SEARCH': 0.08}
        self.user_balances = {}
    
    def search(self, query, user_id):
        # Simulate decentralized search
        results = [
            {
                'title': f'Blockchain result for: {query}',
                'url': f'https://decentralized-web.com/search/{query.replace(" ", "-")}',
                'snippet': f'Decentralized search result about {query} with privacy protection',
                'provider': random.choice(self.search_providers),
                'blockchain_verified': True
            },
            {
                'title': f'Crypto data: {query}',
                'url': f'https://blockchain-explorer.com/{query}',
                'snippet': f'Real-time blockchain data for {query}',
                'provider': 'Brave Search',
                'blockchain_verified': True
            }
        ]
        
        # Reward user with tokens
        if user_id not in self.user_balances:
            self.user_balances[user_id] = {'PRE': 0, 'BAT': 0, 'SEARCH': 0}
        
        for token, reward in self.token_rewards.items():
            self.user_balances[user_id][token] += reward
        
        return results, self.user_balances[user_id]

search_engine = DecentralizedSearchEngine()

# Blockchain Network Simulation
class BlockchainNetwork:
    def __init__(self):
        self.blocks = []
        self.pending_transactions = []
        self.mining_difficulty = 4
        self.mining_reward = 10
        
    def create_genesis_block(self):
        genesis_block = {
            'index': 0,
            'timestamp': time.time(),
            'transactions': [],
            'previous_hash': '0',
            'nonce': 0,
            'hash': self.calculate_hash(0, time.time(), [], '0', 0)
        }
        self.blocks.append(genesis_block)
        return genesis_block
    
    def calculate_hash(self, index, timestamp, transactions, previous_hash, nonce):
        data = f"{index}{timestamp}{json.dumps(transactions)}{previous_hash}{nonce}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    def mine_block(self, miner_address):
        if not self.blocks:
            self.create_genesis_block()
        
        last_block = self.blocks[-1]
        new_index = last_block['index'] + 1
        timestamp = time.time()
        
        # Add mining reward transaction
        reward_transaction = {
            'from': 'system',
            'to': miner_address,
            'amount': self.mining_reward,
            'type': 'mining_reward'
        }
        transactions = self.pending_transactions + [reward_transaction]
        
        # Mine the block
        nonce = 0
        while True:
            hash_value = self.calculate_hash(new_index, timestamp, transactions, last_block['hash'], nonce)
            if hash_value.startswith('0' * self.mining_difficulty):
                break
            nonce += 1
        
        new_block = {
            'index': new_index,
            'timestamp': timestamp,
            'transactions': transactions,
            'previous_hash': last_block['hash'],
            'nonce': nonce,
            'hash': hash_value
        }
        
        self.blocks.append(new_block)
        self.pending_transactions = []
        return new_block

blockchain_network = BlockchainNetwork()

@blockchain_bp.route('/search', methods=['POST'])
def decentralized_search():
    data = request.get_json()
    query = data.get('query', '')
    user_id = data.get('user_id', 'anonymous')
    
    if not query:
        return jsonify({'error': 'Query is required'}), 400
    
    results, user_tokens = search_engine.search(query, user_id)
    
    return jsonify({
        'query': query,
        'results': results,
        'search_provider': 'Unified Decentralized Search',
        'privacy_protected': True,
        'tokens_earned': user_tokens,
        'total_results': len(results),
        'search_time': f"{random.uniform(0.1, 0.5):.2f}s"
    })

@blockchain_bp.route('/wallet/<user_id>')
def get_wallet(user_id):
    balance = search_engine.user_balances.get(user_id, {'PRE': 0, 'BAT': 0, 'SEARCH': 0})
    
    return jsonify({
        'user_id': user_id,
        'balances': balance,
        'wallet_address': f"0x{hashlib.md5(user_id.encode()).hexdigest()[:40]}",
        'total_searches': sum([int(v/0.1) for v in balance.values()]),
        'rewards_earned_today': f"{sum(balance.values()):.2f} tokens"
    })

@blockchain_bp.route('/mine', methods=['POST'])
def mine_block():
    data = request.get_json()
    miner_address = data.get('miner_address', 'default_miner')
    
    new_block = blockchain_network.mine_block(miner_address)
    
    return jsonify({
        'status': 'block_mined',
        'block': new_block,
        'reward': blockchain_network.mining_reward,
        'network_stats': {
            'total_blocks': len(blockchain_network.blocks),
            'difficulty': blockchain_network.mining_difficulty,
            'pending_transactions': len(blockchain_network.pending_transactions)
        }
    })

@blockchain_bp.route('/transaction', methods=['POST'])
def create_transaction():
    data = request.get_json()
    from_address = data.get('from')
    to_address = data.get('to')
    amount = data.get('amount')
    
    if not all([from_address, to_address, amount]):
        return jsonify({'error': 'Missing transaction data'}), 400
    
    transaction = {
        'from': from_address,
        'to': to_address,
        'amount': amount,
        'timestamp': time.time(),
        'type': 'transfer',
        'tx_id': hashlib.sha256(f"{from_address}{to_address}{amount}{time.time()}".encode()).hexdigest()
    }
    
    blockchain_network.pending_transactions.append(transaction)
    
    return jsonify({
        'status': 'transaction_created',
        'transaction': transaction,
        'pending_in_mempool': True,
        'estimated_confirmation': '2-5 minutes'
    })

@blockchain_bp.route('/network/stats')
def network_stats():
    return jsonify({
        'network_name': 'Unified Platform Blockchain',
        'consensus': 'Proof of Work',
        'total_blocks': len(blockchain_network.blocks),
        'pending_transactions': len(blockchain_network.pending_transactions),
        'mining_difficulty': blockchain_network.mining_difficulty,
        'block_reward': blockchain_network.mining_reward,
        'network_hashrate': f"{random.randint(100, 1000)} TH/s",
        'active_nodes': random.randint(5000, 15000),
        'decentralization_score': f"{random.randint(85, 98)}%",
        'search_integration': {
            'total_searches': sum([sum(balances.values()) for balances in search_engine.user_balances.values()]),
            'active_searchers': len(search_engine.user_balances),
            'privacy_protected': True
        }
    })

@blockchain_bp.route('/defi/protocols')
def defi_protocols():
    return jsonify({
        'available_protocols': [
            {
                'name': 'Unified DEX',
                'type': 'Decentralized Exchange',
                'tvl': '$2.5B',
                'apy': '12.5%',
                'features': ['AMM', 'Yield Farming', 'Governance']
            },
            {
                'name': 'Search Rewards Pool',
                'type': 'Staking Protocol',
                'tvl': '$850M',
                'apy': '8.2%',
                'features': ['Search Mining', 'Token Staking', 'Privacy Rewards']
            },
            {
                'name': 'AI Training DAO',
                'type': 'Governance Protocol',
                'tvl': '$1.2B',
                'apy': '15.8%',
                'features': ['Model Training', 'Data Sharing', 'Compute Rewards']
            }
        ],
        'total_tvl': '$4.55B',
        'supported_chains': ['Ethereum', 'Polygon', 'Arbitrum', 'Unified Chain']
    })

@blockchain_bp.route('/nft/marketplace')
def nft_marketplace():
    return jsonify({
        'featured_collections': [
            {
                'name': 'AI Generated Art',
                'floor_price': '0.5 ETH',
                'volume_24h': '125 ETH',
                'items': 10000,
                'description': 'Unique AI-generated artwork from the Unified Platform'
            },
            {
                'name': 'Robot Designs NFT',
                'floor_price': '0.3 ETH',
                'volume_24h': '89 ETH',
                'items': 5000,
                'description': 'Collectible robot designs from Text2Robot system'
            },
            {
                'name': 'Search History Tokens',
                'floor_price': '0.1 ETH',
                'volume_24h': '45 ETH',
                'items': 50000,
                'description': 'Privacy-preserved search history as collectible NFTs'
            }
        ],
        'marketplace_stats': {
            'total_volume': '2,450 ETH',
            'active_traders': 15000,
            'total_sales': 125000,
            'average_price': '0.35 ETH'
        }
    })

@blockchain_bp.route('/smart-contracts/deploy', methods=['POST'])
def deploy_smart_contract():
    data = request.get_json()
    contract_type = data.get('type', 'ERC20')
    contract_name = data.get('name', 'UnifiedToken')
    
    contract_address = f"0x{hashlib.sha256((contract_name + str(time.time())).encode()).hexdigest()[:40]}"
    
    return jsonify({
        'status': 'contract_deployed',
        'contract_address': contract_address,
        'contract_type': contract_type,
        'contract_name': contract_name,
        'deployment_cost': f"{random.uniform(0.01, 0.1):.4f} ETH",
        'verification_status': 'verified',
        'features': [
            'Automated trading',
            'Governance voting',
            'Yield generation',
            'Cross-chain compatibility'
        ]
    })


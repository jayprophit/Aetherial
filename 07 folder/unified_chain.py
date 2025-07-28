"""
UnifiedChain Blockchain Implementation
Core blockchain functionality for the Unified Platform
"""

import hashlib
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import uuid
from collections import defaultdict
import threading
import queue

class TransactionType(Enum):
    TRANSFER = "transfer"
    COURSE_COMPLETION = "course_completion"
    JOB_APPLICATION = "job_application"
    PRODUCT_PURCHASE = "product_purchase"
    CONTENT_CREATION = "content_creation"
    SKILL_VERIFICATION = "skill_verification"
    REPUTATION_UPDATE = "reputation_update"
    STAKING = "staking"
    GOVERNANCE_VOTE = "governance_vote"

class InteractionType(Enum):
    LEARNING = "learning"
    SOCIAL = "social"
    COMMERCE = "commerce"
    EMPLOYMENT = "employment"
    DEVELOPMENT = "development"

@dataclass
class Transaction:
    id: str
    from_address: str
    to_address: str
    amount: float
    transaction_type: TransactionType
    interaction_type: InteractionType
    metadata: Dict[str, Any]
    timestamp: float
    signature: str = ""
    gas_fee: float = 0.001
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'from_address': self.from_address,
            'to_address': self.to_address,
            'amount': self.amount,
            'transaction_type': self.transaction_type.value,
            'interaction_type': self.interaction_type.value,
            'metadata': self.metadata,
            'timestamp': self.timestamp,
            'signature': self.signature,
            'gas_fee': self.gas_fee
        }
    
    def calculate_hash(self) -> str:
        """Calculate transaction hash for verification"""
        tx_string = f"{self.id}{self.from_address}{self.to_address}{self.amount}{self.transaction_type.value}{self.timestamp}"
        return hashlib.sha256(tx_string.encode()).hexdigest()

@dataclass
class Block:
    index: int
    timestamp: float
    transactions: List[Transaction]
    previous_hash: str
    nonce: int = 0
    hash: str = ""
    validator: str = ""
    interaction_weight: float = 0.0
    
    def calculate_hash(self) -> str:
        """Calculate block hash"""
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': [tx.to_dict() for tx in self.transactions],
            'previous_hash': self.previous_hash,
            'nonce': self.nonce,
            'validator': self.validator,
            'interaction_weight': self.interaction_weight
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty: int = 4):
        """Mine block with proof-of-work (simplified for demo)"""
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()

@dataclass
class UserAccount:
    address: str
    balance: float = 0.0
    staked_amount: float = 0.0
    reputation_score: float = 0.0
    interaction_points: Dict[InteractionType, float] = None
    skills_verified: List[str] = None
    courses_completed: List[str] = None
    jobs_completed: int = 0
    content_created: int = 0
    last_activity: float = 0.0
    
    def __post_init__(self):
        if self.interaction_points is None:
            self.interaction_points = {interaction_type: 0.0 for interaction_type in InteractionType}
        if self.skills_verified is None:
            self.skills_verified = []
        if self.courses_completed is None:
            self.courses_completed = []

class UnifiedChain:
    def __init__(self):
        self.chain: List[Block] = []
        self.pending_transactions: List[Transaction] = []
        self.accounts: Dict[str, UserAccount] = {}
        self.validators: Dict[str, float] = {}  # address -> stake amount
        self.mining_reward = 10.0
        self.difficulty = 4
        self.block_time = 3.0  # seconds
        self.max_transactions_per_block = 1000
        self.total_supply = 1_000_000_000  # 1 billion UNI tokens
        self.circulating_supply = 0.0
        self.transaction_pool = queue.Queue()
        self.consensus_lock = threading.Lock()
        
        # Create genesis block
        self.create_genesis_block()
        
        # Initialize system accounts
        self.initialize_system_accounts()
    
    def create_genesis_block(self):
        """Create the first block in the blockchain"""
        genesis_block = Block(
            index=0,
            timestamp=time.time(),
            transactions=[],
            previous_hash="0",
            validator="genesis"
        )
        genesis_block.hash = genesis_block.calculate_hash()
        self.chain.append(genesis_block)
    
    def initialize_system_accounts(self):
        """Initialize system accounts for rewards and operations"""
        system_accounts = [
            "system_rewards",
            "system_treasury", 
            "system_operations",
            "system_staking"
        ]
        
        for account in system_accounts:
            self.accounts[account] = UserAccount(
                address=account,
                balance=self.total_supply * 0.1  # 10% each for system accounts
            )
            self.circulating_supply += self.total_supply * 0.1
    
    def create_account(self, user_id: str) -> str:
        """Create a new blockchain account for a user"""
        address = f"uni_{user_id}_{uuid.uuid4().hex[:8]}"
        
        if address not in self.accounts:
            self.accounts[address] = UserAccount(address=address)
            
            # Give new users some starting tokens
            starter_amount = 100.0
            self.transfer_tokens("system_treasury", address, starter_amount, 
                               TransactionType.TRANSFER, InteractionType.SOCIAL,
                               {"type": "welcome_bonus", "user_id": user_id})
        
        return address
    
    def get_account(self, address: str) -> Optional[UserAccount]:
        """Get account information"""
        return self.accounts.get(address)
    
    def transfer_tokens(self, from_address: str, to_address: str, amount: float,
                       transaction_type: TransactionType, interaction_type: InteractionType,
                       metadata: Dict[str, Any] = None) -> str:
        """Transfer tokens between accounts"""
        if metadata is None:
            metadata = {}
        
        # Validate accounts exist
        if from_address not in self.accounts:
            raise ValueError(f"From address {from_address} not found")
        if to_address not in self.accounts:
            raise ValueError(f"To address {to_address} not found")
        
        # Validate sufficient balance
        if self.accounts[from_address].balance < amount:
            raise ValueError(f"Insufficient balance. Available: {self.accounts[from_address].balance}, Required: {amount}")
        
        # Create transaction
        transaction = Transaction(
            id=str(uuid.uuid4()),
            from_address=from_address,
            to_address=to_address,
            amount=amount,
            transaction_type=transaction_type,
            interaction_type=interaction_type,
            metadata=metadata,
            timestamp=time.time()
        )
        
        # Add to pending transactions
        self.pending_transactions.append(transaction)
        
        # Process transaction immediately for demo
        self.process_transaction(transaction)
        
        return transaction.id
    
    def process_transaction(self, transaction: Transaction):
        """Process a single transaction"""
        from_account = self.accounts[transaction.from_address]
        to_account = self.accounts[transaction.to_address]
        
        # Deduct from sender
        from_account.balance -= transaction.amount
        from_account.balance -= transaction.gas_fee
        
        # Add to receiver
        to_account.balance += transaction.amount
        
        # Update interaction points
        self.update_interaction_points(transaction)
        
        # Update reputation based on transaction type
        self.update_reputation(transaction)
        
        # Update last activity
        from_account.last_activity = transaction.timestamp
        to_account.last_activity = transaction.timestamp
    
    def update_interaction_points(self, transaction: Transaction):
        """Update interaction points based on transaction"""
        from_account = self.accounts[transaction.from_address]
        to_account = self.accounts[transaction.to_address]
        
        # Award points based on interaction type and transaction type
        points_multiplier = {
            TransactionType.COURSE_COMPLETION: 10.0,
            TransactionType.JOB_APPLICATION: 5.0,
            TransactionType.PRODUCT_PURCHASE: 2.0,
            TransactionType.CONTENT_CREATION: 15.0,
            TransactionType.SKILL_VERIFICATION: 20.0,
            TransactionType.TRANSFER: 1.0
        }
        
        base_points = points_multiplier.get(transaction.transaction_type, 1.0)
        
        # Award points to both parties
        from_account.interaction_points[transaction.interaction_type] += base_points
        to_account.interaction_points[transaction.interaction_type] += base_points * 0.5
    
    def update_reputation(self, transaction: Transaction):
        """Update reputation scores based on transaction"""
        from_account = self.accounts[transaction.from_address]
        to_account = self.accounts[transaction.to_address]
        
        # Reputation updates based on transaction type
        if transaction.transaction_type == TransactionType.COURSE_COMPLETION:
            to_account.reputation_score += 1.0
            to_account.courses_completed.append(transaction.metadata.get('course_id', ''))
            
        elif transaction.transaction_type == TransactionType.SKILL_VERIFICATION:
            to_account.reputation_score += 2.0
            skill = transaction.metadata.get('skill', '')
            if skill and skill not in to_account.skills_verified:
                to_account.skills_verified.append(skill)
                
        elif transaction.transaction_type == TransactionType.JOB_APPLICATION:
            if transaction.metadata.get('status') == 'completed':
                to_account.jobs_completed += 1
                to_account.reputation_score += 3.0
                
        elif transaction.transaction_type == TransactionType.CONTENT_CREATION:
            from_account.content_created += 1
            from_account.reputation_score += 0.5
    
    def stake_tokens(self, address: str, amount: float) -> str:
        """Stake tokens for consensus participation"""
        account = self.accounts.get(address)
        if not account:
            raise ValueError(f"Account {address} not found")
        
        if account.balance < amount:
            raise ValueError("Insufficient balance for staking")
        
        # Transfer to staking
        account.balance -= amount
        account.staked_amount += amount
        
        # Add to validators if not already present
        if address not in self.validators:
            self.validators[address] = 0.0
        self.validators[address] += amount
        
        # Create staking transaction
        transaction_id = self.transfer_tokens(
            address, "system_staking", 0.0,  # No actual transfer, just record
            TransactionType.STAKING, InteractionType.SOCIAL,
            {"action": "stake", "amount": amount}
        )
        
        return transaction_id
    
    def unstake_tokens(self, address: str, amount: float) -> str:
        """Unstake tokens (with cooldown period in production)"""
        account = self.accounts.get(address)
        if not account:
            raise ValueError(f"Account {address} not found")
        
        if account.staked_amount < amount:
            raise ValueError("Insufficient staked amount")
        
        # Return to balance
        account.staked_amount -= amount
        account.balance += amount
        
        # Update validators
        if address in self.validators:
            self.validators[address] -= amount
            if self.validators[address] <= 0:
                del self.validators[address]
        
        # Create unstaking transaction
        transaction_id = self.transfer_tokens(
            "system_staking", address, 0.0,  # No actual transfer, just record
            TransactionType.STAKING, InteractionType.SOCIAL,
            {"action": "unstake", "amount": amount}
        )
        
        return transaction_id
    
    def calculate_consensus_weight(self, address: str) -> float:
        """Calculate consensus weight based on stake and interactions"""
        account = self.accounts.get(address)
        if not account:
            return 0.0
        
        # Base weight from staked amount
        stake_weight = account.staked_amount * 0.7
        
        # Interaction weight from platform activity
        total_interactions = sum(account.interaction_points.values())
        interaction_weight = min(total_interactions * 0.1, account.staked_amount * 0.3)
        
        # Reputation weight
        reputation_weight = account.reputation_score * 0.1
        
        return stake_weight + interaction_weight + reputation_weight
    
    def select_validator(self) -> str:
        """Select validator for next block using weighted random selection"""
        if not self.validators:
            return "system_rewards"  # Fallback to system account
        
        # Calculate weights for all validators
        weights = {}
        total_weight = 0.0
        
        for address in self.validators:
            weight = self.calculate_consensus_weight(address)
            weights[address] = weight
            total_weight += weight
        
        if total_weight == 0:
            return list(self.validators.keys())[0]  # Fallback to first validator
        
        # Weighted random selection (simplified)
        import random
        random_value = random.random() * total_weight
        current_weight = 0.0
        
        for address, weight in weights.items():
            current_weight += weight
            if random_value <= current_weight:
                return address
        
        return list(self.validators.keys())[0]  # Fallback
    
    def create_block(self) -> Block:
        """Create a new block with pending transactions"""
        if not self.pending_transactions:
            return None
        
        # Get transactions for this block
        transactions = self.pending_transactions[:self.max_transactions_per_block]
        self.pending_transactions = self.pending_transactions[self.max_transactions_per_block:]
        
        # Select validator
        validator = self.select_validator()
        
        # Calculate interaction weight for this block
        interaction_weight = sum(
            self.calculate_consensus_weight(tx.from_address) + 
            self.calculate_consensus_weight(tx.to_address)
            for tx in transactions
        ) / len(transactions) if transactions else 0.0
        
        # Create new block
        new_block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            transactions=transactions,
            previous_hash=self.chain[-1].hash,
            validator=validator,
            interaction_weight=interaction_weight
        )
        
        # Mine the block (simplified for demo)
        new_block.mine_block(self.difficulty)
        
        return new_block
    
    def add_block(self, block: Block) -> bool:
        """Add a new block to the chain"""
        with self.consensus_lock:
            # Validate block
 
(Content truncated due to size limit. Use line ranges to read in chunks)
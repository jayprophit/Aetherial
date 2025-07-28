from typing import Dict, List, Optional
import hashlib
import time
import json
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class Block:
    index: int
    timestamp: float
    data: Dict
    previous_hash: str
    nonce: int = 0
    hash: str = ""

class OrdinalProtocol:
    def __init__(self):
        self.ordinals: Dict[str, Dict] = {}
        self.inscriptions: Dict[str, Dict] = {}
        self.rarity_scores: Dict[str, float] = {}
        
    def create_ordinal(self, content: Dict, metadata: Dict) -> str:
        """Create a new ordinal with content and metadata"""
        ordinal_id = self._generate_id(content)
        
        self.ordinals[ordinal_id] = {
            "content": content,
            "metadata": metadata,
            "timestamp": time.time(),
            "rarity_score": self._calculate_rarity(content)
        }
        
        return ordinal_id
    
    def inscribe_data(self, ordinal_id: str, data: Dict) -> str:
        """Inscribe additional data onto an existing ordinal"""
        if ordinal_id not in self.ordinals:
            raise ValueError("Ordinal not found")
            
        inscription_id = self._generate_id(data)
        self.inscriptions[inscription_id] = {
            "ordinal_id": ordinal_id,
            "data": data,
            "timestamp": time.time()
        }
        
        return inscription_id
    
    def _generate_id(self, content: Dict) -> str:
        """Generate a unique ID for ordinal or inscription"""
        content_str = json.dumps(content, sort_keys=True)
        return hashlib.sha256(content_str.encode()).hexdigest()
    
    def _calculate_rarity(self, content: Dict) -> float:
        """Calculate rarity score based on content attributes"""
        # Simplified rarity calculation
        return len(json.dumps(content))

class BlockchainNetwork:
    def __init__(self):
        self.chain: List[Block] = []
        self.pending_transactions: List[Dict] = []
        self.nodes: Dict[str, 'Node'] = {}
        self.difficulty = 4
        
        # Create genesis block
        self._create_genesis_block()
    
    def _create_genesis_block(self):
        """Create the initial block in the chain"""
        genesis_block = Block(
            index=0,
            timestamp=time.time(),
            data={"message": "Genesis Block"},
            previous_hash="0"
        )
        self._add_block(genesis_block)
    
    def _add_block(self, block: Block) -> bool:
        """Add a new block to the chain"""
        block.hash = self._calculate_hash(block)
        self.chain.append(block)
        return True
    
    def create_block(self, data: Dict) -> Block:
        """Create and mine a new block"""
        block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            data=data,
            previous_hash=self.chain[-1].hash
        )
        
        block = self._mine_block(block)
        self._add_block(block)
        return block
    
    def _calculate_hash(self, block: Block) -> str:
        """Calculate hash of a block"""
        block_content = f"{block.index}{block.timestamp}{block.data}{block.previous_hash}{block.nonce}"
        return hashlib.sha256(block_content.encode()).hexdigest()
    
    def _mine_block(self, block: Block) -> Block:
        """Mine a block by finding a hash with required difficulty"""
        target = "0" * self.difficulty
        
        while True:
            block.hash = self._calculate_hash(block)
            if block.hash.startswith(target):
                break
            block.nonce += 1
            
        return block
    
    def is_chain_valid(self) -> bool:
        """Verify the integrity of the blockchain"""
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            
            if current.hash != self._calculate_hash(current):
                return False
                
            if current.previous_hash != previous.hash:
                return False
                
        return True

class MeshNetwork:
    def __init__(self):
        self.nodes: Dict[str, 'Node'] = {}
        self.connections: Dict[str, List[str]] = defaultdict(list)
        
    def add_node(self, node_id: str, node: 'Node'):
        """Add a new node to the mesh network"""
        self.nodes[node_id] = node
    
    def connect_nodes(self, node1_id: str, node2_id: str):
        """Create a connection between two nodes"""
        if node1_id not in self.nodes or node2_id not in self.nodes:
            raise ValueError("Node not found")
            
        self.connections[node1_id].append(node2_id)
        self.connections[node2_id].append(node1_id)
    
    def broadcast_message(self, source_id: str, message: Dict):
        """Broadcast a message through the mesh network"""
        visited = set()
        self._broadcast_to_neighbors(source_id, message, visited)
    
    def _broadcast_to_neighbors(self, node_id: str, message: Dict, visited: set):
        """Helper method for broadcasting messages"""
        visited.add(node_id)
        
        for neighbor_id in self.connections[node_id]:
            if neighbor_id not in visited:
                self.nodes[neighbor_id].receive_message(message)
                self._broadcast_to_neighbors(neighbor_id, message, visited)

class Node:
    def __init__(self, node_id: str, blockchain: BlockchainNetwork):
        self.node_id = node_id
        self.blockchain = blockchain
        self.pending_transactions: List[Dict] = []
        
    def receive_message(self, message: Dict):
        """Handle incoming messages from the mesh network"""
        if message.get("type") == "transaction":
            self.pending_transactions.append(message.get("data"))
        elif message.get("type") == "block":
            self._validate_and_add_block(message.get("data"))
    
    def _validate_and_add_block(self, block_data: Dict):
        """Validate and add a new block to the chain"""
        # Implementation would go here
        pass

# Usage example
if __name__ == "__main__":
    # Initialize components
    blockchain = BlockchainNetwork()
    ordinal_protocol = OrdinalProtocol()
    mesh_network = MeshNetwork()
    
    # Create some sample data
    content = {
        "type": "text",
        "content": "Hello, Blockchain!",
        "timestamp": time.time()
    }
    
    metadata = {
        "creator": "user123",
        "version": "1.0"
    }
    
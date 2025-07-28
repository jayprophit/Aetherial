"""
Milvus Integration for Vector Similarity Search
Advanced vector database integration with Milvus for scalable similarity search
"""

import asyncio
import json
import logging
import uuid
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import dataclass, field
from enum import Enum
import os
import pickle
import hashlib
from pathlib import Path

# Milvus imports (simulated for compatibility)
try:
    from pymilvus import (
        connections, Collection, CollectionSchema, FieldSchema, DataType,
        utility, Index, SearchResult as MilvusSearchResult
    )
    MILVUS_AVAILABLE = True
except ImportError:
    logging.warning("Milvus not available, using fallback implementation")
    MILVUS_AVAILABLE = False

class MilvusMetricType(Enum):
    L2 = "L2"
    IP = "IP"  # Inner Product
    COSINE = "COSINE"
    HAMMING = "HAMMING"
    JACCARD = "JACCARD"
    TANIMOTO = "TANIMOTO"

class MilvusIndexType(Enum):
    FLAT = "FLAT"
    IVF_FLAT = "IVF_FLAT"
    IVF_SQ8 = "IVF_SQ8"
    IVF_PQ = "IVF_PQ"
    HNSW = "HNSW"
    ANNOY = "ANNOY"
    AUTOINDEX = "AUTOINDEX"

@dataclass
class MilvusCollection:
    name: str
    description: str
    dimension: int
    metric_type: MilvusMetricType
    index_type: MilvusIndexType
    index_params: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)

@dataclass
class MilvusSearchResult:
    id: str
    score: float
    entity: Dict[str, Any]
    distance: float

class MilvusIntegration:
    """
    Milvus Integration for scalable vector similarity search
    """
    
    def __init__(self, host: str = "localhost", port: int = 19530, 
                 alias: str = "default", data_dir: str = "./milvus_data"):
        self.host = host
        self.port = port
        self.alias = alias
        self.data_dir = data_dir
        self.collections = {}
        self.is_connected = False
        
        # Initialize data directory
        os.makedirs(data_dir, exist_ok=True)
        
        # Connect to Milvus
        self._connect()
        
        # Default index parameters
        self.default_index_params = {
            MilvusIndexType.FLAT: {},
            MilvusIndexType.IVF_FLAT: {"nlist": 1024},
            MilvusIndexType.IVF_SQ8: {"nlist": 1024},
            MilvusIndexType.IVF_PQ: {"nlist": 1024, "m": 16, "nbits": 8},
            MilvusIndexType.HNSW: {"M": 16, "efConstruction": 200},
            MilvusIndexType.ANNOY: {"n_trees": 8},
            MilvusIndexType.AUTOINDEX: {}
        }
        
        # Default search parameters
        self.default_search_params = {
            MilvusIndexType.FLAT: {},
            MilvusIndexType.IVF_FLAT: {"nprobe": 10},
            MilvusIndexType.IVF_SQ8: {"nprobe": 10},
            MilvusIndexType.IVF_PQ: {"nprobe": 10},
            MilvusIndexType.HNSW: {"ef": 64},
            MilvusIndexType.ANNOY: {"search_k": -1},
            MilvusIndexType.AUTOINDEX: {}
        }
    
    def _connect(self):
        """Connect to Milvus server"""
        try:
            if MILVUS_AVAILABLE:
                connections.connect(
                    alias=self.alias,
                    host=self.host,
                    port=self.port
                )
                self.is_connected = True
                logging.info(f"Connected to Milvus at {self.host}:{self.port}")
            else:
                # Fallback mode - use local storage
                self.is_connected = False
                logging.warning("Using fallback mode without Milvus server")
                
        except Exception as e:
            logging.error(f"Failed to connect to Milvus: {e}")
            self.is_connected = False
    
    async def create_collection(self, collection_config: MilvusCollection) -> bool:
        """Create a new Milvus collection"""
        try:
            if MILVUS_AVAILABLE and self.is_connected:
                # Define schema
                fields = [
                    FieldSchema(name="id", dtype=DataType.VARCHAR, max_length=100, is_primary=True),
                    FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=collection_config.dimension),
                    FieldSchema(name="content_id", dtype=DataType.VARCHAR, max_length=100),
                    FieldSchema(name="embedding_type", dtype=DataType.VARCHAR, max_length=50),
                    FieldSchema(name="metadata", dtype=DataType.VARCHAR, max_length=2000),
                    FieldSchema(name="created_at", dtype=DataType.VARCHAR, max_length=50)
                ]
                
                schema = CollectionSchema(
                    fields=fields,
                    description=collection_config.description
                )
                
                # Create collection
                collection = Collection(
                    name=collection_config.name,
                    schema=schema,
                    using=self.alias
                )
                
                # Create index
                index_params = collection_config.index_params or self.default_index_params[collection_config.index_type]
                
                collection.create_index(
                    field_name="vector",
                    index_params={
                        "index_type": collection_config.index_type.value,
                        "metric_type": collection_config.metric_type.value,
                        "params": index_params
                    }
                )
                
                self.collections[collection_config.name] = collection
                
                logging.info(f"Created Milvus collection: {collection_config.name}")
                return True
            else:
                # Fallback: Create local collection metadata
                collection_path = os.path.join(self.data_dir, f"{collection_config.name}.json")
                with open(collection_path, 'w') as f:
                    json.dump({
                        "name": collection_config.name,
                        "description": collection_config.description,
                        "dimension": collection_config.dimension,
                        "metric_type": collection_config.metric_type.value,
                        "index_type": collection_config.index_type.value,
                        "created_at": collection_config.created_at.isoformat(),
                        "vectors": []
                    }, f)
                
                logging.info(f"Created fallback collection: {collection_config.name}")
                return True
                
        except Exception as e:
            logging.error(f"Error creating collection: {e}")
            return False
    
    async def insert_vectors(self, collection_name: str, vectors: List[Dict[str, Any]]) -> bool:
        """Insert vectors into collection"""
        try:
            if MILVUS_AVAILABLE and self.is_connected:
                if collection_name not in self.collections:
                    collection = Collection(collection_name, using=self.alias)
                    self.collections[collection_name] = collection
                else:
                    collection = self.collections[collection_name]
                
                # Prepare data
                ids = [v["id"] for v in vectors]
                vector_data = [v["vector"] for v in vectors]
                content_ids = [v["content_id"] for v in vectors]
                embedding_types = [v["embedding_type"] for v in vectors]
                metadata_list = [json.dumps(v.get("metadata", {})) for v in vectors]
                created_ats = [v.get("created_at", datetime.utcnow().isoformat()) for v in vectors]
                
                # Insert data
                entities = [
                    ids,
                    vector_data,
                    content_ids,
                    embedding_types,
                    metadata_list,
                    created_ats
                ]
                
                insert_result = collection.insert(entities)
                collection.flush()
                
                logging.info(f"Inserted {len(vectors)} vectors into {collection_name}")
                return True
            else:
                # Fallback: Store in local file
                collection_path = os.path.join(self.data_dir, f"{collection_name}.json")
                
                if os.path.exists(collection_path):
                    with open(collection_path, 'r') as f:
                        collection_data = json.load(f)
                else:
                    collection_data = {"vectors": []}
                
                # Convert numpy arrays to lists for JSON serialization
                for vector in vectors:
                    if isinstance(vector["vector"], np.ndarray):
                        vector["vector"] = vector["vector"].tolist()
                    collection_data["vectors"].append(vector)
                
                with open(collection_path, 'w') as f:
                    json.dump(collection_data, f)
                
                logging.info(f"Inserted {len(vectors)} vectors into fallback collection {collection_name}")
                return True
                
        except Exception as e:
            logging.error(f"Error inserting vectors: {e}")
            return False
    
    async def search_vectors(self, collection_name: str, query_vectors: List[np.ndarray],
                           top_k: int = 10, search_params: Optional[Dict[str, Any]] = None,
                           filter_expr: Optional[str] = None) -> List[List[MilvusSearchResult]]:
        """Search for similar vectors"""
        try:
            if MILVUS_AVAILABLE and self.is_connected:
                if collection_name not in self.collections:
                    collection = Collection(collection_name, using=self.alias)
                    self.collections[collection_name] = collection
                else:
                    collection = self.collections[collection_name]
                
                # Load collection
                collection.load()
                
                # Prepare search parameters
                if search_params is None:
                    # Get index type from collection
                    index_info = collection.index()
                    if index_info:
                        index_type = MilvusIndexType(index_info.params["index_type"])
                        search_params = self.default_search_params[index_type]
                    else:
                        search_params = {}
                
                # Convert query vectors to list if numpy arrays
                query_data = []
                for qv in query_vectors:
                    if isinstance(qv, np.ndarray):
                        query_data.append(qv.tolist())
                    else:
                        query_data.append(qv)
                
                # Perform search
                search_results = collection.search(
                    data=query_data,
                    anns_field="vector",
                    param=search_params,
                    limit=top_k,
                    expr=filter_expr,
                    output_fields=["content_id", "embedding_type", "metadata", "created_at"]
                )
                
                # Format results
                formatted_results = []
                for result_set in search_results:
                    result_list = []
                    for hit in result_set:
                        milvus_result = MilvusSearchResult(
                            id=hit.id,
                            score=hit.score,
                            entity={
                                "content_id": hit.entity.get("content_id"),
                                "embedding_type": hit.entity.get("embedding_type"),
                                "metadata": json.loads(hit.entity.get("metadata", "{}")),
                                "created_at": hit.entity.get("created_at")
                            },
                            distance=hit.distance
                        )
                        result_list.append(milvus_result)
                    formatted_results.append(result_list)
                
                return formatted_results
            else:
                # Fallback: Local similarity search
                return await self._fallback_search(collection_name, query_vectors, top_k)
                
        except Exception as e:
            logging.error(f"Error searching vectors: {e}")
            return []
    
    async def _fallback_search(self, collection_name: str, query_vectors: List[np.ndarray],
                             top_k: int) -> List[List[MilvusSearchResult]]:
        """Fallback search using local storage"""
        try:
            collection_path = os.path.join(self.data_dir, f"{collection_name}.json")
            
            if not os.path.exists(collection_path):
                return []
            
            with open(collection_path, 'r') as f:
                collection_data = json.load(f)
            
            vectors = collection_data.get("vectors", [])
            if not vectors:
                return []
            
            results = []
            
            for query_vector in query_vectors:
                if isinstance(query_vector, list):
                    query_vector = np.array(query_vector)
                
                # Calculate similarities
                similarities = []
                for vector_data in vectors:
                    stored_vector = np.array(vector_data["vector"])
                    
                    # Calculate cosine similarity
                    similarity = np.dot(query_vector, stored_vector) / (
                        np.linalg.norm(query_vector) * np.linalg.norm(stored_vector)
                    )
                    
                    similarities.append({
                        "similarity": similarity,
                        "vector_data": vector_data
                    })
                
                # Sort by similarity and take top_k
                similarities.sort(key=lambda x: x["similarity"], reverse=True)
                top_results = similarities[:top_k]
                
                # Format results
                result_list = []
                for i, result in enumerate(top_results):
                    vector_data = result["vector_data"]
                    milvus_result = MilvusSearchResult(
                        id=vector_data["id"],
                        score=result["similarity"],
                        entity={
                            "content_id": vector_data["content_id"],
                            "embedding_type": vector_data["embedding_type"],
                            "metadata": vector_data.get("metadata", {}),
                            "created_at": vector_data.get("created_at")
                        },
                        distance=1.0 - result["similarity"]  # Convert similarity to distance
                    )
                    result_list.append(milvus_result)
                
                results.append(result_list)
            
            return results
            
        except Exception as e:
            logging.error(f"Error in fallback search: {e}")
            return []
    
    async def delete_vectors(self, collection_name: str, ids: List[str]) -> bool:
        """Delete vectors by IDs"""
        try:
            if MILVUS_AVAILABLE and self.is_connected:
                if collection_name not in self.collections:
                    collection = Collection(collection_name, using=self.alias)
                    self.collections[collection_name] = collection
                else:
                    co
(Content truncated due to size limit. Use line ranges to read in chunks)
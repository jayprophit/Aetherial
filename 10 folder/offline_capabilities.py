"""
Offline Capabilities System
Comprehensive offline functionality with data synchronization, caching, and local processing
"""

import os
import json
import sqlite3
import hashlib
import time
import threading
import queue
import asyncio
from typing import Dict, List, Optional, Any, Union, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import pickle
import gzip
import uuid
import shutil
from pathlib import Path

class SyncStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CONFLICT = "conflict"

class DataType(Enum):
    USER_DATA = "user_data"
    CONTENT = "content"
    MEDIA = "media"
    SETTINGS = "settings"
    CACHE = "cache"
    DOCUMENTS = "documents"
    MESSAGES = "messages"
    TRANSACTIONS = "transactions"

class ConflictResolution(Enum):
    CLIENT_WINS = "client_wins"
    SERVER_WINS = "server_wins"
    MERGE = "merge"
    MANUAL = "manual"
    TIMESTAMP = "timestamp"

@dataclass
class OfflineData:
    id: str
    data_type: DataType
    content: Any
    timestamp: datetime
    checksum: str
    version: int
    user_id: str
    sync_status: SyncStatus
    last_modified: datetime
    size_bytes: int

@dataclass
class SyncOperation:
    id: str
    operation_type: str  # create, update, delete
    data_id: str
    data_type: DataType
    payload: Any
    timestamp: datetime
    retry_count: int
    max_retries: int
    priority: int

class LocalDatabase:
    """Local SQLite database for offline data storage"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.connection = None
        self._initialize_database()
    
    def _initialize_database(self):
        """Initialize local database with required tables"""
        self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
        self.connection.execute("PRAGMA foreign_keys = ON")
        
        # Create tables
        self._create_tables()
    
    def _create_tables(self):
        """Create database tables"""
        tables = [
            """
            CREATE TABLE IF NOT EXISTS offline_data (
                id TEXT PRIMARY KEY,
                data_type TEXT NOT NULL,
                content BLOB,
                timestamp TEXT NOT NULL,
                checksum TEXT NOT NULL,
                version INTEGER NOT NULL,
                user_id TEXT NOT NULL,
                sync_status TEXT NOT NULL,
                last_modified TEXT NOT NULL,
                size_bytes INTEGER NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS sync_operations (
                id TEXT PRIMARY KEY,
                operation_type TEXT NOT NULL,
                data_id TEXT NOT NULL,
                data_type TEXT NOT NULL,
                payload BLOB,
                timestamp TEXT NOT NULL,
                retry_count INTEGER NOT NULL,
                max_retries INTEGER NOT NULL,
                priority INTEGER NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS sync_conflicts (
                id TEXT PRIMARY KEY,
                data_id TEXT NOT NULL,
                local_version INTEGER NOT NULL,
                remote_version INTEGER NOT NULL,
                local_content BLOB,
                remote_content BLOB,
                conflict_timestamp TEXT NOT NULL,
                resolution_strategy TEXT,
                resolved BOOLEAN DEFAULT FALSE
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS cache_entries (
                key TEXT PRIMARY KEY,
                value BLOB,
                expiry_time TEXT,
                access_count INTEGER DEFAULT 0,
                last_accessed TEXT,
                size_bytes INTEGER
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS user_preferences (
                user_id TEXT,
                preference_key TEXT,
                preference_value TEXT,
                PRIMARY KEY (user_id, preference_key)
            )
            """
        ]
        
        for table_sql in tables:
            self.connection.execute(table_sql)
        
        self.connection.commit()
    
    def store_data(self, data: OfflineData) -> bool:
        """Store data in local database"""
        try:
            serialized_content = pickle.dumps(data.content)
            compressed_content = gzip.compress(serialized_content)
            
            self.connection.execute("""
                INSERT OR REPLACE INTO offline_data 
                (id, data_type, content, timestamp, checksum, version, user_id, 
                 sync_status, last_modified, size_bytes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data.id, data.data_type.value, compressed_content,
                data.timestamp.isoformat(), data.checksum, data.version,
                data.user_id, data.sync_status.value,
                data.last_modified.isoformat(), data.size_bytes
            ))
            
            self.connection.commit()
            return True
            
        except Exception as e:
            print(f"Error storing data: {e}")
            return False
    
    def retrieve_data(self, data_id: str) -> Optional[OfflineData]:
        """Retrieve data from local database"""
        try:
            cursor = self.connection.execute("""
                SELECT * FROM offline_data WHERE id = ?
            """, (data_id,))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            # Decompress and deserialize content
            compressed_content = row[2]
            serialized_content = gzip.decompress(compressed_content)
            content = pickle.loads(serialized_content)
            
            return OfflineData(
                id=row[0],
                data_type=DataType(row[1]),
                content=content,
                timestamp=datetime.fromisoformat(row[3]),
                checksum=row[4],
                version=row[5],
                user_id=row[6],
                sync_status=SyncStatus(row[7]),
                last_modified=datetime.fromisoformat(row[8]),
                size_bytes=row[9]
            )
            
        except Exception as e:
            print(f"Error retrieving data: {e}")
            return None
    
    def query_data(self, data_type: Optional[DataType] = None, 
                   user_id: Optional[str] = None,
                   sync_status: Optional[SyncStatus] = None) -> List[OfflineData]:
        """Query data with filters"""
        query = "SELECT * FROM offline_data WHERE 1=1"
        params = []
        
        if data_type:
            query += " AND data_type = ?"
            params.append(data_type.value)
        
        if user_id:
            query += " AND user_id = ?"
            params.append(user_id)
        
        if sync_status:
            query += " AND sync_status = ?"
            params.append(sync_status.value)
        
        cursor = self.connection.execute(query, params)
        rows = cursor.fetchall()
        
        results = []
        for row in rows:
            try:
                compressed_content = row[2]
                serialized_content = gzip.decompress(compressed_content)
                content = pickle.loads(serialized_content)
                
                data = OfflineData(
                    id=row[0],
                    data_type=DataType(row[1]),
                    content=content,
                    timestamp=datetime.fromisoformat(row[3]),
                    checksum=row[4],
                    version=row[5],
                    user_id=row[6],
                    sync_status=SyncStatus(row[7]),
                    last_modified=datetime.fromisoformat(row[8]),
                    size_bytes=row[9]
                )
                results.append(data)
                
            except Exception as e:
                print(f"Error deserializing data: {e}")
                continue
        
        return results
    
    def delete_data(self, data_id: str) -> bool:
        """Delete data from local database"""
        try:
            self.connection.execute("DELETE FROM offline_data WHERE id = ?", (data_id,))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error deleting data: {e}")
            return False
    
    def get_database_size(self) -> int:
        """Get total database size in bytes"""
        return os.path.getsize(self.db_path)
    
    def cleanup_old_data(self, days_old: int = 30):
        """Clean up old data to free space"""
        cutoff_date = datetime.now() - timedelta(days=days_old)
        
        self.connection.execute("""
            DELETE FROM offline_data 
            WHERE last_modified < ? AND sync_status = 'completed'
        """, (cutoff_date.isoformat(),))
        
        self.connection.commit()

class CacheManager:
    """Advanced caching system for offline functionality"""
    
    def __init__(self, db: LocalDatabase, max_cache_size: int = 1024 * 1024 * 1024):  # 1GB default
        self.db = db
        self.max_cache_size = max_cache_size
        self.cache_stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'total_size': 0
        }
    
    def get(self, key: str) -> Optional[Any]:
        """Get item from cache"""
        try:
            cursor = self.db.connection.execute("""
                SELECT value, expiry_time FROM cache_entries WHERE key = ?
            """, (key,))
            
            row = cursor.fetchone()
            if not row:
                self.cache_stats['misses'] += 1
                return None
            
            # Check expiry
            if row[1]:
                expiry_time = datetime.fromisoformat(row[1])
                if datetime.now() > expiry_time:
                    self.delete(key)
                    self.cache_stats['misses'] += 1
                    return None
            
            # Update access statistics
            self.db.connection.execute("""
                UPDATE cache_entries 
                SET access_count = access_count + 1, last_accessed = ?
                WHERE key = ?
            """, (datetime.now().isoformat(), key))
            self.db.connection.commit()
            
            # Deserialize value
            value = pickle.loads(gzip.decompress(row[0]))
            self.cache_stats['hits'] += 1
            return value
            
        except Exception as e:
            print(f"Cache get error: {e}")
            self.cache_stats['misses'] += 1
            return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set item in cache with optional TTL (seconds)"""
        try:
            # Serialize and compress value
            serialized = pickle.dumps(value)
            compressed = gzip.compress(serialized)
            size_bytes = len(compressed)
            
            # Calculate expiry time
            expiry_time = None
            if ttl:
                expiry_time = (datetime.now() + timedelta(seconds=ttl)).isoformat()
            
            # Check cache size and evict if necessary
            self._ensure_cache_space(size_bytes)
            
            self.db.connection.execute("""
                INSERT OR REPLACE INTO cache_entries 
                (key, value, expiry_time, access_count, last_accessed, size_bytes)
                VALUES (?, ?, ?, 0, ?, ?)
            """, (key, compressed, expiry_time, datetime.now().isoformat(), size_bytes))
            
            self.db.connection.commit()
            self.cache_stats['total_size'] += size_bytes
            return True
            
        except Exception as e:
            print(f"Cache set error: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """Delete item from cache"""
        try:
            # Get size before deletion
            cursor = self.db.connection.execute("""
                SELECT size_bytes FROM cache_entries WHERE key = ?
            """, (key,))
            row = cursor.fetchone()
            
            self.db.connection.execute("DELETE FROM cache_entries WHERE key = ?", (key,))
            self.db.connection.commit()
            
            if row:
                self.cache_stats['total_size'] -= row[0]
            
            return True
            
        except Exception as e:
            print(f"Cache delete error: {e}")
            return False
    
    def _ensure_cache_space(self, required_bytes: int):
        """Ensure sufficient cache space by evicting old entries"""
        current_size = self._get_current_cache_size()
        
        if current_size + required_bytes > self.max_cache_size:
            # Evict least recently used entries
            bytes_to_free = (current_size + required_bytes) - self.max_cache_size + (self.max_cache_size * 0.1)  # 10% buffer
            
            cursor = self.db.connection.execute("""
                SELECT key, size_bytes FROM cache_entries 
                ORDER BY last_accessed ASC
            """)
            
            freed_bytes = 0
            keys_to_delete = []
            
            for row in cursor.fetchall():
                keys_to_delete.append(row[0])
                freed_bytes += row[1]
                
                if freed_bytes >= bytes_to_free:
                    break
            
            # Delete selected keys
            for key in keys_to_delete:
                self.delete(key)
                self.cache_stats['evictions'] += 1
    
    def _get_current_cache_size(self) -> int:
        """Get current cache size"""
        cursor = self.db.connection.execute("SELECT SUM(size_bytes) FROM cache_entries")
        result = cursor.fetchone()[0]
        return result if result else 0
    
    def clear(self):
        """Clear all cache entries"""
        self.db.connection.execute("DELETE FROM cache_entries")
        self.db.connection.commit()
        self.cache_stats['total_size'] = 0
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        current_size = self._get_current_cache_size()
        hit_rate = self.cache_stats['hits'] / (self.cache_stats['hits'] + self.cache_stats['misses']) if (self.cache_stats['hits'] + self.cache_stats['misses']) > 0 else 0
        
        return {
            'hits': self.cache_stats['hits'],
            'misses': self.cache_stats['misses'],
            'hit_rate': hit_rate,
            'evictions': self.cache_stats['evictions'],
            'current_size_bytes': current_size,
            'max_size_bytes': self.max_cache_size,
            'utilization': current_size / self.max_cache_size if self.max_cache_size > 0 else 0
        }

class SyncManager:
    """Manages data synchronization between offline and online states"""
    
    def __init__(self, db: LocalDatabase):
        self.db = db
        self.sync_queue = queue.PriorityQueue()
        self.sync_workers = []
        self.is_online = False
        self.sync_callbacks = {}
        self.conflict_handlers = {}
        
        # Start sync workers
        self._start_sync_workers()
    
    def _start_sync_workers(self):
        """Start background sync workers"""
        for i in range(3):  # 3 sync workers
            worker = threading.Thread(target=self._sync_worker, daemon=True)
            worker.start()
            self.sync_workers.append(worker)
    
    def _sync_worker(self):
        """Background worker for processing sync operations"""
        while True:
            try:
                priority, operation = self.sync_queue.get(timeout=1)
                if self.is_online:
                    sel
(Content truncated due to size limit. Use line ranges to read in chunks)
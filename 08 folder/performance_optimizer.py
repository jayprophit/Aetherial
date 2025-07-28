#!/usr/bin/env python3
"""
Performance Optimization System
Advanced performance monitoring and optimization for the unified platform
"""

import asyncio
import aiohttp
import psutil
import time
import logging
import json
import sqlite3
import os
import sys
import threading
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import pandas as pd
from collections import defaultdict, deque
import gc
import resource
import tracemalloc
import cProfile
import pstats
import io

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PerformanceMetrics:
    """Performance metrics collection and analysis"""
    
    def __init__(self, max_samples: int = 1000):
        self.max_samples = max_samples
        self.metrics = {
            'cpu': deque(maxlen=max_samples),
            'memory': deque(maxlen=max_samples),
            'disk_io': deque(maxlen=max_samples),
            'network_io': deque(maxlen=max_samples),
            'response_times': deque(maxlen=max_samples),
            'request_counts': deque(maxlen=max_samples),
            'error_rates': deque(maxlen=max_samples),
            'database_queries': deque(maxlen=max_samples)
        }
        self.timestamps = deque(maxlen=max_samples)
        self.monitoring = False
        self.monitor_thread = None
    
    def start_monitoring(self):
        """Start performance monitoring"""
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        logger.info("Performance monitoring started")
    
    def stop_monitoring(self):
        """Stop performance monitoring"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        logger.info("Performance monitoring stopped")
    
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.monitoring:
            try:
                timestamp = datetime.now()
                
                # System metrics
                cpu_percent = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                disk_io = psutil.disk_io_counters()
                network_io = psutil.net_io_counters()
                
                # Store metrics
                self.timestamps.append(timestamp)
                self.metrics['cpu'].append(cpu_percent)
                self.metrics['memory'].append(memory.percent)
                
                if disk_io:
                    self.metrics['disk_io'].append({
                        'read_bytes': disk_io.read_bytes,
                        'write_bytes': disk_io.write_bytes,
                        'read_count': disk_io.read_count,
                        'write_count': disk_io.write_count
                    })
                
                if network_io:
                    self.metrics['network_io'].append({
                        'bytes_sent': network_io.bytes_sent,
                        'bytes_recv': network_io.bytes_recv,
                        'packets_sent': network_io.packets_sent,
                        'packets_recv': network_io.packets_recv
                    })
                
            except Exception as e:
                logger.warning(f"Monitoring error: {e}")
            
            time.sleep(1)
    
    def add_response_time(self, response_time: float):
        """Add response time measurement"""
        self.metrics['response_times'].append(response_time)
    
    def add_request_count(self, count: int):
        """Add request count"""
        self.metrics['request_counts'].append(count)
    
    def add_error_rate(self, rate: float):
        """Add error rate"""
        self.metrics['error_rates'].append(rate)
    
    def add_database_query_time(self, query_time: float):
        """Add database query time"""
        self.metrics['database_queries'].append(query_time)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get performance statistics"""
        stats = {}
        
        for metric_name, values in self.metrics.items():
            if not values:
                continue
            
            if metric_name in ['disk_io', 'network_io']:
                # Handle complex metrics
                if metric_name == 'disk_io' and values:
                    latest = values[-1]
                    stats[metric_name] = {
                        'latest_read_bytes': latest.get('read_bytes', 0),
                        'latest_write_bytes': latest.get('write_bytes', 0)
                    }
                elif metric_name == 'network_io' and values:
                    latest = values[-1]
                    stats[metric_name] = {
                        'latest_bytes_sent': latest.get('bytes_sent', 0),
                        'latest_bytes_recv': latest.get('bytes_recv', 0)
                    }
            else:
                # Handle simple numeric metrics
                numeric_values = [v for v in values if isinstance(v, (int, float))]
                if numeric_values:
                    stats[metric_name] = {
                        'current': numeric_values[-1],
                        'average': np.mean(numeric_values),
                        'min': np.min(numeric_values),
                        'max': np.max(numeric_values),
                        'std': np.std(numeric_values),
                        'count': len(numeric_values)
                    }
        
        return stats
    
    def get_alerts(self) -> List[Dict[str, Any]]:
        """Get performance alerts"""
        alerts = []
        stats = self.get_statistics()
        
        # CPU alerts
        if 'cpu' in stats and stats['cpu']['current'] > 80:
            alerts.append({
                'type': 'cpu_high',
                'severity': 'warning' if stats['cpu']['current'] < 90 else 'critical',
                'message': f"High CPU usage: {stats['cpu']['current']:.1f}%",
                'value': stats['cpu']['current']
            })
        
        # Memory alerts
        if 'memory' in stats and stats['memory']['current'] > 80:
            alerts.append({
                'type': 'memory_high',
                'severity': 'warning' if stats['memory']['current'] < 90 else 'critical',
                'message': f"High memory usage: {stats['memory']['current']:.1f}%",
                'value': stats['memory']['current']
            })
        
        # Response time alerts
        if 'response_times' in stats and stats['response_times']['average'] > 2.0:
            alerts.append({
                'type': 'response_time_high',
                'severity': 'warning' if stats['response_times']['average'] < 5.0 else 'critical',
                'message': f"High response time: {stats['response_times']['average']:.2f}s",
                'value': stats['response_times']['average']
            })
        
        # Error rate alerts
        if 'error_rates' in stats and stats['error_rates']['average'] > 0.05:
            alerts.append({
                'type': 'error_rate_high',
                'severity': 'warning' if stats['error_rates']['average'] < 0.1 else 'critical',
                'message': f"High error rate: {stats['error_rates']['average']:.2%}",
                'value': stats['error_rates']['average']
            })
        
        return alerts

class DatabaseOptimizer:
    """Database performance optimization"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.query_stats = defaultdict(list)
    
    def analyze_queries(self) -> Dict[str, Any]:
        """Analyze database query performance"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get database statistics
            cursor.execute("PRAGMA database_list")
            databases = cursor.fetchall()
            
            cursor.execute("PRAGMA table_list")
            tables = cursor.fetchall()
            
            # Analyze each table
            table_stats = {}
            for table in tables:
                table_name = table[1]  # table name is in second column
                
                try:
                    # Get table info
                    cursor.execute(f"PRAGMA table_info({table_name})")
                    columns = cursor.fetchall()
                    
                    # Get row count
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                    row_count = cursor.fetchone()[0]
                    
                    # Get index info
                    cursor.execute(f"PRAGMA index_list({table_name})")
                    indexes = cursor.fetchall()
                    
                    table_stats[table_name] = {
                        'columns': len(columns),
                        'rows': row_count,
                        'indexes': len(indexes),
                        'column_details': columns,
                        'index_details': indexes
                    }
                    
                except Exception as e:
                    logger.warning(f"Error analyzing table {table_name}: {e}")
            
            conn.close()
            
            return {
                'databases': databases,
                'table_count': len(tables),
                'table_stats': table_stats,
                'total_tables': len(table_stats)
            }
            
        except Exception as e:
            logger.error(f"Database analysis failed: {e}")
            return {}
    
    def optimize_database(self) -> Dict[str, Any]:
        """Optimize database performance"""
        optimizations = []
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Run VACUUM to reclaim space
            cursor.execute("VACUUM")
            optimizations.append("VACUUM completed")
            
            # Analyze tables for query optimization
            cursor.execute("ANALYZE")
            optimizations.append("ANALYZE completed")
            
            # Update database statistics
            cursor.execute("PRAGMA optimize")
            optimizations.append("PRAGMA optimize completed")
            
            conn.close()
            
            return {
                'success': True,
                'optimizations': optimizations,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Database optimization failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def suggest_indexes(self, table_stats: Dict[str, Any]) -> List[str]:
        """Suggest database indexes for optimization"""
        suggestions = []
        
        for table_name, stats in table_stats.items():
            # Suggest indexes for tables with many rows but few indexes
            if stats['rows'] > 1000 and stats['indexes'] < 2:
                suggestions.append(f"Consider adding indexes to table '{table_name}' (rows: {stats['rows']}, indexes: {stats['indexes']})")
            
            # Suggest composite indexes for tables with multiple columns
            if stats['columns'] > 5 and stats['indexes'] < stats['columns'] // 3:
                suggestions.append(f"Consider composite indexes for table '{table_name}' with {stats['columns']} columns")
        
        return suggestions

class CacheOptimizer:
    """Cache optimization and management"""
    
    def __init__(self):
        self.cache_stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'memory_usage': 0
        }
        self.cache_data = {}
        self.access_times = {}
        self.max_size = 1000  # Maximum cache entries
    
    def get_cache_statistics(self) -> Dict[str, Any]:
        """Get cache performance statistics"""
        total_requests = self.cache_stats['hits'] + self.cache_stats['misses']
        hit_rate = self.cache_stats['hits'] / total_requests if total_requests > 0 else 0
        
        return {
            'hit_rate': hit_rate,
            'total_requests': total_requests,
            'cache_size': len(self.cache_data),
            'memory_usage_mb': self.cache_stats['memory_usage'] / (1024 * 1024),
            'evictions': self.cache_stats['evictions'],
            **self.cache_stats
        }
    
    def optimize_cache(self) -> Dict[str, Any]:
        """Optimize cache performance"""
        optimizations = []
        
        # Remove expired entries
        current_time = time.time()
        expired_keys = []
        
        for key, access_time in self.access_times.items():
            if current_time - access_time > 3600:  # 1 hour TTL
                expired_keys.append(key)
        
        for key in expired_keys:
            if key in self.cache_data:
                del self.cache_data[key]
            if key in self.access_times:
                del self.access_times[key]
        
        if expired_keys:
            optimizations.append(f"Removed {len(expired_keys)} expired cache entries")
        
        # Implement LRU eviction if cache is too large
        if len(self.cache_data) > self.max_size:
            # Sort by access time and remove oldest
            sorted_items = sorted(self.access_times.items(), key=lambda x: x[1])
            items_to_remove = len(self.cache_data) - self.max_size
            
            for key, _ in sorted_items[:items_to_remove]:
                if key in self.cache_data:
                    del self.cache_data[key]
                if key in self.access_times:
                    del self.access_times[key]
                self.cache_stats['evictions'] += 1
            
            optimizations.append(f"Evicted {items_to_remove} LRU cache entries")
        
        # Force garbage collection
        gc.collect()
        optimizations.append("Garbage collection completed")
        
        return {
            'optimizations': optimizations,
            'cache_stats': self.get_cache_statistics(),
            'timestamp': datetime.now().isoformat()
        }

class MemoryOptimizer:
    """Memory usage optimization"""
    
    def __init__(self):
        self.memory_snapshots = []
        tracemalloc.start()
    
    def take_snapshot(self) -> Dict[str, Any]:
        """Take memory snapshot"""
        snapshot = tracemalloc.take_snapshot()
        top_stats = snapshot.statistics('lineno')
        
        # Get top 10 memory consumers
        top_10 = []
        for stat in top_stats[:10]:
            top_10.append({
                'filename': stat.traceback.format()[0],
                'size_mb': stat.size / (1024 * 1024),
                'count': stat.count
            })
        
        # System memory info
        memory_info = psutil.virtual_memory()
        
        snapshot_data = {
            'timestamp': datetime.now().isoformat(),
            'total_memory_mb': memory_info.total / (1024 * 1024),
            'available_memory_mb': memory_info.available / (1024 * 1024),
            'used_memory_mb': memory_info.used / (1024 * 1024),
            'memory_percent': memory_info.percent,
            'top_consumers': top_10,
            'total_traced_mb': sum(stat.size for stat in top_stats) / (1024 * 1024)
        }
        
        self.memory_snapshots.append(snapshot_data)
        return snapshot_data
    
    def optimize_memory(self) -> Dict[str, Any]:
        """Optimize memory usage"""
        optimiz
(Content truncated due to size limit. Use line ranges to read in chunks)
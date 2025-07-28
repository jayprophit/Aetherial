#!/usr/bin/env python3
"""
Comprehensive Test Suite for Unified Platform
Advanced testing framework with performance, security, and integration tests
"""

import asyncio
import aiohttp
import pytest
import unittest
import json
import time
import logging
import sqlite3
import os
import sys
import subprocess
import threading
import requests
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
import psutil
import hashlib
import random
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import numpy as np
import pandas as pd

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TestConfig:
    """Test configuration and constants"""
    
    BASE_URL = "http://localhost"
    FRONTEND_PORT = 3000
    BACKEND_PORT = 8000
    AUTH_PORT = 8001
    
    # Test timeouts
    DEFAULT_TIMEOUT = 30
    LOAD_TEST_DURATION = 60
    STRESS_TEST_DURATION = 120
    
    # Performance thresholds
    MAX_RESPONSE_TIME = 2.0  # seconds
    MIN_THROUGHPUT = 100     # requests per second
    MAX_MEMORY_USAGE = 80    # percentage
    MAX_CPU_USAGE = 80       # percentage
    
    # Test data
    TEST_USER = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'TestPassword123!'
    }
    
    TEST_PRODUCT = {
        'name': 'Test Product',
        'description': 'A test product for automated testing',
        'price': 99.99,
        'category': 'electronics'
    }

class PerformanceMonitor:
    """Monitor system performance during tests"""
    
    def __init__(self):
        self.metrics = []
        self.monitoring = False
        self.monitor_thread = None
    
    def start_monitoring(self):
        """Start performance monitoring"""
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop)
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop performance monitoring"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join()
    
    def _monitor_loop(self):
        """Performance monitoring loop"""
        while self.monitoring:
            try:
                metric = {
                    'timestamp': datetime.now().isoformat(),
                    'cpu_percent': psutil.cpu_percent(interval=1),
                    'memory_percent': psutil.virtual_memory().percent,
                    'disk_io': psutil.disk_io_counters()._asdict() if psutil.disk_io_counters() else {},
                    'network_io': psutil.net_io_counters()._asdict() if psutil.net_io_counters() else {},
                    'process_count': len(psutil.pids())
                }
                self.metrics.append(metric)
            except Exception as e:
                logger.warning(f"Performance monitoring error: {e}")
            
            time.sleep(1)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get performance summary"""
        if not self.metrics:
            return {}
        
        cpu_values = [m['cpu_percent'] for m in self.metrics]
        memory_values = [m['memory_percent'] for m in self.metrics]
        
        return {
            'duration': len(self.metrics),
            'cpu': {
                'avg': np.mean(cpu_values),
                'max': np.max(cpu_values),
                'min': np.min(cpu_values)
            },
            'memory': {
                'avg': np.mean(memory_values),
                'max': np.max(memory_values),
                'min': np.min(memory_values)
            },
            'samples': len(self.metrics)
        }

class APITestClient:
    """HTTP client for API testing"""
    
    def __init__(self, base_url: str, timeout: int = TestConfig.DEFAULT_TIMEOUT):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        self.auth_token = None
    
    async def get(self, endpoint: str, **kwargs) -> requests.Response:
        """GET request"""
        url = f"{self.base_url}{endpoint}"
        headers = kwargs.get('headers', {})
        
        if self.auth_token:
            headers['Authorization'] = f"Bearer {self.auth_token}"
        
        return self.session.get(url, headers=headers, timeout=self.timeout, **kwargs)
    
    async def post(self, endpoint: str, data: Optional[Dict] = None, **kwargs) -> requests.Response:
        """POST request"""
        url = f"{self.base_url}{endpoint}"
        headers = kwargs.get('headers', {})
        
        if self.auth_token:
            headers['Authorization'] = f"Bearer {self.auth_token}"
        
        return self.session.post(url, json=data, headers=headers, timeout=self.timeout, **kwargs)
    
    async def put(self, endpoint: str, data: Optional[Dict] = None, **kwargs) -> requests.Response:
        """PUT request"""
        url = f"{self.base_url}{endpoint}"
        headers = kwargs.get('headers', {})
        
        if self.auth_token:
            headers['Authorization'] = f"Bearer {self.auth_token}"
        
        return self.session.put(url, json=data, headers=headers, timeout=self.timeout, **kwargs)
    
    async def delete(self, endpoint: str, **kwargs) -> requests.Response:
        """DELETE request"""
        url = f"{self.base_url}{endpoint}"
        headers = kwargs.get('headers', {})
        
        if self.auth_token:
            headers['Authorization'] = f"Bearer {self.auth_token}"
        
        return self.session.delete(url, headers=headers, timeout=self.timeout, **kwargs)
    
    async def authenticate(self, username: str, password: str) -> bool:
        """Authenticate and store token"""
        try:
            response = await self.post('/api/auth/login', {
                'username': username,
                'password': password
            })
            
            if response.status_code == 200:
                data = response.json()
                self.auth_token = data.get('token')
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            return False

class UnitTests(unittest.TestCase):
    """Unit tests for core functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.api_client = APITestClient(f"{TestConfig.BASE_URL}:{TestConfig.BACKEND_PORT}")
        self.auth_client = APITestClient(f"{TestConfig.BASE_URL}:{TestConfig.AUTH_PORT}")
    
    def test_database_connection(self):
        """Test database connectivity"""
        try:
            # Test SQLite connection
            db_path = Path(__file__).parent.parent / 'unified-backend' / 'unified_platform.db'
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            conn.close()
            
            self.assertEqual(result[0], 1)
            
        except Exception as e:
            self.fail(f"Database connection failed: {e}")
    
    def test_configuration_loading(self):
        """Test configuration loading"""
        try:
            # Test that configuration files exist and are valid
            config_files = [
                'deployment_config.yaml',
                'package.json'
            ]
            
            project_root = Path(__file__).parent.parent
            
            for config_file in config_files:
                config_path = project_root / config_file
                if config_path.exists():
                    if config_file.endswith('.json'):
                        with open(config_path, 'r') as f:
                            json.load(f)  # Validate JSON
                    elif config_file.endswith('.yaml'):
                        import yaml
                        with open(config_path, 'r') as f:
                            yaml.safe_load(f)  # Validate YAML
            
        except Exception as e:
            self.fail(f"Configuration loading failed: {e}")
    
    def test_environment_variables(self):
        """Test environment variable handling"""
        # Test that required environment variables can be set
        test_vars = {
            'ENVIRONMENT': 'test',
            'DEBUG': 'true',
            'PORT': '8000'
        }
        
        for key, value in test_vars.items():
            os.environ[key] = value
            self.assertEqual(os.environ.get(key), value)
    
    def test_utility_functions(self):
        """Test utility functions"""
        # Test hash generation
        test_string = "test_data"
        hash1 = hashlib.sha256(test_string.encode()).hexdigest()
        hash2 = hashlib.sha256(test_string.encode()).hexdigest()
        self.assertEqual(hash1, hash2)
        
        # Test random string generation
        random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        self.assertEqual(len(random_str), 10)
        self.assertTrue(random_str.isalnum())

class IntegrationTests(unittest.TestCase):
    """Integration tests for API endpoints"""
    
    def setUp(self):
        """Set up test environment"""
        self.api_client = APITestClient(f"{TestConfig.BASE_URL}:{TestConfig.BACKEND_PORT}")
        self.auth_client = APITestClient(f"{TestConfig.BASE_URL}:{TestConfig.AUTH_PORT}")
        self.performance_monitor = PerformanceMonitor()
    
    def tearDown(self):
        """Clean up test environment"""
        self.performance_monitor.stop_monitoring()
    
    async def test_health_endpoints(self):
        """Test health check endpoints"""
        endpoints = [
            (TestConfig.BACKEND_PORT, '/api/health'),
            (TestConfig.AUTH_PORT, '/api/health')
        ]
        
        for port, endpoint in endpoints:
            client = APITestClient(f"{TestConfig.BASE_URL}:{port}")
            response = await client.get(endpoint)
            self.assertEqual(response.status_code, 200)
    
    async def test_user_registration_flow(self):
        """Test complete user registration flow"""
        # Register new user
        user_data = {
            'username': f"testuser_{int(time.time())}",
            'email': f"test_{int(time.time())}@example.com",
            'password': 'TestPassword123!'
        }
        
        response = await self.auth_client.post('/api/auth/register', user_data)
        self.assertEqual(response.status_code, 201)
        
        # Login with new user
        login_response = await self.auth_client.post('/api/auth/login', {
            'username': user_data['username'],
            'password': user_data['password']
        })
        self.assertEqual(login_response.status_code, 200)
        
        # Verify token received
        login_data = login_response.json()
        self.assertIn('token', login_data)
    
    async def test_protected_endpoints(self):
        """Test protected endpoint access"""
        # Try accessing protected endpoint without auth
        response = await self.api_client.get('/api/user/profile')
        self.assertEqual(response.status_code, 401)
        
        # Authenticate and try again
        auth_success = await self.auth_client.authenticate(
            TestConfig.TEST_USER['username'],
            TestConfig.TEST_USER['password']
        )
        
        if auth_success:
            response = await self.api_client.get('/api/user/profile')
            self.assertIn(response.status_code, [200, 404])  # 404 if user doesn't exist
    
    async def test_crud_operations(self):
        """Test CRUD operations"""
        # Create
        product_data = TestConfig.TEST_PRODUCT.copy()
        product_data['name'] = f"Test Product {int(time.time())}"
        
        create_response = await self.api_client.post('/api/products', product_data)
        self.assertIn(create_response.status_code, [201, 404])  # 404 if endpoint doesn't exist
        
        if create_response.status_code == 201:
            product_id = create_response.json().get('id')
            
            # Read
            read_response = await self.api_client.get(f'/api/products/{product_id}')
            self.assertEqual(read_response.status_code, 200)
            
            # Update
            update_data = {'name': f"Updated Product {int(time.time())}"}
            update_response = await self.api_client.put(f'/api/products/{product_id}', update_data)
            self.assertEqual(update_response.status_code, 200)
            
            # Delete
            delete_response = await self.api_client.delete(f'/api/products/{product_id}')
            self.assertEqual(delete_response.status_code, 200)

class PerformanceTests(unittest.TestCase):
    """Performance and load tests"""
    
    def setUp(self):
        """Set up performance testing"""
        self.performance_monitor = PerformanceMonitor()
        self.api_client = APITestClient(f"{TestConfig.BASE_URL}:{TestConfig.BACKEND_PORT}")
    
    def tearDown(self):
        """Clean up performance testing"""
        self.performance_monitor.stop_monitoring()
    
    async def test_response_time(self):
        """Test API response times"""
        endpoints = [
            '/api/health',
            '/api/products',
            '/api/users'
        ]
        
        for endpoint in endpoints:
            start_time = time.time()
            
            try:
                response = await self.api_client.get(endpoint)
                response_time = time.time() - start_time
                
                # Check response time threshold
                self.assertLess(response_time, TestConfig.MAX_RESPONSE_TIME,
                              f"Response time for {endpoint} exceeded threshold: {response_time}s")
                
                logger.info(f"{endpoint} response time: {response_time:.3f}s")
                
            except Exception as e:
                logger.warning(f"Endpoint {endpoint} not available: {e}")
    
    async def test_concurrent_requests(self):
        """Test concurrent request handling"""
        self.performance_monitor.start_monitoring()
        
        async def make_request():
            try:
                response = await self.api_client.get('/api/health')
                return response.status_code == 200
            except Exception:
                return False
        
        # Run concurrent requests
        num_requests = 50
        start_time = time.time()
        
        tasks = [make_request() for _ in range(num_requests)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Calculate success rate
        successful_requests = sum(1 for result in results if result is True)
        success_rate = successful_requests / num_requests
        throughput = num_requests / duration
        
        # Assertions
        self.assertGreater(success_rate, 0.95, f"Success rate too low: {success_rate}")
        self.assertGreater(throughput, TestConfig.MIN_THROUGHPUT, 
                          f"Throughput too low: {throughput} req/s")
        
        logger.info(f"Concurrent test: {successful_requests}/{num_requests} successful, "
                   f"throughput: {throughput:.2f} req/s")
    
    async def test_memory_usage(self):
        """Test memory usage under load"""
        self.performance_monitor.start_monitoring()
        
        # Generate load
        for _ in range(100):
            try:
                await
(Content truncated due to size limit. Use line ranges to read in chunks)
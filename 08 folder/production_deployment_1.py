#!/usr/bin/env python3
"""
Production Deployment System
Comprehensive deployment and optimization for the unified platform
"""

import os
import sys
import json
import subprocess
import shutil
import time
import logging
import asyncio
import aiohttp
import psutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import yaml
import docker
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import sqlite3
import hashlib
import zipfile
import tarfile

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('deployment.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class ProductionDeployment:
    """
    Production deployment system for the unified platform
    """
    
    def __init__(self, config_path: str = "deployment_config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
        self.project_root = Path(__file__).parent.parent
        self.deployment_id = self._generate_deployment_id()
        self.docker_client = None
        
        # Initialize Docker client if available
        try:
            self.docker_client = docker.from_env()
            logger.info("Docker client initialized successfully")
        except Exception as e:
            logger.warning(f"Docker not available: {e}")
        
        # Deployment paths
        self.paths = {
            'frontend': self.project_root / 'frontend',
            'backend': self.project_root / 'unified-backend',
            'auth_backend': self.project_root / 'auth-backend',
            'blockchain': self.project_root / 'unified-backend' / 'src' / 'blockchain',
            'ai': self.project_root / 'unified-backend' / 'src' / 'ai',
            'build': self.project_root / 'build',
            'dist': self.project_root / 'dist',
            'logs': self.project_root / 'logs',
            'backups': self.project_root / 'backups'
        }
        
        # Create necessary directories
        for path in self.paths.values():
            path.mkdir(parents=True, exist_ok=True)
    
    def _load_config(self) -> Dict[str, Any]:
        """Load deployment configuration"""
        default_config = {
            'environment': 'production',
            'version': '1.0.0',
            'services': {
                'frontend': {
                    'port': 3000,
                    'build_command': 'npm run build',
                    'start_command': 'npm start',
                    'health_check': '/health'
                },
                'backend': {
                    'port': 8000,
                    'build_command': 'pip install -r requirements.txt',
                    'start_command': 'python src/main.py',
                    'health_check': '/api/health'
                },
                'auth_backend': {
                    'port': 8001,
                    'build_command': 'pip install -r requirements.txt',
                    'start_command': 'python src/main.py',
                    'health_check': '/api/health'
                }
            },
            'database': {
                'type': 'sqlite',
                'path': 'unified_platform.db',
                'backup_interval': 3600  # 1 hour
            },
            'monitoring': {
                'enabled': True,
                'metrics_port': 9090,
                'log_level': 'INFO'
            },
            'security': {
                'ssl_enabled': True,
                'cors_origins': ['*'],
                'rate_limiting': True,
                'max_requests_per_minute': 1000
            },
            'performance': {
                'enable_caching': True,
                'cache_ttl': 3600,
                'compression': True,
                'minification': True
            },
            'deployment': {
                'strategy': 'rolling',
                'max_unavailable': 1,
                'health_check_timeout': 30,
                'rollback_on_failure': True
            }
        }
        
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    user_config = yaml.safe_load(f)
                    default_config.update(user_config)
            except Exception as e:
                logger.warning(f"Failed to load config file: {e}")
        
        return default_config
    
    def _generate_deployment_id(self) -> str:
        """Generate unique deployment ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"deploy_{timestamp}_{hashlib.md5(str(time.time()).encode()).hexdigest()[:8]}"
    
    async def run_deployment(self) -> bool:
        """Run complete deployment process"""
        logger.info(f"Starting deployment {self.deployment_id}")
        
        try:
            # Pre-deployment checks
            if not await self._pre_deployment_checks():
                logger.error("Pre-deployment checks failed")
                return False
            
            # Create backup
            if not await self._create_backup():
                logger.error("Backup creation failed")
                return False
            
            # Build applications
            if not await self._build_applications():
                logger.error("Application build failed")
                return False
            
            # Run tests
            if not await self._run_tests():
                logger.error("Tests failed")
                return False
            
            # Deploy services
            if not await self._deploy_services():
                logger.error("Service deployment failed")
                return False
            
            # Post-deployment verification
            if not await self._post_deployment_verification():
                logger.error("Post-deployment verification failed")
                await self._rollback_deployment()
                return False
            
            # Setup monitoring
            await self._setup_monitoring()
            
            # Cleanup old deployments
            await self._cleanup_old_deployments()
            
            logger.info(f"Deployment {self.deployment_id} completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Deployment failed: {e}")
            await self._rollback_deployment()
            return False
    
    async def _pre_deployment_checks(self) -> bool:
        """Run pre-deployment checks"""
        logger.info("Running pre-deployment checks...")
        
        checks = [
            self._check_system_resources,
            self._check_dependencies,
            self._check_database_connectivity,
            self._check_external_services,
            self._validate_configuration
        ]
        
        for check in checks:
            try:
                if not await check():
                    return False
            except Exception as e:
                logger.error(f"Check failed: {e}")
                return False
        
        logger.info("All pre-deployment checks passed")
        return True
    
    async def _check_system_resources(self) -> bool:
        """Check system resources"""
        logger.info("Checking system resources...")
        
        # Check CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        if cpu_percent > 80:
            logger.warning(f"High CPU usage: {cpu_percent}%")
        
        # Check memory usage
        memory = psutil.virtual_memory()
        if memory.percent > 80:
            logger.warning(f"High memory usage: {memory.percent}%")
        
        # Check disk space
        disk = psutil.disk_usage('/')
        if disk.percent > 80:
            logger.error(f"Low disk space: {disk.percent}% used")
            return False
        
        # Check network connectivity
        try:
            response = requests.get('https://www.google.com', timeout=5)
            if response.status_code != 200:
                logger.error("Network connectivity check failed")
                return False
        except Exception as e:
            logger.error(f"Network check failed: {e}")
            return False
        
        logger.info("System resources check passed")
        return True
    
    async def _check_dependencies(self) -> bool:
        """Check required dependencies"""
        logger.info("Checking dependencies...")
        
        # Check Python dependencies
        try:
            import flask
            import fastapi
            import sqlite3
            import numpy
            import pandas
            logger.info("Python dependencies check passed")
        except ImportError as e:
            logger.error(f"Missing Python dependency: {e}")
            return False
        
        # Check Node.js dependencies
        try:
            result = subprocess.run(['node', '--version'], capture_output=True, text=True)
            if result.returncode != 0:
                logger.error("Node.js not found")
                return False
            logger.info(f"Node.js version: {result.stdout.strip()}")
        except Exception as e:
            logger.error(f"Node.js check failed: {e}")
            return False
        
        # Check npm dependencies
        try:
            result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
            if result.returncode != 0:
                logger.error("npm not found")
                return False
            logger.info(f"npm version: {result.stdout.strip()}")
        except Exception as e:
            logger.error(f"npm check failed: {e}")
            return False
        
        return True
    
    async def _check_database_connectivity(self) -> bool:
        """Check database connectivity"""
        logger.info("Checking database connectivity...")
        
        try:
            db_path = self.paths['backend'] / self.config['database']['path']
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            conn.close()
            logger.info("Database connectivity check passed")
            return True
        except Exception as e:
            logger.error(f"Database connectivity check failed: {e}")
            return False
    
    async def _check_external_services(self) -> bool:
        """Check external service dependencies"""
        logger.info("Checking external services...")
        
        # Add checks for external APIs, services, etc.
        # For now, just return True
        return True
    
    async def _validate_configuration(self) -> bool:
        """Validate deployment configuration"""
        logger.info("Validating configuration...")
        
        required_keys = ['environment', 'version', 'services']
        for key in required_keys:
            if key not in self.config:
                logger.error(f"Missing required config key: {key}")
                return False
        
        # Validate service configurations
        for service_name, service_config in self.config['services'].items():
            required_service_keys = ['port', 'start_command']
            for key in required_service_keys:
                if key not in service_config:
                    logger.error(f"Missing required service config key: {service_name}.{key}")
                    return False
        
        logger.info("Configuration validation passed")
        return True
    
    async def _create_backup(self) -> bool:
        """Create backup of current deployment"""
        logger.info("Creating backup...")
        
        try:
            backup_dir = self.paths['backups'] / f"backup_{self.deployment_id}"
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            # Backup database
            db_path = self.paths['backend'] / self.config['database']['path']
            if db_path.exists():
                shutil.copy2(db_path, backup_dir / 'database.db')
            
            # Backup configuration files
            config_files = [
                'deployment_config.yaml',
                'package.json',
                'requirements.txt'
            ]
            
            for config_file in config_files:
                file_path = self.project_root / config_file
                if file_path.exists():
                    shutil.copy2(file_path, backup_dir / config_file)
            
            # Create archive
            archive_path = self.paths['backups'] / f"backup_{self.deployment_id}.tar.gz"
            with tarfile.open(archive_path, 'w:gz') as tar:
                tar.add(backup_dir, arcname=f"backup_{self.deployment_id}")
            
            # Remove temporary backup directory
            shutil.rmtree(backup_dir)
            
            logger.info(f"Backup created: {archive_path}")
            return True
            
        except Exception as e:
            logger.error(f"Backup creation failed: {e}")
            return False
    
    async def _build_applications(self) -> bool:
        """Build all applications"""
        logger.info("Building applications...")
        
        build_tasks = []
        
        # Build frontend
        if self.paths['frontend'].exists():
            build_tasks.append(self._build_frontend())
        
        # Build backend services
        for service_name in ['backend', 'auth_backend']:
            if self.paths[service_name].exists():
                build_tasks.append(self._build_backend_service(service_name))
        
        # Run builds concurrently
        results = await asyncio.gather(*build_tasks, return_exceptions=True)
        
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Build task {i} failed: {result}")
                return False
            elif not result:
                logger.error(f"Build task {i} returned False")
                return False
        
        logger.info("All applications built successfully")
        return True
    
    async def _build_frontend(self) -> bool:
        """Build frontend application"""
        logger.info("Building frontend...")
        
        try:
            # Install dependencies
            result = await self._run_command(
                ['npm', 'install'],
                cwd=self.paths['frontend']
            )
            if result.returncode != 0:
                logger.error(f"Frontend dependency installation failed: {result.stderr}")
                return False
            
            # Build application
            result = await self._run_command(
                ['npm', 'run', 'build'],
                cwd=self.paths['frontend']
            )
            if result.returncode != 0:
                logger.error(f"Frontend build failed: {result.stderr}")
                return False
            
            logger.info("Frontend build completed")
            return True
            
        except Exception as e:
            logger.error(f"Frontend build error: {e}")
            return False
    
    async def _build_backend_service(self, service_name: str) -> bool:
        """Build backend service"""
        logger.info(f"Building {service_name}...")
        
        try:
            service_path = self.paths[service_name]
            requirements_file = service_path / 'requirements.txt'
            
            if requirements_file.exists():
                # Install Python dependencies
                result = await self._run_command(
                    [sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'],
                    cwd=service_path
                )
                if result.returncode != 0:
  
(Content truncated due to size limit. Use line ranges to read in chunks)
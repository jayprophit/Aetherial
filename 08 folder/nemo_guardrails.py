"""
NeMo Guardrails Implementation for AI Safety
Advanced content filtering, bias detection, and safety guardrails
"""

import asyncio
import json
import logging
import re
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union, Tuple, Set
from dataclasses import dataclass, field
from enum import Enum
import numpy as np
import sqlite3
import os
from pathlib import Path
import hashlib
import pickle
from collections import defaultdict, Counter
import threading
import time

# NLP and ML imports
try:
    import torch
    import torch.nn as nn
    from transformers import (
        AutoTokenizer, AutoModelForSequenceClassification,
        pipeline, AutoModel
    )
    from sentence_transformers import SentenceTransformer
    import spacy
    ADVANCED_NLP_AVAILABLE = True
except ImportError:
    logging.warning("Advanced NLP libraries not available, using basic implementation")
    ADVANCED_NLP_AVAILABLE = False

class GuardrailType(Enum):
    CONTENT_FILTER = "content_filter"
    BIAS_DETECTION = "bias_detection"
    TOXICITY_DETECTION = "toxicity_detection"
    PRIVACY_PROTECTION = "privacy_protection"
    FACTUAL_ACCURACY = "factual_accuracy"
    ETHICAL_COMPLIANCE = "ethical_compliance"
    SAFETY_CHECK = "safety_check"
    HALLUCINATION_DETECTION = "hallucination_detection"

class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ActionType(Enum):
    ALLOW = "allow"
    WARN = "warn"
    BLOCK = "block"
    MODIFY = "modify"
    ESCALATE = "escalate"

@dataclass
class GuardrailRule:
    id: str
    name: str
    description: str
    guardrail_type: GuardrailType
    pattern: Optional[str] = None
    keywords: List[str] = field(default_factory=list)
    threshold: float = 0.5
    risk_level: RiskLevel = RiskLevel.MEDIUM
    action: ActionType = ActionType.WARN
    enabled: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)

@dataclass
class GuardrailResult:
    rule_id: str
    rule_name: str
    guardrail_type: GuardrailType
    triggered: bool
    confidence: float
    risk_level: RiskLevel
    action: ActionType
    message: str
    details: Dict[str, Any] = field(default_factory=dict)
    suggestions: List[str] = field(default_factory=list)

@dataclass
class ContentAnalysis:
    content_id: str
    content_hash: str
    analysis_results: List[GuardrailResult]
    overall_risk: RiskLevel
    recommended_action: ActionType
    safe_to_proceed: bool
    modified_content: Optional[str] = None
    analysis_time: float = 0.0
    created_at: datetime = field(default_factory=datetime.utcnow)

class NeMoGuardrails:
    """
    NeMo Guardrails implementation for comprehensive AI safety
    """
    
    def __init__(self, data_dir: str = "./guardrails_data"):
        self.data_dir = data_dir
        self.db_path = os.path.join(data_dir, "guardrails.db")
        
        # Initialize directories
        os.makedirs(data_dir, exist_ok=True)
        
        # Initialize database
        self._init_database()
        
        # Load models
        self.models = {}
        self.tokenizers = {}
        self._load_models()
        
        # Load rules
        self.rules = {}
        self._load_rules()
        
        # Content patterns and keywords
        self._init_patterns()
        
        # Statistics
        self.stats = {
            "total_analyses": 0,
            "blocked_content": 0,
            "warnings_issued": 0,
            "modifications_made": 0
        }
        
        # Background monitoring
        self.is_running = True
        self._start_background_monitoring()
    
    def _init_database(self):
        """Initialize SQLite database for guardrails"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Guardrail rules table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS guardrail_rules (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                guardrail_type TEXT NOT NULL,
                pattern TEXT,
                keywords TEXT,
                threshold REAL NOT NULL,
                risk_level TEXT NOT NULL,
                action TEXT NOT NULL,
                enabled BOOLEAN NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Content analyses table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS content_analyses (
                id TEXT PRIMARY KEY,
                content_id TEXT NOT NULL,
                content_hash TEXT NOT NULL,
                analysis_results TEXT NOT NULL,
                overall_risk TEXT NOT NULL,
                recommended_action TEXT NOT NULL,
                safe_to_proceed BOOLEAN NOT NULL,
                modified_content TEXT,
                analysis_time REAL NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Violation logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS violation_logs (
                id TEXT PRIMARY KEY,
                content_id TEXT NOT NULL,
                rule_id TEXT NOT NULL,
                guardrail_type TEXT NOT NULL,
                risk_level TEXT NOT NULL,
                action_taken TEXT NOT NULL,
                confidence REAL NOT NULL,
                details TEXT,
                user_id TEXT,
                session_id TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Model performance table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS model_performance (
                id TEXT PRIMARY KEY,
                model_name TEXT NOT NULL,
                guardrail_type TEXT NOT NULL,
                accuracy REAL,
                precision_score REAL,
                recall REAL,
                f1_score REAL,
                false_positive_rate REAL,
                false_negative_rate REAL,
                last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Feedback table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_feedback (
                id TEXT PRIMARY KEY,
                content_id TEXT NOT NULL,
                analysis_id TEXT NOT NULL,
                user_id TEXT,
                feedback_type TEXT NOT NULL,
                is_correct BOOLEAN,
                comments TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create indexes
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_analyses_content ON content_analyses(content_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_analyses_hash ON content_analyses(content_hash)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_violations_content ON violation_logs(content_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_violations_rule ON violation_logs(rule_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_violations_type ON violation_logs(guardrail_type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_feedback_content ON user_feedback(content_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_performance_model ON model_performance(model_name)')
        
        conn.commit()
        conn.close()
    
    def _load_models(self):
        """Load pre-trained models for content analysis"""
        try:
            if ADVANCED_NLP_AVAILABLE:
                # Toxicity detection model
                self.models['toxicity'] = pipeline(
                    "text-classification",
                    model="unitary/toxic-bert",
                    device=0 if torch.cuda.is_available() else -1
                )
                
                # Bias detection model
                self.models['bias'] = pipeline(
                    "text-classification",
                    model="d4data/bias-detection-model",
                    device=0 if torch.cuda.is_available() else -1
                )
                
                # Sentiment analysis
                self.models['sentiment'] = pipeline(
                    "sentiment-analysis",
                    model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                    device=0 if torch.cuda.is_available() else -1
                )
                
                # Hate speech detection
                self.models['hate_speech'] = pipeline(
                    "text-classification",
                    model="martin-ha/toxic-comment-model",
                    device=0 if torch.cuda.is_available() else -1
                )
                
                # Privacy entity recognition
                try:
                    self.models['privacy_ner'] = spacy.load("en_core_web_sm")
                except OSError:
                    logging.warning("Spacy model not available for privacy NER")
                
                # Embedding model for semantic analysis
                self.models['embeddings'] = SentenceTransformer('all-MiniLM-L6-v2')
                
                logging.info("Guardrail models loaded successfully")
            else:
                logging.warning("Using basic pattern-based guardrails")
                
        except Exception as e:
            logging.error(f"Error loading guardrail models: {e}")
    
    def _load_rules(self):
        """Load guardrail rules from database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM guardrail_rules WHERE enabled = 1')
            
            for row in cursor.fetchall():
                rule = GuardrailRule(
                    id=row[0],
                    name=row[1],
                    description=row[2],
                    guardrail_type=GuardrailType(row[3]),
                    pattern=row[4],
                    keywords=json.loads(row[5]) if row[5] else [],
                    threshold=row[6],
                    risk_level=RiskLevel(row[7]),
                    action=ActionType(row[8]),
                    enabled=bool(row[9]),
                    created_at=datetime.fromisoformat(row[10])
                )
                self.rules[rule.id] = rule
            
            conn.close()
            
            # Load default rules if none exist
            if not self.rules:
                self._create_default_rules()
            
            logging.info(f"Loaded {len(self.rules)} guardrail rules")
            
        except Exception as e:
            logging.error(f"Error loading rules: {e}")
            self._create_default_rules()
    
    def _create_default_rules(self):
        """Create default guardrail rules"""
        default_rules = [
            # Content filtering rules
            GuardrailRule(
                id="content_profanity",
                name="Profanity Filter",
                description="Detects and filters profane language",
                guardrail_type=GuardrailType.CONTENT_FILTER,
                keywords=["fuck", "shit", "damn", "bitch", "asshole", "bastard"],
                threshold=0.7,
                risk_level=RiskLevel.MEDIUM,
                action=ActionType.MODIFY
            ),
            
            GuardrailRule(
                id="content_violence",
                name="Violence Detection",
                description="Detects violent content and threats",
                guardrail_type=GuardrailType.CONTENT_FILTER,
                keywords=["kill", "murder", "violence", "attack", "harm", "hurt", "weapon"],
                threshold=0.8,
                risk_level=RiskLevel.HIGH,
                action=ActionType.BLOCK
            ),
            
            # Bias detection rules
            GuardrailRule(
                id="bias_gender",
                name="Gender Bias Detection",
                description="Detects gender-based bias and stereotypes",
                guardrail_type=GuardrailType.BIAS_DETECTION,
                keywords=["women are", "men are", "girls should", "boys should"],
                threshold=0.6,
                risk_level=RiskLevel.MEDIUM,
                action=ActionType.WARN
            ),
            
            GuardrailRule(
                id="bias_racial",
                name="Racial Bias Detection",
                description="Detects racial bias and discrimination",
                guardrail_type=GuardrailType.BIAS_DETECTION,
                keywords=["race", "ethnicity", "color", "nationality"],
                threshold=0.7,
                risk_level=RiskLevel.HIGH,
                action=ActionType.BLOCK
            ),
            
            # Privacy protection rules
            GuardrailRule(
                id="privacy_pii",
                name="PII Detection",
                description="Detects personally identifiable information",
                guardrail_type=GuardrailType.PRIVACY_PROTECTION,
                pattern=r'\b\d{3}-\d{2}-\d{4}\b|\b\d{4}\s?\d{4}\s?\d{4}\s?\d{4}\b',
                threshold=0.9,
                risk_level=RiskLevel.CRITICAL,
                action=ActionType.BLOCK
            ),
            
            # Safety checks
            GuardrailRule(
                id="safety_self_harm",
                name="Self-Harm Detection",
                description="Detects content promoting self-harm",
                guardrail_type=GuardrailType.SAFETY_CHECK,
                keywords=["suicide", "self-harm", "cut myself", "end my life"],
                threshold=0.8,
                risk_level=RiskLevel.CRITICAL,
                action=ActionType.ESCALATE
            ),
            
            # Toxicity detection
            GuardrailRule(
                id="toxicity_general",
                name="General Toxicity",
                description="Detects toxic and harmful content",
                guardrail_type=GuardrailType.TOXICITY_DETECTION,
                threshold=0.7,
                risk_level=RiskLevel.HIGH,
                action=ActionType.BLOCK
            )
        ]
        
        # Save default rules
        for rule in default_rules:
            self.add_rule(rule)
    
    def _init_patterns(self):
        """Initialize content patterns for detection"""
        self.patterns = {
            'email': re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
            'phone': re.compile(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'),
            'ssn': re.compile(r'\b\d{3}-\d{2}-\d{4}\b'),
            'credit_card': re.compile(r'\b\d{4}\s?\d{4}\s?\d{4}\s?\d{4}\b'),
            'ip_address': re.compile(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'),
            'url': re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'),
            'profanity_strong': re.compile(r'\b(fuck|shit|bitch|asshole|cunt|motherfucker)\b', re.IGNORECASE),
            'violence_threats': re.compile(r'\b(kill|murder|die|death|harm|hurt|attack|violence)\b', re.IGNORECASE)
        }
        
        # Bias detection patterns
        self.bias_patterns = {
            'gender_stereotypes': [
                r'\b(women|girls|females?) (are|should|must|always|never)\b',
                r'\b(men|boys|males?) (are|should|must|always|never)\b'
            ],
            'racial_stereotypes': [
                r'\b(black|white|asian|hispanic|latino) (people|person) (are|always|never)\b'
            ],
            'age_bias': [
                r'\b(old|young|elderly|millennial|boomer) (people|person) (are|always|never)\b'
            ]
        }
    
    def _start_background_monitoring(self):
        """Start background monitoring and optimization"""
        def monitor_worker():
            while self.is_running:
        
(Content truncated due to size limit. Use line ranges to read in chunks)
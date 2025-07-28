"""
Learning as a Service (LaaS) System
Provides comprehensive learning management and delivery services
"""

import asyncio
import json
import logging
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum
import sqlite3
import os
from decimal import Decimal
import hashlib
import aiohttp
from pathlib import Path

class LearningType(Enum):
    COURSE = "course"
    WORKSHOP = "workshop"
    WEBINAR = "webinar"
    TUTORIAL = "tutorial"
    CERTIFICATION = "certification"
    ASSESSMENT = "assessment"
    SIMULATION = "simulation"
    MICROLEARNING = "microlearning"

class ContentType(Enum):
    VIDEO = "video"
    AUDIO = "audio"
    TEXT = "text"
    INTERACTIVE = "interactive"
    QUIZ = "quiz"
    ASSIGNMENT = "assignment"
    DOCUMENT = "document"
    PRESENTATION = "presentation"
    CODE = "code"
    SIMULATION = "simulation"

class DifficultyLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

class LearningStatus(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    PAUSED = "paused"
    FAILED = "failed"
    EXPIRED = "expired"

@dataclass
class LearningContent:
    id: str
    title: str
    content_type: ContentType
    content_url: str
    description: str
    duration_minutes: int
    order: int
    is_mandatory: bool = True
    prerequisites: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)

@dataclass
class LearningModule:
    id: str
    title: str
    description: str
    contents: List[LearningContent]
    order: int
    estimated_duration: int
    learning_objectives: List[str] = field(default_factory=list)
    prerequisites: List[str] = field(default_factory=list)
    assessment_id: Optional[str] = None

@dataclass
class LearningPath:
    id: str
    title: str
    description: str
    learning_type: LearningType
    difficulty_level: DifficultyLevel
    modules: List[LearningModule]
    instructor_id: str
    category: str
    tags: List[str] = field(default_factory=list)
    price: Decimal = Decimal('0')
    currency: str = "USD"
    duration_hours: int = 0
    max_participants: Optional[int] = None
    certification_available: bool = False
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

@dataclass
class LearningProgress:
    user_id: str
    learning_path_id: str
    status: LearningStatus
    current_module_id: Optional[str]
    current_content_id: Optional[str]
    completion_percentage: float
    time_spent_minutes: int
    last_accessed: datetime
    started_at: datetime
    completed_at: Optional[datetime] = None
    score: Optional[float] = None
    certificate_id: Optional[str] = None

@dataclass
class Assessment:
    id: str
    title: str
    description: str
    questions: List[Dict[str, Any]]
    passing_score: float
    time_limit_minutes: Optional[int]
    max_attempts: int
    is_proctored: bool = False
    randomize_questions: bool = True
    show_results_immediately: bool = True

@dataclass
class LearningAnalytics:
    user_id: str
    learning_path_id: str
    engagement_score: float
    completion_rate: float
    average_session_duration: int
    total_time_spent: int
    quiz_scores: List[float]
    last_activity: datetime
    learning_velocity: float  # content per hour
    retention_score: float

class LaaS:
    """
    Learning as a Service - Comprehensive learning management system
    """
    
    def __init__(self, data_dir: str = "./laas_data"):
        self.data_dir = data_dir
        self.db_path = os.path.join(data_dir, "laas.db")
        
        # Initialize database
        os.makedirs(data_dir, exist_ok=True)
        self._init_database()
        
        # AI-powered features
        self.ai_recommendations = True
        self.adaptive_learning = True
        self.auto_assessment = True
        
        # Content delivery network
        self.cdn_enabled = True
        self.content_cache = {}
        
        # Analytics and tracking
        self.analytics_enabled = True
        self.real_time_tracking = True
        
        # Integration capabilities
        self.lms_integrations = ["moodle", "canvas", "blackboard", "schoology"]
        self.video_platforms = ["youtube", "vimeo", "wistia", "brightcove"]
        self.assessment_tools = ["proctorio", "respondus", "examity"]
    
    def _init_database(self):
        """Initialize SQLite database for LaaS"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Learning paths table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS learning_paths (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                learning_type TEXT NOT NULL,
                difficulty_level TEXT NOT NULL,
                instructor_id TEXT NOT NULL,
                category TEXT NOT NULL,
                tags TEXT,
                price DECIMAL(10, 2) DEFAULT 0,
                currency TEXT DEFAULT 'USD',
                duration_hours INTEGER DEFAULT 0,
                max_participants INTEGER,
                certification_available BOOLEAN DEFAULT FALSE,
                is_active BOOLEAN DEFAULT TRUE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Learning modules table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS learning_modules (
                id TEXT PRIMARY KEY,
                learning_path_id TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                order_index INTEGER NOT NULL,
                estimated_duration INTEGER DEFAULT 0,
                learning_objectives TEXT,
                prerequisites TEXT,
                assessment_id TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (learning_path_id) REFERENCES learning_paths (id)
            )
        ''')
        
        # Learning content table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS learning_content (
                id TEXT PRIMARY KEY,
                module_id TEXT NOT NULL,
                title TEXT NOT NULL,
                content_type TEXT NOT NULL,
                content_url TEXT NOT NULL,
                description TEXT,
                duration_minutes INTEGER DEFAULT 0,
                order_index INTEGER NOT NULL,
                is_mandatory BOOLEAN DEFAULT TRUE,
                prerequisites TEXT,
                metadata TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (module_id) REFERENCES learning_modules (id)
            )
        ''')
        
        # User progress table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS learning_progress (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                learning_path_id TEXT NOT NULL,
                status TEXT NOT NULL,
                current_module_id TEXT,
                current_content_id TEXT,
                completion_percentage REAL DEFAULT 0,
                time_spent_minutes INTEGER DEFAULT 0,
                last_accessed DATETIME DEFAULT CURRENT_TIMESTAMP,
                started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                completed_at DATETIME,
                score REAL,
                certificate_id TEXT,
                UNIQUE(user_id, learning_path_id),
                FOREIGN KEY (learning_path_id) REFERENCES learning_paths (id)
            )
        ''')
        
        # Assessments table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS assessments (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                questions TEXT NOT NULL,
                passing_score REAL NOT NULL,
                time_limit_minutes INTEGER,
                max_attempts INTEGER DEFAULT 3,
                is_proctored BOOLEAN DEFAULT FALSE,
                randomize_questions BOOLEAN DEFAULT TRUE,
                show_results_immediately BOOLEAN DEFAULT TRUE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Assessment attempts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS assessment_attempts (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                assessment_id TEXT NOT NULL,
                attempt_number INTEGER NOT NULL,
                answers TEXT NOT NULL,
                score REAL NOT NULL,
                passed BOOLEAN NOT NULL,
                started_at DATETIME NOT NULL,
                completed_at DATETIME NOT NULL,
                time_taken_minutes INTEGER NOT NULL,
                FOREIGN KEY (assessment_id) REFERENCES assessments (id)
            )
        ''')
        
        # Learning analytics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS learning_analytics (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                learning_path_id TEXT NOT NULL,
                engagement_score REAL DEFAULT 0,
                completion_rate REAL DEFAULT 0,
                average_session_duration INTEGER DEFAULT 0,
                total_time_spent INTEGER DEFAULT 0,
                quiz_scores TEXT,
                last_activity DATETIME DEFAULT CURRENT_TIMESTAMP,
                learning_velocity REAL DEFAULT 0,
                retention_score REAL DEFAULT 0,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, learning_path_id),
                FOREIGN KEY (learning_path_id) REFERENCES learning_paths (id)
            )
        ''')
        
        # Certificates table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS certificates (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                learning_path_id TEXT NOT NULL,
                certificate_url TEXT NOT NULL,
                issued_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                expires_at DATETIME,
                verification_code TEXT UNIQUE,
                is_valid BOOLEAN DEFAULT TRUE,
                FOREIGN KEY (learning_path_id) REFERENCES learning_paths (id)
            )
        ''')
        
        # Learning sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS learning_sessions (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                learning_path_id TEXT NOT NULL,
                content_id TEXT,
                session_start DATETIME NOT NULL,
                session_end DATETIME,
                duration_minutes INTEGER DEFAULT 0,
                interactions INTEGER DEFAULT 0,
                completion_status TEXT DEFAULT 'in_progress',
                device_type TEXT,
                ip_address TEXT,
                user_agent TEXT,
                FOREIGN KEY (learning_path_id) REFERENCES learning_paths (id)
            )
        ''')
        
        # Create indexes
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_progress_user ON learning_progress(user_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_progress_path ON learning_progress(learning_path_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_analytics_user ON learning_analytics(user_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_sessions_user ON learning_sessions(user_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_certificates_user ON certificates(user_id)')
        
        conn.commit()
        conn.close()
    
    async def create_learning_path(self, learning_path: LearningPath) -> str:
        """Create a new learning path"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO learning_paths 
                (id, title, description, learning_type, difficulty_level, instructor_id, 
                 category, tags, price, currency, duration_hours, max_participants, 
                 certification_available, is_active)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                learning_path.id,
                learning_path.title,
                learning_path.description,
                learning_path.learning_type.value,
                learning_path.difficulty_level.value,
                learning_path.instructor_id,
                learning_path.category,
                json.dumps(learning_path.tags),
                float(learning_path.price),
                learning_path.currency,
                learning_path.duration_hours,
                learning_path.max_participants,
                learning_path.certification_available,
                learning_path.is_active
            ))
            
            # Create modules
            for module in learning_path.modules:
                await self._create_module(cursor, learning_path.id, module)
            
            conn.commit()
            conn.close()
            
            logging.info(f"Created learning path: {learning_path.id}")
            return learning_path.id
            
        except Exception as e:
            logging.error(f"Error creating learning path: {e}")
            raise
    
    async def _create_module(self, cursor, learning_path_id: str, module: LearningModule):
        """Create a learning module"""
        cursor.execute('''
            INSERT INTO learning_modules 
            (id, learning_path_id, title, description, order_index, estimated_duration,
             learning_objectives, prerequisites, assessment_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            module.id,
            learning_path_id,
            module.title,
            module.description,
            module.order,
            module.estimated_duration,
            json.dumps(module.learning_objectives),
            json.dumps(module.prerequisites),
            module.assessment_id
        ))
        
        # Create content
        for content in module.contents:
            cursor.execute('''
                INSERT INTO learning_content 
                (id, module_id, title, content_type, content_url, description,
                 duration_minutes, order_index, is_mandatory, prerequisites, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                content.id,
                module.id,
                content.title,
                content.content_type.value,
                content.content_url,
                content.description,
                content.duration_minutes,
                content.order,
                content.is_mandatory,
                json.dumps(content.prerequisites),
                json.dumps(content.metadata)
            ))
    
    async def enroll_user(self, user_id: str, learning_path_id: str) -> bool:
        """Enroll user in a learning path"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if already enrolled
            cursor.execute('''
                SELECT id FROM learning_progress 
                WHERE user_id = ? AND learning_path_id = ?
            ''', (user_id, learning_path_id))
            
            if cursor.fetchone():
                conn.close()
                return False  # Already e
(Content truncated due to size limit. Use line ranges to read in chunks)
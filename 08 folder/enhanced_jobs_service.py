"""
Enhanced Job Marketplace Service
Advanced AI-powered job matching and freelance platform
"""

import asyncio
import json
import logging
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import dataclass, field
from enum import Enum
import sqlite3
import os
from decimal import Decimal
import hashlib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import re
from pathlib import Path

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

class JobType(Enum):
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    FREELANCE = "freelance"
    INTERNSHIP = "internship"
    TEMPORARY = "temporary"
    REMOTE = "remote"
    HYBRID = "hybrid"

class ExperienceLevel(Enum):
    ENTRY = "entry"
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"
    LEAD = "lead"
    EXECUTIVE = "executive"

class JobStatus(Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    FILLED = "filled"
    CANCELLED = "cancelled"
    EXPIRED = "expired"

class ApplicationStatus(Enum):
    PENDING = "pending"
    REVIEWING = "reviewing"
    SHORTLISTED = "shortlisted"
    INTERVIEWED = "interviewed"
    OFFERED = "offered"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"

class ProjectStatus(Enum):
    POSTED = "posted"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    DISPUTED = "disputed"

class SkillLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

@dataclass
class JobPosting:
    id: str
    company_id: str
    title: str
    description: str
    requirements: List[str]
    responsibilities: List[str]
    skills_required: List[Dict[str, Any]]
    job_type: JobType
    experience_level: ExperienceLevel
    salary_min: Optional[Decimal]
    salary_max: Optional[Decimal]
    currency: str
    location: str
    remote_allowed: bool
    benefits: List[str]
    application_deadline: Optional[datetime]
    status: JobStatus
    posted_by: str
    department: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    ai_score: float = 0.0
    view_count: int = 0
    application_count: int = 0
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

@dataclass
class FreelanceProject:
    id: str
    client_id: str
    title: str
    description: str
    category: str
    subcategory: str
    skills_required: List[Dict[str, Any]]
    budget_type: str  # fixed, hourly
    budget_min: Decimal
    budget_max: Decimal
    currency: str
    duration: str
    experience_level: ExperienceLevel
    project_type: str  # one_time, ongoing
    attachments: List[str]
    status: ProjectStatus
    deadline: Optional[datetime]
    proposals_count: int = 0
    hired_freelancer_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)

@dataclass
class UserProfile:
    id: str
    user_id: str
    profile_type: str  # job_seeker, employer, freelancer, client
    title: str
    bio: str
    skills: List[Dict[str, Any]]
    experience: List[Dict[str, Any]]
    education: List[Dict[str, Any]]
    certifications: List[Dict[str, Any]]
    portfolio: List[Dict[str, Any]]
    hourly_rate: Optional[Decimal]
    availability: str
    location: str
    languages: List[Dict[str, str]]
    social_links: Dict[str, str]
    preferences: Dict[str, Any]
    ai_profile_score: float = 0.0
    completion_percentage: float = 0.0
    verification_status: str = "unverified"
    created_at: datetime = field(default_factory=datetime.utcnow)

@dataclass
class JobApplication:
    id: str
    job_id: str
    applicant_id: str
    cover_letter: str
    resume_url: str
    portfolio_urls: List[str]
    expected_salary: Optional[Decimal]
    availability_date: Optional[datetime]
    status: ApplicationStatus
    ai_match_score: float
    recruiter_notes: Optional[str] = None
    interview_scheduled: Optional[datetime] = None
    feedback: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

@dataclass
class FreelanceProposal:
    id: str
    project_id: str
    freelancer_id: str
    cover_letter: str
    proposed_budget: Decimal
    proposed_timeline: str
    milestones: List[Dict[str, Any]]
    portfolio_samples: List[str]
    ai_match_score: float
    status: str = "submitted"
    client_feedback: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)

@dataclass
class Interview:
    id: str
    application_id: str
    interviewer_id: str
    interview_type: str  # phone, video, in_person, technical
    scheduled_time: datetime
    duration_minutes: int
    meeting_link: Optional[str]
    notes: Optional[str]
    rating: Optional[int]
    status: str = "scheduled"
    feedback: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)

@dataclass
class SkillAssessment:
    id: str
    user_id: str
    skill_name: str
    assessment_type: str  # quiz, coding, portfolio
    score: float
    max_score: float
    completion_time: int  # minutes
    certificate_url: Optional[str]
    verified: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)

class EnhancedJobsService:
    """
    Enhanced Job Marketplace with AI-powered matching and advanced features
    """
    
    def __init__(self, data_dir: str = "./jobs_data"):
        self.data_dir = data_dir
        self.db_path = os.path.join(data_dir, "enhanced_jobs.db")
        
        # Initialize database
        os.makedirs(data_dir, exist_ok=True)
        self._init_database()
        
        # AI and ML components
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        
        # Skill categories and taxonomy
        self.skill_categories = {
            "programming": ["python", "javascript", "java", "c++", "react", "node.js", "django", "flask"],
            "design": ["photoshop", "illustrator", "figma", "sketch", "ui/ux", "graphic design"],
            "marketing": ["seo", "social media", "content marketing", "ppc", "analytics"],
            "data_science": ["machine learning", "data analysis", "sql", "tableau", "r", "statistics"],
            "project_management": ["agile", "scrum", "kanban", "jira", "project planning"],
            "sales": ["lead generation", "crm", "negotiation", "customer service"],
            "finance": ["accounting", "financial analysis", "excel", "quickbooks", "budgeting"],
            "writing": ["copywriting", "technical writing", "content creation", "editing"]
        }
        
        # Industry classifications
        self.industries = [
            "technology", "healthcare", "finance", "education", "retail", "manufacturing",
            "consulting", "media", "real_estate", "automotive", "aerospace", "energy",
            "telecommunications", "government", "non_profit", "hospitality", "agriculture"
        ]
        
        # AI matching weights
        self.matching_weights = {
            "skills": 0.35,
            "experience": 0.25,
            "location": 0.15,
            "salary": 0.10,
            "job_type": 0.10,
            "industry": 0.05
        }
        
        # Advanced features
        self.ai_resume_parsing = True
        self.automated_screening = True
        self.video_interviews = True
        self.skill_assessments = True
        self.blockchain_verification = True
        self.predictive_analytics = True
        
        # Integration capabilities
        self.integrations = {
            "ats_systems": ["greenhouse", "lever", "workday", "bamboohr"],
            "video_platforms": ["zoom", "teams", "google_meet", "webex"],
            "assessment_tools": ["codility", "hackerrank", "testgorilla"],
            "background_checks": ["checkr", "sterling", "accurate"],
            "payment_systems": ["stripe", "paypal", "wise", "payoneer"]
        }
    
    def _init_database(self):
        """Initialize SQLite database for enhanced jobs service"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Job postings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS job_postings (
                id TEXT PRIMARY KEY,
                company_id TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                requirements TEXT NOT NULL,
                responsibilities TEXT NOT NULL,
                skills_required TEXT NOT NULL,
                job_type TEXT NOT NULL,
                experience_level TEXT NOT NULL,
                salary_min DECIMAL(12, 2),
                salary_max DECIMAL(12, 2),
                currency TEXT NOT NULL,
                location TEXT NOT NULL,
                remote_allowed BOOLEAN DEFAULT FALSE,
                benefits TEXT,
                application_deadline DATETIME,
                status TEXT NOT NULL,
                posted_by TEXT NOT NULL,
                department TEXT,
                tags TEXT,
                ai_score REAL DEFAULT 0.0,
                view_count INTEGER DEFAULT 0,
                application_count INTEGER DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Freelance projects table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS freelance_projects (
                id TEXT PRIMARY KEY,
                client_id TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT NOT NULL,
                skills_required TEXT NOT NULL,
                budget_type TEXT NOT NULL,
                budget_min DECIMAL(12, 2) NOT NULL,
                budget_max DECIMAL(12, 2) NOT NULL,
                currency TEXT NOT NULL,
                duration TEXT NOT NULL,
                experience_level TEXT NOT NULL,
                project_type TEXT NOT NULL,
                attachments TEXT,
                status TEXT NOT NULL,
                deadline DATETIME,
                proposals_count INTEGER DEFAULT 0,
                hired_freelancer_id TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # User profiles table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_profiles (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL UNIQUE,
                profile_type TEXT NOT NULL,
                title TEXT NOT NULL,
                bio TEXT NOT NULL,
                skills TEXT NOT NULL,
                experience TEXT NOT NULL,
                education TEXT NOT NULL,
                certifications TEXT NOT NULL,
                portfolio TEXT NOT NULL,
                hourly_rate DECIMAL(8, 2),
                availability TEXT NOT NULL,
                location TEXT NOT NULL,
                languages TEXT NOT NULL,
                social_links TEXT NOT NULL,
                preferences TEXT NOT NULL,
                ai_profile_score REAL DEFAULT 0.0,
                completion_percentage REAL DEFAULT 0.0,
                verification_status TEXT DEFAULT 'unverified',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Job applications table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS job_applications (
                id TEXT PRIMARY KEY,
                job_id TEXT NOT NULL,
                applicant_id TEXT NOT NULL,
                cover_letter TEXT NOT NULL,
                resume_url TEXT NOT NULL,
                portfolio_urls TEXT,
                expected_salary DECIMAL(12, 2),
                availability_date DATETIME,
                status TEXT NOT NULL,
                ai_match_score REAL NOT NULL,
                recruiter_notes TEXT,
                interview_scheduled DATETIME,
                feedback TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (job_id) REFERENCES job_postings (id),
                FOREIGN KEY (applicant_id) REFERENCES user_profiles (user_id),
                UNIQUE(job_id, applicant_id)
            )
        ''')
        
        # Freelance proposals table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS freelance_proposals (
                id TEXT PRIMARY KEY,
                project_id TEXT NOT NULL,
                freelancer_id TEXT NOT NULL,
                cover_letter TEXT NOT NULL,
                proposed_budget DECIMAL(12, 2) NOT NULL,
                proposed_timeline TEXT NOT NULL,
                milestones TEXT NOT NULL,
                portfolio_samples TEXT,
                ai_match_score REAL NOT NULL,
                status TEXT DEFAULT 'submitted',
                client_feedback TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES freelance_projects (id),
                FOREIGN KEY (freelancer_id) REFERENCES user_profiles (user_id),
                UNIQUE(project_id, freelancer_id)
            )
        ''')
        
        # Interviews table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS interviews (
                id TEXT PRIMARY KEY,
                application_id TEXT NOT NULL,
                interviewer_id TEXT NOT NULL,
                interview_type TEXT NOT NULL,
                scheduled_time DATETIME NOT NULL,
                duration_minutes INTEGER NOT NULL,
                meeting_link TEXT,
                notes TEXT,
                rating INTEGER CHECK (rating >= 1 AND rating <= 5),
                status TEXT DEFAULT 'scheduled',
                feedback TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (application_id) REFERENCES job_applications (id)
            )
        ''')
        
        # Skill assessments table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS skill_assessments (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                skill_name TEXT NOT NULL,
                assessment_type TEXT NOT NULL,
                score REAL NOT NULL,
                max_score REAL NOT NULL,
                completion_time INTEGER NOT NULL,
                certificate_url TEXT,
                verified BOOLEAN DEFAULT FALSE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user_profiles (user_id)
            )
        ''')
        
        # Job recommendations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS job_recommendations (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                job_id TEXT NOT NULL,
               
(Content truncated due to size limit. Use line ranges to read in chunks)
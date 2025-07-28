from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    company = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    job_title = db.Column(db.String(100), nullable=True)
    company_size = db.Column(db.String(50), nullable=True)
    industry = db.Column(db.String(100), nullable=True)
    
    # Access control fields
    access_level = db.Column(db.String(20), default='basic')  # guest, basic, verified, kyc_individual, kyc_business
    verification_status = db.Column(db.String(30), default='email_pending')  # email_pending, email_verified, phone_verified, kyc_pending, kyc_verified, kyc_rejected
    registration_type = db.Column(db.String(20), default='basic')  # basic, kyc_individual, kyc_business
    
    # Status fields
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    verified_at = db.Column(db.DateTime, nullable=True)
    
    # Trial and subscription
    trial_status = db.Column(db.String(20), default='none')  # none, active, expired, converted
    subscription_plan = db.Column(db.String(50), nullable=True)
    
    # KYC fields
    kyc_status = db.Column(db.String(20), default='not_started')  # not_started, in_progress, pending_review, approved, rejected, expired
    kyc_level = db.Column(db.String(20), nullable=True)  # individual, business
    kyc_completed_at = db.Column(db.DateTime, nullable=True)
    
    # Legacy field for compatibility
    username = db.Column(db.String(80), unique=True, nullable=True)

    def __repr__(self):
        return f'<User {self.email}>'

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'firstName': self.first_name,
            'lastName': self.last_name,
            'company': self.company,
            'phone': self.phone,
            'jobTitle': self.job_title,
            'companySize': self.company_size,
            'industry': self.industry,
            'accessLevel': self.access_level,
            'verificationStatus': self.verification_status,
            'registrationType': self.registration_type,
            'isActive': self.is_active,
            'isVerified': self.is_verified,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'lastLogin': self.last_login.isoformat() if self.last_login else None,
            'verifiedAt': self.verified_at.isoformat() if self.verified_at else None,
            'trialStatus': self.trial_status,
            'subscriptionPlan': self.subscription_plan,
            'kycStatus': self.kyc_status,
            'kycLevel': self.kyc_level,
            'kycCompletedAt': self.kyc_completed_at.isoformat() if self.kyc_completed_at else None,
            'username': self.username  # For compatibility
        }
    
    def has_access_to_feature(self, feature, action):
        """Check if user has access to a specific feature and action"""
        # This would integrate with the access control system
        access_matrix = {
            'guest': 0,
            'basic': 1,
            'verified': 2,
            'kyc_individual': 3,
            'kyc_business': 4
        }
        
        user_level = access_matrix.get(self.access_level, 0)
        
        # Define minimum levels for different features
        feature_requirements = {
            'social_media_post': 1,
            'ecommerce_sell': 2,
            'blockchain_basic': 3,
            'business_features': 4
        }
        
        required_level = feature_requirements.get(f"{feature}_{action}", 0)
        return user_level >= required_level
    
    def get_available_features(self):
        """Get list of features available to this user"""
        level_features = {
            'guest': [
                'browse_content',
                'view_demos',
                'use_basic_tools'
            ],
            'basic': [
                'create_profile',
                'post_content',
                'save_preferences',
                'basic_messaging',
                'join_communities'
            ],
            'verified': [
                'higher_transaction_limits',
                'premium_features',
                'advanced_tools',
                'priority_support',
                'create_paid_content'
            ],
            'kyc_individual': [
                'blockchain_access',
                'cryptocurrency_transactions',
                'financial_services',
                'advanced_ai_features',
                'api_access'
            ],
            'kyc_business': [
                'business_accounts',
                'enterprise_tools',
                'corporate_features',
                'advanced_analytics',
                'custom_integrations'
            ]
        }
        
        # Get cumulative features up to user's level
        available = []
        levels = ['guest', 'basic', 'verified', 'kyc_individual', 'kyc_business']
        user_level_index = levels.index(self.access_level) if self.access_level in levels else 0
        
        for i in range(user_level_index + 1):
            available.extend(level_features.get(levels[i], []))
        
        return list(set(available))  # Remove duplicates


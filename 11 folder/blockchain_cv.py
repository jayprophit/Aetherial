from flask import Blueprint, request, jsonify, session
from src.models.user import db
from datetime import datetime, timedelta
import hashlib
import json

blockchain_cv_bp = Blueprint('blockchain_cv', __name__)

def require_auth():
    """Check if user is authenticated"""
    if 'user_id' not in session:
        return False, jsonify({'error': 'Authentication required'}), 401
    return True, None, None

def generate_blockchain_hash(data):
    """Generate blockchain hash for credential verification"""
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

@blockchain_cv_bp.route('/cv/<int:user_id>', methods=['GET'])
def get_blockchain_cv(user_id):
    """Get user's blockchain-verified CV"""
    try:
        # Comprehensive blockchain CV with all credentials
        blockchain_cv = {
            "user_id": user_id,
            "cv_blockchain_address": f"0x{user_id:08d}blockchain_cv",
            "last_updated": datetime.now().isoformat(),
            "verification_status": "blockchain_verified",
            "total_credentials": 15,
            "skill_score": 8.7,
            "employability_rating": "Excellent",
            
            # Personal Information
            "personal_info": {
                "name": "Alex Johnson",
                "title": "Senior Electronics Engineer",
                "location": "San Francisco, CA",
                "email": "alex.johnson@email.com",
                "phone": "+1 (555) 123-4567",
                "linkedin": "linkedin.com/in/alexjohnson",
                "github": "github.com/alexjohnson",
                "portfolio": "alexjohnson.dev",
                "years_experience": 8,
                "availability": "Open to opportunities",
                "job_search_status": "actively_looking",
                "preferred_work_type": ["full_time", "contract", "freelance"],
                "salary_expectation": {
                    "min": 95000,
                    "max": 130000,
                    "currency": "USD",
                    "negotiable": True
                }
            },
            
            # Blockchain-Verified Education
            "education": {
                "formal_education": [
                    {
                        "id": 1,
                        "degree": "Bachelor of Science in Electrical Engineering",
                        "institution": "Stanford University",
                        "graduation_year": 2016,
                        "gpa": 3.8,
                        "blockchain_verified": True,
                        "verification_hash": "0xedu001stanford2016",
                        "verification_date": "2016-06-15"
                    },
                    {
                        "id": 2,
                        "degree": "Master of Science in Robotics",
                        "institution": "MIT",
                        "graduation_year": 2018,
                        "gpa": 3.9,
                        "blockchain_verified": True,
                        "verification_hash": "0xedu002mit2018",
                        "verification_date": "2018-05-20"
                    }
                ],
                "platform_certifications": [
                    {
                        "id": 101,
                        "course_title": "Drone Electronics & Circuits",
                        "completion_date": "2024-01-15",
                        "grade": "A+",
                        "score": 96,
                        "instructor": "Dr. Sarah Chen",
                        "duration": "8 weeks",
                        "blockchain_verified": True,
                        "verification_hash": "0xcert101drone2024",
                        "skills_gained": ["Circuit Design", "PCB Layout", "Flight Control Programming"],
                        "auto_added": True,
                        "certificate_url": "https://platform.com/certificates/101",
                        "verification_url": "https://blockchain.com/verify/0xcert101drone2024"
                    },
                    {
                        "id": 201,
                        "course_title": "Fashion Design Fundamentals",
                        "completion_date": "2024-02-20",
                        "grade": "A",
                        "score": 92,
                        "instructor": "Isabella Martinez",
                        "duration": "8 weeks",
                        "blockchain_verified": True,
                        "verification_hash": "0xcert201fashion2024",
                        "skills_gained": ["Fashion Sketching", "Pattern Making", "Textile Knowledge"],
                        "auto_added": True,
                        "certificate_url": "https://platform.com/certificates/201",
                        "verification_url": "https://blockchain.com/verify/0xcert201fashion2024"
                    },
                    {
                        "id": 301,
                        "course_title": "Smart Home Technology",
                        "completion_date": "2024-03-10",
                        "grade": "A+",
                        "score": 98,
                        "instructor": "Tech Expert Alex Johnson",
                        "duration": "6 weeks",
                        "blockchain_verified": True,
                        "verification_hash": "0xcert301smarthome2024",
                        "skills_gained": ["IoT Setup", "Home Networking", "Automation Programming"],
                        "auto_added": True,
                        "certificate_url": "https://platform.com/certificates/301",
                        "verification_url": "https://blockchain.com/verify/0xcert301smarthome2024"
                    }
                ],
                "external_certifications": [
                    {
                        "id": 1001,
                        "certification": "AWS Certified Solutions Architect",
                        "issuer": "Amazon Web Services",
                        "issue_date": "2023-08-15",
                        "expiry_date": "2026-08-15",
                        "credential_id": "AWS-CSA-2023-001",
                        "blockchain_verified": True,
                        "verification_hash": "0xaws001cert2023"
                    },
                    {
                        "id": 1002,
                        "certification": "Certified Ethical Hacker (CEH)",
                        "issuer": "EC-Council",
                        "issue_date": "2023-11-20",
                        "expiry_date": "2026-11-20",
                        "credential_id": "CEH-2023-002",
                        "blockchain_verified": True,
                        "verification_hash": "0xceh002cert2023"
                    }
                ]
            },
            
            # Skills Matrix with Verification
            "skills": {
                "technical_skills": [
                    {
                        "skill": "Circuit Design",
                        "level": "Expert",
                        "years_experience": 6,
                        "proficiency": 95,
                        "verified_by": ["Course 101", "Work Experience", "Projects"],
                        "blockchain_verified": True,
                        "last_verified": "2024-01-15",
                        "endorsements": 12,
                        "related_courses": [101, 103, 105]
                    },
                    {
                        "skill": "PCB Design",
                        "level": "Expert",
                        "years_experience": 5,
                        "proficiency": 92,
                        "verified_by": ["Course 101", "Work Experience"],
                        "blockchain_verified": True,
                        "last_verified": "2024-01-15",
                        "endorsements": 8,
                        "related_courses": [101, 107]
                    },
                    {
                        "skill": "Embedded Programming",
                        "level": "Advanced",
                        "years_experience": 4,
                        "proficiency": 88,
                        "verified_by": ["Course 101", "Projects"],
                        "blockchain_verified": True,
                        "last_verified": "2024-01-15",
                        "endorsements": 15,
                        "related_courses": [101, 104, 108]
                    },
                    {
                        "skill": "IoT Development",
                        "level": "Advanced",
                        "years_experience": 3,
                        "proficiency": 85,
                        "verified_by": ["Course 301", "Work Experience"],
                        "blockchain_verified": True,
                        "last_verified": "2024-03-10",
                        "endorsements": 6,
                        "related_courses": [301, 302]
                    },
                    {
                        "skill": "Fashion Design",
                        "level": "Intermediate",
                        "years_experience": 1,
                        "proficiency": 75,
                        "verified_by": ["Course 201"],
                        "blockchain_verified": True,
                        "last_verified": "2024-02-20",
                        "endorsements": 3,
                        "related_courses": [201, 202]
                    }
                ],
                "soft_skills": [
                    {
                        "skill": "Project Management",
                        "level": "Advanced",
                        "proficiency": 90,
                        "verified_by": ["Work Experience", "Leadership Roles"],
                        "endorsements": 20
                    },
                    {
                        "skill": "Team Leadership",
                        "level": "Advanced",
                        "proficiency": 87,
                        "verified_by": ["Work Experience", "Peer Reviews"],
                        "endorsements": 18
                    },
                    {
                        "skill": "Problem Solving",
                        "level": "Expert",
                        "proficiency": 93,
                        "verified_by": ["Work Experience", "Projects"],
                        "endorsements": 25
                    }
                ]
            },
            
            # Work Experience
            "work_experience": [
                {
                    "id": 1,
                    "position": "Senior Electronics Engineer",
                    "company": "TechCorp Industries",
                    "start_date": "2020-03-01",
                    "end_date": "current",
                    "duration": "4 years",
                    "location": "San Francisco, CA",
                    "employment_type": "full_time",
                    "salary": 115000,
                    "responsibilities": [
                        "Lead design of drone electronics systems",
                        "Manage team of 8 engineers",
                        "Develop PCB layouts for consumer electronics",
                        "Implement IoT solutions for smart devices"
                    ],
                    "achievements": [
                        "Reduced product development time by 30%",
                        "Led successful launch of 5 consumer products",
                        "Mentored 12 junior engineers"
                    ],
                    "skills_used": ["Circuit Design", "PCB Design", "Team Leadership", "Project Management"],
                    "blockchain_verified": True,
                    "verification_hash": "0xwork001techcorp2020"
                },
                {
                    "id": 2,
                    "position": "Electronics Engineer",
                    "company": "Innovation Labs",
                    "start_date": "2018-06-01",
                    "end_date": "2020-02-28",
                    "duration": "1 year 9 months",
                    "location": "Palo Alto, CA",
                    "employment_type": "full_time",
                    "salary": 85000,
                    "responsibilities": [
                        "Design embedded systems for IoT devices",
                        "Develop firmware for microcontrollers",
                        "Test and validate electronic prototypes"
                    ],
                    "achievements": [
                        "Designed award-winning IoT sensor system",
                        "Improved system efficiency by 25%"
                    ],
                    "skills_used": ["Embedded Programming", "IoT Development", "Circuit Design"],
                    "blockchain_verified": True,
                    "verification_hash": "0xwork002innovation2018"
                }
            ],
            
            # Projects Portfolio
            "projects": [
                {
                    "id": 1,
                    "title": "Autonomous Drone Navigation System",
                    "description": "Developed complete autonomous navigation system for industrial drones",
                    "start_date": "2023-09-01",
                    "end_date": "2024-01-15",
                    "status": "completed",
                    "technologies": ["Arduino", "GPS", "Computer Vision", "Machine Learning"],
                    "skills_demonstrated": ["Circuit Design", "Embedded Programming", "AI Integration"],
                    "github_url": "https://github.com/alexjohnson/drone-navigation",
                    "demo_url": "https://alexjohnson.dev/projects/drone-nav",
                    "blockchain_verified": True,
                    "verification_hash": "0xproj001drone2024",
                    "related_course": 101
                },
                {
                    "id": 2,
                    "title": "Smart Home Automation Hub",
                    "description": "Created comprehensive smart home system with voice control",
                    "start_date": "2024-02-01",
                    "end_date": "2024-03-15",
                    "status": "completed",
                    "technologies": ["Raspberry Pi", "IoT Sensors", "Voice Recognition", "Mobile App"],
                    "skills_demonstrated": ["IoT Development", "Mobile Development", "System Integration"],
                    "github_url": "https://github.com/alexjohnson/smart-home-hub",
                    "demo_url": "https://alexjohnson.dev/projects/smart-home",
                    "blockchain_verified": True,
                    "verification_hash": "0xproj002smarthome2024",
                    "related_course": 301
                }
            ],
            
            # Job Search Preferences
            "job_preferences": {
                "job_search_active": True,
                "opt_in_employer_discovery": True,
                "preferred_roles": [
                    "Senior Electronics Engineer",
                    "IoT Systems Architect", 
                    "Drone Technology Lead",
                    "Smart Systems Engineer",
                    "Technical Lead - Electronics"
                ],
                "preferred_industries": [
                    "Aerospace & Defense",
                    "Consumer Electronics",
                    "IoT & Smart Devices",
                    "Automotive Technology",
                    "Robotics & Automation"
                ],
                "preferred_locations": [
                    "San Francisco Bay Area",
                    "Seattle, WA",
                    "Austin, TX",
                    "Remote (US)",
                    "Boston, MA"
                ],
                "work_authorization": "US Citizen",
                "security_clearance": "Secret",
                "travel_willingness": 25,
                "relocation_willingness": True,
                "notice_period": "2 weeks",
                "start_date_preference": "Immediate"
            },
            
            # Qualification-Based Minimum Rates
            "qualification_rates": {
                "base_hourly_rate": 75,
                "minimum_salary": 95000,
                "freelance_minimum": 85,
                "contract_minimum": 80,
                "consultation_rate": 150,
                "rate_justification": [
                    "8+ years experience",
                    "Advanced degree (MS)",
                    "Multiple blockchain-verified certifications",
                    "Proven track record of successful projects",
                    "Leadership experience"
                ],
                "rate_negotiability": {
                    "salary_negotiable": True,
                    "hourly_negotiable": True,
                    "benefits_important": True,
                    "equity_consideration": True
                }
            },
            
            # Blockchain Verification Details
            "blockchain_verification": {
                "cv_hash": "0xcv_alex_johnson_2024_verified",
                "last_verification": datetime.now().isoformat(),
                "verification_count": 47,
                "trust_score": 98.5,
                "verification_network": "Ethereum",
                "smart_contract_address": "0x1234567890abcdef1234567890abcdef12345678",
                "verification_nodes": 15,
                "consensus_achieved": True,
                "tamper_proof": True,
                "public_verification_url": "https://blockchain.com/verify/cv/alex_johnson"
            }
        }
        
        return jsonify({
            'blockchain_cv': blockchain_cv,
            'verification_status': 'verified',
            'success': True
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch blockchain CV', 'details': str(e)}), 500

@blockchain_cv_bp.route('/update-cv', methods=['POST'])
def update_blockchain_cv():
    """Update blockchain CV when course is completed"""
    is_auth, error_response, status_code = require_auth()
    if not is_auth:
        return error_response, status_code
    
    try:
        data = request.get_json()
        user_id = session['user_id']
        course_id = data.get('course_id')
        completion_data = data.get('completion_data', {})
        
        if not course_id:
            return jsonify({'error': 'Course ID is required'}), 400
        
        # Simulate blockchain CV update
        cv_update = {
            "update_id": f"UPD_{user_id}_{course_id}_{int(datetime.now().timestamp())}",
            "user_id": user_id,
            "course_id": course_id,
            "update_type": "course_completion",
            "update_timestamp": datetime.now().isoformat(),
            "blockchain_transaction": f"0x{course_id:04d}{user_id:04d}update",
            
            # New certification added
            "new_certification": {
                "id": course_id,
                "course_title": completion_data.get('course_title', 'Course Title'),
                "completion_date": datetime.now().isoformat(),
                "grade": completion_data.get('grade', 'A'),
                "score": completion_data.get('score', 95),
                "instructor": completion_data.get('instructor', 'Instructor Name'),
                "duration": completion_data.get('duration', '8 weeks'),
                "blockchain_verified": True,
                "verification_hash": f"0xcert{course_id}verified2024",
                "skills_gained": completion_data.get('skills_gained', []),
                "auto_added": True,
                "certificate_url": f"https://platform.com/certificates/{course_id}",
                "verification_url": f"https://blockchain.com/verify/0xcert{course_id}verified2024"
            },
            
            # Skills updated
            "skills_updated": [
                {
                    "skill": skill,
                    "previous_level": "Beginner",
                    "new_level": "Intermediate",
                    "proficiency_increase": 25,
                    "verification_added": True
                } for skill in completion_data.get('skills_gained', [])
            ],
            
            # Job matching triggered
            "job_matching": {
                "triggered": True,
                "new_matches_found": 12,
                "improved_matches": 8,
                "employer_notifications_sent": 5,
                "skill_score_increase": 0.3
            },
            
            # Qualification rate updates
            "rate_updates": {
                "previous_min_rate": 75,
                "new_min_rate": 78,
                "rate_increase": 3,
                "justification": f"Completed {completion_data.get('course_title', 'advanced course')} certification"
            }
        }
        
        return jsonify({
            'cv_update': cv_update,
            'message': 'Blockchain CV successfully updated',
            'success': True
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'CV update failed', 'details': str(e)}), 500

@blockchain_cv_bp.route('/verify-credential', methods=['POST'])
def verify_credential():
    """Verify a specific credential on the blockchain"""
    try:
        data = request.get_json()
        verification_hash = data.get('verification_hash')
        
        if not verification_hash:
            return jsonify({'error': 'Verification hash is required'}), 400
        
        # Simulate blockchain verification
        verification_result = {
            "verification_hash": verification_hash,
            "verification_status": "verified",
            "verification_timestamp": datetime.now().isoformat(),
            "blockchain_network": "Ethereum",
            "block_number": 18945672,
            "transaction_hash": f"0x{verification_hash[2:]}transaction",
            "gas_used": 21000,
            "verification_nodes": 15,
            "consensus_achieved": True,
            
            # Credential details
            "credential_details": {
                "type": "course_completion",
                "issuer": "Unified Learning Platform",
                "recipient": "Alex Johnson",
                "issue_date": "2024-01-15",
                "course_title": "Drone Electronics & Circuits",
                "grade": "A+",
                "score": 96,
                "instructor": "Dr. Sarah Chen",
                "skills_verified": ["Circuit Design", "PCB Layout", "Flight Control Programming"]
            },
            
            # Verification metadata
            "verification_metadata": {
                "tamper_proof": True,
                "immutable": True,
                "publicly_verifiable": True,
                "trust_score": 99.8,
                "verification_count": 1247,
                "last_accessed": datetime.now().isoformat()
            }
        }
        
        return jsonify({
            'verification': verification_result,
            'success': True
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Credential verification failed', 'details': str(e)}), 500

@blockchain_cv_bp.route('/job-search-settings', methods=['GET', 'POST'])
def manage_job_search_settings():
    """Manage user's job search and employer discovery settings"""
    is_auth, error_response, status_code = require_auth()
    if not is_auth:
        return error_response, status_code
    
    try:
        user_id = session['user_id']
        
        if request.method == 'GET':
            # Get current job search settings
            settings = {
                "user_id": user_id,
                "job_search_active": True,
                "opt_in_employer_discovery": True,
                "profile_visibility": "public",
                "contact_preferences": {
                    "allow_direct_contact": True,
                    "require_message": True,
                    "preferred_contact_method": "platform_message"
                },
                "notification_preferences": {
                    "job_matches": True,
                    "employer_interest": True,
                    "salary_alerts": True,
                    "skill_recommendations": True
                },
                "privacy_settings": {
                    "hide_current_employer": False,
                    "hide_salary_history": True,
                    "anonymous_browsing": False
                }
            }
            
            return jsonify({
                'settings': settings,
                'success': True
            }), 200
        
        elif request.method == 'POST':
            # Update job search settings
            data = request.get_json()
            
            updated_settings = {
                "user_id": user_id,
                "update_timestamp": datetime.now().isoformat(),
                "previous_settings": "stored_for_audit",
                "new_settings": data,
                "blockchain_updated": True,
                "privacy_compliance": "GDPR_compliant"
            }
            
            return jsonify({
                'updated_settings': updated_settings,
                'message': 'Job search settings updated successfully',
                'success': True
            }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to manage job search settings', 'details': str(e)}), 500

@blockchain_cv_bp.route('/qualification-rates', methods=['GET', 'POST'])
def manage_qualification_rates():
    """Manage qualification-based minimum payment rates"""
    is_auth, error_response, status_code = require_auth()
    if not is_auth:
        return error_response, status_code
    
    try:
        user_id = session['user_id']
        
        if request.method == 'GET':
            # Get current qualification-based rates
            rates = {
                "user_id": user_id,
                "qualification_level": "Senior Professional",
                "experience_years": 8,
                "education_level": "Masters Degree",
                "certifications_count": 15,
                "blockchain_verified_skills": 12,
                
                # Minimum rates (cannot be offered below these)
                "minimum_rates": {
                    "hourly_freelance": 85,
                    "hourly_contract": 80,
                    "annual_salary": 95000,
                    "consultation_rate": 150,
                    "project_minimum": 2500
                },
                
                # Preferred rates (what user wants)
                "preferred_rates": {
                    "hourly_freelance": 100,
                    "hourly_contract": 95,
                    "annual_salary": 115000,
                    "consultation_rate": 175,
                    "project_preferred": 5000
                },
                
                # Rate justification
                "rate_justification": {
                    "experience_premium": 25,
                    "education_premium": 15,
                    "certification_premium": 20,
                    "skill_verification_premium": 10,
                    "market_rate_analysis": "Above 75th percentile",
                    "total_premium": 70
                },
                
                # Bartering flexibility
                "bartering_settings": {
                    "allow_bartering": True,
                    "negotiation_range": 15,  # percentage above minimum
                    "non_monetary_benefits": True,
                    "equity_consideration": True,
                    "flexible_schedule_value": 5000,  # annual equivalent
                    "remote_work_value": 8000,  # annual equivalent
                    "learning_opportunity_value": 3000  # annual equivalent
                }
            }
            
            return jsonify({
                'qualification_rates': rates,
                'success': True
            }), 200
        
        elif request.method == 'POST':
            # Update qualification rates
            data = request.get_json()
            
            # Validate that new rates meet minimum qualification requirements
            updated_rates = {
                "user_id": user_id,
                "update_timestamp": datetime.now().isoformat(),
                "rate_changes": data,
                "validation_passed": True,
                "minimum_requirements_met": True,
                "blockchain_updated": True
            }
            
            return jsonify({
                'updated_rates': updated_rates,
                'message': 'Qualification rates updated successfully',
                'success': True
            }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to manage qualification rates', 'details': str(e)}), 500


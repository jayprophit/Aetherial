"""
E-Learning Platform API - Udemy/Open University Features
Complete educational platform with courses, certifications, and learning management
"""

from flask import Blueprint, request, jsonify
import random
import time
from datetime import datetime, timedelta

elearning_bp = Blueprint('elearning', __name__)

# Mock data for demonstration
COURSES_DATABASE = [
    {
        "course_id": "course001",
        "title": "Advanced AI and Machine Learning for Supply Chain Optimization",
        "subtitle": "Master AI algorithms and machine learning techniques for revolutionizing supply chain management",
        "description": "This comprehensive course covers cutting-edge AI and ML techniques specifically designed for supply chain optimization. Learn how to implement predictive analytics, automated decision-making, and intelligent forecasting systems.",
        "instructor_id": "instructor001",
        "instructor_info": {
            "name": "Dr. John Smith",
            "title": "AI Research Director",
            "bio": "15+ years experience in AI and supply chain optimization",
            "avatar": "/images/instructors/john_smith.jpg",
            "rating": 4.9,
            "students_taught": 25000,
            "courses_created": 12
        },
        "category": "Technology",
        "subcategory": "Artificial Intelligence",
        "level": "Advanced",
        "language": "English",
        "duration_hours": 45.5,
        "total_lectures": 156,
        "total_resources": 89,
        "price": 199.99,
        "original_price": 299.99,
        "discount_percentage": 33.33,
        "currency": "USD",
        "thumbnail": "/images/courses/ai_supply_chain.jpg",
        "preview_video": "/videos/courses/ai_supply_chain_preview.mp4",
        "rating": {
            "average": 4.8,
            "total_reviews": 2340,
            "distribution": {"5": 1850, "4": 350, "3": 100, "2": 30, "1": 10}
        },
        "enrollment": {
            "total_students": 15420,
            "completion_rate": 78.5,
            "certificate_eligible": True
        },
        "features": [
            "45.5 hours of video content",
            "89 downloadable resources",
            "Certificate of completion",
            "Lifetime access",
            "Mobile and TV access",
            "Assignments and quizzes"
        ],
        "requirements": [
            "Basic programming knowledge (Python preferred)",
            "Understanding of statistics and mathematics",
            "Familiarity with supply chain concepts"
        ],
        "learning_outcomes": [
            "Implement AI algorithms for supply chain optimization",
            "Build predictive models for demand forecasting",
            "Design automated decision-making systems",
            "Optimize logistics and inventory management",
            "Create intelligent supplier selection algorithms"
        ],
        "syllabus": [
            {
                "section_id": "section001",
                "title": "Introduction to AI in Supply Chain",
                "lectures": 12,
                "duration_minutes": 180,
                "preview_available": True
            },
            {
                "section_id": "section002", 
                "title": "Machine Learning Fundamentals",
                "lectures": 18,
                "duration_minutes": 270,
                "preview_available": False
            },
            {
                "section_id": "section003",
                "title": "Predictive Analytics for Demand Forecasting",
                "lectures": 25,
                "duration_minutes": 450,
                "preview_available": False
            }
        ],
        "tags": ["AI", "Machine Learning", "Supply Chain", "Optimization", "Python"],
        "created_at": "2024-01-10T10:00:00Z",
        "updated_at": "2024-01-25T14:30:00Z",
        "status": "published",
        "bestseller": True,
        "featured": True
    },
    {
        "course_id": "course002",
        "title": "Robotics Engineering: From Design to Deployment",
        "subtitle": "Complete guide to robotics design, programming, and real-world applications",
        "description": "Learn to design, build, and program robots for various applications including construction, underwater exploration, and industrial automation. This hands-on course covers mechanical design, control systems, and AI integration.",
        "instructor_id": "instructor002",
        "instructor_info": {
            "name": "Prof. Sarah Johnson",
            "title": "Robotics Engineering Professor",
            "bio": "20+ years in robotics research and development",
            "avatar": "/images/instructors/sarah_johnson.jpg",
            "rating": 4.9,
            "students_taught": 18500,
            "courses_created": 8
        },
        "category": "Engineering",
        "subcategory": "Robotics",
        "level": "Intermediate",
        "language": "English",
        "duration_hours": 38.0,
        "total_lectures": 124,
        "total_resources": 67,
        "price": 179.99,
        "original_price": 249.99,
        "discount_percentage": 28.0,
        "currency": "USD",
        "thumbnail": "/images/courses/robotics_engineering.jpg",
        "preview_video": "/videos/courses/robotics_preview.mp4",
        "rating": {
            "average": 4.7,
            "total_reviews": 1890,
            "distribution": {"5": 1420, "4": 350, "3": 90, "2": 20, "1": 10}
        },
        "enrollment": {
            "total_students": 12300,
            "completion_rate": 82.1,
            "certificate_eligible": True
        },
        "features": [
            "38 hours of video content",
            "67 downloadable resources",
            "Hands-on projects",
            "Certificate of completion",
            "Lifetime access",
            "Community forum access"
        ],
        "requirements": [
            "Basic engineering or technical background",
            "Understanding of physics and mathematics",
            "Access to basic tools (optional for projects)"
        ],
        "learning_outcomes": [
            "Design mechanical systems for robots",
            "Program robot control systems",
            "Integrate sensors and actuators",
            "Implement AI for autonomous behavior",
            "Deploy robots in real-world scenarios"
        ],
        "syllabus": [
            {
                "section_id": "section004",
                "title": "Robotics Fundamentals",
                "lectures": 15,
                "duration_minutes": 225,
                "preview_available": True
            },
            {
                "section_id": "section005",
                "title": "Mechanical Design and CAD",
                "lectures": 20,
                "duration_minutes": 360,
                "preview_available": False
            }
        ],
        "tags": ["Robotics", "Engineering", "AI", "Automation", "Design"],
        "created_at": "2024-01-15T09:00:00Z",
        "updated_at": "2024-01-26T11:20:00Z",
        "status": "published",
        "bestseller": False,
        "featured": True
    }
]

INSTRUCTORS_DATABASE = {
    "instructor001": {
        "instructor_id": "instructor001",
        "name": "Dr. John Smith",
        "title": "AI Research Director",
        "bio": "Dr. John Smith is a leading expert in artificial intelligence and supply chain optimization with over 15 years of experience in both academia and industry. He has published 50+ research papers and holds 12 patents in AI algorithms.",
        "avatar": "/images/instructors/john_smith.jpg",
        "cover_image": "/images/instructors/john_smith_cover.jpg",
        "expertise": ["Artificial Intelligence", "Machine Learning", "Supply Chain", "Optimization", "Data Science"],
        "education": [
            {"degree": "Ph.D. in Computer Science", "institution": "MIT", "year": 2008},
            {"degree": "M.S. in Artificial Intelligence", "institution": "Stanford", "year": 2005}
        ],
        "experience": [
            {"position": "AI Research Director", "company": "TechFlow Systems", "years": "2018-Present"},
            {"position": "Senior ML Engineer", "company": "Google", "years": "2012-2018"}
        ],
        "stats": {
            "total_students": 25000,
            "courses_created": 12,
            "average_rating": 4.9,
            "total_reviews": 5600,
            "years_teaching": 8
        },
        "social_links": {
            "linkedin": "https://linkedin.com/in/johnsmith-ai",
            "twitter": "https://twitter.com/johnsmith_ai",
            "website": "https://johnsmith-ai.com"
        },
        "verified": True,
        "badges": ["Top Instructor", "AI Expert", "Industry Professional"]
    }
}

ENROLLMENTS_DATABASE = {}
PROGRESS_DATABASE = {}
CERTIFICATES_DATABASE = []

@elearning_bp.route('/api/elearning/courses/search', methods=['GET'])
def search_courses():
    """
    Search and filter courses with AI-powered recommendations
    """
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    level = request.args.get('level', '')  # beginner, intermediate, advanced
    price_range = request.args.get('price_range', '')  # free, paid, under_50, under_100
    rating = float(request.args.get('min_rating', 0))
    sort_by = request.args.get('sort_by', 'relevance')  # relevance, rating, price, newest, popular
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 12))
    
    # Filter courses
    filtered_courses = COURSES_DATABASE.copy()
    
    # Text search
    if query:
        query_lower = query.lower()
        filtered_courses = [
            c for c in filtered_courses
            if query_lower in c['title'].lower() or 
               query_lower in c['description'].lower() or
               any(query_lower in tag.lower() for tag in c['tags'])
        ]
    
    # Category filter
    if category:
        filtered_courses = [c for c in filtered_courses if c['category'].lower() == category.lower()]
    
    # Level filter
    if level:
        filtered_courses = [c for c in filtered_courses if c['level'].lower() == level.lower()]
    
    # Price range filter
    if price_range == 'free':
        filtered_courses = [c for c in filtered_courses if c['price'] == 0]
    elif price_range == 'under_50':
        filtered_courses = [c for c in filtered_courses if 0 < c['price'] <= 50]
    elif price_range == 'under_100':
        filtered_courses = [c for c in filtered_courses if 0 < c['price'] <= 100]
    
    # Rating filter
    if rating > 0:
        filtered_courses = [c for c in filtered_courses if c['rating']['average'] >= rating]
    
    # Sort courses
    if sort_by == 'rating':
        filtered_courses.sort(key=lambda x: x['rating']['average'], reverse=True)
    elif sort_by == 'price':
        filtered_courses.sort(key=lambda x: x['price'])
    elif sort_by == 'newest':
        filtered_courses.sort(key=lambda x: x['created_at'], reverse=True)
    elif sort_by == 'popular':
        filtered_courses.sort(key=lambda x: x['enrollment']['total_students'], reverse=True)
    else:  # relevance
        # Add AI relevance score
        for course in filtered_courses:
            relevance_score = random.uniform(0.7, 0.98)
            if query:
                if query.lower() in course['title'].lower():
                    relevance_score += 0.1
                if any(query.lower() in tag.lower() for tag in course['tags']):
                    relevance_score += 0.05
            course['ai_relevance_score'] = min(1.0, relevance_score)
        
        filtered_courses.sort(key=lambda x: x['ai_relevance_score'], reverse=True)
    
    # Pagination
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    paginated_courses = filtered_courses[start_idx:end_idx]
    
    return jsonify({
        "status": "success",
        "search_results": {
            "query": query,
            "total_results": len(filtered_courses),
            "page": page,
            "per_page": limit,
            "total_pages": (len(filtered_courses) + limit - 1) // limit,
            "courses": paginated_courses
        },
        "filters": {
            "categories": ["Technology", "Engineering", "Business", "Design", "Science"],
            "levels": ["Beginner", "Intermediate", "Advanced"],
            "price_ranges": ["Free", "Under $50", "Under $100", "Premium"]
        },
        "recommendations": {
            "trending_topics": ["AI", "Robotics", "Supply Chain", "Machine Learning"],
            "popular_instructors": ["Dr. John Smith", "Prof. Sarah Johnson"]
        }
    })

@elearning_bp.route('/api/elearning/courses/<course_id>', methods=['GET'])
def get_course_details(course_id):
    """
    Get detailed course information
    """
    course = next((c for c in COURSES_DATABASE if c['course_id'] == course_id), None)
    if not course:
        return jsonify({"status": "error", "message": "Course not found"}), 404
    
    # Get instructor details
    instructor = INSTRUCTORS_DATABASE.get(course['instructor_id'], {})
    
    # Get related courses
    related_courses = []
    for c in COURSES_DATABASE:
        if c['course_id'] != course_id and (
            c['category'] == course['category'] or 
            any(tag in course['tags'] for tag in c['tags'])
        ):
            related_courses.append({
                "course_id": c['course_id'],
                "title": c['title'],
                "instructor": c['instructor_info']['name'],
                "price": c['price'],
                "rating": c['rating']['average'],
                "thumbnail": c['thumbnail']
            })
    
    # AI-powered insights
    ai_insights = {
        "difficulty_match": random.choice(["Perfect match", "Slightly challenging", "Good fit"]),
        "time_commitment": f"{course['duration_hours']} hours over {random.randint(4, 12)} weeks",
        "career_impact": random.choice(["High", "Medium", "Significant"]),
        "skill_level_after": course['level'],
        "job_market_demand": random.choice(["Very High", "High", "Growing"])
    }
    
    course_details = course.copy()
    course_details.update({
        "instructor_details": instructor,
        "related_courses": related_courses[:6],
        "ai_insights": ai_insights,
        "enrollment_status": "available",
        "last_updated": course['updated_at']
    })
    
    return jsonify({
        "status": "success",
        "course": course_details
    })

@elearning_bp.route('/api/elearning/courses/<course_id>/enroll', methods=['POST'])
def enroll_in_course(course_id):
    """
    Enroll student in a course
    """
    data = request.get_json()
    
    student_id = data.get('student_id')
    payment_method = data.get('payment_method', {})
    
    course = next((c for c in COURSES_DATABASE if c['course_id'] == course_id), None)
    if not course:
        return jsonify({"status": "error", "message": "Course not found"}), 404
    
    # Check if already enrolled
    if student_id in ENROLLMENTS_DATABASE.get(course_id, {}):
        return jsonify({"status": "error", "message": "Already enrolled in this course"}), 400
    
    # Create enrollment
    enrollment_id = f"enroll{int(time.time())}"
    enrollment = {
        "enrollment_id": enrollment_id,
        "course_id": course_id,
        "student_id": student_id,
        "enrolled_at": datetime.now().isoformat() + "Z",
        "payment_status": "completed",
        "amount_paid": course['price'],
        "currency": course['currency'],
        "access_expires": None,  # Lifetime access
        "progress": {
            "completed_lectures": 0,
            "total_lectures": course['total_lectures'],
            "completion_percentage": 0,
            "last_accessed": datetime.now().isoformat() + "Z",
            "time_spent_minutes": 0
        },
        "certificate_eligible": course['enrollment']['certificate_eligible'],
        "certificate_earned": False
    }
    
    # Add to enrollments
    if course_id not in ENROLLMENTS_DATABASE:
        ENROLLMENTS_DATABASE[course_id] = {}
    ENROLLMENTS_DATABASE[course_id][student_id] = enrollment
    
    # Update course enrollment count
    course['enrollment']['total_students'] += 1
    
    return jsonify({
        "status": "success",
        "message": "Successfully enrolled in course",
        "enrollment": enrollment,
        "course_access": {
            "course_url": f"/courses/{course_id}/learn",
            "mobile_app_access": True,
            "download_access": True,
            "lifetime_access": True
        }
    })

@elearning_bp.route('/api/elearning/courses/<course_id>/progress', methods=['GET', 'POST'])
def handle_course_progress(course_id):
    """
    Get or update student's course progress
    """
    student_id = request.args.get('student_id') if request.method == 'GET' else request.get_json().get('student_id')
    
    # Check enrollment
    enrollment = ENROLLMENTS_DATABASE.get(course_id, {}).get(student_id)
    if not enrollment:
        return jsonify({"status": "error", "message": "Not enrolled in this course"}), 404
    
    if request.method == 'GET':
        # Get progress
        course = next((c for c in COURSES_DATABASE if c['course_id'] == course_id), None)
        
        progress_data = {
            "course_info": {
                "course_id": course_id,
                "title": course['title'],
                "thumbnail": course['thumbnail']
            },
            "progress": enrollment['progress'],
            "current_section": "section001",  # Current section being studied
            "next_lecture": {
                "lecture_id": "lecture001",
                "title": "Introduction to AI in Supply Chain",
                "duration_minutes": 15,
                "section": "Introduction to AI in Supply Chain"
            },
            "achievements": [
                {"type": "first_lecture", "title": "First Steps", "earned_at": "2024-01-27T10:00:00Z"},
                {"type": "week_streak", "title": "Week Warrior", "earned_at": "2024-01-27T10:00:00Z"}
            ],
            "study_streak": 5,  # Days in a row
            "estimated_completion": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        }
        
        return jsonify({
            "status": "success",
            "progress": progress_data
        })
    
    elif request.method == 'POST':
        # Update progress
        data = request.get_json()
        
        lecture_id = data.get('lecture_id')
        time_spent = data.get('time_spent_minutes', 0)
        completed = data.get('completed', False)
        
        # Update progress
        enrollment['progress']['time_spent_minutes'] += time_spent
        enrollment['progress']['last_accessed'] = datetime.now().isoformat() + "Z"
        
        if completed:
            enrollment['progress']['completed_lectures'] += 1
            enrollment['progress']['completion_percentage'] = (
                enrollment['progress']['completed_lectures'] / 
                enrollment['progress']['total_lectures'] * 100
            )
        
        # Check for certificate eligibility
        if enrollment['progress']['completion_percentage'] >= 80 and enrollment['certificate_eligible']:
            enrollment['certificate_earned'] = True
        
        return jsonify({
            "status": "success",
            "message": "Progress updated",
            "progress": enrollment['progress'],
            "achievements_unlocked": [] if not completed else [
                {"type": "lecture_complete", "title": f"Completed {lecture_id}"}
            ]
        })

@elearning_bp.route('/api/elearning/certificates/generate', methods=['POST'])
def generate_certificate():
    """
    Generate completion certificate for student
    """
    data = request.get_json()
    
    student_id = data.get('student_id')
    course_id = data.get('course_id')
    
    # Check enrollment and completion
    enrollment = ENROLLMENTS_DATABASE.get(course_id, {}).get(student_id)
    if not enrollment:
        return jsonify({"status": "error", "message": "Not enrolled in this course"}), 404
    
    if not enrollment['certificate_earned']:
        return jsonify({"status": "error", "message": "Certificate not yet earned"}), 400
    
    course = next((c for c in COURSES_DATABASE if c['course_id'] == course_id), None)
    
    # Generate certificate
    certificate_id = f"cert{int(time.time())}"
    certificate = {
        "certificate_id": certificate_id,
        "student_id": student_id,
        "course_id": course_id,
        "course_title": course['title'],
        "instructor_name": course['instructor_info']['name'],
        "completion_date": datetime.now().strftime("%Y-%m-%d"),
        "issued_date": datetime.now().isoformat() + "Z",
        "certificate_url": f"/certificates/{certificate_id}.pdf",
        "verification_url": f"/verify/{certificate_id}",
        "grade": "Pass",  # Could be calculated based on quiz scores
        "skills_acquired": course['learning_outcomes'],
        "credential_id": certificate_id,
        "blockchain_verified": True,  # For tamper-proof verification
        "valid": True
    }
    
    CERTIFICATES_DATABASE.append(certificate)
    
    return jsonify({
        "status": "success",
        "message": "Certificate generated successfully",
        "certificate": certificate,
        "sharing_options": {
            "linkedin": f"https://linkedin.com/share-certificate/{certificate_id}",
            "twitter": f"https://twitter.com/share-certificate/{certificate_id}",
            "download_pdf": certificate['certificate_url']
        }
    })

@elearning_bp.route('/api/elearning/students/<student_id>/dashboard', methods=['GET'])
def get_student_dashboard(student_id):
    """
    Get student's learning dashboard
    """
    # Get all enrollments for student
    student_enrollments = []
    for course_id, enrollments in ENROLLMENTS_DATABASE.items():
        if student_id in enrollments:
            enrollment = enrollments[student_id]
            course = next((c for c in COURSES_DATABASE if c['course_id'] == course_id), None)
            if course:
                student_enrollments.append({
                    "course": {
                        "course_id": course_id,
                        "title": course['title'],
                        "thumbnail": course['thumbnail'],
                        "instructor": course['instructor_info']['name']
                    },
                    "enrollment": enrollment
                })
    
    # Calculate statistics
    total_courses = len(student_enrollments)
    completed_courses = len([e for e in student_enrollments if e['enrollment']['progress']['completion_percentage'] == 100])
    total_time_spent = sum(e['enrollment']['progress']['time_spent_minutes'] for e in student_enrollments)
    certificates_earned = len([e for e in student_enrollments if e['enrollment']['certificate_earned']])
    
    # Get certificates
    student_certificates = [cert for cert in CERTIFICATES_DATABASE if cert['student_id'] == student_id]
    
    dashboard = {
        "student_info": {
            "student_id": student_id,
            "learning_streak": 7,  # Days in a row
            "total_time_spent_hours": round(total_time_spent / 60, 1),
            "skill_level": "Intermediate",
            "learning_goals": ["Complete AI course", "Earn robotics certificate"]
        },
        "statistics": {
            "total_courses": total_courses,
            "completed_courses": completed_courses,
            "in_progress_courses": total_courses - completed_courses,
            "certificates_earned": certificates_earned,
            "average_progress": round(sum(e['enrollment']['progress']['completion_percentage'] for e in student_enrollments) / max(total_courses, 1), 1)
        },
        "current_courses": student_enrollments,
        "certificates": student_certificates,
        "recommendations": [
            {
                "course_id": "course003",
                "title": "Advanced Robotics Programming",
                "reason": "Based on your interest in AI and robotics",
                "match_score": 0.92
            }
        ],
        "achievements": [
            {"type": "first_course", "title": "Learning Journey Begins", "earned_at": "2024-01-15"},
            {"type": "week_streak", "title": "Consistent Learner", "earned_at": "2024-01-27"}
        ],
        "learning_path": {
            "current_path": "AI & Robotics Specialist",
            "progress": 45,
            "next_milestone": "Complete Robotics Engineering course",
            "estimated_completion": "3 months"
        }
    }
    
    return jsonify({
        "status": "success",
        "dashboard": dashboard
    })

@elearning_bp.route('/api/elearning/instructors/<instructor_id>', methods=['GET'])
def get_instructor_profile(instructor_id):
    """
    Get instructor profile and courses
    """
    instructor = INSTRUCTORS_DATABASE.get(instructor_id)
    if not instructor:
        return jsonify({"status": "error", "message": "Instructor not found"}), 404
    
    # Get instructor's courses
    instructor_courses = [c for c in COURSES_DATABASE if c['instructor_id'] == instructor_id]
    
    # Calculate additional stats
    total_students = sum(c['enrollment']['total_students'] for c in instructor_courses)
    total_reviews = sum(c['rating']['total_reviews'] for c in instructor_courses)
    avg_rating = sum(c['rating']['average'] * c['rating']['total_reviews'] for c in instructor_courses) / max(total_reviews, 1)
    
    instructor_profile = instructor.copy()
    instructor_profile.update({
        "courses": instructor_courses,
        "updated_stats": {
            "total_students": total_students,
            "total_reviews": total_reviews,
            "average_rating": round(avg_rating, 2),
            "total_course_hours": sum(c['duration_hours'] for c in instructor_courses)
        },
        "recent_reviews": [
            {
                "course_title": "Advanced AI and Machine Learning",
                "rating": 5,
                "comment": "Excellent instructor! Clear explanations and practical examples.",
                "student_name": "John D.",
                "date": "2024-01-25"
            }
        ]
    })
    
    return jsonify({
        "status": "success",
        "instructor": instructor_profile
    })

@elearning_bp.route('/api/elearning/analytics/platform', methods=['GET'])
def get_platform_analytics():
    """
    Get e-learning platform analytics
    """
    analytics = {
        "overview": {
            "total_courses": len(COURSES_DATABASE),
            "total_instructors": len(INSTRUCTORS_DATABASE),
            "total_students": 45000,
            "total_enrollments": sum(len(enrollments) for enrollments in ENROLLMENTS_DATABASE.values()),
            "completion_rate": 76.8,
            "satisfaction_score": 4.7
        },
        "course_performance": {
            "most_popular_courses": [
                {"course_id": "course001", "title": "Advanced AI and Machine Learning", "enrollments": 15420},
                {"course_id": "course002", "title": "Robotics Engineering", "enrollments": 12300}
            ],
            "highest_rated_courses": [
                {"course_id": "course001", "title": "Advanced AI and Machine Learning", "rating": 4.8},
                {"course_id": "course002", "title": "Robotics Engineering", "rating": 4.7}
            ],
            "trending_categories": ["Technology", "Engineering", "Business", "Design"]
        },
        "student_engagement": {
            "average_time_per_session": 45.5,
            "daily_active_users": 8500,
            "course_completion_rate": 76.8,
            "certificate_completion_rate": 68.2,
            "mobile_usage_percentage": 42.3
        },
        "revenue_metrics": {
            "total_revenue": 2450000,
            "average_course_price": 189.99,
            "conversion_rate": 12.5,
            "refund_rate": 2.1
        },
        "learning_outcomes": {
            "skills_acquired": 125000,
            "career_advancements": 8500,
            "salary_increases": 6200,
            "job_placements": 3400
        }
    }
    
    return jsonify({
        "status": "success",
        "analytics": analytics,
        "generated_at": datetime.now().isoformat()
    })


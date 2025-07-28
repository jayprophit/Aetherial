from flask import Blueprint, jsonify, request
import random
from datetime import datetime, timedelta

courses_bp = Blueprint('courses', __name__)

# Comprehensive course categories and data
COURSE_CATEGORIES = {
    "AI & Machine Learning": {
        "icon": "🤖",
        "courses": [
            {
                "id": 1,
                "title": "Advanced Emotional AI Development",
                "instructor": "Dr. Sarah Chen",
                "rating": 4.9,
                "students": 15420,
                "duration": "12 weeks",
                "price": 199.99,
                "level": "Advanced",
                "description": "Master the development of emotional AI systems using LSTM-Transformer-VAE architectures",
                "modules": 24,
                "certificate": True,
                "skills": ["Neural Networks", "Emotional Intelligence", "Deep Learning", "Python", "TensorFlow"],
                "preview_video": "https://example.com/preview1.mp4",
                "materials": ["PDF Guides", "Code Examples", "Datasets", "Research Papers"]
            },
            {
                "id": 2,
                "title": "Quantum Machine Learning Fundamentals",
                "instructor": "Prof. Michael Rodriguez",
                "rating": 4.8,
                "students": 8930,
                "duration": "8 weeks",
                "price": 149.99,
                "level": "Intermediate",
                "description": "Explore quantum computing applications in machine learning and AI",
                "modules": 16,
                "certificate": True,
                "skills": ["Quantum Computing", "QAOA", "VQE", "Qiskit", "Linear Algebra"],
                "preview_video": "https://example.com/preview2.mp4",
                "materials": ["Quantum Simulators", "Code Labs", "Theory PDFs", "Practice Problems"]
            },
            {
                "id": 3,
                "title": "Multi-Agent Systems Architecture",
                "instructor": "Dr. Lisa Wang",
                "rating": 4.7,
                "students": 12340,
                "duration": "10 weeks",
                "price": 179.99,
                "level": "Advanced",
                "description": "Design and implement distributed AI systems with multiple intelligent agents",
                "modules": 20,
                "certificate": True,
                "skills": ["Distributed Systems", "Agent Communication", "Coordination", "Python", "ROS"],
                "preview_video": "https://example.com/preview3.mp4",
                "materials": ["Simulation Tools", "Agent Frameworks", "Case Studies", "Project Templates"]
            }
        ]
    },
    "Blockchain & Web3": {
        "icon": "⛓️",
        "courses": [
            {
                "id": 4,
                "title": "DeFi Protocol Development",
                "instructor": "Alex Thompson",
                "rating": 4.9,
                "students": 9870,
                "duration": "14 weeks",
                "price": 249.99,
                "level": "Advanced",
                "description": "Build decentralized finance protocols from scratch using Solidity and Web3",
                "modules": 28,
                "certificate": True,
                "skills": ["Solidity", "Smart Contracts", "DeFi", "Web3.js", "Ethereum"],
                "preview_video": "https://example.com/preview4.mp4",
                "materials": ["Smart Contract Templates", "Testing Frameworks", "Security Audits", "Deployment Guides"]
            },
            {
                "id": 5,
                "title": "NFT Marketplace Creation",
                "instructor": "Emma Davis",
                "rating": 4.6,
                "students": 7650,
                "duration": "6 weeks",
                "price": 129.99,
                "level": "Intermediate",
                "description": "Create your own NFT marketplace with minting, trading, and IPFS integration",
                "modules": 12,
                "certificate": True,
                "skills": ["NFTs", "IPFS", "React", "Solidity", "MetaMask"],
                "preview_video": "https://example.com/preview5.mp4",
                "materials": ["Frontend Templates", "Smart Contracts", "IPFS Setup", "Wallet Integration"]
            }
        ]
    },
    "Robotics & IoT": {
        "icon": "🤖",
        "courses": [
            {
                "id": 6,
                "title": "Text2Robot Command Systems",
                "instructor": "Dr. James Park",
                "rating": 4.8,
                "students": 5430,
                "duration": "9 weeks",
                "price": 189.99,
                "level": "Advanced",
                "description": "Develop natural language interfaces for robotic control systems",
                "modules": 18,
                "certificate": True,
                "skills": ["NLP", "Robotics", "ROS", "Python", "Computer Vision"],
                "preview_video": "https://example.com/preview6.mp4",
                "materials": ["Robot Simulators", "NLP Models", "Hardware Guides", "Integration Examples"]
            },
            {
                "id": 7,
                "title": "IoT Fleet Management",
                "instructor": "Maria Gonzalez",
                "rating": 4.7,
                "students": 8920,
                "duration": "7 weeks",
                "price": 159.99,
                "level": "Intermediate",
                "description": "Manage large-scale IoT device deployments with real-time monitoring",
                "modules": 14,
                "certificate": True,
                "skills": ["IoT", "MQTT", "Cloud Computing", "Device Management", "Analytics"],
                "preview_video": "https://example.com/preview7.mp4",
                "materials": ["IoT Platforms", "Monitoring Tools", "Cloud Services", "Security Protocols"]
            }
        ]
    },
    "Healthcare Technology": {
        "icon": "🏥",
        "courses": [
            {
                "id": 8,
                "title": "AI Medical Diagnosis Systems",
                "instructor": "Dr. Robert Kim",
                "rating": 4.9,
                "students": 6780,
                "duration": "11 weeks",
                "price": 219.99,
                "level": "Advanced",
                "description": "Develop AI systems for medical image analysis and diagnosis",
                "modules": 22,
                "certificate": True,
                "skills": ["Medical AI", "Computer Vision", "Deep Learning", "DICOM", "Healthcare"],
                "preview_video": "https://example.com/preview8.mp4",
                "materials": ["Medical Datasets", "Imaging Tools", "Compliance Guides", "Case Studies"]
            },
            {
                "id": 9,
                "title": "Telemedicine Platform Development",
                "instructor": "Dr. Jennifer Lee",
                "rating": 4.6,
                "students": 4320,
                "duration": "8 weeks",
                "price": 169.99,
                "level": "Intermediate",
                "description": "Build secure telemedicine platforms with video consultation features",
                "modules": 16,
                "certificate": True,
                "skills": ["Telemedicine", "WebRTC", "HIPAA", "Security", "React"],
                "preview_video": "https://example.com/preview9.mp4",
                "materials": ["Platform Templates", "Security Frameworks", "Compliance Docs", "Integration APIs"]
            }
        ]
    },
    "E-Commerce & Business": {
        "icon": "🛒",
        "courses": [
            {
                "id": 10,
                "title": "Advanced E-Commerce Analytics",
                "instructor": "David Wilson",
                "rating": 4.8,
                "students": 11230,
                "duration": "6 weeks",
                "price": 139.99,
                "level": "Intermediate",
                "description": "Master e-commerce analytics, conversion optimization, and customer insights",
                "modules": 12,
                "certificate": True,
                "skills": ["Analytics", "Data Science", "E-Commerce", "Python", "SQL"],
                "preview_video": "https://example.com/preview10.mp4",
                "materials": ["Analytics Tools", "Datasets", "Dashboard Templates", "Case Studies"]
            },
            {
                "id": 11,
                "title": "Supply Chain Optimization",
                "instructor": "Susan Brown",
                "rating": 4.7,
                "students": 7890,
                "duration": "10 weeks",
                "price": 199.99,
                "level": "Advanced",
                "description": "Optimize supply chain operations using AI and data analytics",
                "modules": 20,
                "certificate": True,
                "skills": ["Supply Chain", "Optimization", "AI", "Logistics", "Data Analysis"],
                "preview_video": "https://example.com/preview11.mp4",
                "materials": ["Optimization Tools", "Case Studies", "Simulation Software", "Industry Reports"]
            }
        ]
    },
    "Cybersecurity": {
        "icon": "🔒",
        "courses": [
            {
                "id": 12,
                "title": "Advanced Threat Detection",
                "instructor": "Mark Johnson",
                "rating": 4.9,
                "students": 9450,
                "duration": "12 weeks",
                "price": 229.99,
                "level": "Advanced",
                "description": "Implement advanced threat detection systems using AI and machine learning",
                "modules": 24,
                "certificate": True,
                "skills": ["Cybersecurity", "Threat Detection", "AI", "Network Security", "Python"],
                "preview_video": "https://example.com/preview12.mp4",
                "materials": ["Security Tools", "Threat Intelligence", "Lab Environments", "Incident Response"]
            }
        ]
    }
}

# Learning paths and specializations
LEARNING_PATHS = [
    {
        "id": 1,
        "title": "AI Engineer Career Path",
        "description": "Complete learning path from beginner to advanced AI engineer",
        "courses": [1, 2, 3],
        "duration": "30 weeks",
        "certificate": "AI Engineer Professional Certificate",
        "price": 499.99,
        "students": 3420
    },
    {
        "id": 2,
        "title": "Blockchain Developer Specialization",
        "description": "Become a professional blockchain developer",
        "courses": [4, 5],
        "duration": "20 weeks",
        "certificate": "Blockchain Developer Certificate",
        "price": 349.99,
        "students": 2180
    },
    {
        "id": 3,
        "title": "Healthcare Technology Expert",
        "description": "Specialize in healthcare technology and medical AI",
        "courses": [8, 9],
        "duration": "19 weeks",
        "certificate": "Healthcare Technology Certificate",
        "price": 369.99,
        "students": 1890
    }
]

@courses_bp.route('/overview', methods=['GET'])
def get_courses_overview():
    total_courses = sum(len(cat["courses"]) for cat in COURSE_CATEGORIES.values())
    total_students = sum(course["students"] for cat in COURSE_CATEGORIES.values() for course in cat["courses"])
    avg_rating = sum(course["rating"] for cat in COURSE_CATEGORIES.values() for course in cat["courses"]) / total_courses
    
    return jsonify({
        "total_courses": total_courses,
        "total_students": total_students,
        "average_rating": round(avg_rating, 1),
        "categories": len(COURSE_CATEGORIES),
        "learning_paths": len(LEARNING_PATHS),
        "certificates_issued": 45670,
        "completion_rate": 87.3,
        "satisfaction_rate": 94.8
    })

@courses_bp.route('/categories', methods=['GET'])
def get_course_categories():
    categories = []
    for name, data in COURSE_CATEGORIES.items():
        categories.append({
            "name": name,
            "icon": data["icon"],
            "course_count": len(data["courses"]),
            "total_students": sum(course["students"] for course in data["courses"]),
            "avg_rating": round(sum(course["rating"] for course in data["courses"]) / len(data["courses"]), 1)
        })
    return jsonify(categories)

@courses_bp.route('/category/<category_name>', methods=['GET'])
def get_courses_by_category(category_name):
    if category_name in COURSE_CATEGORIES:
        return jsonify(COURSE_CATEGORIES[category_name]["courses"])
    return jsonify({"error": "Category not found"}), 404

@courses_bp.route('/course/<int:course_id>', methods=['GET'])
def get_course_details(course_id):
    for category in COURSE_CATEGORIES.values():
        for course in category["courses"]:
            if course["id"] == course_id:
                # Add additional details for individual course view
                course_details = course.copy()
                course_details.update({
                    "curriculum": [
                        {"module": 1, "title": "Introduction and Fundamentals", "duration": "2 hours", "completed": False},
                        {"module": 2, "title": "Core Concepts", "duration": "3 hours", "completed": False},
                        {"module": 3, "title": "Practical Applications", "duration": "4 hours", "completed": False},
                        {"module": 4, "title": "Advanced Techniques", "duration": "3 hours", "completed": False},
                        {"module": 5, "title": "Project Implementation", "duration": "5 hours", "completed": False}
                    ],
                    "reviews": [
                        {"user": "John D.", "rating": 5, "comment": "Excellent course with practical examples!", "date": "2024-01-15"},
                        {"user": "Sarah M.", "rating": 4, "comment": "Very informative and well-structured.", "date": "2024-01-10"},
                        {"user": "Mike R.", "rating": 5, "comment": "Best course I've taken on this topic!", "date": "2024-01-08"}
                    ],
                    "prerequisites": ["Basic programming knowledge", "Mathematics fundamentals"],
                    "career_outcomes": ["AI Engineer", "Machine Learning Specialist", "Data Scientist"],
                    "completion_time": "3-6 months",
                    "language": "English",
                    "subtitles": ["English", "Spanish", "French", "German", "Chinese"]
                })
                return jsonify(course_details)
    return jsonify({"error": "Course not found"}), 404

@courses_bp.route('/learning-paths', methods=['GET'])
def get_learning_paths():
    return jsonify(LEARNING_PATHS)

@courses_bp.route('/search', methods=['GET'])
def search_courses():
    query = request.args.get('q', '').lower()
    level = request.args.get('level', '')
    category = request.args.get('category', '')
    min_rating = float(request.args.get('min_rating', 0))
    max_price = float(request.args.get('max_price', 999999))
    
    results = []
    for cat_name, cat_data in COURSE_CATEGORIES.items():
        if category and category != cat_name:
            continue
            
        for course in cat_data["courses"]:
            # Filter by search criteria
            if (query in course["title"].lower() or 
                query in course["description"].lower() or
                any(query in skill.lower() for skill in course["skills"])):
                
                if (level == '' or course["level"] == level) and \
                   (course["rating"] >= min_rating) and \
                   (course["price"] <= max_price):
                    
                    course_result = course.copy()
                    course_result["category"] = cat_name
                    results.append(course_result)
    
    return jsonify({
        "results": results,
        "total": len(results),
        "query": query,
        "filters": {
            "level": level,
            "category": category,
            "min_rating": min_rating,
            "max_price": max_price
        }
    })

@courses_bp.route('/featured', methods=['GET'])
def get_featured_courses():
    # Get top-rated courses across all categories
    featured = []
    for cat_name, cat_data in COURSE_CATEGORIES.items():
        for course in cat_data["courses"]:
            if course["rating"] >= 4.8:
                course_featured = course.copy()
                course_featured["category"] = cat_name
                featured.append(course_featured)
    
    # Sort by rating and student count
    featured.sort(key=lambda x: (x["rating"], x["students"]), reverse=True)
    return jsonify(featured[:6])  # Return top 6 featured courses

@courses_bp.route('/trending', methods=['GET'])
def get_trending_courses():
    # Simulate trending courses based on recent enrollment
    trending = []
    for cat_name, cat_data in COURSE_CATEGORIES.items():
        for course in cat_data["courses"]:
            if course["students"] > 8000:  # High enrollment threshold
                course_trending = course.copy()
                course_trending["category"] = cat_name
                course_trending["recent_enrollments"] = random.randint(100, 500)
                trending.append(course_trending)
    
    # Sort by recent enrollments
    trending.sort(key=lambda x: x["recent_enrollments"], reverse=True)
    return jsonify(trending[:8])  # Return top 8 trending courses

@courses_bp.route('/instructor/<instructor_name>', methods=['GET'])
def get_instructor_courses(instructor_name):
    instructor_courses = []
    instructor_info = None
    
    for cat_name, cat_data in COURSE_CATEGORIES.items():
        for course in cat_data["courses"]:
            if course["instructor"].lower() == instructor_name.lower():
                course_info = course.copy()
                course_info["category"] = cat_name
                instructor_courses.append(course_info)
                
                if not instructor_info:
                    instructor_info = {
                        "name": course["instructor"],
                        "total_students": 0,
                        "total_courses": 0,
                        "avg_rating": 0,
                        "bio": f"Expert instructor specializing in {cat_name}",
                        "experience": "10+ years",
                        "education": "PhD in Computer Science",
                        "certifications": ["Industry Expert", "Certified Instructor"]
                    }
    
    if instructor_courses:
        instructor_info["total_courses"] = len(instructor_courses)
        instructor_info["total_students"] = sum(course["students"] for course in instructor_courses)
        instructor_info["avg_rating"] = round(sum(course["rating"] for course in instructor_courses) / len(instructor_courses), 1)
        
        return jsonify({
            "instructor": instructor_info,
            "courses": instructor_courses
        })
    
    return jsonify({"error": "Instructor not found"}), 404

@courses_bp.route('/enroll', methods=['POST'])
def enroll_course():
    data = request.get_json()
    course_id = data.get('course_id')
    user_id = data.get('user_id')
    
    # Simulate enrollment process
    enrollment = {
        "enrollment_id": random.randint(10000, 99999),
        "course_id": course_id,
        "user_id": user_id,
        "enrollment_date": datetime.now().isoformat(),
        "status": "active",
        "progress": 0,
        "access_expires": (datetime.now() + timedelta(days=365)).isoformat()
    }
    
    return jsonify({
        "success": True,
        "enrollment": enrollment,
        "message": "Successfully enrolled in course!"
    })

@courses_bp.route('/progress/<int:course_id>/<int:user_id>', methods=['GET'])
def get_course_progress(course_id, user_id):
    # Simulate course progress
    progress = {
        "course_id": course_id,
        "user_id": user_id,
        "overall_progress": random.randint(0, 100),
        "modules_completed": random.randint(0, 24),
        "total_modules": 24,
        "time_spent": f"{random.randint(10, 100)} hours",
        "last_accessed": datetime.now().isoformat(),
        "quiz_scores": [85, 92, 78, 88, 95],
        "assignments_completed": random.randint(0, 5),
        "total_assignments": 5,
        "certificate_eligible": random.choice([True, False])
    }
    
    return jsonify(progress)


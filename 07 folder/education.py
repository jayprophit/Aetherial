from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from src.models.user import db, User, Course

education_bp = Blueprint('education', __name__)

@education_bp.route('/courses', methods=['GET'])
def get_courses():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 12, type=int)
        category = request.args.get('category')
        level = request.args.get('level')
        search = request.args.get('search')
        
        query = Course.query.filter_by(is_published=True)
        
        if category:
            query = query.filter(Course.category == category)
        if level:
            query = query.filter(Course.level == level)
        if search:
            query = query.filter(Course.title.contains(search))
        
        courses = query.paginate(page=page, per_page=per_page, error_out=False)
        
        # Sample courses data
        sample_courses = [
            {
                'id': '1',
                'title': 'Complete Rust Programming Bootcamp',
                'description': 'Master systems programming with Rust from beginner to advanced',
                'instructor': 'Dr. Sarah Chen',
                'category': 'Programming',
                'level': 'Beginner',
                'price': 89.99,
                'duration_hours': 40,
                'thumbnail_url': '/api/placeholder/300/200',
                'rating': 4.8,
                'students': 15420,
                'technologies': ['Rust', 'Systems Programming', 'Memory Safety']
            },
            {
                'id': '2',
                'title': 'Go Microservices Architecture',
                'description': 'Build scalable microservices with Go and Kubernetes',
                'instructor': 'Mike Johnson',
                'category': 'Backend Development',
                'level': 'Intermediate',
                'price': 129.99,
                'duration_hours': 35,
                'thumbnail_url': '/api/placeholder/300/200',
                'rating': 4.9,
                'students': 8750,
                'technologies': ['Go', 'Kubernetes', 'Docker', 'Microservices']
            },
            {
                'id': '3',
                'title': 'TypeScript Full-Stack Development',
                'description': 'Build modern web applications with TypeScript, React, and Node.js',
                'instructor': 'Emma Rodriguez',
                'category': 'Full-Stack',
                'level': 'Intermediate',
                'price': 99.99,
                'duration_hours': 50,
                'thumbnail_url': '/api/placeholder/300/200',
                'rating': 4.7,
                'students': 22100,
                'technologies': ['TypeScript', 'React', 'Node.js', 'Express']
            },
            {
                'id': '4',
                'title': 'Julia for Scientific Computing',
                'description': 'High-performance computing and data science with Julia',
                'instructor': 'Prof. David Kim',
                'category': 'Data Science',
                'level': 'Advanced',
                'price': 149.99,
                'duration_hours': 30,
                'thumbnail_url': '/api/placeholder/300/200',
                'rating': 4.6,
                'students': 3200,
                'technologies': ['Julia', 'Scientific Computing', 'Machine Learning']
            },
            {
                'id': '5',
                'title': 'Python Django REST APIs',
                'description': 'Build powerful REST APIs with Django and Django REST Framework',
                'instructor': 'Lisa Wang',
                'category': 'Backend Development',
                'level': 'Intermediate',
                'price': 79.99,
                'duration_hours': 25,
                'thumbnail_url': '/api/placeholder/300/200',
                'rating': 4.8,
                'students': 18900,
                'technologies': ['Python', 'Django', 'REST API', 'PostgreSQL']
            },
            {
                'id': '6',
                'title': 'Flutter Mobile App Development',
                'description': 'Create beautiful cross-platform mobile apps with Flutter and Dart',
                'instructor': 'Alex Thompson',
                'category': 'Mobile Development',
                'level': 'Beginner',
                'price': 94.99,
                'duration_hours': 45,
                'thumbnail_url': '/api/placeholder/300/200',
                'rating': 4.7,
                'students': 12600,
                'technologies': ['Flutter', 'Dart', 'Mobile Development', 'Firebase']
            }
        ]
        
        return jsonify({
            'courses': sample_courses,
            'total': len(sample_courses),
            'page': page,
            'per_page': per_page,
            'pages': 1
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get courses: {str(e)}'}), 500

@education_bp.route('/courses/<course_id>', methods=['GET'])
def get_course(course_id):
    try:
        # Sample course detail
        course_detail = {
            'id': course_id,
            'title': 'Complete Rust Programming Bootcamp',
            'description': 'Master systems programming with Rust from beginner to advanced. This comprehensive course covers memory safety, ownership, concurrency, and building real-world applications.',
            'instructor': {
                'name': 'Dr. Sarah Chen',
                'bio': 'Senior Systems Engineer at Mozilla with 10+ years of Rust experience',
                'avatar': '/api/placeholder/100/100',
                'rating': 4.9
            },
            'category': 'Programming',
            'level': 'Beginner',
            'price': 89.99,
            'duration_hours': 40,
            'thumbnail_url': '/api/placeholder/800/400',
            'rating': 4.8,
            'students': 15420,
            'technologies': ['Rust', 'Systems Programming', 'Memory Safety', 'Concurrency'],
            'what_you_learn': [
                'Rust fundamentals and syntax',
                'Memory management and ownership',
                'Error handling and pattern matching',
                'Concurrency and async programming',
                'Building CLI applications',
                'Web development with Rust',
                'Testing and debugging techniques'
            ],
            'curriculum': [
                {
                    'section': 'Getting Started with Rust',
                    'lessons': [
                        'Introduction to Rust',
                        'Setting up the development environment',
                        'Your first Rust program',
                        'Variables and data types'
                    ]
                },
                {
                    'section': 'Ownership and Memory Management',
                    'lessons': [
                        'Understanding ownership',
                        'References and borrowing',
                        'Lifetimes',
                        'Smart pointers'
                    ]
                },
                {
                    'section': 'Advanced Concepts',
                    'lessons': [
                        'Traits and generics',
                        'Error handling',
                        'Concurrency',
                        'Async programming'
                    ]
                }
            ],
            'requirements': [
                'Basic programming knowledge',
                'Computer with internet connection',
                'No prior Rust experience needed'
            ],
            'reviews': [
                {
                    'user': 'John D.',
                    'rating': 5,
                    'comment': 'Excellent course! Very clear explanations.',
                    'date': '2024-01-15'
                },
                {
                    'user': 'Maria S.',
                    'rating': 4,
                    'comment': 'Great content, could use more practical examples.',
                    'date': '2024-01-10'
                }
            ]
        }
        
        return jsonify(course_detail), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get course: {str(e)}'}), 500

@education_bp.route('/categories', methods=['GET'])
def get_categories():
    try:
        categories = [
            {'id': 'programming', 'name': 'Programming', 'count': 245},
            {'id': 'web-development', 'name': 'Web Development', 'count': 189},
            {'id': 'mobile-development', 'name': 'Mobile Development', 'count': 156},
            {'id': 'data-science', 'name': 'Data Science', 'count': 134},
            {'id': 'devops', 'name': 'DevOps', 'count': 98},
            {'id': 'cloud-computing', 'name': 'Cloud Computing', 'count': 87},
            {'id': 'cybersecurity', 'name': 'Cybersecurity', 'count': 76},
            {'id': 'ai-ml', 'name': 'AI & Machine Learning', 'count': 65}
        ]
        
        return jsonify({'categories': categories}), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get categories: {str(e)}'}), 500

@education_bp.route('/my-courses', methods=['GET'])
@jwt_required()
def get_my_courses():
    try:
        current_user_id = get_jwt_identity()
        
        # Sample enrolled courses
        enrolled_courses = [
            {
                'id': '1',
                'title': 'Complete Rust Programming Bootcamp',
                'progress': 65,
                'last_accessed': '2024-01-20',
                'completion_date': None,
                'certificate_url': None
            },
            {
                'id': '3',
                'title': 'TypeScript Full-Stack Development',
                'progress': 100,
                'last_accessed': '2024-01-18',
                'completion_date': '2024-01-18',
                'certificate_url': '/certificates/typescript-fullstack-cert.pdf'
            }
        ]
        
        return jsonify({'courses': enrolled_courses}), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get enrolled courses: {str(e)}'}), 500

@education_bp.route('/enroll/<course_id>', methods=['POST'])
@jwt_required()
def enroll_course(course_id):
    try:
        current_user_id = get_jwt_identity()
        
        # In a real application, handle payment and enrollment logic here
        
        return jsonify({
            'message': 'Successfully enrolled in course',
            'course_id': course_id,
            'enrollment_date': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to enroll in course: {str(e)}'}), 500


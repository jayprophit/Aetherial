from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from src.models.user import db, User, Job

jobs_bp = Blueprint('jobs', __name__)

@jobs_bp.route('/jobs', methods=['GET'])
def get_jobs():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 12, type=int)
        job_type = request.args.get('job_type')
        location = request.args.get('location')
        experience_level = request.args.get('experience_level')
        search = request.args.get('search')
        
        # Sample jobs data
        sample_jobs = [
            {
                'id': '1',
                'title': 'Senior Rust Developer',
                'company': {
                    'id': 'company1',
                    'name': 'Mozilla Corporation',
                    'logo': '/api/placeholder/80/80',
                    'rating': 4.8,
                    'size': '1000-5000 employees'
                },
                'description': 'Join our team building the next generation of web browsers and developer tools with Rust. You\'ll work on performance-critical systems and contribute to open-source projects.',
                'location': 'San Francisco, CA (Remote OK)',
                'job_type': 'Full-time',
                'salary_min': 150000,
                'salary_max': 220000,
                'currency': 'USD',
                'required_skills': ['Rust', 'Systems Programming', 'WebAssembly', 'Git', 'Linux'],
                'preferred_skills': ['C++', 'JavaScript', 'Performance Optimization'],
                'experience_level': 'Senior',
                'posted_date': '2024-01-18',
                'application_deadline': '2024-02-18',
                'benefits': [
                    'Health, dental, and vision insurance',
                    'Unlimited PTO',
                    'Remote work options',
                    'Professional development budget',
                    'Stock options'
                ],
                'requirements': [
                    '5+ years of systems programming experience',
                    'Strong knowledge of Rust programming language',
                    'Experience with concurrent and parallel programming',
                    'Understanding of memory management and performance optimization',
                    'Open source contribution experience preferred'
                ],
                'is_featured': True,
                'applications_count': 45,
                'views_count': 1250
            },
            {
                'id': '2',
                'title': 'Go Backend Engineer',
                'company': {
                    'id': 'company2',
                    'name': 'Google Cloud',
                    'logo': '/api/placeholder/80/80',
                    'rating': 4.9,
                    'size': '10000+ employees'
                },
                'description': 'Build scalable cloud infrastructure and microservices using Go. Work with Kubernetes, gRPC, and distributed systems at massive scale.',
                'location': 'Mountain View, CA',
                'job_type': 'Full-time',
                'salary_min': 140000,
                'salary_max': 200000,
                'currency': 'USD',
                'required_skills': ['Go', 'Kubernetes', 'Docker', 'gRPC', 'Microservices'],
                'preferred_skills': ['Protocol Buffers', 'Istio', 'Terraform', 'GCP'],
                'experience_level': 'Mid-level',
                'posted_date': '2024-01-17',
                'application_deadline': '2024-02-17',
                'benefits': [
                    'Comprehensive health coverage',
                    'Generous parental leave',
                    'On-site fitness facilities',
                    'Free meals and snacks',
                    'Learning and development opportunities'
                ],
                'requirements': [
                    '3+ years of Go programming experience',
                    'Experience with cloud platforms (GCP preferred)',
                    'Knowledge of containerization and orchestration',
                    'Understanding of distributed systems concepts',
                    'Strong problem-solving skills'
                ],
                'is_featured': True,
                'applications_count': 78,
                'views_count': 2100
            },
            {
                'id': '3',
                'title': 'TypeScript Full-Stack Developer',
                'company': {
                    'id': 'company3',
                    'name': 'Vercel',
                    'logo': '/api/placeholder/80/80',
                    'rating': 4.7,
                    'size': '100-500 employees'
                },
                'description': 'Help build the future of web development with Next.js and TypeScript. Work on developer tools that millions of developers use daily.',
                'location': 'Remote (Global)',
                'job_type': 'Full-time',
                'salary_min': 120000,
                'salary_max': 180000,
                'currency': 'USD',
                'required_skills': ['TypeScript', 'React', 'Next.js', 'Node.js', 'GraphQL'],
                'preferred_skills': ['Prisma', 'Tailwind CSS', 'Serverless', 'Edge Computing'],
                'experience_level': 'Mid-level',
                'posted_date': '2024-01-16',
                'application_deadline': '2024-02-16',
                'benefits': [
                    'Fully remote work',
                    'Equity package',
                    'Health and wellness stipend',
                    'Home office setup budget',
                    'Conference and learning budget'
                ],
                'requirements': [
                    '4+ years of TypeScript/JavaScript experience',
                    'Strong React and Next.js knowledge',
                    'Experience with modern web development tools',
                    'Understanding of serverless architectures',
                    'Excellent communication skills for remote work'
                ],
                'is_featured': False,
                'applications_count': 92,
                'views_count': 1800
            },
            {
                'id': '4',
                'title': 'Julia Research Scientist',
                'company': {
                    'id': 'company4',
                    'name': 'Julia Computing',
                    'logo': '/api/placeholder/80/80',
                    'rating': 4.6,
                    'size': '50-100 employees'
                },
                'description': 'Advance the state of scientific computing with Julia. Work on high-performance computing, machine learning, and numerical analysis projects.',
                'location': 'Boston, MA (Hybrid)',
                'job_type': 'Full-time',
                'salary_min': 130000,
                'salary_max': 170000,
                'currency': 'USD',
                'required_skills': ['Julia', 'Scientific Computing', 'Linear Algebra', 'Statistics', 'Machine Learning'],
                'preferred_skills': ['CUDA', 'MPI', 'Distributed Computing', 'Python', 'R'],
                'experience_level': 'Senior',
                'posted_date': '2024-01-15',
                'application_deadline': '2024-02-15',
                'benefits': [
                    'Research publication opportunities',
                    'Conference speaking opportunities',
                    'Flexible work arrangements',
                    'Professional development budget',
                    'Sabbatical opportunities'
                ],
                'requirements': [
                    'PhD in Computer Science, Mathematics, or related field',
                    'Strong Julia programming skills',
                    'Experience with high-performance computing',
                    'Published research in relevant areas',
                    'Excellent analytical and problem-solving skills'
                ],
                'is_featured': False,
                'applications_count': 23,
                'views_count': 650
            },
            {
                'id': '5',
                'title': 'Python Django Developer',
                'company': {
                    'id': 'company5',
                    'name': 'Instagram',
                    'logo': '/api/placeholder/80/80',
                    'rating': 4.8,
                    'size': '5000-10000 employees'
                },
                'description': 'Scale one of the world\'s largest Django applications. Work on backend systems that serve billions of users worldwide.',
                'location': 'Menlo Park, CA',
                'job_type': 'Full-time',
                'salary_min': 160000,
                'salary_max': 230000,
                'currency': 'USD',
                'required_skills': ['Python', 'Django', 'PostgreSQL', 'Redis', 'Celery'],
                'preferred_skills': ['Cassandra', 'Memcached', 'GraphQL', 'React', 'Machine Learning'],
                'experience_level': 'Senior',
                'posted_date': '2024-01-14',
                'application_deadline': '2024-02-14',
                'benefits': [
                    'Meta stock options',
                    'Comprehensive health benefits',
                    'Wellness programs',
                    'On-site amenities',
                    'Career development programs'
                ],
                'requirements': [
                    '5+ years of Python/Django experience',
                    'Experience with large-scale web applications',
                    'Knowledge of database optimization',
                    'Understanding of caching strategies',
                    'Experience with distributed systems'
                ],
                'is_featured': True,
                'applications_count': 156,
                'views_count': 3200
            },
            {
                'id': '6',
                'title': 'Flutter Mobile Developer',
                'company': {
                    'id': 'company6',
                    'name': 'Spotify',
                    'logo': '/api/placeholder/80/80',
                    'rating': 4.7,
                    'size': '1000-5000 employees'
                },
                'description': 'Build beautiful mobile experiences for millions of music lovers. Work on cross-platform mobile apps using Flutter and Dart.',
                'location': 'Stockholm, Sweden (Remote OK)',
                'job_type': 'Full-time',
                'salary_min': 80000,
                'salary_max': 120000,
                'currency': 'EUR',
                'required_skills': ['Flutter', 'Dart', 'Mobile Development', 'REST APIs', 'State Management'],
                'preferred_skills': ['Firebase', 'GraphQL', 'CI/CD', 'App Store Optimization'],
                'experience_level': 'Mid-level',
                'posted_date': '2024-01-13',
                'application_deadline': '2024-02-13',
                'benefits': [
                    'Spotify Premium for family',
                    'Flexible working hours',
                    'Wellness allowance',
                    'Parental leave',
                    'Learning and development budget'
                ],
                'requirements': [
                    '3+ years of mobile development experience',
                    'Strong Flutter and Dart skills',
                    'Experience with app store deployment',
                    'Knowledge of mobile UI/UX best practices',
                    'Understanding of mobile performance optimization'
                ],
                'is_featured': False,
                'applications_count': 67,
                'views_count': 1400
            }
        ]
        
        return jsonify({
            'jobs': sample_jobs,
            'total': len(sample_jobs),
            'page': page,
            'per_page': per_page,
            'pages': 1
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get jobs: {str(e)}'}), 500

@jobs_bp.route('/jobs/<job_id>', methods=['GET'])
def get_job(job_id):
    try:
        # Sample job detail
        job_detail = {
            'id': job_id,
            'title': 'Senior Rust Developer',
            'company': {
                'id': 'company1',
                'name': 'Mozilla Corporation',
                'logo': '/api/placeholder/120/120',
                'cover_image': '/api/placeholder/800/200',
                'rating': 4.8,
                'size': '1000-5000 employees',
                'founded': '1998',
                'industry': 'Technology',
                'website': 'https://mozilla.org',
                'description': 'Mozilla is a global non-profit organization dedicated to making the internet a global public resource, open and accessible to all.',
                'locations': ['San Francisco', 'Toronto', 'Berlin', 'Remote'],
                'social_links': {
                    'linkedin': 'https://linkedin.com/company/mozilla-corporation',
                    'twitter': 'https://twitter.com/mozilla',
                    'github': 'https://github.com/mozilla'
                }
            },
            'description': '''
            Join our team building the next generation of web browsers and developer tools with Rust. You'll work on performance-critical systems and contribute to open-source projects that impact millions of users worldwide.
            
            **What you'll do:**
            • Develop and maintain core browser engine components
            • Optimize performance-critical code paths
            • Collaborate with open-source community
            • Design and implement new language features
            • Write comprehensive tests and documentation
            
            **Impact:**
            Your work will directly impact the browsing experience of millions of users and contribute to the advancement of web standards and technologies.
            ''',
            'location': 'San Francisco, CA (Remote OK)',
            'job_type': 'Full-time',
            'salary_min': 150000,
            'salary_max': 220000,
            'currency': 'USD',
            'equity': 'Yes',
            'required_skills': ['Rust', 'Systems Programming', 'WebAssembly', 'Git', 'Linux'],
            'preferred_skills': ['C++', 'JavaScript', 'Performance Optimization', 'LLVM', 'WebGL'],
            'experience_level': 'Senior',
            'posted_date': '2024-01-18',
            'application_deadline': '2024-02-18',
            'benefits': [
                'Health, dental, and vision insurance',
                'Unlimited PTO',
                'Remote work options',
                'Professional development budget ($3,000/year)',
                'Stock options',
                'Sabbatical program',
                'Wellness stipend',
                'Home office setup budget'
            ],
            'requirements': [
                '5+ years of systems programming experience',
                'Strong knowledge of Rust programming language',
                'Experience with concurrent and parallel programming',
                'Understanding of memory management and performance optimization',
                'Open source contribution experience preferred',
                'Experience with browser engines or similar large codebases',
                'Strong debugging and profiling skills'
            ],
            'nice_to_have': [
                'Contributions to Rust ecosystem',
                'Experience with WebAssembly',
                'Knowledge of web standards',
                'Graphics programming experience',
                'Compiler or language implementation experience'
            ],
            'team_info': {
       
(Content truncated due to size limit. Use line ranges to read in chunks)
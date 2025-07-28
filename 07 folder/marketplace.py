from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from src.models.user import db, User, Product

marketplace_bp = Blueprint('marketplace', __name__)

@marketplace_bp.route('/products', methods=['GET'])
def get_products():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 12, type=int)
        category = request.args.get('category')
        search = request.args.get('search')
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        
        # Sample products data
        sample_products = [
            {
                'id': '1',
                'name': 'Rust Development Toolkit',
                'description': 'Complete development environment setup for Rust programming',
                'seller': {
                    'id': 'seller1',
                    'name': 'DevTools Pro',
                    'rating': 4.8,
                    'avatar': '/api/placeholder/50/50'
                },
                'category': 'Development Tools',
                'price': 49.99,
                'original_price': 79.99,
                'discount': 38,
                'stock_quantity': 100,
                'images': ['/api/placeholder/300/300', '/api/placeholder/300/300'],
                'is_digital': True,
                'rating': 4.7,
                'reviews_count': 234,
                'technologies': ['Rust', 'IDE', 'Debugging Tools'],
                'features': [
                    'Advanced code completion',
                    'Integrated debugger',
                    'Performance profiler',
                    'Package manager integration'
                ]
            },
            {
                'id': '2',
                'name': 'Go Microservices Template',
                'description': 'Production-ready microservices template with Go and Kubernetes',
                'seller': {
                    'id': 'seller2',
                    'name': 'CloudNative Solutions',
                    'rating': 4.9,
                    'avatar': '/api/placeholder/50/50'
                },
                'category': 'Code Templates',
                'price': 89.99,
                'original_price': 129.99,
                'discount': 31,
                'stock_quantity': 50,
                'images': ['/api/placeholder/300/300', '/api/placeholder/300/300'],
                'is_digital': True,
                'rating': 4.8,
                'reviews_count': 156,
                'technologies': ['Go', 'Kubernetes', 'Docker', 'gRPC'],
                'features': [
                    'Docker containerization',
                    'Kubernetes deployment configs',
                    'CI/CD pipeline setup',
                    'Monitoring and logging'
                ]
            },
            {
                'id': '3',
                'name': 'TypeScript React Components Library',
                'description': 'Professional UI components library built with TypeScript and React',
                'seller': {
                    'id': 'seller3',
                    'name': 'UI Masters',
                    'rating': 4.6,
                    'avatar': '/api/placeholder/50/50'
                },
                'category': 'UI Components',
                'price': 69.99,
                'original_price': 99.99,
                'discount': 30,
                'stock_quantity': 200,
                'images': ['/api/placeholder/300/300', '/api/placeholder/300/300'],
                'is_digital': True,
                'rating': 4.5,
                'reviews_count': 89,
                'technologies': ['TypeScript', 'React', 'Styled Components'],
                'features': [
                    '50+ reusable components',
                    'TypeScript definitions',
                    'Storybook documentation',
                    'Theme customization'
                ]
            },
            {
                'id': '4',
                'name': 'Julia Scientific Computing Package',
                'description': 'High-performance computing libraries for scientific applications',
                'seller': {
                    'id': 'seller4',
                    'name': 'SciComp Labs',
                    'rating': 4.9,
                    'avatar': '/api/placeholder/50/50'
                },
                'category': 'Scientific Software',
                'price': 199.99,
                'original_price': 299.99,
                'discount': 33,
                'stock_quantity': 25,
                'images': ['/api/placeholder/300/300', '/api/placeholder/300/300'],
                'is_digital': True,
                'rating': 4.9,
                'reviews_count': 45,
                'technologies': ['Julia', 'CUDA', 'MPI', 'Linear Algebra'],
                'features': [
                    'GPU acceleration support',
                    'Parallel computing utilities',
                    'Advanced visualization',
                    'Benchmark suite included'
                ]
            },
            {
                'id': '5',
                'name': 'Python Django E-commerce Template',
                'description': 'Complete e-commerce solution built with Django and modern technologies',
                'seller': {
                    'id': 'seller5',
                    'name': 'WebDev Experts',
                    'rating': 4.7,
                    'avatar': '/api/placeholder/50/50'
                },
                'category': 'Web Templates',
                'price': 149.99,
                'original_price': 199.99,
                'discount': 25,
                'stock_quantity': 75,
                'images': ['/api/placeholder/300/300', '/api/placeholder/300/300'],
                'is_digital': True,
                'rating': 4.6,
                'reviews_count': 178,
                'technologies': ['Python', 'Django', 'PostgreSQL', 'Redis'],
                'features': [
                    'Payment gateway integration',
                    'Inventory management',
                    'Admin dashboard',
                    'Mobile responsive design'
                ]
            },
            {
                'id': '6',
                'name': 'Flutter Mobile App Starter Kit',
                'description': 'Professional mobile app template with authentication and backend integration',
                'seller': {
                    'id': 'seller6',
                    'name': 'Mobile Innovations',
                    'rating': 4.8,
                    'avatar': '/api/placeholder/50/50'
                },
                'category': 'Mobile Templates',
                'price': 119.99,
                'original_price': 159.99,
                'discount': 25,
                'stock_quantity': 60,
                'images': ['/api/placeholder/300/300', '/api/placeholder/300/300'],
                'is_digital': True,
                'rating': 4.7,
                'reviews_count': 92,
                'technologies': ['Flutter', 'Dart', 'Firebase', 'REST API'],
                'features': [
                    'User authentication',
                    'Push notifications',
                    'Offline support',
                    'State management (Bloc)'
                ]
            }
        ]
        
        return jsonify({
            'products': sample_products,
            'total': len(sample_products),
            'page': page,
            'per_page': per_page,
            'pages': 1
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get products: {str(e)}'}), 500

@marketplace_bp.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    try:
        # Sample product detail
        product_detail = {
            'id': product_id,
            'name': 'Rust Development Toolkit',
            'description': 'Complete development environment setup for Rust programming with advanced features for professional developers.',
            'long_description': '''
            This comprehensive Rust Development Toolkit provides everything you need to build high-performance applications with Rust. 
            
            **What's Included:**
            - Advanced IDE with intelligent code completion
            - Integrated debugger with memory visualization
            - Performance profiler and benchmarking tools
            - Package manager with dependency analysis
            - Code formatter and linter
            - Testing framework integration
            - Documentation generator
            
            **Key Features:**
            - Memory safety analysis
            - Ownership and borrowing checker
            - Async/await support
            - Cross-compilation tools
            - WebAssembly integration
            - FFI bindings generator
            
            **System Requirements:**
            - Windows 10/11, macOS 10.15+, or Linux
            - 4GB RAM minimum (8GB recommended)
            - 2GB free disk space
            - Internet connection for updates
            ''',
            'seller': {
                'id': 'seller1',
                'name': 'DevTools Pro',
                'bio': 'Professional development tools company specializing in Rust ecosystem',
                'rating': 4.8,
                'total_sales': 15420,
                'member_since': '2020-03-15',
                'avatar': '/api/placeholder/100/100',
                'social_links': {
                    'website': 'https://devtools-pro.com',
                    'github': 'https://github.com/devtools-pro',
                    'twitter': 'https://twitter.com/devtools_pro'
                }
            },
            'category': 'Development Tools',
            'price': 49.99,
            'original_price': 79.99,
            'discount': 38,
            'stock_quantity': 100,
            'images': [
                '/api/placeholder/800/600',
                '/api/placeholder/800/600',
                '/api/placeholder/800/600',
                '/api/placeholder/800/600'
            ],
            'is_digital': True,
            'file_size': '2.5 GB',
            'file_format': 'Installer Package',
            'license': 'Commercial License',
            'rating': 4.7,
            'reviews_count': 234,
            'technologies': ['Rust', 'IDE', 'Debugging Tools', 'Performance Analysis'],
            'features': [
                'Advanced code completion with AI assistance',
                'Integrated debugger with memory visualization',
                'Performance profiler and benchmarking tools',
                'Package manager integration',
                'Real-time error detection',
                'Code refactoring tools',
                'Git integration',
                'Plugin ecosystem'
            ],
            'related_courses': [
                {
                    'id': '1',
                    'title': 'Complete Rust Programming Bootcamp',
                    'price': 89.99,
                    'thumbnail': '/api/placeholder/200/150'
                },
                {
                    'id': '7',
                    'title': 'Advanced Rust Systems Programming',
                    'price': 129.99,
                    'thumbnail': '/api/placeholder/200/150'
                }
            ],
            'reviews': [
                {
                    'id': '1',
                    'user': {
                        'name': 'John D.',
                        'avatar': '/api/placeholder/40/40'
                    },
                    'rating': 5,
                    'title': 'Excellent development environment!',
                    'comment': 'This toolkit has significantly improved my Rust development workflow. The debugger is particularly impressive.',
                    'date': '2024-01-15',
                    'verified_purchase': True
                },
                {
                    'id': '2',
                    'user': {
                        'name': 'Maria S.',
                        'avatar': '/api/placeholder/40/40'
                    },
                    'rating': 4,
                    'title': 'Great tools, minor issues',
                    'comment': 'Overall very good, but the installation process could be smoother. Once set up, it works perfectly.',
                    'date': '2024-01-10',
                    'verified_purchase': True
                },
                {
                    'id': '3',
                    'user': {
                        'name': 'Alex K.',
                        'avatar': '/api/placeholder/40/40'
                    },
                    'rating': 5,
                    'title': 'Best Rust IDE I\'ve used',
                    'comment': 'The code completion and error detection are top-notch. Highly recommended for serious Rust development.',
                    'date': '2024-01-08',
                    'verified_purchase': True
                }
            ],
            'changelog': [
                {
                    'version': '2.1.0',
                    'date': '2024-01-20',
                    'changes': [
                        'Added WebAssembly debugging support',
                        'Improved memory profiler accuracy',
                        'Fixed syntax highlighting issues',
                        'Updated Rust toolchain to 1.75'
                    ]
                },
                {
                    'version': '2.0.5',
                    'date': '2024-01-10',
                    'changes': [
                        'Performance improvements',
                        'Bug fixes in code completion',
                        'Enhanced error messages'
                    ]
                }
            ]
        }
        
        return jsonify(product_detail), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get product: {str(e)}'}), 500

@marketplace_bp.route('/categories', methods=['GET'])
def get_categories():
    try:
        categories = [
            {'id': 'development-tools', 'name': 'Development Tools', 'count': 156},
            {'id': 'code-templates', 'name': 'Code Templates', 'count': 234},
            {'id': 'ui-components', 'name': 'UI Components', 'count': 189},
            {'id': 'mobile-templates', 'name': 'Mobile Templates', 'count': 98},
            {'id': 'web-templates', 'name': 'Web Templates', 'count': 145},
            {'id': 'scientific-software', 'name': 'Scientific Software', 'count': 67},
            {'id': 'plugins-extensions', 'name': 'Plugins & Extensions', 'count': 123},
            {'id': 'documentation', 'name': 'Documentation & Guides', 'count': 89}
        ]
        
        return jsonify({'categories': categories}), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get categories: {str(e)}'}), 500

@marketplace_bp.route('/cart', methods=['GET'])
@jwt_required()
def get_cart():
    try:
        current_user_id = get_jwt_identity()
        
        # Sample cart data
        cart_items = [
            {
                'id': '1',
                'product': {
                    'id': '1',
                    'name': 'Rust Development Toolkit',
                    'price': 49.99,
                    'image': '/api/placeholder/100/100'
                },
                'quantity': 1,
                'added_date': '2024-01-20'
            }
        ]
        
        total = sum(item['product']['price'] * item['quantity'] for item in cart_items)
        
        return jsonify({
            'items': cart_items,
            'total': total,
            'item_count': len(cart_items)
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to 
(Content truncated due to size limit. Use line ranges to read in chunks)
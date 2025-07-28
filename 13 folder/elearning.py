from flask import Blueprint, request, jsonify, session
from src.models.user import db
from datetime import datetime

elearning_bp = Blueprint('elearning', __name__)

def require_auth():
    """Check if user is authenticated"""
    if 'user_id' not in session:
        return False, jsonify({'error': 'Authentication required'}), 401
    return True, None, None

@elearning_bp.route('/courses', methods=['GET'])
def get_all_courses():
    """Get comprehensive course catalog with universal product linking"""
    try:
        # Comprehensive course catalog covering ALL e-commerce categories
        all_courses = {
            "technology_engineering": {
                "id": 1,
                "name": "Technology & Engineering",
                "icon": "Cpu",
                "subcategories": {
                    "electronics": {
                        "id": 11,
                        "name": "Electronics & Circuit Design",
                        "courses": [
                            {
                                "id": 101,
                                "title": "Drone Electronics & Circuits",
                                "duration": "8 weeks",
                                "difficulty": "Intermediate",
                                "price": 199.99,
                                "rating": 4.8,
                                "students": 2340,
                                "instructor": "Dr. Sarah Chen",
                                "description": "Master drone electronics from basic circuits to advanced flight controllers",
                                "linked_products": [
                                    {"id": 101, "name": "Professional Racing Drone", "category": "electronics_technology"},
                                    {"id": 102, "name": "Industrial Inspection Drone", "category": "electronics_technology"},
                                    {"id": 104, "name": "Arduino Mega Development Kit", "category": "electronics_technology"}
                                ],
                                "skills_gained": ["Circuit Design", "PCB Layout", "Flight Control Programming"],
                                "certificate": "Blockchain Verified",
                                "career_paths": ["Drone Engineer", "Electronics Engineer", "UAV Systems Designer"]
                            },
                            {
                                "id": 102,
                                "title": "Smartphone Repair & Electronics",
                                "duration": "6 weeks",
                                "difficulty": "Beginner",
                                "price": 149.99,
                                "rating": 4.7,
                                "students": 5670,
                                "instructor": "Mike Rodriguez",
                                "description": "Learn to repair smartphones, tablets, and mobile devices",
                                "linked_products": [
                                    {"id": 201, "name": "iPhone 15 Pro", "category": "electronics_technology"},
                                    {"id": 202, "name": "Samsung Galaxy S24", "category": "electronics_technology"},
                                    {"id": 203, "name": "iPad Pro", "category": "electronics_technology"}
                                ],
                                "skills_gained": ["Mobile Repair", "Microsoldering", "Diagnostics"],
                                "certificate": "Blockchain Verified",
                                "career_paths": ["Mobile Repair Technician", "Electronics Repair Specialist"]
                            }
                        ]
                    },
                    "robotics": {
                        "id": 12,
                        "name": "Robotics & AI",
                        "courses": [
                            {
                                "id": 103,
                                "title": "Humanoid Robot Programming",
                                "duration": "12 weeks",
                                "difficulty": "Advanced",
                                "price": 399.99,
                                "rating": 4.9,
                                "students": 890,
                                "instructor": "Prof. David Kim",
                                "description": "Program humanoid robots for research and commercial applications",
                                "linked_products": [
                                    {"id": 103, "name": "Humanoid Research Robot", "category": "electronics_technology"},
                                    {"id": 301, "name": "Robot Development Kit", "category": "electronics_technology"}
                                ],
                                "skills_gained": ["Robot Programming", "AI Integration", "Motion Control"],
                                "certificate": "Blockchain Verified",
                                "career_paths": ["Robotics Engineer", "AI Researcher", "Automation Specialist"]
                            }
                        ]
                    },
                    "programming": {
                        "id": 13,
                        "name": "Programming & Software",
                        "courses": [
                            {
                                "id": 104,
                                "title": "Mobile App Development",
                                "duration": "10 weeks",
                                "difficulty": "Intermediate",
                                "price": 299.99,
                                "rating": 4.8,
                                "students": 12340,
                                "instructor": "Lisa Wang",
                                "description": "Build iOS and Android apps from scratch",
                                "linked_products": [
                                    {"id": 201, "name": "iPhone 15 Pro", "category": "electronics_technology"},
                                    {"id": 202, "name": "Samsung Galaxy S24", "category": "electronics_technology"},
                                    {"id": 204, "name": "MacBook Pro", "category": "electronics_technology"}
                                ],
                                "skills_gained": ["iOS Development", "Android Development", "UI/UX Design"],
                                "certificate": "Blockchain Verified",
                                "career_paths": ["Mobile Developer", "Software Engineer", "App Entrepreneur"]
                            }
                        ]
                    }
                }
            },
            "fashion_design": {
                "id": 2,
                "name": "Fashion & Design",
                "icon": "Shirt",
                "subcategories": {
                    "fashion_design": {
                        "id": 21,
                        "name": "Fashion Design",
                        "courses": [
                            {
                                "id": 201,
                                "title": "Fashion Design Fundamentals",
                                "duration": "8 weeks",
                                "difficulty": "Beginner",
                                "price": 179.99,
                                "rating": 4.6,
                                "students": 3450,
                                "instructor": "Isabella Martinez",
                                "description": "Learn fashion design from sketching to pattern making",
                                "linked_products": [
                                    {"id": 401, "name": "Designer Evening Dress", "category": "fashion_apparel"},
                                    {"id": 402, "name": "Casual Summer Dress", "category": "fashion_apparel"},
                                    {"id": 403, "name": "Business Suit", "category": "fashion_apparel"}
                                ],
                                "skills_gained": ["Fashion Sketching", "Pattern Making", "Textile Knowledge"],
                                "certificate": "Blockchain Verified",
                                "career_paths": ["Fashion Designer", "Pattern Maker", "Fashion Illustrator"]
                            },
                            {
                                "id": 202,
                                "title": "Sustainable Fashion & Textiles",
                                "duration": "6 weeks",
                                "difficulty": "Intermediate",
                                "price": 199.99,
                                "rating": 4.7,
                                "students": 2180,
                                "instructor": "Dr. Emma Green",
                                "description": "Create eco-friendly fashion with sustainable materials",
                                "linked_products": [
                                    {"id": 404, "name": "Organic Cotton T-Shirt", "category": "fashion_apparel"},
                                    {"id": 405, "name": "Recycled Polyester Jacket", "category": "fashion_apparel"},
                                    {"id": 406, "name": "Hemp Jeans", "category": "fashion_apparel"}
                                ],
                                "skills_gained": ["Sustainable Design", "Eco-Materials", "Circular Fashion"],
                                "certificate": "Blockchain Verified",
                                "career_paths": ["Sustainable Fashion Designer", "Textile Researcher", "Eco-Fashion Consultant"]
                            }
                        ]
                    },
                    "jewelry_design": {
                        "id": 22,
                        "name": "Jewelry Design",
                        "courses": [
                            {
                                "id": 203,
                                "title": "Jewelry Making & Design",
                                "duration": "10 weeks",
                                "difficulty": "Intermediate",
                                "price": 249.99,
                                "rating": 4.8,
                                "students": 1560,
                                "instructor": "Master Craftsman John Silver",
                                "description": "Create beautiful jewelry from design to finished piece",
                                "linked_products": [
                                    {"id": 501, "name": "Diamond Engagement Ring", "category": "fashion_apparel"},
                                    {"id": 502, "name": "Gold Necklace", "category": "fashion_apparel"},
                                    {"id": 503, "name": "Silver Bracelet", "category": "fashion_apparel"}
                                ],
                                "skills_gained": ["Jewelry Design", "Metalworking", "Gem Setting"],
                                "certificate": "Blockchain Verified",
                                "career_paths": ["Jewelry Designer", "Goldsmith", "Jewelry Appraiser"]
                            }
                        ]
                    }
                }
            },
            "home_improvement": {
                "id": 3,
                "name": "Home & Garden",
                "icon": "Home",
                "subcategories": {
                    "home_automation": {
                        "id": 31,
                        "name": "Home Automation",
                        "courses": [
                            {
                                "id": 301,
                                "title": "Smart Home Technology",
                                "duration": "6 weeks",
                                "difficulty": "Intermediate",
                                "price": 189.99,
                                "rating": 4.7,
                                "students": 4320,
                                "instructor": "Tech Expert Alex Johnson",
                                "description": "Build and manage smart home systems",
                                "linked_products": [
                                    {"id": 601, "name": "Smart Thermostat", "category": "home_garden"},
                                    {"id": 602, "name": "Smart Door Lock", "category": "home_garden"},
                                    {"id": 603, "name": "Smart Security Camera", "category": "home_garden"},
                                    {"id": 604, "name": "Smart Light Bulbs", "category": "home_garden"}
                                ],
                                "skills_gained": ["IoT Setup", "Home Networking", "Automation Programming"],
                                "certificate": "Blockchain Verified",
                                "career_paths": ["Smart Home Installer", "IoT Technician", "Home Automation Consultant"]
                            }
                        ]
                    },
                    "woodworking": {
                        "id": 32,
                        "name": "Woodworking & Carpentry",
                        "courses": [
                            {
                                "id": 302,
                                "title": "Furniture Making Masterclass",
                                "duration": "12 weeks",
                                "difficulty": "Intermediate",
                                "price": 299.99,
                                "rating": 4.9,
                                "students": 2890,
                                "instructor": "Master Carpenter Robert Wood",
                                "description": "Create beautiful custom furniture from scratch",
                                "linked_products": [
                                    {"id": 701, "name": "Dining Table Set", "category": "home_garden"},
                                    {"id": 702, "name": "Bookshelf", "category": "home_garden"},
                                    {"id": 703, "name": "Coffee Table", "category": "home_garden"},
                                    {"id": 704, "name": "Power Tools Set", "category": "home_garden"}
                                ],
                                "skills_gained": ["Woodworking", "Furniture Design", "Tool Usage"],
                                "certificate": "Blockchain Verified",
                                "career_paths": ["Furniture Maker", "Carpenter", "Custom Woodworker"]
                            }
                        ]
                    },
                    "gardening": {
                        "id": 33,
                        "name": "Gardening & Horticulture",
                        "courses": [
                            {
                                "id": 303,
                                "title": "Organic Gardening Complete Guide",
                                "duration": "8 weeks",
                                "difficulty": "Beginner",
                                "price": 149.99,
                                "rating": 4.8,
                                "students": 6780,
                                "instructor": "Garden Expert Maria Flores",
                                "description": "Grow organic vegetables, herbs, and flowers",
                                "linked_products": [
                                    {"id": 801, "name": "Garden Tool Set", "category": "home_garden"},
                                    {"id": 802, "name": "Organic Seeds Collection", "category": "home_garden"},
                                    {"id": 803, "name": "Compost Bin", "category": "home_garden"},
                                    {"id": 804, "name": "Garden Hose System", "category": "home_garden"}
                                ],
                                "skills_gained": ["Organic Gardening", "Plant Care", "Soil Management"],
                                "certificate": "Blockchain Verified",
                                "career_paths": ["Organic Farmer", "Garden Designer", "Horticulturist"]
                            }
                        ]
                    }
                }
            },
            "health_fitness": {
                "id": 4,
                "name": "Health & Fitness",
                "icon": "Heart",
                "subcategories": {
                    "fitness_training": {
                        "id": 41,
                        "name": "Fitness & Training",
                        "courses": [
                            {
                                "id": 401,
                                "title": "Personal Trainer Certification",
                                "duration": "10 weeks",
                                "difficulty": "Intermediate",
                                "price": 349.99,
                                "rating": 4.9,
                                "students": 5430,
                                "instructor": "Fitness Expert Jake Strong",
                                "description": "Become a certified personal trainer",
                                "linked_products": [
                                    {"id": 901, "name": "Home Gym Equipment Set", "category": "health_beauty"},
                                    {"id": 902, "name": "Fitness Tracker Watch", "category": "health_beauty"},
                                    {"id": 903, "name": "Protein Supplements", "category": "health_beauty"},
                                    {"id": 904, "name": "Yoga Mat", "category": "health_beauty"}
                                ],
                                "skills_gained": ["Exercise Science", "Nutrition", "Client Training"],
                                "certificate": "Blockchain Verified",
                                "career_paths": ["Personal Trainer", "Fitness Coach", "Gym Manager"]
                            }
                        ]
                    },
                    "nutrition": {
                        "id": 42,
                        "name": "Nutrition & Wellness",
                        "courses": [
                            {
                                "id": 402,
                                "title": "Sports Nutrition Specialist",
                                "duration": "8 weeks",
                                "difficulty": "Advanced",
                                "price": 279.99,
                                "rating": 4.8,
                                "students": 3210,
                                "instructor": "Dr. Nutrition Sarah Health",
                                "description": "Master sports nutrition and supplementation",
                                "linked_products": [
                                    {"id": 903, "name": "Protein Supplements", "category": "health_beauty"},
                                    {"id": 905, "name": "Vitamin Complex", "category": "health_beauty"},
                                    {"id": 906, "name": "Energy Bars", "category": "food_beverages"},
                                    {"id": 907, "name": "Sports Drinks", "category": "food_beverages"}
                                ],
                                "skills_gained": ["Sports Nutrition", "Supplement Science", "Meal Planning"],
                                "certificate": "Blockchain Verified",
                                "career_paths": ["Sports Nutritionist", "Wellness Coach", "Supplement Consultant"]
                            }
                        ]
                    }
                }
            },
            "automotive_mechanical": {
                "id": 5,
                "name": "Automotive & Mechanical",
                "icon": "Car",
                "subcategories": {
                    "auto_repair": {
                        "id": 51,
                        "name": "Auto Repair & Maintenance",
                        "courses": [
                            {
                                "id": 501,
                                "title": "Complete Auto Repair Course",
                                "duration": "16 weeks",
                                "difficulty": "Intermediate",
                                "price": 449.99,
                                "rating": 4.8,
                                "students": 4560,
                                "instructor": "Master Mechanic Tony Wrench",
                                "description": "Learn to repair and maintain all vehicle systems",
                                "linked_products": [
                                    {"id": 1001, "name": "Brake Pads Set", "category": "automotive"},
                                    {"id": 1002, "name": "Engine Oil", "category": "automotive"},
                                    {"id": 1003, "name": "Car Battery", "category": "automotive"},
                                    {"id": 1004, "name": "Auto Tool Set", "category": "automotive"}
                                ],
                                "skills_gained": ["Engine Repair", "Brake Systems", "Electrical Diagnostics"],
                                "certificate": "Blockchain Verified",
                                "career_paths": ["Auto Mechanic", "Service Technician", "Shop Owner"]
                            }
                        ]
                    },
                    "electric_vehicles": {
                        "id": 52,
                        "name": "Electric Vehicle Technology",
                        "courses": [
                            {
                                "id": 502,
                                "title": "EV Repair & Maintenance",
                                "duration": "12 weeks",
                                "difficulty": "Advanced",
                                "price": 399.99,
                                "rating": 4.9,
                                "students": 2340,
                                "instructor": "EV Expert Dr. Electric",
                                "description": "Specialize in electric vehicle technology",
                                "linked_products": [
                                    {"id": 1101, "name": "Tesla Model 3", "category": "automotive"},
                                    {"id": 1102, "name": "EV Charging Station", "category": "automotive"},
                                    {"id": 1103, "name": "EV Battery Pack", "category": "automotive"},
                                    {"id": 1104, "name": "EV Diagnostic Tools", "category": "automotive"}
                                ],
                                "skills_gained": ["EV Systems", "Battery Technology", "Charging Infrastructure"],
                                "certificate": "Blockchain Verified",
                                "career_paths": ["EV Technician", "Charging Station Installer", "EV Engineer"]
                            }
                        ]
                    }
                }
            },
            "culinary_arts": {
                "id": 6,
                "name": "Culinary Arts & Food",
                "icon": "ChefHat",
                "subcategories": {
                    "professional_cooking": {
                        "id": 61,
                        "name": "Professional Cooking",
                        "courses": [
                            {
                                "id": 601,
                                "title": "Culinary Arts Professional",
                                "duration": "20 weeks",
                                "difficulty": "Intermediate",
                                "price": 599.99,
                                "rating": 4.9,
                                "students": 3450,
                                "instructor": "Chef Gordon Excellence",
                                "description": "Master professional cooking techniques",
                                "linked_products": [
                                    {"id": 1201, "name": "Professional Chef Knife Set", "category": "food_beverages"},
                                    {"id": 1202, "name": "Commercial Blender", "category": "food_beverages"},
                                    {"id": 1203, "name": "Cast Iron Cookware", "category": "food_beverages"},
                                    {"id": 1204, "name": "Spice Collection", "category": "food_beverages"}
                                ],
                                "skills_gained": ["Knife Skills", "Cooking Techniques", "Menu Planning"],
                                "certificate": "Blockchain Verified",
                                "career_paths": ["Professional Chef", "Restaurant Owner", "Culinary Instructor"]
                            }
                        ]
                    },
                    "baking_pastry": {
                        "id": 62,
                        "name": "Baking & Pastry",
                        "courses": [
                            {
                                "id": 602,
                                "title": "Professional Baking & Pastry",
                                "duration": "14 weeks",
                                "difficulty": "Intermediate",
                                "price": 449.99,
                                "rating": 4.8,
                                "students": 2890,
                                "instructor": "Pastry Chef Marie Sweet",
                                "description": "Master the art of baking and pastry making",
                                "linked_products": [
                                    {"id": 1301, "name": "Stand Mixer Professional", "category": "food_beverages"},
                                    {"id": 1302, "name": "Baking Tools Set", "category": "food_beverages"},
                                    {"id": 1303, "name": "Pastry Ingredients Kit", "category": "food_beverages"},
                                    {"id": 1304, "name": "Convection Oven", "category": "food_beverages"}
                                ],
                                "skills_gained": ["Bread Making", "Pastry Techniques", "Cake Decorating"],
                                "certificate": "Blockchain Verified",
                                "career_paths": ["Pastry Chef", "Bakery Owner", "Cake Designer"]
                            }
                        ]
                    }
                }
            },
            "business_entrepreneurship": {
                "id": 7,
                "name": "Business & Entrepreneurship",
                "icon": "Briefcase",
                "subcategories": {
                    "ecommerce_business": {
                        "id": 71,
                        "name": "E-commerce & Online Business",
                        "courses": [
                            {
                                "id": 701,
                                "title": "E-commerce Business Mastery",
                                "duration": "12 weeks",
                                "difficulty": "Intermediate",
                                "price": 349.99,
                                "rating": 4.8,
                                "students": 8760,
                                "instructor": "Business Expert Lisa Success",
                                "description": "Build and scale successful online businesses",
                                "linked_products": [
                                    {"id": 1401, "name": "Business Laptop", "category": "electronics_technology"},
                                    {"id": 1402, "name": "Office Desk Setup", "category": "business_industrial"},
                                    {"id": 1403, "name": "Shipping Supplies", "category": "business_industrial"},
                                    {"id": 1404, "name": "Inventory Software", "category": "business_industrial"}
                                ],
                                "skills_gained": ["E-commerce Strategy", "Digital Marketing", "Supply Chain"],
                                "certificate": "Blockchain Verified",
                                "career_paths": ["E-commerce Entrepreneur", "Online Store Manager", "Digital Marketer"]
                            }
                        ]
                    }
                }
            },
            "arts_creativity": {
                "id": 8,
                "name": "Arts & Creativity",
                "icon": "Palette",
                "subcategories": {
                    "digital_art": {
                        "id": 81,
                        "name": "Digital Art & Design",
                        "courses": [
                            {
                                "id": 801,
                                "title": "Digital Art & Illustration",
                                "duration": "10 weeks",
                                "difficulty": "Intermediate",
                                "price": 279.99,
                                "rating": 4.7,
                                "students": 5670,
                                "instructor": "Artist Pro Creative",
                                "description": "Create stunning digital artwork and illustrations",
                                "linked_products": [
                                    {"id": 1501, "name": "Graphics Tablet", "category": "electronics_technology"},
                                    {"id": 1502, "name": "Digital Art Software", "category": "electronics_technology"},
                                    {"id": 1503, "name": "Color Calibration Monitor", "category": "electronics_technology"},
                                    {"id": 1504, "name": "Stylus Pen", "category": "electronics_technology"}
                                ],
                                "skills_gained": ["Digital Painting", "Illustration", "Graphic Design"],
                                "certificate": "Blockchain Verified",
                                "career_paths": ["Digital Artist", "Illustrator", "Graphic Designer"]
                            }
                        ]
                    }
                }
            }
        }
        
        # Calculate total courses and students
        total_courses = 0
        total_students = 0
        for category in all_courses.values():
            for subcategory in category.get('subcategories', {}).values():
                for course in subcategory.get('courses', []):
                    total_courses += 1
                    total_students += course.get('students', 0)
        
        return jsonify({
            'courses': all_courses,
            'total_categories': len(all_courses),
            'total_courses': total_courses,
            'total_students': total_students,
            'featured_courses': [
                {'id': 101, 'title': 'Drone Electronics & Circuits', 'category': 'technology_engineering'},
                {'id': 201, 'title': 'Fashion Design Fundamentals', 'category': 'fashion_design'},
                {'id': 301, 'title': 'Smart Home Technology', 'category': 'home_improvement'},
                {'id': 401, 'title': 'Personal Trainer Certification', 'category': 'health_fitness'}
            ]
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch courses', 'details': str(e)}), 500

@elearning_bp.route('/courses/<int:course_id>', methods=['GET'])
def get_course_details(course_id):
    """Get detailed course information with product integration"""
    try:
        course_details = {
            "id": course_id,
            "title": "Drone Electronics & Circuits",
            "category": "technology_engineering",
            "subcategory": "electronics",
            "duration": "8 weeks",
            "difficulty": "Intermediate",
            "price": 199.99,
            "original_price": 249.99,
            "discount": 20,
            "rating": 4.8,
            "reviews_count": 234,
            "students_enrolled": 2340,
            "completion_rate": 87,
            "instructor": {
                "id": 1001,
                "name": "Dr. Sarah Chen",
                "title": "Electronics Engineering Professor",
                "experience": "15 years",
                "rating": 4.9,
                "students_taught": 15670,
                "bio": "Leading expert in drone electronics and autonomous systems",
                "credentials": ["PhD Electronics Engineering", "IEEE Senior Member", "Drone Industry Consultant"]
            },
            "description": "Master drone electronics from basic circuits to advanced flight controllers. Learn to design, build, and program drone systems.",
            "detailed_description": "This comprehensive course covers everything from basic electronic principles to advanced drone flight control systems. You'll learn circuit design, PCB layout, programming, and system integration.",
            
            # Course Content Structure
            "curriculum": {
                "weeks": [
                    {
                        "week": 1,
                        "title": "Electronics Fundamentals",
                        "topics": ["Ohm's Law", "Circuit Analysis", "Component Identification"],
                        "duration": "6 hours",
                        "assignments": 2,
                        "linked_products": [
                            {"id": 104, "name": "Arduino Mega Development Kit", "relevance": "Practice platform"}
                        ]
                    },
                    {
                        "week": 2,
                        "title": "Power Systems & Batteries",
                        "topics": ["LiPo Batteries", "Power Distribution", "Voltage Regulation"],
                        "duration": "7 hours",
                        "assignments": 3,
                        "linked_products": [
                            {"id": 1601, "name": "LiPo Battery Pack", "relevance": "Hands-on practice"},
                            {"id": 1602, "name": "Battery Charger", "relevance": "Essential tool"}
                        ]
                    },
                    {
                        "week": 3,
                        "title": "Motor Control Systems",
                        "topics": ["Brushless Motors", "ESCs", "PWM Control"],
                        "duration": "8 hours",
                        "assignments": 2,
                        "linked_products": [
                            {"id": 1603, "name": "Brushless Motor Set", "relevance": "Course project"},
                            {"id": 1604, "name": "ESC Controllers", "relevance": "Required component"}
                        ]
                    },
                    {
                        "week": 4,
                        "title": "Sensors & Navigation",
                        "topics": ["IMU Sensors", "GPS Systems", "Sensor Fusion"],
                        "duration": "7 hours",
                        "assignments": 3,
                        "linked_products": [
                            {"id": 1605, "name": "IMU Sensor Module", "relevance": "Lab exercises"},
                            {"id": 1606, "name": "GPS Module", "relevance": "Navigation project"}
                        ]
                    },
                    {
                        "week": 5,
                        "title": "Flight Controllers",
                        "topics": ["Autopilot Systems", "PID Control", "Stabilization"],
                        "duration": "9 hours",
                        "assignments": 2,
                        "linked_products": [
                            {"id": 1607, "name": "Flight Controller Board", "relevance": "Core component"},
                            {"id": 101, "name": "Professional Racing Drone", "relevance": "Reference platform"}
                        ]
                    },
                    {
                        "week": 6,
                        "title": "Communication Systems",
                        "topics": ["Radio Systems", "Telemetry", "FPV Video"],
                        "duration": "6 hours",
                        "assignments": 2,
                        "linked_products": [
                            {"id": 1608, "name": "Radio Transmitter", "relevance": "Control system"},
                            {"id": 1609, "name": "FPV Camera", "relevance": "Video system"}
                        ]
                    },
                    {
                        "week": 7,
                        "title": "PCB Design & Manufacturing",
                        "topics": ["Circuit Layout", "PCB Design Software", "Manufacturing"],
                        "duration": "8 hours",
                        "assignments": 1,
                        "linked_products": [
                            {"id": 1610, "name": "PCB Design Software", "relevance": "Design tool"},
                            {"id": 1611, "name": "Soldering Kit", "relevance": "Assembly tool"}
                        ]
                    },
                    {
                        "week": 8,
                        "title": "Final Project & Testing",
                        "topics": ["System Integration", "Testing", "Troubleshooting"],
                        "duration": "10 hours",
                        "assignments": 1,
                        "linked_products": [
                            {"id": 102, "name": "Industrial Inspection Drone", "relevance": "Advanced example"},
                            {"id": 1612, "name": "Testing Equipment", "relevance": "Validation tools"}
                        ]
                    }
                ]
            },
            
            # Learning Outcomes & Skills
            "learning_outcomes": [
                "Design and analyze drone electronic circuits",
                "Program flight control systems",
                "Integrate sensors and navigation systems",
                "Create PCB layouts for drone electronics",
                "Troubleshoot and repair drone systems",
                "Understand power management and battery systems"
            ],
            "skills_gained": [
                "Circuit Design & Analysis",
                "PCB Layout & Design",
                "Embedded Programming",
                "Sensor Integration",
                "Power Electronics",
                "System Testing & Validation"
            ],
            
            # Product Integration & Recommendations
            "product_integration": {
                "required_products": [
                    {
                        "id": 104,
                        "name": "Arduino Mega Development Kit",
                        "price": 89.99,
                        "reason": "Essential for hands-on programming exercises",
                        "week_used": [1, 2, 3]
                    },
                    {
                        "id": 1611,
                        "name": "Soldering Kit",
                        "price": 45.99,
                        "reason": "Required for circuit assembly projects",
                        "week_used": [3, 4, 7, 8]
                    }
                ],
                "recommended_products": [
                    {
                        "id": 101,
                        "name": "Professional Racing Drone",
                        "price": 899.99,
                        "discount": 15,
                        "final_price": 764.99,
                        "reason": "Perfect platform to apply learned skills",
                        "bundle_savings": 135.00
                    },
                    {
                        "id": 1607,
                        "name": "Flight Controller Board",
                        "price": 129.99,
                        "reason": "Advanced project component",
                        "week_used": [5, 6, 8]
                    }
                ],
                "optional_products": [
                    {
                        "id": 1608,
                        "name": "Radio Transmitter",
                        "price": 199.99,
                        "reason": "For complete drone control system",
                        "week_used": [6]
                    }
                ]
            },
            
            # Blockchain CV Integration
            "blockchain_integration": {
                "certificate_type": "Blockchain Verified Professional Certificate",
                "skills_added_to_cv": [
                    "Drone Electronics Design",
                    "Flight Control Programming",
                    "PCB Design & Layout",
                    "Embedded Systems Development",
                    "Sensor Integration",
                    "Power Electronics"
                ],
                "job_matching_keywords": [
                    "Drone Engineer",
                    "Electronics Engineer", 
                    "UAV Systems Designer",
                    "Flight Control Engineer",
                    "Embedded Systems Engineer",
                    "Aerospace Electronics"
                ],
                "career_advancement": {
                    "entry_level": "Electronics Technician ($45,000-$55,000)",
                    "mid_level": "Drone Engineer ($65,000-$85,000)",
                    "senior_level": "UAV Systems Architect ($90,000-$120,000)"
                }
            },
            
            # Prerequisites & Requirements
            "prerequisites": [
                "Basic understanding of electronics",
                "High school mathematics",
                "Computer with internet access"
            ],
            "requirements": {
                "time_commitment": "8-10 hours per week",
                "equipment_needed": "Arduino kit, basic tools",
                "software": "Free software provided",
                "internet": "Stable internet connection required"
            },
            
            # Assessment & Certification
            "assessment": {
                "quizzes": 16,
                "assignments": 16,
                "projects": 3,
                "final_exam": True,
                "passing_grade": 80,
                "certificate_requirements": [
                    "Complete all assignments",
                    "Pass final exam (80%+)",
                    "Submit final project"
                ]
            },
            
            # Support & Community
            "support": {
                "instructor_access": "Direct messaging",
                "response_time": "< 24 hours",
                "office_hours": "Weekly live sessions",
                "community_forum": True,
                "peer_support": "Study groups available"
            }
        }
        
        return jsonify({
            'course': course_details,
            'success': True
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch course details', 'details': str(e)}), 500

@elearning_bp.route('/product-course-links/<int:product_id>', methods=['GET'])
def get_product_course_links(product_id):
    """Get all courses related to a specific product"""
    try:
        # Universal product-to-course linking system
        product_course_links = {
            "product_id": product_id,
            "product_name": "Professional Racing Drone",
            "related_courses": [
                {
                    "id": 101,
                    "title": "Drone Electronics & Circuits",
                    "relevance": "Core Technology",
                    "match_percentage": 95,
                    "price": 199.99,
                    "duration": "8 weeks",
                    "skills": ["Circuit Design", "Flight Control", "Electronics"]
                },
                {
                    "id": 102,
                    "title": "Aerodynamics & Flight Control",
                    "relevance": "Flight Mechanics",
                    "match_percentage": 88,
                    "price": 249.99,
                    "duration": "6 weeks",
                    "skills": ["Aerodynamics", "Control Theory", "Flight Dynamics"]
                },
                {
                    "id": 103,
                    "title": "CAD Design for Drones",
                    "relevance": "Design & Manufacturing",
                    "match_percentage": 75,
                    "price": 149.99,
                    "duration": "4 weeks",
                    "skills": ["CAD Design", "3D Modeling", "Manufacturing"]
                },
                {
                    "id": 104,
                    "title": "Drone Photography & Videography",
                    "relevance": "Applications",
                    "match_percentage": 65,
                    "price": 179.99,
                    "duration": "5 weeks",
                    "skills": ["Photography", "Video Production", "Drone Operations"]
                },
                {
                    "id": 105,
                    "title": "Drone Business & Regulations",
                    "relevance": "Commercial Use",
                    "match_percentage": 60,
                    "price": 129.99,
                    "duration": "3 weeks",
                    "skills": ["Business Planning", "Regulations", "Commercial Operations"]
                }
            ],
            "learning_path": {
                "title": "Complete Drone Mastery Path",
                "total_courses": 5,
                "total_duration": "26 weeks",
                "total_price": 909.95,
                "bundle_price": 649.99,
                "savings": 259.96,
                "completion_order": [101, 103, 102, 104, 105]
            }
        }
        
        return jsonify({
            'product_course_links': product_course_links,
            'success': True
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch product course links', 'details': str(e)}), 500

@elearning_bp.route('/enroll', methods=['POST'])
def enroll_in_course():
    """Enroll user in a course with automatic CV update"""
    is_auth, error_response, status_code = require_auth()
    if not is_auth:
        return error_response, status_code
    
    try:
        data = request.get_json()
        course_id = data.get('course_id')
        user_id = session['user_id']
        
        if not course_id:
            return jsonify({'error': 'Course ID is required'}), 400
        
        # In a real implementation, you would:
        # 1. Process payment
        # 2. Enroll user in course
        # 3. Update blockchain CV with enrolled course
        # 4. Trigger job matching algorithm
        
        enrollment_result = {
            "enrollment_id": f"ENR_{user_id}_{course_id}_{int(datetime.now().timestamp())}",
            "course_id": course_id,
            "user_id": user_id,
            "enrollment_date": datetime.now().isoformat(),
            "status": "enrolled",
            "blockchain_cv_updated": True,
            "skills_added": [
                "Drone Electronics",
                "Circuit Design", 
                "Flight Control Programming"
            ],
            "job_matches_triggered": True,
            "estimated_completion": "8 weeks",
            "certificate_blockchain_address": f"0x{course_id:04d}{user_id:04d}blockchain"
        }
        
        return jsonify({
            'enrollment': enrollment_result,
            'message': 'Successfully enrolled in course',
            'success': True
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Enrollment failed', 'details': str(e)}), 500


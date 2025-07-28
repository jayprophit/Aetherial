from flask import Blueprint, request, jsonify, session
from src.models.user import db
from datetime import datetime

ecommerce_bp = Blueprint('ecommerce', __name__)

def require_auth():
    """Check if user is authenticated"""
    if 'user_id' not in session:
        return False, jsonify({'error': 'Authentication required'}), 401
    return True, None, None

@ecommerce_bp.route('/categories', methods=['GET'])
def get_all_categories():
    """Get comprehensive cascading categories covering all genres and industries"""
    try:
        all_categories = {
            "electronics_technology": {
                "id": 1,
                "name": "Electronics & Technology",
                "icon": "Zap",
                "subcategories": {
                    "drones_uavs": {
                        "id": 11,
                        "name": "Drones & UAVs",
                        "icon": "Plane",
                        "sub_subcategories": {
                            "racing_drones": {"name": "Racing Drones", "count": 156},
                            "camera_drones": {"name": "Camera Drones", "count": 234},
                            "industrial_drones": {"name": "Industrial Drones", "count": 89},
                            "military_drones": {"name": "Military/Defense", "count": 45},
                            "delivery_drones": {"name": "Delivery Drones", "count": 67}
                        }
                    },
                    "robotics": {
                        "id": 12,
                        "name": "Robotics",
                        "icon": "Bot",
                        "sub_subcategories": {
                            "humanoid_robots": {"name": "Humanoid Robots", "count": 34},
                            "industrial_robots": {"name": "Industrial Robots", "count": 78},
                            "service_robots": {"name": "Service Robots", "count": 123},
                            "educational_robots": {"name": "Educational Robots", "count": 189},
                            "pet_robots": {"name": "Pet/Companion Robots", "count": 56}
                        }
                    },
                    "smart_devices": {
                        "id": 13,
                        "name": "Smart Devices & IoT",
                        "icon": "Smartphone",
                        "sub_subcategories": {
                            "smart_home": {"name": "Smart Home", "count": 567},
                            "wearables": {"name": "Wearables", "count": 345},
                            "smart_appliances": {"name": "Smart Appliances", "count": 234},
                            "iot_sensors": {"name": "IoT Sensors", "count": 456},
                            "smart_security": {"name": "Smart Security", "count": 289}
                        }
                    },
                    "computers_laptops": {
                        "id": 14,
                        "name": "Computers & Laptops",
                        "icon": "Monitor",
                        "sub_subcategories": {
                            "gaming_pcs": {"name": "Gaming PCs", "count": 234},
                            "workstations": {"name": "Workstations", "count": 156},
                            "laptops": {"name": "Laptops", "count": 789},
                            "tablets": {"name": "Tablets", "count": 345},
                            "accessories": {"name": "Accessories", "count": 567}
                        }
                    }
                }
            },
            "fashion_apparel": {
                "id": 2,
                "name": "Fashion & Apparel",
                "icon": "Shirt",
                "subcategories": {
                    "mens_clothing": {
                        "id": 21,
                        "name": "Men's Clothing",
                        "icon": "User",
                        "sub_subcategories": {
                            "casual_wear": {"name": "Casual Wear", "count": 1234},
                            "formal_wear": {"name": "Formal Wear", "count": 567},
                            "sportswear": {"name": "Sportswear", "count": 890},
                            "outerwear": {"name": "Outerwear", "count": 456},
                            "underwear": {"name": "Underwear", "count": 234}
                        }
                    },
                    "womens_clothing": {
                        "id": 22,
                        "name": "Women's Clothing",
                        "icon": "UserCheck",
                        "sub_subcategories": {
                            "dresses": {"name": "Dresses", "count": 2345},
                            "tops_blouses": {"name": "Tops & Blouses", "count": 1567},
                            "pants_jeans": {"name": "Pants & Jeans", "count": 1234},
                            "activewear": {"name": "Activewear", "count": 890},
                            "lingerie": {"name": "Lingerie", "count": 567}
                        }
                    },
                    "shoes_footwear": {
                        "id": 23,
                        "name": "Shoes & Footwear",
                        "icon": "Footprints",
                        "sub_subcategories": {
                            "sneakers": {"name": "Sneakers", "count": 1890},
                            "dress_shoes": {"name": "Dress Shoes", "count": 567},
                            "boots": {"name": "Boots", "count": 789},
                            "sandals": {"name": "Sandals", "count": 456},
                            "athletic_shoes": {"name": "Athletic Shoes", "count": 1234}
                        }
                    },
                    "accessories": {
                        "id": 24,
                        "name": "Accessories",
                        "icon": "Watch",
                        "sub_subcategories": {
                            "jewelry": {"name": "Jewelry", "count": 2345},
                            "watches": {"name": "Watches", "count": 890},
                            "bags_purses": {"name": "Bags & Purses", "count": 1567},
                            "belts": {"name": "Belts", "count": 456},
                            "sunglasses": {"name": "Sunglasses", "count": 789}
                        }
                    }
                }
            },
            "home_garden": {
                "id": 3,
                "name": "Home & Garden",
                "icon": "Home",
                "subcategories": {
                    "furniture": {
                        "id": 31,
                        "name": "Furniture",
                        "icon": "Sofa",
                        "sub_subcategories": {
                            "living_room": {"name": "Living Room", "count": 1234},
                            "bedroom": {"name": "Bedroom", "count": 890},
                            "dining_room": {"name": "Dining Room", "count": 567},
                            "office": {"name": "Office", "count": 456},
                            "outdoor": {"name": "Outdoor", "count": 345}
                        }
                    },
                    "appliances": {
                        "id": 32,
                        "name": "Appliances",
                        "icon": "Refrigerator",
                        "sub_subcategories": {
                            "kitchen": {"name": "Kitchen", "count": 789},
                            "laundry": {"name": "Laundry", "count": 345},
                            "cleaning": {"name": "Cleaning", "count": 234},
                            "hvac": {"name": "HVAC", "count": 156},
                            "small_appliances": {"name": "Small Appliances", "count": 567}
                        }
                    },
                    "tools_hardware": {
                        "id": 33,
                        "name": "Tools & Hardware",
                        "icon": "Wrench",
                        "sub_subcategories": {
                            "power_tools": {"name": "Power Tools", "count": 456},
                            "hand_tools": {"name": "Hand Tools", "count": 789},
                            "hardware": {"name": "Hardware", "count": 345},
                            "safety_equipment": {"name": "Safety Equipment", "count": 234},
                            "measuring_tools": {"name": "Measuring Tools", "count": 156}
                        }
                    },
                    "garden_outdoor": {
                        "id": 34,
                        "name": "Garden & Outdoor",
                        "icon": "TreePine",
                        "sub_subcategories": {
                            "gardening_tools": {"name": "Gardening Tools", "count": 345},
                            "plants_seeds": {"name": "Plants & Seeds", "count": 567},
                            "outdoor_furniture": {"name": "Outdoor Furniture", "count": 234},
                            "grills_outdoor_cooking": {"name": "Grills & Outdoor Cooking", "count": 189},
                            "lawn_care": {"name": "Lawn Care", "count": 278}
                        }
                    }
                }
            },
            "health_beauty": {
                "id": 4,
                "name": "Health & Beauty",
                "icon": "Heart",
                "subcategories": {
                    "skincare": {
                        "id": 41,
                        "name": "Skincare",
                        "icon": "Sparkles",
                        "sub_subcategories": {
                            "face_care": {"name": "Face Care", "count": 1234},
                            "body_care": {"name": "Body Care", "count": 890},
                            "anti_aging": {"name": "Anti-Aging", "count": 567},
                            "acne_treatment": {"name": "Acne Treatment", "count": 345},
                            "natural_organic": {"name": "Natural & Organic", "count": 456}
                        }
                    },
                    "fitness_wellness": {
                        "id": 42,
                        "name": "Fitness & Wellness",
                        "icon": "Dumbbell",
                        "sub_subcategories": {
                            "exercise_equipment": {"name": "Exercise Equipment", "count": 567},
                            "supplements": {"name": "Supplements", "count": 890},
                            "yoga_meditation": {"name": "Yoga & Meditation", "count": 345},
                            "fitness_trackers": {"name": "Fitness Trackers", "count": 234},
                            "recovery_therapy": {"name": "Recovery & Therapy", "count": 189}
                        }
                    },
                    "medical_devices": {
                        "id": 43,
                        "name": "Medical Devices",
                        "icon": "Stethoscope",
                        "sub_subcategories": {
                            "diagnostic_tools": {"name": "Diagnostic Tools", "count": 234},
                            "monitoring_devices": {"name": "Monitoring Devices", "count": 345},
                            "therapeutic_devices": {"name": "Therapeutic Devices", "count": 189},
                            "mobility_aids": {"name": "Mobility Aids", "count": 156},
                            "first_aid": {"name": "First Aid", "count": 278}
                        }
                    }
                }
            },
            "automotive": {
                "id": 5,
                "name": "Automotive",
                "icon": "Car",
                "subcategories": {
                    "car_parts": {
                        "id": 51,
                        "name": "Car Parts",
                        "icon": "Settings",
                        "sub_subcategories": {
                            "engine_parts": {"name": "Engine Parts", "count": 567},
                            "brake_parts": {"name": "Brake Parts", "count": 345},
                            "electrical": {"name": "Electrical", "count": 234},
                            "suspension": {"name": "Suspension", "count": 189},
                            "exhaust": {"name": "Exhaust", "count": 156}
                        }
                    },
                    "accessories": {
                        "id": 52,
                        "name": "Accessories",
                        "icon": "Wrench",
                        "sub_subcategories": {
                            "interior": {"name": "Interior", "count": 456},
                            "exterior": {"name": "Exterior", "count": 345},
                            "electronics": {"name": "Electronics", "count": 234},
                            "performance": {"name": "Performance", "count": 189},
                            "maintenance": {"name": "Maintenance", "count": 278}
                        }
                    },
                    "electric_vehicles": {
                        "id": 53,
                        "name": "Electric Vehicles",
                        "icon": "Zap",
                        "sub_subcategories": {
                            "ev_cars": {"name": "Electric Cars", "count": 89},
                            "ev_bikes": {"name": "Electric Bikes", "count": 234},
                            "ev_scooters": {"name": "Electric Scooters", "count": 156},
                            "charging_equipment": {"name": "Charging Equipment", "count": 123},
                            "ev_accessories": {"name": "EV Accessories", "count": 67}
                        }
                    }
                }
            },
            "sports_recreation": {
                "id": 6,
                "name": "Sports & Recreation",
                "icon": "Trophy",
                "subcategories": {
                    "team_sports": {
                        "id": 61,
                        "name": "Team Sports",
                        "icon": "Users",
                        "sub_subcategories": {
                            "football": {"name": "Football", "count": 345},
                            "basketball": {"name": "Basketball", "count": 234},
                            "soccer": {"name": "Soccer", "count": 456},
                            "baseball": {"name": "Baseball", "count": 189},
                            "volleyball": {"name": "Volleyball", "count": 123}
                        }
                    },
                    "outdoor_activities": {
                        "id": 62,
                        "name": "Outdoor Activities",
                        "icon": "Mountain",
                        "sub_subcategories": {
                            "camping": {"name": "Camping", "count": 567},
                            "hiking": {"name": "Hiking", "count": 456},
                            "fishing": {"name": "Fishing", "count": 345},
                            "hunting": {"name": "Hunting", "count": 234},
                            "cycling": {"name": "Cycling", "count": 789}
                        }
                    },
                    "water_sports": {
                        "id": 63,
                        "name": "Water Sports",
                        "icon": "Waves",
                        "sub_subcategories": {
                            "swimming": {"name": "Swimming", "count": 234},
                            "surfing": {"name": "Surfing", "count": 156},
                            "diving": {"name": "Diving", "count": 123},
                            "boating": {"name": "Boating", "count": 189},
                            "water_skiing": {"name": "Water Skiing", "count": 89}
                        }
                    },
                    "gaming_esports": {
                        "id": 64,
                        "name": "Gaming & Esports",
                        "icon": "Gamepad2",
                        "sub_subcategories": {
                            "gaming_pcs": {"name": "Gaming PCs", "count": 345},
                            "consoles": {"name": "Consoles", "count": 234},
                            "gaming_accessories": {"name": "Gaming Accessories", "count": 567},
                            "esports_gear": {"name": "Esports Gear", "count": 189},
                            "vr_ar": {"name": "VR/AR", "count": 123}
                        }
                    }
                }
            },
            "books_media": {
                "id": 7,
                "name": "Books & Media",
                "icon": "Book",
                "subcategories": {
                    "books": {
                        "id": 71,
                        "name": "Books",
                        "icon": "BookOpen",
                        "sub_subcategories": {
                            "fiction": {"name": "Fiction", "count": 2345},
                            "non_fiction": {"name": "Non-Fiction", "count": 1890},
                            "textbooks": {"name": "Textbooks", "count": 567},
                            "children_books": {"name": "Children's Books", "count": 890},
                            "ebooks": {"name": "E-Books", "count": 3456}
                        }
                    },
                    "music": {
                        "id": 72,
                        "name": "Music",
                        "icon": "Music",
                        "sub_subcategories": {
                            "vinyl_records": {"name": "Vinyl Records", "count": 567},
                            "cds": {"name": "CDs", "count": 345},
                            "digital_music": {"name": "Digital Music", "count": 2345},
                            "instruments": {"name": "Instruments", "count": 456},
                            "audio_equipment": {"name": "Audio Equipment", "count": 789}
                        }
                    },
                    "movies_tv": {
                        "id": 73,
                        "name": "Movies & TV",
                        "icon": "Film",
                        "sub_subcategories": {
                            "dvd_bluray": {"name": "DVD/Blu-ray", "count": 456},
                            "digital_movies": {"name": "Digital Movies", "count": 1234},
                            "tv_shows": {"name": "TV Shows", "count": 890},
                            "documentaries": {"name": "Documentaries", "count": 345},
                            "streaming_services": {"name": "Streaming Services", "count": 234}
                        }
                    },
                    "games": {
                        "id": 74,
                        "name": "Games",
                        "icon": "Dice6",
                        "sub_subcategories": {
                            "video_games": {"name": "Video Games", "count": 1567},
                            "board_games": {"name": "Board Games", "count": 456},
                            "card_games": {"name": "Card Games", "count": 234},
                            "puzzle_games": {"name": "Puzzle Games", "count": 189},
                            "educational_games": {"name": "Educational Games", "count": 123}
                        }
                    }
                }
            },
            "food_beverages": {
                "id": 8,
                "name": "Food & Beverages",
                "icon": "UtensilsCrossed",
                "subcategories": {
                    "gourmet_specialty": {
                        "id": 81,
                        "name": "Gourmet & Specialty",
                        "icon": "ChefHat",
                        "sub_subcategories": {
                            "artisan_foods": {"name": "Artisan Foods", "count": 345},
                            "international_cuisine": {"name": "International Cuisine", "count": 567},
                            "organic_foods": {"name": "Organic Foods", "count": 456},
                            "gluten_free": {"name": "Gluten-Free", "count": 234},
                            "vegan_vegetarian": {"name": "Vegan/Vegetarian", "count": 389}
                        }
                    },
                    "beverages": {
                        "id": 82,
                        "name": "Beverages",
                        "icon": "Coffee",
                        "sub_subcategories": {
                            "coffee_tea": {"name": "Coffee & Tea", "count": 567},
                            "wine_spirits": {"name": "Wine & Spirits", "count": 345},
                            "craft_beer": {"name": "Craft Beer", "count": 234},
                            "soft_drinks": {"name": "Soft Drinks", "count": 189},
                            "health_drinks": {"name": "Health Drinks", "count": 156}
                        }
                    },
                    "cooking_baking": {
                        "id": 83,
                        "name": "Cooking & Baking",
                        "icon": "Cookie",
                        "sub_subcategories": {
                            "baking_supplies": {"name": "Baking Supplies", "count": 234},
                            "spices_seasonings": {"name": "Spices & Seasonings", "count": 345},
                            "cooking_oils": {"name": "Cooking Oils", "count": 156},
                            "meal_kits": {"name": "Meal Kits", "count": 189},
                            "kitchen_gadgets": {"name": "Kitchen Gadgets", "count": 278}
                        }
                    }
                }
            },
            "business_industrial": {
                "id": 9,
                "name": "Business & Industrial",
                "icon": "Building2",
                "subcategories": {
                    "office_supplies": {
                        "id": 91,
                        "name": "Office Supplies",
                        "icon": "FileText",
                        "sub_subcategories": {
                            "stationery": {"name": "Stationery", "count": 456},
                            "office_furniture": {"name": "Office Furniture", "count": 234},
                            "printing_supplies": {"name": "Printing Supplies", "count": 189},
                            "technology": {"name": "Technology", "count": 345},
                            "organization": {"name": "Organization", "count": 123}
                        }
                    },
                    "manufacturing": {
                        "id": 92,
                        "name": "Manufacturing",
                        "icon": "Factory",
                        "sub_subcategories": {
                            "3d_printing": {"name": "3D Printing", "count": 234},
                            "cnc_machines": {"name": "CNC Machines", "count": 156},
                            "industrial_tools": {"name": "Industrial Tools", "count": 345},
                            "safety_equipment": {"name": "Safety Equipment", "count": 189},
                            "quality_control": {"name": "Quality Control", "count": 123}
                        }
                    },
                    "professional_services": {
                        "id": 93,
                        "name": "Professional Services",
                        "icon": "Briefcase",
                        "sub_subcategories": {
                            "consulting": {"name": "Consulting", "count": 189},
                            "legal_services": {"name": "Legal Services", "count": 123},
                            "accounting": {"name": "Accounting", "count": 156},
                            "marketing": {"name": "Marketing", "count": 234},
                            "it_services": {"name": "IT Services", "count": 278}
                        }
                    }
                }
            },
            "art_collectibles": {
                "id": 10,
                "name": "Art & Collectibles",
                "icon": "Palette",
                "subcategories": {
                    "fine_art": {
                        "id": 101,
                        "name": "Fine Art",
                        "icon": "Paintbrush2",
                        "sub_subcategories": {
                            "paintings": {"name": "Paintings", "count": 345},
                            "sculptures": {"name": "Sculptures", "count": 156},
                            "photography": {"name": "Photography", "count": 234},
                            "digital_art": {"name": "Digital Art", "count": 189},
                            "mixed_media": {"name": "Mixed Media", "count": 123}
                        }
                    },
                    "collectibles": {
                        "id": 102,
                        "name": "Collectibles",
                        "icon": "Star",
                        "sub_subcategories": {
                            "vintage_antiques": {"name": "Vintage & Antiques", "count": 567},
                            "coins_currency": {"name": "Coins & Currency", "count": 234},
                            "stamps": {"name": "Stamps", "count": 156},
                            "trading_cards": {"name": "Trading Cards", "count": 345},
                            "memorabilia": {"name": "Memorabilia", "count": 189}
                        }
                    },
                    "crafts_handmade": {
                        "id": 103,
                        "name": "Crafts & Handmade",
                        "icon": "Scissors",
                        "sub_subcategories": {
                            "jewelry": {"name": "Handmade Jewelry", "count": 456},
                            "pottery_ceramics": {"name": "Pottery & Ceramics", "count": 234},
                            "textiles": {"name": "Textiles", "count": 189},
                            "woodworking": {"name": "Woodworking", "count": 156},
                            "metalwork": {"name": "Metalwork", "count": 123}
                        }
                    }
                }
            }
        }
        
        # Calculate total products across all categories
        total_products = 0
        for category in all_categories.values():
            for subcategory in category.get('subcategories', {}).values():
                for sub_subcat in subcategory.get('sub_subcategories', {}).values():
                    total_products += sub_subcat.get('count', 0)
        
        return jsonify({
            'categories': all_categories,
            'total_categories': len(all_categories),
            'total_subcategories': sum(len(cat.get('subcategories', {})) for cat in all_categories.values()),
            'total_products': total_products,
            'featured_categories': [
                'electronics_technology',
                'fashion_apparel', 
                'home_garden',
                'health_beauty',
                'automotive',
                'sports_recreation'
            ]
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch categories', 'details': str(e)}), 500

@ecommerce_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product_details(product_id):
    """Get detailed product information with comprehensive learning integration"""
    try:
        # Enhanced product details with learning integration for ALL categories
        product_details = {
            "id": product_id,
            "name": "Professional Racing Drone",
            "category": "electronics_technology",
            "subcategory": "drones_uavs",
            "sub_subcategory": "racing_drones",
            "price": 899.99,
            "original_price": 1199.99,
            "discount": 25,
            "currency": "USD",
            "images": [
                "https://images.unsplash.com/photo-1473968512647-3e447244af8f?w=800",
                "https://images.unsplash.com/photo-1508614589041-895b88991e3e?w=800",
                "https://images.unsplash.com/photo-1446776877081-d282a0f896e2?w=800",
                "https://images.unsplash.com/photo-1551808525-51a94da548ce?w=800"
            ],
            "rating": 4.8,
            "reviews_count": 156,
            "description": "Professional-grade racing drone designed for competitive FPV racing and aerial photography.",
            "detailed_description": "This cutting-edge racing drone combines speed, agility, and precision in a lightweight carbon fiber frame. Perfect for both competitive racing and professional aerial photography.",
            
            # Comprehensive Technical Specifications with Learning Integration
            "technical_specs": {
                "materials": [
                    {
                        "name": "Carbon Fiber Frame",
                        "description": "Ultra-lightweight yet durable composite material",
                        "properties": {
                            "weight": "45g",
                            "tensile_strength": "3500 MPa",
                            "density": "1.6 g/cm³"
                        },
                        "learning_courses": [
                            {"id": 301, "title": "Composite Materials Engineering", "duration": "6 weeks", "price": 199.99},
                            {"id": 302, "title": "Carbon Fiber Manufacturing", "duration": "4 weeks", "price": 149.99}
                        ]
                    },
                    {
                        "name": "Aluminum Alloy Motors",
                        "description": "High-performance brushless motors with precision bearings",
                        "properties": {
                            "power": "2300KV",
                            "efficiency": "85%",
                            "operating_temp": "-20°C to 60°C"
                        },
                        "learning_courses": [
                            {"id": 303, "title": "Electric Motor Design & Control", "duration": "8 weeks", "price": 249.99},
                            {"id": 304, "title": "Brushless Motor Technology", "duration": "5 weeks", "price": 179.99}
                        ]
                    }
                ],
                "components": [
                    {
                        "name": "Flight Controller",
                        "description": "Advanced autopilot system with GPS and IMU",
                        "specifications": {
                            "processor": "ARM Cortex-M7",
                            "sensors": "9-axis IMU, Barometer, GPS",
                            "update_rate": "8kHz"
                        },
                        "learning_courses": [
                            {"id": 305, "title": "Flight Control Systems", "duration": "10 weeks", "price": 299.99},
                            {"id": 306, "title": "Autopilot Programming", "duration": "8 weeks", "price": 249.99}
                        ]
                    },
                    {
                        "name": "Electronic Speed Controllers (ESCs)",
                        "description": "32-bit ESCs with active braking and telemetry",
                        "specifications": {
                            "current": "35A continuous",
                            "voltage": "3-6S LiPo",
                            "protocol": "DShot1200"
                        },
                        "learning_courses": [
                            {"id": 307, "title": "Power Electronics & Motor Control", "duration": "8 weeks", "price": 229.99},
                            {"id": 308, "title": "ESC Programming & Tuning", "duration": "4 weeks", "price": 149.99}
                        ]
                    }
                ],
                "circuits": [
                    {
                        "name": "Power Distribution Board",
                        "description": "Distributes power to all components with filtering",
                        "schematic_available": True,
                        "pcb_files_included": True,
                        "learning_courses": [
                            {"id": 309, "title": "PCB Design & Layout", "duration": "6 weeks", "price": 199.99},
                            {"id": 310, "title": "Power Distribution Systems", "duration": "5 weeks", "price": 179.99}
                        ]
                    },
                    {
                        "name": "Radio Receiver Circuit",
                        "description": "2.4GHz receiver with diversity antennas",
                        "schematic_available": True,
                        "learning_courses": [
                            {"id": 311, "title": "RF Circuit Design", "duration": "8 weeks", "price": 249.99},
                            {"id": 312, "title": "Antenna Design & Theory", "duration": "6 weeks", "price": 199.99}
                        ]
                    }
                ],
                "patents": [
                    {
                        "number": "US10123456",
                        "title": "Autonomous Flight Control System",
                        "description": "Advanced algorithms for autonomous navigation and obstacle avoidance",
                        "filing_date": "2020-03-15",
                        "learning_courses": [
                            {"id": 313, "title": "Patent Research & Analysis", "duration": "4 weeks", "price": 149.99},
                            {"id": 314, "title": "Intellectual Property Law", "duration": "6 weeks", "price": 199.99}
                        ]
                    }
                ]
            },
            
            # Comprehensive Learning Integration
            "learning_integration": {
                "recommended_learning_paths": [
                    {
                        "id": 1,
                        "title": "Complete Drone Engineering Mastery",
                        "description": "From beginner to expert drone engineer",
                        "total_duration": "24 weeks",
                        "total_courses": 8,
                        "difficulty": "Beginner to Advanced",
                        "price": 1599.99,
                        "bundle_price": 999.99,
                        "savings": 600.00,
                        "courses": [
                            {"id": 201, "title": "Drone Fundamentals", "duration": "3 weeks", "difficulty": "Beginner"},
                            {"id": 202, "title": "Electronics for Drones", "duration": "4 weeks", "difficulty": "Intermediate"},
                            {"id": 203, "title": "Flight Dynamics & Control", "duration": "4 weeks", "difficulty": "Intermediate"},
                            {"id": 204, "title": "Advanced Autopilot Systems", "duration": "5 weeks", "difficulty": "Advanced"},
                            {"id": 205, "title": "Drone Manufacturing", "duration": "3 weeks", "difficulty": "Intermediate"},
                            {"id": 206, "title": "Commercial Drone Operations", "duration": "2 weeks", "difficulty": "Intermediate"},
                            {"id": 207, "title": "Drone Repair & Maintenance", "duration": "2 weeks", "difficulty": "Beginner"},
                            {"id": 208, "title": "Drone Business & Regulations", "duration": "1 week", "difficulty": "Beginner"}
                        ],
                        "career_outcomes": [
                            "Drone Engineer",
                            "UAV Systems Designer", 
                            "Flight Control Engineer",
                            "Drone Pilot/Operator",
                            "Drone Business Owner"
                        ],
                        "certification": "Blockchain-Verified Professional Drone Engineer Certificate"
                    }
                ],
                "skill_development": {
                    "technical_skills": [
                        "Circuit Design & Analysis",
                        "PCB Layout & Manufacturing",
                        "Flight Control Programming",
                        "3D CAD Design",
                        "Materials Engineering",
                        "RF System Design",
                        "Power Electronics",
                        "Embedded Systems Programming"
                    ],
                    "business_skills": [
                        "Product Development",
                        "Patent Research",
                        "Regulatory Compliance",
                        "Project Management",
                        "Quality Assurance",
                        "Supply Chain Management"
                    ]
                },
                "blockchain_cv_integration": {
                    "auto_update": True,
                    "skills_added": [
                        "Drone Technology",
                        "UAV Systems",
                        "Flight Control",
                        "Electronics Engineering"
                    ],
                    "certificates_earned": "Auto-added to blockchain CV upon course completion",
                    "job_matching": "Automatically matched with relevant drone engineering jobs"
                }
            },
            
            # Manufacturing & DIY Information
            "manufacturing_info": {
                "blueprints_available": True,
                "cad_files_included": [
                    "Frame Design (STEP, STL)",
                    "Motor Mounts (STEP, STL)", 
                    "Camera Gimbal (STEP, STL)",
                    "Landing Gear (STEP, STL)"
                ],
                "assembly_guide": {
                    "included": True,
                    "format": "Interactive 3D guide + Video tutorials",
                    "estimated_time": "8-12 hours",
                    "difficulty": "Intermediate"
                },
                "tools_required": [
                    "Soldering Iron (60W)",
                    "Hex Key Set (1.5-3mm)",
                    "Digital Multimeter",
                    "Heat Shrink Tubing",
                    "Wire Strippers",
                    "Screwdriver Set"
                ],
                "bill_of_materials": {
                    "total_components": 47,
                    "estimated_cost": "$650",
                    "suppliers_list": "Included with purchase"
                }
            },
            
            # Seller Information
            "seller": {
                "id": 1001,
                "name": "AeroTech Innovations",
                "rating": 4.9,
                "total_sales": 2340,
                "years_in_business": 8,
                "verified": True,
                "certifications": ["ISO 9001", "CE Certified", "FCC Approved"],
                "social_links": {
                    "website": "https://aerotech-innovations.com",
                    "youtube": "https://youtube.com/aerotechinnovations",
                    "instagram": "@aerotechinnovations",
                    "linkedin": "company/aerotech-innovations",
                    "twitter": "@aerotechinnov"
                },
                "support": {
                    "warranty": "2 years full warranty",
                    "support_hours": "24/7 technical support",
                    "response_time": "< 2 hours"
                }
            },
            
            # Stock and Shipping
            "availability": {
                "in_stock": True,
                "quantity": 47,
                "shipping": {
                    "free_shipping": True,
                    "standard_delivery": "2-3 business days",
                    "express_delivery": "Next day (additional $29.99)",
                    "international": "5-10 business days"
                },
                "return_policy": {
                    "period": "30 days",
                    "condition": "Unopened original packaging",
                    "return_shipping": "Free return shipping"
                }
            },
            
            # Related Products & Recommendations
            "recommendations": {
                "frequently_bought_together": [
                    {"id": 1002, "name": "FPV Goggles Pro", "price": 299.99},
                    {"id": 1003, "name": "Radio Controller", "price": 199.99},
                    {"id": 1004, "name": "LiPo Battery Pack", "price": 89.99}
                ],
                "customers_also_viewed": [
                    {"id": 1005, "name": "Camera Drone Pro", "price": 1299.99},
                    {"id": 1006, "name": "Racing Drone Kit", "price": 599.99}
                ]
            }
        }
        
        return jsonify({
            'product': product_details,
            'success': True
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch product details', 'details': str(e)}), 500

# Additional routes for comprehensive e-commerce functionality would continue here...
# Including cart management, checkout, order tracking, reviews, etc.


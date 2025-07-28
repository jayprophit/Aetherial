from flask import Blueprint, jsonify, request
import random
from datetime import datetime, timedelta

products_bp = Blueprint('products', __name__)

# Comprehensive product categories and data
PRODUCT_CATEGORIES = {
    "Electronics & Tech": {
        "icon": "📱",
        "subcategories": ["Smartphones", "Laptops", "Components", "Accessories", "Smart Home"],
        "products": [
            {
                "id": 1,
                "name": "Quantum Processing Unit - QPU-2024",
                "seller": "QuantumTech Industries",
                "price": 15999.99,
                "original_price": 18999.99,
                "rating": 4.9,
                "reviews": 234,
                "stock": 15,
                "category": "Components",
                "subcategory": "Processors",
                "description": "Revolutionary quantum processing unit for advanced computing applications",
                "features": ["128 Qubits", "Quantum Error Correction", "Cryogenic Cooling", "API Integration"],
                "specifications": {
                    "Qubits": "128 Physical, 64 Logical",
                    "Coherence Time": "100 microseconds",
                    "Gate Fidelity": "99.9%",
                    "Operating Temperature": "15 millikelvin",
                    "Connectivity": "Quantum Network Ready"
                },
                "images": [
                    "https://example.com/qpu1.jpg",
                    "https://example.com/qpu2.jpg",
                    "https://example.com/qpu3.jpg"
                ],
                "videos": ["https://example.com/qpu_demo.mp4"],
                "cad_files": ["qpu_schematic.dwg", "qpu_3d_model.step"],
                "materials": ["Superconducting Niobium", "Silicon Substrate", "Aluminum Wiring"],
                "manufacturing": "Precision lithography and ion beam etching",
                "related_courses": [1, 2],  # Quantum ML courses
                "seller_info": {
                    "company": "QuantumTech Industries",
                    "rating": 4.8,
                    "years_active": 8,
                    "total_sales": 1250,
                    "response_time": "< 2 hours",
                    "social_links": {
                        "website": "https://quantumtech.com",
                        "linkedin": "https://linkedin.com/company/quantumtech",
                        "twitter": "https://twitter.com/quantumtech"
                    }
                },
                "shipping": {
                    "free_shipping": True,
                    "estimated_delivery": "3-5 business days",
                    "international": True,
                    "special_handling": "Temperature controlled"
                },
                "warranty": "2 years manufacturer warranty",
                "return_policy": "30 days return policy"
            },
            {
                "id": 2,
                "name": "AI Neural Chip - NeuralCore X1",
                "seller": "BrainTech Solutions",
                "price": 2499.99,
                "original_price": 2999.99,
                "rating": 4.7,
                "reviews": 567,
                "stock": 45,
                "category": "Components",
                "subcategory": "AI Chips",
                "description": "Advanced neural processing chip for AI and machine learning applications",
                "features": ["1000 TOPS Performance", "Low Power Consumption", "Edge AI Optimized", "TensorFlow Compatible"],
                "specifications": {
                    "Performance": "1000 TOPS",
                    "Power": "15W TDP",
                    "Memory": "32GB HBM3",
                    "Interfaces": "PCIe 5.0, USB-C",
                    "AI Frameworks": "TensorFlow, PyTorch, ONNX"
                },
                "images": [
                    "https://example.com/neural1.jpg",
                    "https://example.com/neural2.jpg"
                ],
                "videos": ["https://example.com/neural_demo.mp4"],
                "materials": ["7nm Silicon", "Copper Interconnects", "Thermal Interface Material"],
                "manufacturing": "Advanced semiconductor fabrication",
                "related_courses": [1, 3],  # AI courses
                "seller_info": {
                    "company": "BrainTech Solutions",
                    "rating": 4.6,
                    "years_active": 5,
                    "total_sales": 3420,
                    "response_time": "< 1 hour"
                },
                "shipping": {
                    "free_shipping": True,
                    "estimated_delivery": "2-4 business days",
                    "international": True
                },
                "warranty": "3 years manufacturer warranty"
            }
        ]
    },
    "Digital Products": {
        "icon": "💾",
        "subcategories": ["Software", "Apps", "Games", "Digital Art", "Templates"],
        "products": [
            {
                "id": 3,
                "name": "Advanced CAD Design Suite Pro",
                "seller": "DesignMaster Studios",
                "price": 899.99,
                "original_price": 1299.99,
                "rating": 4.8,
                "reviews": 1234,
                "stock": 999,  # Digital product - unlimited
                "category": "Software",
                "subcategory": "CAD Software",
                "description": "Professional CAD software for mechanical, electrical, and architectural design",
                "features": ["3D Modeling", "Simulation", "Rendering", "Collaboration Tools", "Cloud Sync"],
                "specifications": {
                    "File Formats": "DWG, STEP, IGES, STL, OBJ",
                    "Operating System": "Windows, macOS, Linux",
                    "RAM": "8GB minimum, 16GB recommended",
                    "Graphics": "OpenGL 4.0 compatible",
                    "License": "Perpetual with 1 year updates"
                },
                "images": [
                    "https://example.com/cad1.jpg",
                    "https://example.com/cad2.jpg"
                ],
                "videos": ["https://example.com/cad_demo.mp4"],
                "demo_available": True,
                "demo_link": "https://example.com/cad_demo",
                "file_size": "2.5 GB",
                "download_format": "Installer Package",
                "related_courses": [6, 7],  # Robotics and IoT courses
                "seller_info": {
                    "company": "DesignMaster Studios",
                    "rating": 4.9,
                    "years_active": 12,
                    "total_sales": 15670
                },
                "instant_download": True,
                "license_type": "Commercial Use Allowed"
            },
            {
                "id": 4,
                "name": "AI Music Generation Engine",
                "seller": "SoundAI Labs",
                "price": 199.99,
                "original_price": 299.99,
                "rating": 4.6,
                "reviews": 890,
                "stock": 999,
                "category": "Software",
                "subcategory": "Audio Software",
                "description": "AI-powered music generation software for composers and producers",
                "features": ["Multiple Genres", "Real-time Generation", "MIDI Export", "VST Plugin", "Royalty-free"],
                "specifications": {
                    "Audio Formats": "WAV, MP3, FLAC, MIDI",
                    "Sample Rate": "Up to 192kHz",
                    "Bit Depth": "24-bit",
                    "Plugin Formats": "VST3, AU, AAX",
                    "Operating System": "Windows, macOS"
                },
                "images": [
                    "https://example.com/music1.jpg",
                    "https://example.com/music2.jpg"
                ],
                "audio_previews": [
                    "https://example.com/preview1.mp3",
                    "https://example.com/preview2.mp3",
                    "https://example.com/preview3.mp3"
                ],
                "demo_available": True,
                "file_size": "850 MB",
                "related_courses": [1],  # AI courses
                "seller_info": {
                    "company": "SoundAI Labs",
                    "rating": 4.7,
                    "years_active": 6,
                    "total_sales": 5430
                },
                "instant_download": True,
                "license_type": "Royalty-free Commercial License"
            }
        ]
    },
    "Books & Education": {
        "icon": "📚",
        "subcategories": ["Technical Books", "Research Papers", "Guides", "Tutorials", "Documentation"],
        "products": [
            {
                "id": 5,
                "name": "Advanced Quantum Computing: Theory and Practice",
                "seller": "Academic Press Digital",
                "price": 89.99,
                "original_price": 129.99,
                "rating": 4.9,
                "reviews": 456,
                "stock": 999,
                "category": "Technical Books",
                "subcategory": "Quantum Computing",
                "description": "Comprehensive guide to quantum computing algorithms and implementations",
                "features": ["600+ Pages", "Code Examples", "Interactive Simulations", "Problem Sets"],
                "specifications": {
                    "Format": "PDF, EPUB, Interactive Web",
                    "Pages": "624",
                    "Language": "English",
                    "Publication": "2024 Edition",
                    "ISBN": "978-0-123456-78-9"
                },
                "images": [
                    "https://example.com/book1.jpg",
                    "https://example.com/book2.jpg"
                ],
                "preview_pages": 25,
                "table_of_contents": [
                    "Chapter 1: Quantum Mechanics Fundamentals",
                    "Chapter 2: Quantum Gates and Circuits",
                    "Chapter 3: Quantum Algorithms",
                    "Chapter 4: Quantum Error Correction",
                    "Chapter 5: Quantum Machine Learning",
                    "Chapter 6: Practical Implementations"
                ],
                "authors": ["Dr. Alice Quantum", "Prof. Bob Entanglement"],
                "file_size": "45 MB",
                "related_courses": [2],  # Quantum ML course
                "seller_info": {
                    "company": "Academic Press Digital",
                    "rating": 4.8,
                    "years_active": 15,
                    "total_sales": 12340
                },
                "instant_download": True,
                "drm_free": True
            },
            {
                "id": 6,
                "name": "Emotional AI Development Handbook",
                "seller": "TechBooks Publishing",
                "price": 69.99,
                "original_price": 99.99,
                "rating": 4.7,
                "reviews": 234,
                "stock": 999,
                "category": "Technical Books",
                "subcategory": "Artificial Intelligence",
                "description": "Complete guide to developing emotionally intelligent AI systems",
                "features": ["450+ Pages", "Python Code", "Case Studies", "Research References"],
                "specifications": {
                    "Format": "PDF, EPUB",
                    "Pages": "456",
                    "Language": "English",
                    "Publication": "2024 Edition",
                    "ISBN": "978-0-987654-32-1"
                },
                "images": [
                    "https://example.com/ebook1.jpg"
                ],
                "preview_pages": 30,
                "authors": ["Dr. Sarah Chen", "Dr. Michael Rodriguez"],
                "file_size": "38 MB",
                "related_courses": [1],  # Emotional AI course
                "seller_info": {
                    "company": "TechBooks Publishing",
                    "rating": 4.6,
                    "years_active": 8,
                    "total_sales": 8760
                },
                "instant_download": True,
                "drm_free": True
            }
        ]
    },
    "Hardware & Components": {
        "icon": "🔧",
        "subcategories": ["Sensors", "Actuators", "Boards", "Modules", "Tools"],
        "products": [
            {
                "id": 7,
                "name": "IoT Sensor Development Kit",
                "seller": "IoTech Components",
                "price": 299.99,
                "original_price": 399.99,
                "rating": 4.8,
                "reviews": 345,
                "stock": 78,
                "category": "Development Kits",
                "subcategory": "IoT",
                "description": "Complete IoT sensor development kit with multiple sensors and connectivity options",
                "features": ["20+ Sensors", "WiFi/Bluetooth", "Cloud Integration", "Mobile App", "Open Source"],
                "specifications": {
                    "Microcontroller": "ESP32-S3",
                    "Sensors": "Temperature, Humidity, Pressure, Light, Motion, Gas",
                    "Connectivity": "WiFi 6, Bluetooth 5.0, LoRaWAN",
                    "Power": "Battery + Solar Panel",
                    "Enclosure": "IP65 Rated"
                },
                "images": [
                    "https://example.com/iot1.jpg",
                    "https://example.com/iot2.jpg",
                    "https://example.com/iot3.jpg"
                ],
                "videos": ["https://example.com/iot_demo.mp4"],
                "cad_files": ["iot_pcb.kicad", "enclosure.step"],
                "materials": ["PCB", "Plastic Enclosure", "Electronic Components"],
                "manufacturing": "SMT Assembly and Testing",
                "related_courses": [7],  # IoT course
                "seller_info": {
                    "company": "IoTech Components",
                    "rating": 4.7,
                    "years_active": 7,
                    "total_sales": 2340
                },
                "shipping": {
                    "free_shipping": True,
                    "estimated_delivery": "5-7 business days",
                    "international": True
                },
                "warranty": "1 year manufacturer warranty"
            }
        ]
    },
    "Services & Consulting": {
        "icon": "🎯",
        "subcategories": ["AI Consulting", "Development Services", "Training", "Support", "Custom Solutions"],
        "products": [
            {
                "id": 8,
                "name": "Custom AI Model Development Service",
                "seller": "AI Solutions Pro",
                "price": 4999.99,
                "original_price": 7499.99,
                "rating": 4.9,
                "reviews": 89,
                "stock": 10,  # Limited availability
                "category": "AI Consulting",
                "subcategory": "Custom Development",
                "description": "Professional AI model development service for enterprise applications",
                "features": ["Custom Architecture", "Training & Optimization", "Deployment Support", "6 Months Support"],
                "specifications": {
                    "Delivery Time": "4-8 weeks",
                    "Model Types": "Classification, Regression, NLP, Computer Vision",
                    "Frameworks": "TensorFlow, PyTorch, Scikit-learn",
                    "Deployment": "Cloud, Edge, On-premise",
                    "Support": "6 months included"
                },
                "images": [
                    "https://example.com/service1.jpg"
                ],
                "portfolio_examples": [
                    "Medical Diagnosis AI",
                    "Financial Fraud Detection",
                    "Autonomous Vehicle Vision",
                    "Natural Language Processing"
                ],
                "related_courses": [1, 2, 3],  # AI courses
                "seller_info": {
                    "company": "AI Solutions Pro",
                    "rating": 4.9,
                    "years_active": 10,
                    "total_sales": 156,
                    "team_size": "25+ AI Engineers"
                },
                "consultation_required": True,
                "custom_quote": True
            }
        ]
    }
}

# Marketplace statistics
MARKETPLACE_STATS = {
    "total_products": 0,
    "total_sellers": 1250,
    "total_sales": 2456789,
    "average_rating": 4.7,
    "categories": len(PRODUCT_CATEGORIES),
    "daily_orders": random.randint(2000, 5000),
    "revenue_today": random.randint(50000, 150000)
}

# Calculate total products
for category in PRODUCT_CATEGORIES.values():
    MARKETPLACE_STATS["total_products"] += len(category["products"])

@products_bp.route('/overview', methods=['GET'])
def get_products_overview():
    return jsonify(MARKETPLACE_STATS)

@products_bp.route('/categories', methods=['GET'])
def get_product_categories():
    categories = []
    for name, data in PRODUCT_CATEGORIES.items():
        category_products = data["products"]
        categories.append({
            "name": name,
            "icon": data["icon"],
            "subcategories": data["subcategories"],
            "product_count": len(category_products),
            "avg_price": round(sum(p["price"] for p in category_products) / len(category_products), 2),
            "avg_rating": round(sum(p["rating"] for p in category_products) / len(category_products), 1),
            "total_reviews": sum(p["reviews"] for p in category_products)
        })
    return jsonify(categories)

@products_bp.route('/category/<category_name>', methods=['GET'])
def get_products_by_category(category_name):
    if category_name in PRODUCT_CATEGORIES:
        return jsonify(PRODUCT_CATEGORIES[category_name]["products"])
    return jsonify({"error": "Category not found"}), 404

@products_bp.route('/product/<int:product_id>', methods=['GET'])
def get_product_details(product_id):
    for category in PRODUCT_CATEGORIES.values():
        for product in category["products"]:
            if product["id"] == product_id:
                # Add additional details for individual product view
                product_details = product.copy()
                product_details.update({
                    "reviews_detailed": [
                        {
                            "user": "TechExpert2024",
                            "rating": 5,
                            "title": "Excellent quality and performance!",
                            "comment": "This product exceeded my expectations. The build quality is outstanding and it performs exactly as advertised.",
                            "date": "2024-01-20",
                            "verified_purchase": True,
                            "helpful_votes": 23
                        },
                        {
                            "user": "EngineerPro",
                            "rating": 4,
                            "title": "Good value for money",
                            "comment": "Solid product with good documentation. Shipping was fast and packaging was secure.",
                            "date": "2024-01-18",
                            "verified_purchase": True,
                            "helpful_votes": 15
                        },
                        {
                            "user": "StudentDev",
                            "rating": 5,
                            "title": "Perfect for learning!",
                            "comment": "Great for educational purposes. The related courses really help understand how to use it effectively.",
                            "date": "2024-01-15",
                            "verified_purchase": True,
                            "helpful_votes": 8
                        }
                    ],
                    "frequently_bought_together": [
                        {"id": 2, "name": "AI Neural Chip", "price": 2499.99},
                        {"id": 7, "name": "IoT Sensor Kit", "price": 299.99}
                    ],
                    "similar_products": [
                        {"id": 2, "name": "AI Neural Chip", "price": 2499.99, "rating": 4.7},
                        {"id": 7, "name": "IoT Sensor Kit", "price": 299.99, "rating": 4.8}
                    ],
                    "questions_answers": [
                        {
                            "question": "Is this compatible with existing systems?",
                            "answer": "Yes, it's designed to be compatible with most standard interfaces.",
                            "date": "2024-01-19"
                        },
                        {
                            "question": "What's included in the package?",
                            "answer": "The package includes the main unit, documentation, and all necessary cables.",
                            "date": "2024-01-17"
                        }
                    ],
                    "technical_support": {
                        "documentation": "Comprehensive user manual and API docs",
                        "community": "Active developer community forum",
                        "support_email": "support@seller.com",
                        "response_time": "< 24 hours"
                    }
                })
                return jsonify(product_details)
    return jsonify({"error": "Product not found"}), 404

@products_bp.route('/search', methods=['GET'])
def search_products():
    query = request.args.get('q', '').lower()
    category = request.args.get('category', '')
    min_price = float(request.args.get('min_price', 0))
    max_price = float(request.args.get('max_price', 999999))
    min_rating = float(request.args.get('min_rating', 0))
    sort_by = request.args.get('sort', 'relevance')  # relevance, price_low, price_high, rating, newest
    
    results = []
    for cat_name, cat_data in PRODUCT_CATEGORIES.items():
        if category and category != cat_name:
            continue
            
        for product in cat_data["products"]:
            # Filter by search criteria
            if (query in product["name"].lower() or 
                query in product["description"].lower() or
                any(query in feature.lower() for feature in product["features"])):
                
                if (min_price <= product["price"] <= max_price) and \
                   (product["rating"] >= min_rating):
                    
                    product_result = product.copy()
                    product_result["category"] = cat_name
                    results.append(product_result)
    
    # Sort results
    if sort_by == 'price_low':
        results.sort(key=lambda x: x["price"])
    elif sort_by == 'price_high':
        results.sort(key=lambda x: x["price"], reverse=True)
    elif sort_by == 'rating':
        results.sort(key=lambda x: x["rating"], reverse=True)
    elif sort_by == 'newest':
        results.sort(key=lambda x: x["id"], reverse=True)
    
    return jsonify({
        "results": results,
        "total": len(results),
        "query": query,
        "filters": {
            "category": category,
            "min_price": min_price,
            "max_price": max_price,
            "min_rating": min_rating,
            "sort_by": sort_by
        }
    })

@products_bp.route('/featured', methods=['GET'])
def get_featured_products():
    # Get top-rated products across all categories
    featured = []
    for cat_name, cat_data in PRODUCT_CATEGORIES.items():
        for product in cat_data["products"]:
            if product["rating"] >= 4.8:
                product_featured = product.copy()
                product_featured["category"] = cat_name
                featured.append(product_featured)
    
    # Sort by rating and reviews
    featured.sort(key=lambda x: (x["rating"], x["reviews"]), reverse=True)
    return jsonify(featured[:8])  # Return top 8 featured products

@products_bp.route('/deals', methods=['GET'])
def get_deals():
    # Products with significant discounts
    deals = []
    for cat_name, cat_data in PRODUCT_CATEGORIES.items():
        for product in cat_data["products"]:
            if "original_price" in product:
                discount = ((product["original_price"] - product["price"]) / product["original_price"]) * 100
                if discount >= 20:  # 20% or more discount
                    deal_product = product.copy()
                    deal_product["category"] = cat_name
                    deal_product["discount_percentage"] = round(discount, 1)
                    deal_product["savings"] = round(product["original_price"] - product["price"], 2)
                    deals.append(deal_product)
    
    # Sort by discount percentage
    deals.sort(key=lambda x: x["discount_percentage"], reverse=True)
    return jsonify(deals)

@products_bp.route('/seller/<seller_name>', methods=['GET'])
def get_seller_products(seller_name):
    seller_products = []
    seller_info = None
    
    for cat_name, cat_data in PRODUCT_CATEGORIES.items():
        for product in cat_data["products"]:
            if product["seller"].lower() == seller_name.lower():
                product_info = product.copy()
                product_info["category"] = cat_name
                seller_products.append(product_info)
                
                if not seller_info and "seller_info" in product:
                    seller_info = product["seller_info"].copy()
    
    if seller_products:
        if not seller_info:
            seller_info = {
                "company": seller_name,
                "rating": 4.5,
                "years_active": 5,
                "total_sales": 1000
            }
        
        seller_info["total_products"] = len(seller_products)
        seller_info["avg_product_rating"] = round(sum(p["rating"] for p in seller_products) / len(seller_products), 1)
        
        return jsonify({
            "seller": seller_info,
            "products": seller_products
        })
    
    return jsonify({"error": "Seller not found"}), 404

@products_bp.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    user_id = data.get('user_id')
    
    # Simulate adding to cart
    cart_item = {
        "cart_id": random.randint(10000, 99999),
        "product_id": product_id,
        "quantity": quantity,
        "user_id": user_id,
        "added_date": datetime.now().isoformat(),
        "status": "active"
    }
    
    return jsonify({
        "success": True,
        "cart_item": cart_item,
        "message": "Product added to cart successfully!"
    })

@products_bp.route('/wishlist', methods=['POST'])
def add_to_wishlist():
    data = request.get_json()
    product_id = data.get('product_id')
    user_id = data.get('user_id')
    
    # Simulate adding to wishlist
    wishlist_item = {
        "wishlist_id": random.randint(10000, 99999),
        "product_id": product_id,
        "user_id": user_id,
        "added_date": datetime.now().isoformat()
    }
    
    return jsonify({
        "success": True,
        "wishlist_item": wishlist_item,
        "message": "Product added to wishlist!"
    })

@products_bp.route('/recommendations/<int:user_id>', methods=['GET'])
def get_recommendations(user_id):
    # Simulate personalized recommendations
    recommendations = []
    all_products = []
    
    # Collect all products
    for cat_name, cat_data in PRODUCT_CATEGORIES.items():
        for product in cat_data["products"]:
            product_rec = product.copy()
            product_rec["category"] = cat_name
            all_products.append(product_rec)
    
    # Get random recommendations (in real app, this would be ML-based)
    recommendations = random.sample(all_products, min(6, len(all_products)))
    
    return jsonify({
        "user_id": user_id,
        "recommendations": recommendations,
        "reason": "Based on your browsing history and preferences"
    })


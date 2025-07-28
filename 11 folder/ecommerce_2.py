"""
E-Commerce Platform API - Amazon/eBay/Alibaba-like Marketplace
Complete marketplace with products, orders, payments, and seller management
"""

from flask import Blueprint, request, jsonify
import random
import time
from datetime import datetime, timedelta

ecommerce_bp = Blueprint('ecommerce', __name__)

# Mock data for demonstration
PRODUCTS_DATABASE = [
    {
        "product_id": "prod001",
        "title": "AI-Powered Smart Robot Assistant",
        "description": "Advanced robotics assistant with AI capabilities for home and office automation. Features voice control, object recognition, and task automation.",
        "category": "Electronics",
        "subcategory": "Robotics",
        "brand": "TechFlow Robotics",
        "seller_id": "seller001",
        "seller_name": "TechFlow Store",
        "seller_rating": 4.8,
        "price": 1299.99,
        "original_price": 1599.99,
        "discount_percentage": 18.75,
        "currency": "USD",
        "stock_quantity": 45,
        "images": [
            "/images/products/robot_assistant_1.jpg",
            "/images/products/robot_assistant_2.jpg",
            "/images/products/robot_assistant_3.jpg"
        ],
        "specifications": {
            "dimensions": "30cm x 25cm x 40cm",
            "weight": "3.5 kg",
            "battery_life": "8 hours",
            "connectivity": "Wi-Fi, Bluetooth 5.0",
            "ai_features": ["Voice Recognition", "Object Detection", "Natural Language Processing"]
        },
        "ratings": {
            "average": 4.6,
            "total_reviews": 234,
            "distribution": {"5": 145, "4": 67, "3": 15, "2": 5, "1": 2}
        },
        "shipping": {
            "free_shipping": True,
            "estimated_delivery": "2-3 business days",
            "shipping_from": "California, USA",
            "international_shipping": True
        },
        "tags": ["AI", "Robot", "Smart Home", "Automation", "Voice Control"],
        "created_at": "2024-01-15T10:00:00Z",
        "updated_at": "2024-01-27T08:30:00Z",
        "featured": True,
        "bestseller": True
    },
    {
        "product_id": "prod002",
        "title": "Professional Construction Toolkit",
        "description": "Complete construction toolkit with premium tools for professional builders and contractors. Includes power tools, hand tools, and safety equipment.",
        "category": "Tools & Hardware",
        "subcategory": "Construction Tools",
        "brand": "BuildMaster Pro",
        "seller_id": "seller002",
        "seller_name": "BuildMaster Supplies",
        "seller_rating": 4.9,
        "price": 899.99,
        "original_price": 1199.99,
        "discount_percentage": 25.0,
        "currency": "USD",
        "stock_quantity": 23,
        "images": [
            "/images/products/construction_toolkit_1.jpg",
            "/images/products/construction_toolkit_2.jpg"
        ],
        "specifications": {
            "items_included": "50+ tools",
            "case_material": "Heavy-duty aluminum",
            "warranty": "2 years",
            "weight": "15 kg",
            "certifications": ["OSHA Compliant", "ISO 9001"]
        },
        "ratings": {
            "average": 4.8,
            "total_reviews": 156,
            "distribution": {"5": 125, "4": 25, "3": 4, "2": 1, "1": 1}
        },
        "shipping": {
            "free_shipping": True,
            "estimated_delivery": "3-5 business days",
            "shipping_from": "Texas, USA",
            "international_shipping": True
        },
        "tags": ["Construction", "Tools", "Professional", "Hardware", "Building"],
        "created_at": "2024-01-10T14:20:00Z",
        "updated_at": "2024-01-26T16:45:00Z",
        "featured": False,
        "bestseller": True
    },
    {
        "product_id": "prod003",
        "title": "Underwater Exploration Drone",
        "description": "Advanced underwater drone for marine exploration, research, and inspection. Features 4K camera, sonar mapping, and remote control capabilities.",
        "category": "Electronics",
        "subcategory": "Drones",
        "brand": "AquaTech Systems",
        "seller_id": "seller003",
        "seller_name": "Marine Tech Solutions",
        "seller_rating": 4.7,
        "price": 2499.99,
        "original_price": 2999.99,
        "discount_percentage": 16.67,
        "currency": "USD",
        "stock_quantity": 12,
        "images": [
            "/images/products/underwater_drone_1.jpg",
            "/images/products/underwater_drone_2.jpg",
            "/images/products/underwater_drone_3.jpg",
            "/images/products/underwater_drone_4.jpg"
        ],
        "specifications": {
            "max_depth": "100 meters",
            "camera": "4K Ultra HD",
            "battery_life": "4 hours",
            "control_range": "500 meters",
            "features": ["Sonar Mapping", "GPS Navigation", "Live Streaming"]
        },
        "ratings": {
            "average": 4.5,
            "total_reviews": 89,
            "distribution": {"5": 56, "4": 25, "3": 6, "2": 1, "1": 1}
        },
        "shipping": {
            "free_shipping": True,
            "estimated_delivery": "5-7 business days",
            "shipping_from": "Florida, USA",
            "international_shipping": True
        },
        "tags": ["Underwater", "Drone", "Marine", "Exploration", "4K Camera"],
        "created_at": "2024-01-20T09:15:00Z",
        "updated_at": "2024-01-27T11:20:00Z",
        "featured": True,
        "bestseller": False
    }
]

SELLERS_DATABASE = {
    "seller001": {
        "seller_id": "seller001",
        "business_name": "TechFlow Store",
        "display_name": "TechFlow",
        "description": "Leading provider of AI and robotics solutions for consumers and businesses.",
        "logo": "/images/sellers/techflow_logo.jpg",
        "banner": "/images/sellers/techflow_banner.jpg",
        "rating": 4.8,
        "total_reviews": 1250,
        "products_count": 156,
        "years_selling": 5,
        "location": "California, USA",
        "verified": True,
        "badges": ["Top Seller", "Fast Shipping", "Excellent Service"],
        "policies": {
            "return_policy": "30-day returns",
            "shipping_policy": "Free shipping on orders over $100",
            "warranty": "1-year manufacturer warranty"
        },
        "contact": {
            "email": "support@techflow.com",
            "phone": "+1-555-0123",
            "website": "https://techflow.com"
        }
    },
    "seller002": {
        "seller_id": "seller002",
        "business_name": "BuildMaster Supplies",
        "display_name": "BuildMaster",
        "description": "Professional construction tools and supplies for contractors and DIY enthusiasts.",
        "logo": "/images/sellers/buildmaster_logo.jpg",
        "banner": "/images/sellers/buildmaster_banner.jpg",
        "rating": 4.9,
        "total_reviews": 890,
        "products_count": 234,
        "years_selling": 8,
        "location": "Texas, USA",
        "verified": True,
        "badges": ["Trusted Seller", "Industry Expert", "Fast Shipping"],
        "policies": {
            "return_policy": "60-day returns",
            "shipping_policy": "Free shipping on orders over $75",
            "warranty": "2-year warranty on power tools"
        },
        "contact": {
            "email": "orders@buildmaster.com",
            "phone": "+1-555-0456",
            "website": "https://buildmaster.com"
        }
    }
}

ORDERS_DATABASE = []
CART_DATABASE = {}

@ecommerce_bp.route('/api/ecommerce/products/search', methods=['GET'])
def search_products():
    """
    Advanced product search with AI-powered recommendations
    """
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    min_price = float(request.args.get('min_price', 0))
    max_price = float(request.args.get('max_price', 999999))
    sort_by = request.args.get('sort_by', 'relevance')  # relevance, price_low, price_high, rating, newest
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 20))
    
    # Filter products
    filtered_products = PRODUCTS_DATABASE.copy()
    
    # Text search
    if query:
        query_lower = query.lower()
        filtered_products = [
            p for p in filtered_products
            if query_lower in p['title'].lower() or 
               query_lower in p['description'].lower() or
               any(query_lower in tag.lower() for tag in p['tags'])
        ]
    
    # Category filter
    if category:
        filtered_products = [p for p in filtered_products if p['category'].lower() == category.lower()]
    
    # Price range filter
    filtered_products = [
        p for p in filtered_products 
        if min_price <= p['price'] <= max_price
    ]
    
    # Sort products
    if sort_by == 'price_low':
        filtered_products.sort(key=lambda x: x['price'])
    elif sort_by == 'price_high':
        filtered_products.sort(key=lambda x: x['price'], reverse=True)
    elif sort_by == 'rating':
        filtered_products.sort(key=lambda x: x['ratings']['average'], reverse=True)
    elif sort_by == 'newest':
        filtered_products.sort(key=lambda x: x['created_at'], reverse=True)
    else:  # relevance (AI-powered)
        # Add AI relevance score
        for product in filtered_products:
            relevance_score = random.uniform(0.7, 0.98)
            if query:
                # Boost score if query matches title or tags
                if query.lower() in product['title'].lower():
                    relevance_score += 0.1
                if any(query.lower() in tag.lower() for tag in product['tags']):
                    relevance_score += 0.05
            product['ai_relevance_score'] = min(1.0, relevance_score)
        
        filtered_products.sort(key=lambda x: x['ai_relevance_score'], reverse=True)
    
    # Pagination
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    paginated_products = filtered_products[start_idx:end_idx]
    
    # AI-powered recommendations
    recommendations = []
    if query:
        # Generate related product recommendations
        for product in PRODUCTS_DATABASE[:3]:
            if product not in paginated_products:
                recommendations.append({
                    "product_id": product['product_id'],
                    "title": product['title'],
                    "price": product['price'],
                    "image": product['images'][0],
                    "rating": product['ratings']['average'],
                    "reason": "Customers who searched for this also viewed"
                })
    
    return jsonify({
        "status": "success",
        "search_results": {
            "query": query,
            "total_results": len(filtered_products),
            "page": page,
            "per_page": limit,
            "total_pages": (len(filtered_products) + limit - 1) // limit,
            "products": paginated_products,
            "filters_applied": {
                "category": category,
                "price_range": [min_price, max_price],
                "sort_by": sort_by
            }
        },
        "recommendations": recommendations,
        "search_suggestions": ["AI robot", "construction tools", "underwater drone", "smart home"],
        "categories": ["Electronics", "Tools & Hardware", "Home & Garden", "Sports & Outdoors"]
    })

@ecommerce_bp.route('/api/ecommerce/products/<product_id>', methods=['GET'])
def get_product_details(product_id):
    """
    Get detailed product information
    """
    product = next((p for p in PRODUCTS_DATABASE if p['product_id'] == product_id), None)
    if not product:
        return jsonify({"status": "error", "message": "Product not found"}), 404
    
    # Get seller information
    seller = SELLERS_DATABASE.get(product['seller_id'], {})
    
    # Generate related products
    related_products = []
    for p in PRODUCTS_DATABASE:
        if p['product_id'] != product_id and p['category'] == product['category']:
            related_products.append({
                "product_id": p['product_id'],
                "title": p['title'],
                "price": p['price'],
                "image": p['images'][0],
                "rating": p['ratings']['average']
            })
    
    # AI-powered insights
    ai_insights = {
        "price_trend": random.choice(["stable", "decreasing", "increasing"]),
        "demand_level": random.choice(["high", "medium", "low"]),
        "best_time_to_buy": "Now" if random.random() > 0.5 else "Wait for sale",
        "similar_products_avg_price": round(sum(p['price'] for p in PRODUCTS_DATABASE if p['category'] == product['category']) / len([p for p in PRODUCTS_DATABASE if p['category'] == product['category']]), 2),
        "popularity_score": round(random.uniform(0.7, 0.95), 2)
    }
    
    product_details = product.copy()
    product_details.update({
        "seller_info": seller,
        "related_products": related_products[:6],
        "ai_insights": ai_insights,
        "availability_status": "in_stock" if product['stock_quantity'] > 0 else "out_of_stock",
        "estimated_delivery_date": (datetime.now() + timedelta(days=random.randint(2, 7))).strftime("%Y-%m-%d")
    })
    
    return jsonify({
        "status": "success",
        "product": product_details
    })

@ecommerce_bp.route('/api/ecommerce/cart/add', methods=['POST'])
def add_to_cart():
    """
    Add product to shopping cart
    """
    data = request.get_json()
    
    user_id = data.get('user_id')
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    # Find product
    product = next((p for p in PRODUCTS_DATABASE if p['product_id'] == product_id), None)
    if not product:
        return jsonify({"status": "error", "message": "Product not found"}), 404
    
    # Check stock
    if quantity > product['stock_quantity']:
        return jsonify({"status": "error", "message": "Insufficient stock"}), 400
    
    # Initialize cart for user if not exists
    if user_id not in CART_DATABASE:
        CART_DATABASE[user_id] = []
    
    # Check if product already in cart
    existing_item = next((item for item in CART_DATABASE[user_id] if item['product_id'] == product_id), None)
    
    if existing_item:
        existing_item['quantity'] += quantity
        existing_item['updated_at'] = datetime.now().isoformat()
    else:
        cart_item = {
            "cart_item_id": f"cart{int(time.time())}",
            "product_id": product_id,
            "product_title": product['title'],
            "product_image": product['images'][0],
            "price": product['price'],
            "quantity": quantity,
            "seller_id": product['seller_id'],
            "seller_name": product['seller_name'],
            "added_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        CART_DATABASE[user_id].append(cart_item)
    
    # Calculate cart totals
    cart_total = sum(item['price'] * item['quantity'] for item in CART_DATABASE[user_id])
    cart_count = sum(item['quantity'] for item in CART_DATABASE[user_id])
    
    return jsonify({
        "status": "success",
        "message": "Product added to cart",
        "cart_summary": {
            "total_items": cart_count,
            "total_amount": round(cart_total, 2),
            "currency": "USD"
        }
    })

@ecommerce_bp.route('/api/ecommerce/cart/<user_id>', methods=['GET'])
def get_cart(user_id):
    """
    Get user's shopping cart
    """
    cart_items = CART_DATABASE.get(user_id, [])
    
    # Calculate totals
    subtotal = sum(item['price'] * item['quantity'] for item in cart_items)
    shipping_cost = 0 if subtotal > 100 else 15.99  # Free shipping over $100
    tax = subtotal * 0.08  # 8% tax
    total = subtotal + shipping_cost + tax
    
    # Group items by seller for shipping optimization
    sellers = {}
    for item in cart_items:
        seller_id = item['seller_id']
        if seller_id not in sellers:
            sellers[seller_id] = {
                "seller_id": seller_id,
                "seller_name": item['seller_name'],
                "items": [],
                "subtotal": 0
            }
        sellers[seller_id]['items'].append(item)
        sellers[seller_id]['subtotal'] += item['price'] * item['quantity']
    
    return jsonify({
        "status": "success",
        "cart": {
            "items": cart_items,
            "grouped_by_seller": list(sellers.values()),
            "summary": {
                "item_count": len(cart_items),
                "total_quantity": sum(item['quantity'] for item in cart_items),
                "subtotal": round(subtotal, 2),
                "shipping_cost": round(shipping_cost, 2),
                "tax": round(tax, 2),
                "total": round(total, 2),
                "currency": "USD",
                "free_shipping_eligible": subtotal > 100
            },
            "recommendations": [
                {
                    "type": "frequently_bought_together",
                    "products": [
                        {"product_id": "prod004", "title": "Smart Home Hub", "price": 199.99}
                    ]
                }
            ]
        }
    })

@ecommerce_bp.route('/api/ecommerce/orders/create', methods=['POST'])
def create_order():
    """
    Create a new order from cart
    """
    data = request.get_json()
    
    user_id = data.get('user_id')
    shipping_address = data.get('shipping_address', {})
    payment_method = data.get('payment_method', {})
    
    cart_items = CART_DATABASE.get(user_id, [])
    if not cart_items:
        return jsonify({"status": "error", "message": "Cart is empty"}), 400
    
    # Calculate order totals
    subtotal = sum(item['price'] * item['quantity'] for item in cart_items)
    shipping_cost = 0 if subtotal > 100 else 15.99
    tax = subtotal * 0.08
    total = subtotal + shipping_cost + tax
    
    # Create order
    order_id = f"ORD{int(time.time())}"
    order = {
        "order_id": order_id,
        "user_id": user_id,
        "items": cart_items.copy(),
        "shipping_address": shipping_address,
        "payment_method": payment_method,
        "order_status": "confirmed",
        "payment_status": "paid",
        "tracking_number": f"TRK{random.randint(100000000, 999999999)}",
        "estimated_delivery": (datetime.now() + timedelta(days=random.randint(2, 7))).strftime("%Y-%m-%d"),
        "totals": {
            "subtotal": round(subtotal, 2),
            "shipping_cost": round(shipping_cost, 2),
            "tax": round(tax, 2),
            "total": round(total, 2),
            "currency": "USD"
        },
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    # Add to orders database
    ORDERS_DATABASE.append(order)
    
    # Clear cart
    CART_DATABASE[user_id] = []
    
    # Update product stock
    for item in cart_items:
        product = next((p for p in PRODUCTS_DATABASE if p['product_id'] == item['product_id']), None)
        if product:
            product['stock_quantity'] -= item['quantity']
    
    return jsonify({
        "status": "success",
        "message": "Order created successfully",
        "order": order,
        "next_steps": [
            "Order confirmation email sent",
            "Payment processed",
            "Preparing for shipment"
        ]
    })

@ecommerce_bp.route('/api/ecommerce/orders/<user_id>', methods=['GET'])
def get_user_orders(user_id):
    """
    Get user's order history
    """
    user_orders = [order for order in ORDERS_DATABASE if order['user_id'] == user_id]
    user_orders.sort(key=lambda x: x['created_at'], reverse=True)
    
    # Add order status details
    for order in user_orders:
        order['status_details'] = {
            "current_status": order['order_status'],
            "status_history": [
                {"status": "confirmed", "timestamp": order['created_at'], "description": "Order confirmed"},
                {"status": "processing", "timestamp": order['created_at'], "description": "Preparing for shipment"},
            ],
            "can_cancel": order['order_status'] in ['confirmed', 'processing'],
            "can_return": order['order_status'] == 'delivered'
        }
    
    return jsonify({
        "status": "success",
        "orders": user_orders,
        "summary": {
            "total_orders": len(user_orders),
            "total_spent": sum(order['totals']['total'] for order in user_orders),
            "pending_orders": len([o for o in user_orders if o['order_status'] in ['confirmed', 'processing', 'shipped']]),
            "completed_orders": len([o for o in user_orders if o['order_status'] == 'delivered'])
        }
    })

@ecommerce_bp.route('/api/ecommerce/sellers/<seller_id>', methods=['GET'])
def get_seller_profile(seller_id):
    """
    Get seller profile and products
    """
    seller = SELLERS_DATABASE.get(seller_id)
    if not seller:
        return jsonify({"status": "error", "message": "Seller not found"}), 404
    
    # Get seller's products
    seller_products = [p for p in PRODUCTS_DATABASE if p['seller_id'] == seller_id]
    
    # Calculate seller stats
    total_reviews = sum(p['ratings']['total_reviews'] for p in seller_products)
    avg_rating = sum(p['ratings']['average'] * p['ratings']['total_reviews'] for p in seller_products) / max(total_reviews, 1)
    
    seller_profile = seller.copy()
    seller_profile.update({
        "products": seller_products,
        "stats": {
            "total_products": len(seller_products),
            "total_reviews": total_reviews,
            "average_rating": round(avg_rating, 2),
            "response_rate": "98%",
            "response_time": "< 2 hours",
            "shipping_speed": "Fast"
        },
        "recent_reviews": [
            {
                "review_id": "rev001",
                "product_title": "AI-Powered Smart Robot Assistant",
                "rating": 5,
                "comment": "Excellent product and fast shipping!",
                "reviewer": "John D.",
                "date": "2024-01-25"
            }
        ]
    })
    
    return jsonify({
        "status": "success",
        "seller": seller_profile
    })

@ecommerce_bp.route('/api/ecommerce/analytics/marketplace', methods=['GET'])
def get_marketplace_analytics():
    """
    Get marketplace analytics and insights
    """
    analytics = {
        "overview": {
            "total_products": len(PRODUCTS_DATABASE),
            "total_sellers": len(SELLERS_DATABASE),
            "total_orders": len(ORDERS_DATABASE),
            "total_revenue": sum(order['totals']['total'] for order in ORDERS_DATABASE),
            "active_users": 15420,
            "conversion_rate": 3.2
        },
        "top_categories": [
            {"category": "Electronics", "products": 156, "revenue": 245000},
            {"category": "Tools & Hardware", "products": 89, "revenue": 125000},
            {"category": "Home & Garden", "products": 67, "revenue": 89000}
        ],
        "trending_products": [
            {
                "product_id": "prod001",
                "title": "AI-Powered Smart Robot Assistant",
                "trend_score": 94.5,
                "sales_growth": "+45%"
            }
        ],
        "seller_performance": {
            "top_sellers": [
                {"seller_id": "seller001", "name": "TechFlow Store", "revenue": 125000, "rating": 4.8},
                {"seller_id": "seller002", "name": "BuildMaster Supplies", "revenue": 98000, "rating": 4.9}
            ],
            "average_seller_rating": 4.7,
            "seller_satisfaction": 92.3
        },
        "market_insights": {
            "fastest_growing_category": "Electronics",
            "seasonal_trends": ["AI products trending up", "Construction tools stable"],
            "price_trends": "Competitive pricing driving sales",
            "customer_satisfaction": 4.6
        }
    }
    
    return jsonify({
        "status": "success",
        "analytics": analytics,
        "generated_at": datetime.now().isoformat()
    })


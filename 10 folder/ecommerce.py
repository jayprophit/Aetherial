"""
E-commerce routes for Unified Platform
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, jwt_required
import uuid
import random
from datetime import datetime, timedelta

ecommerce_bp = Blueprint('ecommerce', __name__)

# In-memory storage for demo
products = {}
categories = {}
shopping_carts = {}
orders = {}
reviews = {}

# Initialize sample categories
sample_categories = {
    'electronics': {'name': 'Electronics', 'description': 'Electronic devices and gadgets'},
    'clothing': {'name': 'Clothing', 'description': 'Fashion and apparel'},
    'books': {'name': 'Books', 'description': 'Books and literature'},
    'home': {'name': 'Home & Garden', 'description': 'Home improvement and garden supplies'},
    'sports': {'name': 'Sports & Outdoors', 'description': 'Sports equipment and outdoor gear'},
    'health': {'name': 'Health & Beauty', 'description': 'Health and beauty products'}
}

for cat_id, cat_data in sample_categories.items():
    categories[cat_id] = {
        'id': cat_id,
        'name': cat_data['name'],
        'description': cat_data['description'],
        'created_at': datetime.utcnow().isoformat(),
        'product_count': 0
    }

# Initialize sample products
sample_products = [
    {
        'name': 'Smartphone Pro Max',
        'description': 'Latest flagship smartphone with advanced features',
        'price': 999.99,
        'category': 'electronics',
        'stock': 50,
        'images': ['smartphone1.jpg', 'smartphone2.jpg']
    },
    {
        'name': 'Wireless Headphones',
        'description': 'Premium noise-canceling wireless headphones',
        'price': 299.99,
        'category': 'electronics',
        'stock': 100,
        'images': ['headphones1.jpg']
    },
    {
        'name': 'Designer T-Shirt',
        'description': 'Premium cotton designer t-shirt',
        'price': 49.99,
        'category': 'clothing',
        'stock': 200,
        'images': ['tshirt1.jpg']
    }
]

for product_data in sample_products:
    product_id = str(uuid.uuid4())
    products[product_id] = {
        'id': product_id,
        'name': product_data['name'],
        'description': product_data['description'],
        'price': product_data['price'],
        'category_id': product_data['category'],
        'stock_quantity': product_data['stock'],
        'images': product_data['images'],
        'rating': round(random.uniform(3.5, 5.0), 1),
        'review_count': random.randint(10, 500),
        'created_at': datetime.utcnow().isoformat(),
        'updated_at': datetime.utcnow().isoformat(),
        'is_active': True,
        'sku': f"SKU{random.randint(100000, 999999)}",
        'weight': round(random.uniform(0.1, 5.0), 2),
        'dimensions': f"{random.randint(5, 30)}x{random.randint(5, 30)}x{random.randint(1, 10)} cm",
        'tags': ['featured', 'bestseller'] if random.choice([True, False]) else []
    }
    categories[product_data['category']]['product_count'] += 1

@ecommerce_bp.route('/products', methods=['GET'])
def get_products():
    """Get products with filtering and pagination"""
    try:
        # Get query parameters
        category = request.args.get('category')
        search = request.args.get('search', '').lower()
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        sort_by = request.args.get('sort_by', 'created_at')
        sort_order = request.args.get('sort_order', 'desc')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Filter products
        filtered_products = []
        for product in products.values():
            if not product['is_active']:
                continue
            
            # Category filter
            if category and product['category_id'] != category:
                continue
            
            # Search filter
            if search and search not in product['name'].lower() and search not in product['description'].lower():
                continue
            
            # Price filters
            if min_price is not None and product['price'] < min_price:
                continue
            if max_price is not None and product['price'] > max_price:
                continue
            
            filtered_products.append(product)
        
        # Sort products
        reverse = sort_order == 'desc'
        if sort_by == 'price':
            filtered_products.sort(key=lambda x: x['price'], reverse=reverse)
        elif sort_by == 'rating':
            filtered_products.sort(key=lambda x: x['rating'], reverse=reverse)
        elif sort_by == 'name':
            filtered_products.sort(key=lambda x: x['name'], reverse=reverse)
        else:  # created_at
            filtered_products.sort(key=lambda x: x['created_at'], reverse=reverse)
        
        # Pagination
        total_products = len(filtered_products)
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_products = filtered_products[start_idx:end_idx]
        
        return jsonify({
            'success': True,
            'products': paginated_products,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total_products,
                'pages': (total_products + per_page - 1) // per_page
            },
            'filters': {
                'category': category,
                'search': search,
                'min_price': min_price,
                'max_price': max_price,
                'sort_by': sort_by,
                'sort_order': sort_order
            }
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@ecommerce_bp.route('/products/<product_id>', methods=['GET'])
def get_product(product_id):
    """Get product details"""
    try:
        if product_id not in products:
            return jsonify({'success': False, 'error': 'Product not found'}), 404
        
        product = products[product_id]
        
        if not product['is_active']:
            return jsonify({'success': False, 'error': 'Product not available'}), 404
        
        # Get category info
        category_info = categories.get(product['category_id'], {})
        
        # Get recent reviews
        product_reviews = [
            review for review in reviews.values()
            if review['product_id'] == product_id
        ]
        product_reviews.sort(key=lambda x: x['created_at'], reverse=True)
        recent_reviews = product_reviews[:5]
        
        product_details = {
            **product,
            'category': category_info,
            'recent_reviews': recent_reviews,
            'in_stock': product['stock_quantity'] > 0,
            'shipping_info': {
                'free_shipping': product['price'] > 50,
                'estimated_delivery': '2-5 business days',
                'shipping_cost': 0 if product['price'] > 50 else 9.99
            }
        }
        
        return jsonify({
            'success': True,
            'product': product_details
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@ecommerce_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get product categories"""
    try:
        return jsonify({
            'success': True,
            'categories': list(categories.values())
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@ecommerce_bp.route('/cart/add', methods=['POST'])
@jwt_required()
def add_to_cart():
    """Add item to shopping cart"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        required_fields = ['product_id', 'quantity']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400
        
        product_id = data['product_id']
        quantity = int(data['quantity'])
        
        # Validate product
        if product_id not in products:
            return jsonify({'success': False, 'error': 'Product not found'}), 404
        
        product = products[product_id]
        
        if not product['is_active']:
            return jsonify({'success': False, 'error': 'Product not available'}), 404
        
        if quantity <= 0:
            return jsonify({'success': False, 'error': 'Quantity must be positive'}), 400
        
        if quantity > product['stock_quantity']:
            return jsonify({'success': False, 'error': 'Insufficient stock'}), 400
        
        # Get or create cart
        if user_id not in shopping_carts:
            shopping_carts[user_id] = {
                'user_id': user_id,
                'items': {},
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            }
        
        cart = shopping_carts[user_id]
        
        # Add or update item in cart
        if product_id in cart['items']:
            cart['items'][product_id]['quantity'] += quantity
        else:
            cart['items'][product_id] = {
                'product_id': product_id,
                'quantity': quantity,
                'added_at': datetime.utcnow().isoformat()
            }
        
        # Check total quantity doesn't exceed stock
        total_quantity = cart['items'][product_id]['quantity']
        if total_quantity > product['stock_quantity']:
            return jsonify({'success': False, 'error': 'Total quantity exceeds available stock'}), 400
        
        cart['updated_at'] = datetime.utcnow().isoformat()
        
        return jsonify({
            'success': True,
            'message': 'Item added to cart',
            'cart_item_count': len(cart['items'])
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@ecommerce_bp.route('/cart', methods=['GET'])
@jwt_required()
def get_cart():
    """Get shopping cart"""
    try:
        user_id = get_jwt_identity()
        
        if user_id not in shopping_carts:
            return jsonify({
                'success': True,
                'cart': {
                    'items': [],
                    'total_items': 0,
                    'subtotal': 0,
                    'shipping': 0,
                    'tax': 0,
                    'total': 0
                }
            }), 200
        
        cart = shopping_carts[user_id]
        cart_items = []
        subtotal = 0
        
        for item in cart['items'].values():
            product = products.get(item['product_id'])
            if product and product['is_active']:
                item_total = product['price'] * item['quantity']
                cart_items.append({
                    'product_id': item['product_id'],
                    'product_name': product['name'],
                    'product_price': product['price'],
                    'product_image': product['images'][0] if product['images'] else None,
                    'quantity': item['quantity'],
                    'item_total': round(item_total, 2),
                    'in_stock': product['stock_quantity'] >= item['quantity']
                })
                subtotal += item_total
        
        # Calculate shipping and tax
        shipping = 0 if subtotal > 50 else 9.99
        tax = round(subtotal * 0.08, 2)  # 8% tax
        total = round(subtotal + shipping + tax, 2)
        
        cart_summary = {
            'items': cart_items,
            'total_items': len(cart_items),
            'subtotal': round(subtotal, 2),
            'shipping': shipping,
            'tax': tax,
            'total': total,
            'updated_at': cart['updated_at']
        }
        
        return jsonify({
            'success': True,
            'cart': cart_summary
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@ecommerce_bp.route('/cart/update', methods=['PUT'])
@jwt_required()
def update_cart_item():
    """Update cart item quantity"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        required_fields = ['product_id', 'quantity']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400
        
        product_id = data['product_id']
        quantity = int(data['quantity'])
        
        if user_id not in shopping_carts:
            return jsonify({'success': False, 'error': 'Cart not found'}), 404
        
        cart = shopping_carts[user_id]
        
        if product_id not in cart['items']:
            return jsonify({'success': False, 'error': 'Item not in cart'}), 404
        
        if quantity <= 0:
            # Remove item from cart
            del cart['items'][product_id]
        else:
            # Validate stock
            product = products.get(product_id)
            if not product or quantity > product['stock_quantity']:
                return jsonify({'success': False, 'error': 'Insufficient stock'}), 400
            
            cart['items'][product_id]['quantity'] = quantity
        
        cart['updated_at'] = datetime.utcnow().isoformat()
        
        return jsonify({
            'success': True,
            'message': 'Cart updated successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@ecommerce_bp.route('/orders/create', methods=['POST'])
@jwt_required()
def create_order():
    """Create order from cart"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        required_fields = ['shipping_address', 'payment_method']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400
        
        if user_id not in shopping_carts or not shopping_carts[user_id]['items']:
            return jsonify({'success': False, 'error': 'Cart is empty'}), 400
        
        cart = shopping_carts[user_id]
        order_id = str(uuid.uuid4())
        order_number = f"ORD{random.randint(100000, 999999)}"
        
        # Calculate order totals
        order_items = []
        subtotal = 0
        
        for item in cart['items'].values():
            product = products.get(item['product_id'])
            if product and product['is_active']:
                if product['stock_quantity'] < item['quantity']:
                    return jsonify({
                        'success': False, 
                        'error': f'Insufficient stock for {product["name"]}'
                    }), 400
                
                item_total = product['price'] * item['quantity']
                order_items.append({
                    'product_id': item['product_id'],
                    'product_name': product['name'],
                    'product_price': product['price'],
                    'quantity': item['quantity'],
                    'item_total': round(item_total, 2)
                })
                subtotal += item_total
                
                # Update stock
                product['stock_quantity'] -= item['quantity']
        
        shipping = 0 if subtotal > 50 else 9.99
        tax = round(subtotal * 0.08, 2)
        total = round(subtotal + shipping + tax, 2)
        
        # Create order
        order = {
            'id': order_id,
            'order_number': order_number,
            'user_id': user_id,
            'items': order_items,
            'subtotal': round(subtotal, 2),
            'shipping': shipping,
            'tax': tax,
            'total': total,
            'status': 'confirmed',
            'payment_status': 'paid',
            'shipping_address': data['shipping_address'],
            'payment_method': data['payment_method'],
            'created_at': datetime.utcnow().isoformat(),
            'estimated_delivery': (datetime.utcnow() + timedelta(days=5)).isoformat(),
            'tracking_number': f"TRK{random.randint(1000000000, 9999999999)}"
        }
        
        orders[order_id] = order
        
        # Clear cart
        shopping_carts[user_id]['items'] = {}
        
        return jsonify({
            'success': True,
            'order': order
        }), 201
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@ecommerce_bp.route('/orders', methods=['GET'])
@jwt_required()
def get_orders():
    """Get user's orders"""
    try:
        user_id = get_jwt_identity()
        
        user_orders = []
        for order in orders.values():
            if order['user_id'] == user_id:
                user_orders.append(order)
        
        # Sort by creation date (newest first)
        user_orders.sort(key=lambda x: x['created_at'], reverse=True)
        
        return jsonify({
            'success': True,
            'orders': user_orders,
            'total_count': len(user_orders),
            'total_spent': sum(order['total'] for order in user_orders)
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@ecommerce_bp.route('/orders/<order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    """Get order details"""
    try:
        user_id = get_jwt_identity()
        
        if order_id not in orders:
            return jsonify({'success': False, 'error': 'Order not found'}), 404
        
        order = orders[order_id]
        
        if order['user_id'] != user_id:
            return jsonify({'success': False, 'error': 'Unauthorized access'}), 403
        
        return jsonify({
            'success': True,
            'order': order
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@ecommerce_bp.route('/search', methods=['GET'])
def search_products():
    """Search products"""
    try:
        query = request.args.get('q', '').lower()
        category = request.args.get('category')
        
        if not query:
            return jsonify({'success': False, 'error': 'Search query is required'}), 400
        
        search_results = []
        for product in products.values():
            if not product['is_active']:
                continue
            
            # Search in name and description
            if (query in product['name'].lower() or 
                query in product['description'].lower() or
                query in product.get('sku', '').lower()):
                
                # Category filter
                if category and product['category_id'] != category:
                    continue
                
                search_results.append(product)
        
        # Sort by relevance (simplified)
        search_results.sort(key=lambda x: x['rating'], reverse=True)
        
        return jsonify({
            'success': True,
            'query': query,
            'results': search_results,
            'total_results': len(search_results)
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


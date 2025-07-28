from flask import Blueprint, request, jsonify
import json
import uuid
from datetime import datetime

store_builder_bp = Blueprint('store_builder', __name__)

# Mock database for stores and pages
stores_db = {}
pages_db = {}
templates_db = {}

# Initialize with some default templates
default_templates = {
    'modern_minimal': {
        'id': 'modern_minimal',
        'name': 'Modern Minimal',
        'description': 'Clean and minimal design perfect for modern brands',
        'category': 'business',
        'preview_image': '/templates/modern_minimal.jpg',
        'structure': {
            'header': {
                'type': 'header',
                'components': ['logo', 'navigation', 'cart_icon']
            },
            'hero': {
                'type': 'hero',
                'components': ['hero_image', 'hero_text', 'cta_button']
            },
            'featured_products': {
                'type': 'product_grid',
                'components': ['product_cards']
            },
            'footer': {
                'type': 'footer',
                'components': ['footer_links', 'social_icons', 'copyright']
            }
        }
    },
    'fashion_boutique': {
        'id': 'fashion_boutique',
        'name': 'Fashion Boutique',
        'description': 'Elegant design for fashion and lifestyle brands',
        'category': 'fashion',
        'preview_image': '/templates/fashion_boutique.jpg',
        'structure': {
            'header': {
                'type': 'header',
                'components': ['logo', 'navigation', 'search', 'cart_icon']
            },
            'hero': {
                'type': 'hero_slider',
                'components': ['image_slider', 'overlay_text']
            },
            'categories': {
                'type': 'category_grid',
                'components': ['category_cards']
            },
            'featured_products': {
                'type': 'product_carousel',
                'components': ['product_cards']
            },
            'newsletter': {
                'type': 'newsletter',
                'components': ['email_signup']
            },
            'footer': {
                'type': 'footer',
                'components': ['footer_links', 'social_icons', 'copyright']
            }
        }
    },
    'tech_store': {
        'id': 'tech_store',
        'name': 'Tech Store',
        'description': 'Modern design for electronics and tech products',
        'category': 'technology',
        'preview_image': '/templates/tech_store.jpg',
        'structure': {
            'header': {
                'type': 'header',
                'components': ['logo', 'mega_menu', 'search', 'user_account', 'cart_icon']
            },
            'hero': {
                'type': 'hero_video',
                'components': ['background_video', 'hero_text', 'cta_buttons']
            },
            'features': {
                'type': 'feature_grid',
                'components': ['feature_cards']
            },
            'products': {
                'type': 'product_grid',
                'components': ['product_cards', 'filters', 'sorting']
            },
            'testimonials': {
                'type': 'testimonials',
                'components': ['testimonial_cards']
            },
            'footer': {
                'type': 'footer',
                'components': ['footer_links', 'social_icons', 'copyright']
            }
        }
    }
}

templates_db.update(default_templates)

@store_builder_bp.route('/templates', methods=['GET'])
def get_templates():
    """Get all available store templates"""
    category = request.args.get('category')
    templates = list(templates_db.values())
    
    if category:
        templates = [t for t in templates if t.get('category') == category]
    
    return jsonify({
        'success': True,
        'templates': templates
    })

@store_builder_bp.route('/stores', methods=['POST'])
def create_store():
    """Create a new store"""
    data = request.get_json()
    
    store_id = str(uuid.uuid4())
    store = {
        'id': store_id,
        'name': data.get('name'),
        'subdomain': data.get('subdomain'),
        'template_id': data.get('template_id'),
        'owner_id': data.get('owner_id'),
        'settings': {
            'currency': data.get('currency', 'USD'),
            'language': data.get('language', 'en'),
            'timezone': data.get('timezone', 'UTC'),
            'theme_colors': {
                'primary': '#3B82F6',
                'secondary': '#10B981',
                'accent': '#F59E0B'
            }
        },
        'pages': [],
        'products': [],
        'created_at': datetime.utcnow().isoformat(),
        'updated_at': datetime.utcnow().isoformat(),
        'status': 'active'
    }
    
    stores_db[store_id] = store
    
    # Create default pages based on template
    if data.get('template_id') and data.get('template_id') in templates_db:
        template = templates_db[data.get('template_id')]
        create_default_pages(store_id, template)
    
    return jsonify({
        'success': True,
        'store': store
    })

@store_builder_bp.route('/stores/<store_id>', methods=['GET'])
def get_store(store_id):
    """Get store details"""
    if store_id not in stores_db:
        return jsonify({'success': False, 'error': 'Store not found'}), 404
    
    return jsonify({
        'success': True,
        'store': stores_db[store_id]
    })

@store_builder_bp.route('/stores/<store_id>', methods=['PUT'])
def update_store(store_id):
    """Update store settings"""
    if store_id not in stores_db:
        return jsonify({'success': False, 'error': 'Store not found'}), 404
    
    data = request.get_json()
    store = stores_db[store_id]
    
    # Update allowed fields
    if 'name' in data:
        store['name'] = data['name']
    if 'settings' in data:
        store['settings'].update(data['settings'])
    
    store['updated_at'] = datetime.utcnow().isoformat()
    
    return jsonify({
        'success': True,
        'store': store
    })

@store_builder_bp.route('/stores/<store_id>/pages', methods=['GET'])
def get_store_pages(store_id):
    """Get all pages for a store"""
    if store_id not in stores_db:
        return jsonify({'success': False, 'error': 'Store not found'}), 404
    
    store_pages = [page for page in pages_db.values() if page['store_id'] == store_id]
    
    return jsonify({
        'success': True,
        'pages': store_pages
    })

@store_builder_bp.route('/stores/<store_id>/pages', methods=['POST'])
def create_page(store_id):
    """Create a new page for a store"""
    if store_id not in stores_db:
        return jsonify({'success': False, 'error': 'Store not found'}), 404
    
    data = request.get_json()
    
    page_id = str(uuid.uuid4())
    page = {
        'id': page_id,
        'store_id': store_id,
        'name': data.get('name'),
        'slug': data.get('slug'),
        'type': data.get('type', 'custom'),  # home, product, collection, custom
        'title': data.get('title'),
        'meta_description': data.get('meta_description'),
        'content': data.get('content', []),  # Array of page elements
        'settings': {
            'seo_enabled': True,
            'comments_enabled': False,
            'published': True
        },
        'created_at': datetime.utcnow().isoformat(),
        'updated_at': datetime.utcnow().isoformat()
    }
    
    pages_db[page_id] = page
    stores_db[store_id]['pages'].append(page_id)
    
    return jsonify({
        'success': True,
        'page': page
    })

@store_builder_bp.route('/pages/<page_id>', methods=['GET'])
def get_page(page_id):
    """Get page details"""
    if page_id not in pages_db:
        return jsonify({'success': False, 'error': 'Page not found'}), 404
    
    return jsonify({
        'success': True,
        'page': pages_db[page_id]
    })

@store_builder_bp.route('/pages/<page_id>', methods=['PUT'])
def update_page(page_id):
    """Update page content and settings"""
    if page_id not in pages_db:
        return jsonify({'success': False, 'error': 'Page not found'}), 404
    
    data = request.get_json()
    page = pages_db[page_id]
    
    # Update allowed fields
    if 'name' in data:
        page['name'] = data['name']
    if 'title' in data:
        page['title'] = data['title']
    if 'meta_description' in data:
        page['meta_description'] = data['meta_description']
    if 'content' in data:
        page['content'] = data['content']
    if 'settings' in data:
        page['settings'].update(data['settings'])
    
    page['updated_at'] = datetime.utcnow().isoformat()
    
    return jsonify({
        'success': True,
        'page': page
    })

@store_builder_bp.route('/pages/<page_id>', methods=['DELETE'])
def delete_page(page_id):
    """Delete a page"""
    if page_id not in pages_db:
        return jsonify({'success': False, 'error': 'Page not found'}), 404
    
    page = pages_db[page_id]
    store_id = page['store_id']
    
    # Remove from store's pages list
    if store_id in stores_db:
        stores_db[store_id]['pages'] = [p for p in stores_db[store_id]['pages'] if p != page_id]
    
    # Delete the page
    del pages_db[page_id]
    
    return jsonify({
        'success': True,
        'message': 'Page deleted successfully'
    })

@store_builder_bp.route('/elements', methods=['GET'])
def get_available_elements():
    """Get all available page elements for the page builder"""
    elements = {
        'layout': [
            {
                'type': 'container',
                'name': 'Container',
                'description': 'Responsive container for content',
                'icon': 'layout',
                'settings': ['width', 'padding', 'margin', 'background']
            },
            {
                'type': 'row',
                'name': 'Row',
                'description': 'Horizontal row with columns',
                'icon': 'columns',
                'settings': ['columns', 'gap', 'alignment']
            },
            {
                'type': 'column',
                'name': 'Column',
                'description': 'Vertical column for content',
                'icon': 'column',
                'settings': ['width', 'padding', 'alignment']
            }
        ],
        'content': [
            {
                'type': 'heading',
                'name': 'Heading',
                'description': 'Text heading (H1-H6)',
                'icon': 'heading',
                'settings': ['text', 'level', 'alignment', 'color', 'font']
            },
            {
                'type': 'paragraph',
                'name': 'Paragraph',
                'description': 'Text paragraph',
                'icon': 'text',
                'settings': ['text', 'alignment', 'color', 'font']
            },
            {
                'type': 'image',
                'name': 'Image',
                'description': 'Image with optional caption',
                'icon': 'image',
                'settings': ['src', 'alt', 'caption', 'alignment', 'size']
            },
            {
                'type': 'video',
                'name': 'Video',
                'description': 'Video player',
                'icon': 'video',
                'settings': ['src', 'poster', 'controls', 'autoplay']
            },
            {
                'type': 'button',
                'name': 'Button',
                'description': 'Call-to-action button',
                'icon': 'button',
                'settings': ['text', 'link', 'style', 'size', 'color']
            }
        ],
        'ecommerce': [
            {
                'type': 'product_grid',
                'name': 'Product Grid',
                'description': 'Grid of products',
                'icon': 'grid',
                'settings': ['columns', 'products', 'show_price', 'show_rating']
            },
            {
                'type': 'product_carousel',
                'name': 'Product Carousel',
                'description': 'Sliding product carousel',
                'icon': 'carousel',
                'settings': ['products', 'autoplay', 'navigation']
            },
            {
                'type': 'add_to_cart',
                'name': 'Add to Cart',
                'description': 'Add to cart button',
                'icon': 'cart',
                'settings': ['product_id', 'style', 'text']
            },
            {
                'type': 'price_display',
                'name': 'Price Display',
                'description': 'Product price with currency',
                'icon': 'dollar-sign',
                'settings': ['product_id', 'show_currency', 'format']
            }
        ],
        'forms': [
            {
                'type': 'contact_form',
                'name': 'Contact Form',
                'description': 'Contact form with fields',
                'icon': 'mail',
                'settings': ['fields', 'submit_text', 'email_to']
            },
            {
                'type': 'newsletter_signup',
                'name': 'Newsletter Signup',
                'description': 'Email newsletter subscription',
                'icon': 'mail-plus',
                'settings': ['placeholder', 'button_text', 'list_id']
            },
            {
                'type': 'search_bar',
                'name': 'Search Bar',
                'description': 'Product search functionality',
                'icon': 'search',
                'settings': ['placeholder', 'categories', 'filters']
            }
        ],
        'navigation': [
            {
                'type': 'menu',
                'name': 'Navigation Menu',
                'description': 'Site navigation menu',
                'icon': 'menu',
                'settings': ['items', 'style', 'mobile_behavior']
            },
            {
                'type': 'breadcrumb',
                'name': 'Breadcrumb',
                'description': 'Navigation breadcrumb trail',
                'icon': 'chevron-right',
                'settings': ['separator', 'show_home', 'style']
            }
        ],
        'social': [
            {
                'type': 'social_icons',
                'name': 'Social Icons',
                'description': 'Social media links',
                'icon': 'share',
                'settings': ['platforms', 'style', 'size']
            },
            {
                'type': 'social_feed',
                'name': 'Social Feed',
                'description': 'Social media feed widget',
                'icon': 'rss',
                'settings': ['platform', 'count', 'layout']
            }
        ]
    }
    
    return jsonify({
        'success': True,
        'elements': elements
    })

@store_builder_bp.route('/stores/<store_id>/products', methods=['GET'])
def get_store_products(store_id):
    """Get all products for a store"""
    if store_id not in stores_db:
        return jsonify({'success': False, 'error': 'Store not found'}), 404
    
    # Mock products data
    products = [
        {
            'id': '1',
            'name': 'Premium Wireless Headphones',
            'description': 'High-quality wireless headphones with noise cancellation',
            'price': 299.99,
            'currency': 'USD',
            'images': ['/products/headphones-1.jpg', '/products/headphones-2.jpg'],
            'category': 'Electronics',
            'stock': 50,
            'sku': 'WH-001',
            'status': 'active'
        },
        {
            'id': '2',
            'name': 'Smart Fitness Watch',
            'description': 'Advanced fitness tracking with heart rate monitor',
            'price': 199.99,
            'currency': 'USD',
            'images': ['/products/watch-1.jpg', '/products/watch-2.jpg'],
            'category': 'Wearables',
            'stock': 25,
            'sku': 'SW-002',
      
(Content truncated due to size limit. Use line ranges to read in chunks)
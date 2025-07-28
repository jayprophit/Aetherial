from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import json
import os
from datetime import datetime
import re

social_links_bp = Blueprint('social_links', __name__)

# Supported social networks with validation patterns
SUPPORTED_NETWORKS = {
    'linkedin': {
        'name': 'LinkedIn',
        'url_pattern': 'https://linkedin.com/in/{username}',
        'validation_regex': r'^[a-zA-Z0-9\-]+$',
        'api_endpoint': 'https://api.linkedin.com/v2/people/(id:{username})',
        'sync_enabled': True
    },
    'github': {
        'name': 'GitHub',
        'url_pattern': 'https://github.com/{username}',
        'validation_regex': r'^[a-zA-Z0-9\-]+$',
        'api_endpoint': 'https://api.github.com/users/{username}',
        'sync_enabled': True
    },
    'twitter': {
        'name': 'Twitter/X',
        'url_pattern': 'https://twitter.com/{username}',
        'validation_regex': r'^[a-zA-Z0-9_]+$',
        'api_endpoint': 'https://api.twitter.com/2/users/by/username/{username}',
        'sync_enabled': True
    },
    'instagram': {
        'name': 'Instagram',
        'url_pattern': 'https://instagram.com/{username}',
        'validation_regex': r'^[a-zA-Z0-9_.]+$',
        'api_endpoint': None,  # Instagram API requires special permissions
        'sync_enabled': False
    },
    'youtube': {
        'name': 'YouTube',
        'url_pattern': 'https://youtube.com/@{username}',
        'validation_regex': r'^[a-zA-Z0-9_\-]+$',
        'api_endpoint': 'https://www.googleapis.com/youtube/v3/channels?forUsername={username}',
        'sync_enabled': True
    },
    'stackoverflow': {
        'name': 'Stack Overflow',
        'url_pattern': 'https://stackoverflow.com/users/{username}',
        'validation_regex': r'^[0-9]+$',
        'api_endpoint': 'https://api.stackexchange.com/2.3/users/{username}?site=stackoverflow',
        'sync_enabled': True
    },
    'behance': {
        'name': 'Behance',
        'url_pattern': 'https://behance.net/{username}',
        'validation_regex': r'^[a-zA-Z0-9_\-]+$',
        'api_endpoint': None,
        'sync_enabled': False
    },
    'dribbble': {
        'name': 'Dribbble',
        'url_pattern': 'https://dribbble.com/{username}',
        'validation_regex': r'^[a-zA-Z0-9_\-]+$',
        'api_endpoint': 'https://api.dribbble.com/v2/user/{username}',
        'sync_enabled': True
    },
    'medium': {
        'name': 'Medium',
        'url_pattern': 'https://medium.com/@{username}',
        'validation_regex': r'^[a-zA-Z0-9_\-\.]+$',
        'api_endpoint': None,
        'sync_enabled': False
    },
    'devto': {
        'name': 'Dev.to',
        'url_pattern': 'https://dev.to/{username}',
        'validation_regex': r'^[a-zA-Z0-9_\-]+$',
        'api_endpoint': 'https://dev.to/api/users/by_username?url={username}',
        'sync_enabled': True
    },
    'codepen': {
        'name': 'CodePen',
        'url_pattern': 'https://codepen.io/{username}',
        'validation_regex': r'^[a-zA-Z0-9_\-]+$',
        'api_endpoint': None,
        'sync_enabled': False
    },
    'gitlab': {
        'name': 'GitLab',
        'url_pattern': 'https://gitlab.com/{username}',
        'validation_regex': r'^[a-zA-Z0-9_\-\.]+$',
        'api_endpoint': 'https://gitlab.com/api/v4/users?username={username}',
        'sync_enabled': True
    },
    'bitbucket': {
        'name': 'Bitbucket',
        'url_pattern': 'https://bitbucket.org/{username}',
        'validation_regex': r'^[a-zA-Z0-9_\-]+$',
        'api_endpoint': 'https://api.bitbucket.org/2.0/users/{username}',
        'sync_enabled': True
    },
    'twitch': {
        'name': 'Twitch',
        'url_pattern': 'https://twitch.tv/{username}',
        'validation_regex': r'^[a-zA-Z0-9_]+$',
        'api_endpoint': 'https://api.twitch.tv/helix/users?login={username}',
        'sync_enabled': True
    },
    'discord': {
        'name': 'Discord',
        'url_pattern': 'discord://{username}',
        'validation_regex': r'^.+#[0-9]{4}$',
        'api_endpoint': None,
        'sync_enabled': False
    },
    'reddit': {
        'name': 'Reddit',
        'url_pattern': 'https://reddit.com/u/{username}',
        'validation_regex': r'^[a-zA-Z0-9_\-]+$',
        'api_endpoint': 'https://www.reddit.com/user/{username}/about.json',
        'sync_enabled': True
    },
    'pinterest': {
        'name': 'Pinterest',
        'url_pattern': 'https://pinterest.com/{username}',
        'validation_regex': r'^[a-zA-Z0-9_]+$',
        'api_endpoint': None,
        'sync_enabled': False
    },
    'tiktok': {
        'name': 'TikTok',
        'url_pattern': 'https://tiktok.com/@{username}',
        'validation_regex': r'^[a-zA-Z0-9_.]+$',
        'api_endpoint': None,
        'sync_enabled': False
    },
    'facebook': {
        'name': 'Facebook',
        'url_pattern': 'https://facebook.com/{username}',
        'validation_regex': r'^[a-zA-Z0-9.]+$',
        'api_endpoint': None,  # Facebook API requires special permissions
        'sync_enabled': False
    },
    'snapchat': {
        'name': 'Snapchat',
        'url_pattern': 'https://snapchat.com/add/{username}',
        'validation_regex': r'^[a-zA-Z0-9_\-\.]+$',
        'api_endpoint': None,
        'sync_enabled': False
    },
    'telegram': {
        'name': 'Telegram',
        'url_pattern': 'https://t.me/{username}',
        'validation_regex': r'^[a-zA-Z0-9_]+$',
        'api_endpoint': None,
        'sync_enabled': False
    },
    'whatsapp': {
        'name': 'WhatsApp',
        'url_pattern': 'https://wa.me/{username}',
        'validation_regex': r'^[0-9]+$',
        'api_endpoint': None,
        'sync_enabled': False
    },
    'spotify': {
        'name': 'Spotify',
        'url_pattern': 'https://open.spotify.com/user/{username}',
        'validation_regex': r'^[a-zA-Z0-9_]+$',
        'api_endpoint': 'https://api.spotify.com/v1/users/{username}',
        'sync_enabled': True
    },
    'steam': {
        'name': 'Steam',
        'url_pattern': 'https://steamcommunity.com/id/{username}',
        'validation_regex': r'^[a-zA-Z0-9_\-]+$',
        'api_endpoint': None,
        'sync_enabled': False
    },
    'hackerrank': {
        'name': 'HackerRank',
        'url_pattern': 'https://hackerrank.com/{username}',
        'validation_regex': r'^[a-zA-Z0-9_\-]+$',
        'api_endpoint': None,
        'sync_enabled': False
    },
    'leetcode': {
        'name': 'LeetCode',
        'url_pattern': 'https://leetcode.com/{username}',
        'validation_regex': r'^[a-zA-Z0-9_\-]+$',
        'api_endpoint': None,
        'sync_enabled': False
    },
    'replit': {
        'name': 'Replit',
        'url_pattern': 'https://replit.com/@{username}',
        'validation_regex': r'^[a-zA-Z0-9_\-]+$',
        'api_endpoint': None,
        'sync_enabled': False
    },
    'angellist': {
        'name': 'AngelList',
        'url_pattern': 'https://angel.co/u/{username}',
        'validation_regex': r'^[a-zA-Z0-9_\-]+$',
        'api_endpoint': None,
        'sync_enabled': False
    },
    'producthunt': {
        'name': 'Product Hunt',
        'url_pattern': 'https://producthunt.com/@{username}',
        'validation_regex': r'^[a-zA-Z0-9_\-]+$',
        'api_endpoint': None,
        'sync_enabled': False
    },
    'substack': {
        'name': 'Substack',
        'url_pattern': 'https://{username}.substack.com',
        'validation_regex': r'^[a-zA-Z0-9\-]+$',
        'api_endpoint': None,
        'sync_enabled': False
    },
    'deviantart': {
        'name': 'DeviantArt',
        'url_pattern': 'https://deviantart.com/{username}',
        'validation_regex': r'^[a-zA-Z0-9\-]+$',
        'api_endpoint': None,
        'sync_enabled': False
    }
}

def get_user_social_links_file(user_id):
    """Get the file path for user social links"""
    links_dir = '/tmp/user_social_links'
    os.makedirs(links_dir, exist_ok=True)
    return os.path.join(links_dir, f'user_{user_id}_social_links.json')

def load_user_social_links(user_id):
    """Load user social links from file"""
    links_file = get_user_social_links_file(user_id)
    
    if os.path.exists(links_file):
        try:
            with open(links_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading user social links: {e}")
    
    return {}

def save_user_social_links(user_id, links):
    """Save user social links to file"""
    links_file = get_user_social_links_file(user_id)
    
    try:
        with open(links_file, 'w') as f:
            json.dump(links, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving user social links: {e}")
        return False

def validate_username(network_id, username):
    """Validate username format for a specific network"""
    if network_id not in SUPPORTED_NETWORKS:
        return False, "Unsupported network"
    
    network = SUPPORTED_NETWORKS[network_id]
    pattern = network['validation_regex']
    
    if not re.match(pattern, username):
        return False, f"Invalid username format for {network['name']}"
    
    return True, "Valid"

@social_links_bp.route('/networks', methods=['GET'])
def get_supported_networks():
    """Get list of supported social networks"""
    networks = []
    for network_id, network_info in SUPPORTED_NETWORKS.items():
        networks.append({
            'id': network_id,
            'name': network_info['name'],
            'url_pattern': network_info['url_pattern'],
            'sync_enabled': network_info['sync_enabled']
        })
    
    return jsonify({
        'success': True,
        'networks': networks,
        'total_count': len(networks)
    })

@social_links_bp.route('/my-links', methods=['GET'])
@jwt_required()
def get_my_social_links():
    """Get user's connected social links"""
    try:
        user_id = get_jwt_identity()
        social_links = load_user_social_links(user_id)
        
        # Add network info to each link
        enriched_links = {}
        for network_id, link_data in social_links.items():
            if network_id in SUPPORTED_NETWORKS:
                enriched_links[network_id] = {
                    **link_data,
                    'network_name': SUPPORTED_NETWORKS[network_id]['name'],
                    'sync_enabled': SUPPORTED_NETWORKS[network_id]['sync_enabled']
                }
        
        return jsonify({
            'success': True,
            'social_links': enriched_links,
            'connected_count': len(enriched_links)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@social_links_bp.route('/connect', methods=['POST'])
@jwt_required()
def connect_social_link():
    """Connect a new social network"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        network_id = data.get('network_id')
        username = data.get('username', '').strip()
        
        if not network_id or not username:
            return jsonify({
                'success': False,
                'message': 'Network ID and username are required'
            }), 400
        
        # Validate network
        if network_id not in SUPPORTED_NETWORKS:
            return jsonify({
                'success': False,
                'message': 'Unsupported social network'
            }), 400
        
        # Validate username format
        is_valid, validation_message = validate_username(network_id, username)
        if not is_valid:
            return jsonify({
                'success': False,
                'message': validation_message
            }), 400
        
        # Load current social links
        social_links = load_user_social_links(user_id)
        
        # Create profile URL
        network_info = SUPPORTED_NETWORKS[network_id]
        profile_url = network_info['url_pattern'].format(username=username)
        
        # Add/update the social link
        social_links[network_id] = {
            'username': username,
            'profile_url': profile_url,
            'connected_at': datetime.now().isoformat(),
            'verified': False,  # Will be set to True after verification
            'sync_enabled': data.get('sync_enabled', False),
            'public': data.get('public', True)
        }
        
        # Save updated links
        if save_user_social_links(user_id, social_links):
            return jsonify({
                'success': True,
                'message': f'Successfully connected {network_info["name"]}',
                'social_link': {
                    'network_id': network_id,
                    'network_name': network_info['name'],
                    **social_links[network_id]
                }
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to save social link'
            }), 500
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@social_links_bp.route('/disconnect/<network_id>', methods=['DELETE'])
@jwt_required()
def disconnect_social_link(network_id):
    """Disconnect a social network"""
    try:
        user_id = get_jwt_identity()
        
        if network_id not in SUPPORTED_NETWORKS:
            return jsonify({
                'success': False,
                'message': 'Unsupported social network'
            }), 400
        
        # Load current social links
        social_links = load_user_social_links(user_id)
        
        if network_id not in social_links:
            return jsonify({
                'success': False,
                'message': 'Social network not connected'
            }), 404
        
        # Remove the social link
        network_name = SUPPORTED_NETWORKS[network_id]['name']
        del social_links[network_id]
        
        # Save updated links
        if save_user_social_links(user_id, social_links):
            return jsonify({
                'success': True,
                'message': f'Successfully disconnected {network_name}'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to save changes'
            }), 500
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@social_links_bp.route('/update/<network_id>', methods=['PUT'])
@jwt_required()
def update_social_link(network_id):
    """Update social link settings"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if network_id not in SUPPORTED_NETWORKS:
            return jsonify({
                'success': False,
                'message': 'Unsupported social network'
            }), 400
        
        # Load current social links
        social_links = load_user_social_links(user_id)
        
        if network_id not in social_links:
            return jsonify({
                'success': False,
                'message': 'Social network not connected'
            }), 404
        
        # Update settings
        if 'sync_enabled' in data:
            social_links[network_id]['sync_enabled'] = data['sync_enabled']
        
        if 'public' in data:
            social_links[network_id]['public'] = data['public']
        
        if 'username' in data:
            username = data['username'].strip()
            is_valid, validation_message = validate_username(network_id, username)
            if not is_valid:
                return jsonify({
                    'success': False,
                    'message': validation_message
                }), 400
            
            social_links[network_id]['username'] = username
            social_links[network_id]['profile_url'] = SUPPORTE
(Content truncated due to size limit. Use line ranges to read in chunks)
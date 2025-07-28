from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import json
import os
from datetime import datetime

settings_bp = Blueprint('settings', __name__)

# Default user settings
DEFAULT_SETTINGS = {
    'theme': {
        'mode': 'light',  # light, dark, auto, high-contrast, sepia
        'primary_color': '#3b82f6',  # blue
        'accent_color': '#10b981',   # emerald
        'font_size': 'medium',       # small, medium, large, extra-large
        'font_family': 'inter',      # inter, roboto, open-sans, poppins
        'border_radius': 'medium',   # none, small, medium, large, full
        'animations': True,
        'reduced_motion': False
    },
    'layout': {
        'sidebar_collapsed': False,
        'compact_mode': False,
        'show_breadcrumbs': True,
        'show_tooltips': True,
        'grid_density': 'comfortable'  # compact, comfortable, spacious
    },
    'accessibility': {
        'high_contrast': False,
        'large_text': False,
        'screen_reader': False,
        'keyboard_navigation': True,
        'focus_indicators': True
    },
    'notifications': {
        'email_notifications': True,
        'push_notifications': True,
        'sound_enabled': True,
        'desktop_notifications': True,
        'marketing_emails': False
    },
    'privacy': {
        'profile_visibility': 'public',  # public, friends, private
        'show_online_status': True,
        'allow_friend_requests': True,
        'show_activity': True,
        'data_collection': True
    },
    'developer': {
        'code_theme': 'vs-dark',        # vs-light, vs-dark, monokai, github
        'font_size': 14,
        'tab_size': 2,
        'word_wrap': True,
        'line_numbers': True,
        'minimap': True,
        'auto_save': True,
        'vim_mode': False
    },
    'language': {
        'interface_language': 'en',     # en, es, fr, de, zh, ja, etc.
        'date_format': 'MM/DD/YYYY',
        'time_format': '12h',           # 12h, 24h
        'timezone': 'UTC',
        'currency': 'USD'
    },
    'performance': {
        'animations_enabled': True,
        'lazy_loading': True,
        'image_quality': 'high',        # low, medium, high
        'auto_play_videos': False,
        'preload_content': True
    }
}

# Available theme presets
THEME_PRESETS = {
    'light': {
        'name': 'Light',
        'description': 'Clean and bright interface',
        'colors': {
            'background': '#ffffff',
            'surface': '#f8fafc',
            'primary': '#3b82f6',
            'secondary': '#64748b',
            'accent': '#10b981',
            'text': '#1e293b',
            'text_secondary': '#64748b',
            'border': '#e2e8f0',
            'success': '#10b981',
            'warning': '#f59e0b',
            'error': '#ef4444',
            'info': '#3b82f6'
        }
    },
    'dark': {
        'name': 'Dark',
        'description': 'Easy on the eyes for low-light environments',
        'colors': {
            'background': '#0f172a',
            'surface': '#1e293b',
            'primary': '#60a5fa',
            'secondary': '#94a3b8',
            'accent': '#34d399',
            'text': '#f1f5f9',
            'text_secondary': '#94a3b8',
            'border': '#334155',
            'success': '#34d399',
            'warning': '#fbbf24',
            'error': '#f87171',
            'info': '#60a5fa'
        }
    },
    'auto': {
        'name': 'Auto',
        'description': 'Automatically switches between light and dark based on system preference',
        'colors': 'system'
    },
    'high-contrast': {
        'name': 'High Contrast',
        'description': 'Maximum contrast for better accessibility',
        'colors': {
            'background': '#000000',
            'surface': '#1a1a1a',
            'primary': '#ffffff',
            'secondary': '#cccccc',
            'accent': '#ffff00',
            'text': '#ffffff',
            'text_secondary': '#cccccc',
            'border': '#ffffff',
            'success': '#00ff00',
            'warning': '#ffff00',
            'error': '#ff0000',
            'info': '#00ffff'
        }
    },
    'sepia': {
        'name': 'Sepia',
        'description': 'Warm, paper-like appearance that reduces eye strain',
        'colors': {
            'background': '#f7f3e9',
            'surface': '#f0ead6',
            'primary': '#8b4513',
            'secondary': '#a0522d',
            'accent': '#cd853f',
            'text': '#2f1b14',
            'text_secondary': '#5d4e37',
            'border': '#deb887',
            'success': '#228b22',
            'warning': '#ff8c00',
            'error': '#dc143c',
            'info': '#4682b4'
        }
    },
    'blue': {
        'name': 'Ocean Blue',
        'description': 'Calming blue-themed interface',
        'colors': {
            'background': '#f0f9ff',
            'surface': '#e0f2fe',
            'primary': '#0284c7',
            'secondary': '#0369a1',
            'accent': '#0891b2',
            'text': '#0c4a6e',
            'text_secondary': '#075985',
            'border': '#bae6fd',
            'success': '#059669',
            'warning': '#d97706',
            'error': '#dc2626',
            'info': '#0284c7'
        }
    },
    'green': {
        'name': 'Nature Green',
        'description': 'Fresh and natural green theme',
        'colors': {
            'background': '#f0fdf4',
            'surface': '#dcfce7',
            'primary': '#16a34a',
            'secondary': '#15803d',
            'accent': '#059669',
            'text': '#14532d',
            'text_secondary': '#166534',
            'border': '#bbf7d0',
            'success': '#16a34a',
            'warning': '#d97706',
            'error': '#dc2626',
            'info': '#0284c7'
        }
    },
    'purple': {
        'name': 'Royal Purple',
        'description': 'Elegant purple-themed interface',
        'colors': {
            'background': '#faf5ff',
            'surface': '#f3e8ff',
            'primary': '#9333ea',
            'secondary': '#7c3aed',
            'accent': '#a855f7',
            'text': '#581c87',
            'text_secondary': '#6b21a8',
            'border': '#d8b4fe',
            'success': '#059669',
            'warning': '#d97706',
            'error': '#dc2626',
            'info': '#0284c7'
        }
    }
}

# User settings storage (in production, this would be in a database)
user_settings = {}

def get_user_settings_file(user_id):
    """Get the file path for user settings"""
    settings_dir = '/tmp/user_settings'
    os.makedirs(settings_dir, exist_ok=True)
    return os.path.join(settings_dir, f'user_{user_id}_settings.json')

def load_user_settings(user_id):
    """Load user settings from file"""
    settings_file = get_user_settings_file(user_id)
    
    if os.path.exists(settings_file):
        try:
            with open(settings_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading user settings: {e}")
    
    return DEFAULT_SETTINGS.copy()

def save_user_settings(user_id, settings):
    """Save user settings to file"""
    settings_file = get_user_settings_file(user_id)
    
    try:
        with open(settings_file, 'w') as f:
            json.dump(settings, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving user settings: {e}")
        return False

@settings_bp.route('/get', methods=['GET'])
@jwt_required()
def get_settings():
    """Get user settings"""
    try:
        user_id = get_jwt_identity()
        settings = load_user_settings(user_id)
        
        return jsonify({
            'success': True,
            'settings': settings,
            'last_updated': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@settings_bp.route('/update', methods=['POST'])
@jwt_required()
def update_settings():
    """Update user settings"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Load current settings
        current_settings = load_user_settings(user_id)
        
        # Update settings with provided data
        def deep_update(base_dict, update_dict):
            for key, value in update_dict.items():
                if key in base_dict and isinstance(base_dict[key], dict) and isinstance(value, dict):
                    deep_update(base_dict[key], value)
                else:
                    base_dict[key] = value
        
        deep_update(current_settings, data)
        
        # Save updated settings
        if save_user_settings(user_id, current_settings):
            return jsonify({
                'success': True,
                'message': 'Settings updated successfully',
                'settings': current_settings
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to save settings'
            }), 500
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@settings_bp.route('/theme', methods=['GET'])
def get_theme_presets():
    """Get available theme presets"""
    return jsonify({
        'success': True,
        'presets': THEME_PRESETS,
        'default_theme': 'light'
    })

@settings_bp.route('/theme/<theme_name>', methods=['POST'])
@jwt_required()
def apply_theme_preset(theme_name):
    """Apply a theme preset"""
    try:
        if theme_name not in THEME_PRESETS:
            return jsonify({
                'success': False,
                'message': 'Theme preset not found'
            }), 404
        
        user_id = get_jwt_identity()
        current_settings = load_user_settings(user_id)
        
        # Update theme settings
        current_settings['theme']['mode'] = theme_name
        
        # If theme has specific colors, update them
        theme_preset = THEME_PRESETS[theme_name]
        if 'colors' in theme_preset and theme_preset['colors'] != 'system':
            current_settings['theme']['colors'] = theme_preset['colors']
        
        # Save updated settings
        if save_user_settings(user_id, current_settings):
            return jsonify({
                'success': True,
                'message': f'Theme "{theme_preset["name"]}" applied successfully',
                'theme': theme_preset,
                'settings': current_settings
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to save theme settings'
            }), 500
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@settings_bp.route('/reset', methods=['POST'])
@jwt_required()
def reset_settings():
    """Reset settings to default"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        category = data.get('category', 'all')  # all, theme, layout, accessibility, etc.
        
        current_settings = load_user_settings(user_id)
        
        if category == 'all':
            current_settings = DEFAULT_SETTINGS.copy()
        elif category in DEFAULT_SETTINGS:
            current_settings[category] = DEFAULT_SETTINGS[category].copy()
        else:
            return jsonify({
                'success': False,
                'message': 'Invalid settings category'
            }), 400
        
        # Save reset settings
        if save_user_settings(user_id, current_settings):
            return jsonify({
                'success': True,
                'message': f'Settings reset successfully ({category})',
                'settings': current_settings
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to reset settings'
            }), 500
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@settings_bp.route('/export', methods=['GET'])
@jwt_required()
def export_settings():
    """Export user settings"""
    try:
        user_id = get_jwt_identity()
        settings = load_user_settings(user_id)
        
        export_data = {
            'version': '1.0',
            'exported_at': datetime.now().isoformat(),
            'user_id': user_id,
            'settings': settings
        }
        
        return jsonify({
            'success': True,
            'export_data': export_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@settings_bp.route('/import', methods=['POST'])
@jwt_required()
def import_settings():
    """Import user settings"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if 'export_data' not in data:
            return jsonify({
                'success': False,
                'message': 'Invalid import data'
            }), 400
        
        export_data = data['export_data']
        
        if 'settings' not in export_data:
            return jsonify({
                'success': False,
                'message': 'No settings found in import data'
            }), 400
        
        imported_settings = export_data['settings']
        
        # Validate imported settings structure
        def validate_settings(settings, default):
            validated = {}
            for key, value in default.items():
                if key in settings:
                    if isinstance(value, dict):
                        validated[key] = validate_settings(settings[key], value)
                    else:
                        validated[key] = settings[key]
                else:
                    validated[key] = value
            return validated
        
        validated_settings = validate_settings(imported_settings, DEFAULT_SETTINGS)
        
        # Save imported settings
        if save_user_settings(user_id, validated_settings):
            return jsonify({
                'success': True,
                'message': 'Settings imported successfully',
                'settings': validated_settings
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to save imported settings'
            }), 500
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@settings_bp.route('/accessibility', methods=['POST'])
@jwt_required()
def update_accessibility_settings():
    """Update accessibility settings"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        current_settings = load_user_settings(user_id)
        
        # Update accessibility settings
        if 'accessibility' in data:
            current_settings['accessibility'].update(data['accessibility'])
        
        # Auto-adjust theme based on accessibility needs
        if data.get('accessibility', {}).get('high_contrast'):
            current_settings['theme']['mode'] = 'high-contrast'
        
        if data.get('accessibility', {}).get('large_text'):
            current_settings['theme']['font_size'] = 'extra-large'
        
        # Save updated settings
        if save_user_settings(user_id, current_settings):
            return jsonify({
                'success': True,
                'message': 'Accessibility settings updated successfully',
                'settings': current_settings
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to save accessibility settings'
            }), 
(Content truncated due to size limit. Use line ranges to read in chunks)
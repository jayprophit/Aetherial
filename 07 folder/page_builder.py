from flask import Blueprint, request, jsonify
import json
import uuid
from datetime import datetime

page_builder_bp = Blueprint('page_builder', __name__)

# Mock database for page builder elements and themes
elements_db = {}
themes_db = {}
user_pages_db = {}

# Initialize with default themes
default_themes = {
    'modern_light': {
        'id': 'modern_light',
        'name': 'Modern Light',
        'description': 'Clean and bright modern theme',
        'category': 'modern',
        'colors': {
            'primary': '#3B82F6',
            'secondary': '#10B981',
            'accent': '#F59E0B',
            'background': '#FFFFFF',
            'surface': '#F8FAFC',
            'text': '#1F2937',
            'text_secondary': '#6B7280'
        },
        'typography': {
            'font_family': 'Inter, sans-serif',
            'heading_font': 'Inter, sans-serif',
            'font_sizes': {
                'xs': '0.75rem',
                'sm': '0.875rem',
                'base': '1rem',
                'lg': '1.125rem',
                'xl': '1.25rem',
                '2xl': '1.5rem',
                '3xl': '1.875rem',
                '4xl': '2.25rem'
            }
        },
        'spacing': {
            'xs': '0.25rem',
            'sm': '0.5rem',
            'md': '1rem',
            'lg': '1.5rem',
            'xl': '2rem',
            '2xl': '3rem'
        },
        'borders': {
            'radius': '0.5rem',
            'width': '1px'
        }
    },
    'dark_professional': {
        'id': 'dark_professional',
        'name': 'Dark Professional',
        'description': 'Sleek dark theme for professional sites',
        'category': 'dark',
        'colors': {
            'primary': '#6366F1',
            'secondary': '#06B6D4',
            'accent': '#F59E0B',
            'background': '#111827',
            'surface': '#1F2937',
            'text': '#F9FAFB',
            'text_secondary': '#D1D5DB'
        },
        'typography': {
            'font_family': 'Inter, sans-serif',
            'heading_font': 'Inter, sans-serif',
            'font_sizes': {
                'xs': '0.75rem',
                'sm': '0.875rem',
                'base': '1rem',
                'lg': '1.125rem',
                'xl': '1.25rem',
                '2xl': '1.5rem',
                '3xl': '1.875rem',
                '4xl': '2.25rem'
            }
        },
        'spacing': {
            'xs': '0.25rem',
            'sm': '0.5rem',
            'md': '1rem',
            'lg': '1.5rem',
            'xl': '2rem',
            '2xl': '3rem'
        },
        'borders': {
            'radius': '0.5rem',
            'width': '1px'
        }
    },
    'colorful_creative': {
        'id': 'colorful_creative',
        'name': 'Colorful Creative',
        'description': 'Vibrant theme for creative projects',
        'category': 'creative',
        'colors': {
            'primary': '#EC4899',
            'secondary': '#8B5CF6',
            'accent': '#F59E0B',
            'background': '#FEFEFE',
            'surface': '#FDF2F8',
            'text': '#1F2937',
            'text_secondary': '#6B7280'
        },
        'typography': {
            'font_family': 'Poppins, sans-serif',
            'heading_font': 'Poppins, sans-serif',
            'font_sizes': {
                'xs': '0.75rem',
                'sm': '0.875rem',
                'base': '1rem',
                'lg': '1.125rem',
                'xl': '1.25rem',
                '2xl': '1.5rem',
                '3xl': '1.875rem',
                '4xl': '2.25rem'
            }
        },
        'spacing': {
            'xs': '0.25rem',
            'sm': '0.5rem',
            'md': '1rem',
            'lg': '1.5rem',
            'xl': '2rem',
            '2xl': '3rem'
        },
        'borders': {
            'radius': '1rem',
            'width': '2px'
        }
    }
}

themes_db.update(default_themes)

@page_builder_bp.route('/themes', methods=['GET'])
def get_themes():
    """Get all available themes"""
    category = request.args.get('category')
    themes = list(themes_db.values())
    
    if category:
        themes = [t for t in themes if t.get('category') == category]
    
    return jsonify({
        'success': True,
        'themes': themes
    })

@page_builder_bp.route('/elements/library', methods=['GET'])
def get_element_library():
    """Get comprehensive element library for page builder"""
    library = {
        'layout': {
            'container': {
                'name': 'Container',
                'description': 'Responsive container wrapper',
                'icon': 'layout',
                'category': 'layout',
                'settings': {
                    'width': {'type': 'select', 'options': ['full', 'container', 'narrow'], 'default': 'container'},
                    'padding': {'type': 'spacing', 'default': 'md'},
                    'margin': {'type': 'spacing', 'default': 'none'},
                    'background_color': {'type': 'color', 'default': 'transparent'},
                    'background_image': {'type': 'image', 'default': ''},
                    'min_height': {'type': 'number', 'default': 'auto'},
                    'custom_css': {'type': 'textarea', 'default': ''}
                },
                'default_content': {
                    'type': 'container',
                    'settings': {
                        'width': 'container',
                        'padding': 'md'
                    },
                    'children': []
                }
            },
            'section': {
                'name': 'Section',
                'description': 'Full-width section wrapper',
                'icon': 'square',
                'category': 'layout',
                'settings': {
                    'background_color': {'type': 'color', 'default': 'transparent'},
                    'background_image': {'type': 'image', 'default': ''},
                    'padding_top': {'type': 'spacing', 'default': 'xl'},
                    'padding_bottom': {'type': 'spacing', 'default': 'xl'},
                    'overlay_color': {'type': 'color', 'default': 'transparent'},
                    'overlay_opacity': {'type': 'range', 'min': 0, 'max': 100, 'default': 0}
                }
            },
            'row': {
                'name': 'Row',
                'description': 'Horizontal row with columns',
                'icon': 'columns',
                'category': 'layout',
                'settings': {
                    'columns': {'type': 'number', 'min': 1, 'max': 12, 'default': 2},
                    'gap': {'type': 'spacing', 'default': 'md'},
                    'vertical_alignment': {'type': 'select', 'options': ['top', 'center', 'bottom'], 'default': 'top'},
                    'wrap': {'type': 'boolean', 'default': True}
                }
            },
            'column': {
                'name': 'Column',
                'description': 'Flexible column container',
                'icon': 'column',
                'category': 'layout',
                'settings': {
                    'width': {'type': 'select', 'options': ['auto', '25%', '33%', '50%', '66%', '75%', '100%'], 'default': 'auto'},
                    'padding': {'type': 'spacing', 'default': 'md'},
                    'background_color': {'type': 'color', 'default': 'transparent'},
                    'text_alignment': {'type': 'select', 'options': ['left', 'center', 'right'], 'default': 'left'}
                }
            }
        },
        'content': {
            'heading': {
                'name': 'Heading',
                'description': 'Text heading (H1-H6)',
                'icon': 'heading',
                'category': 'content',
                'settings': {
                    'text': {'type': 'text', 'default': 'Your Heading Here'},
                    'level': {'type': 'select', 'options': ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'], 'default': 'h2'},
                    'alignment': {'type': 'select', 'options': ['left', 'center', 'right'], 'default': 'left'},
                    'color': {'type': 'color', 'default': 'text'},
                    'font_size': {'type': 'select', 'options': ['sm', 'base', 'lg', 'xl', '2xl', '3xl', '4xl'], 'default': '2xl'},
                    'font_weight': {'type': 'select', 'options': ['normal', 'medium', 'semibold', 'bold'], 'default': 'bold'},
                    'margin_bottom': {'type': 'spacing', 'default': 'md'}
                }
            },
            'paragraph': {
                'name': 'Paragraph',
                'description': 'Text paragraph',
                'icon': 'type',
                'category': 'content',
                'settings': {
                    'text': {'type': 'textarea', 'default': 'Your paragraph text goes here. You can write multiple lines and format the text as needed.'},
                    'alignment': {'type': 'select', 'options': ['left', 'center', 'right', 'justify'], 'default': 'left'},
                    'color': {'type': 'color', 'default': 'text'},
                    'font_size': {'type': 'select', 'options': ['xs', 'sm', 'base', 'lg', 'xl'], 'default': 'base'},
                    'line_height': {'type': 'select', 'options': ['tight', 'normal', 'relaxed', 'loose'], 'default': 'normal'},
                    'margin_bottom': {'type': 'spacing', 'default': 'md'}
                }
            },
            'image': {
                'name': 'Image',
                'description': 'Image with optional caption',
                'icon': 'image',
                'category': 'content',
                'settings': {
                    'src': {'type': 'image', 'default': '/placeholder-image.jpg'},
                    'alt': {'type': 'text', 'default': 'Image description'},
                    'caption': {'type': 'text', 'default': ''},
                    'alignment': {'type': 'select', 'options': ['left', 'center', 'right'], 'default': 'center'},
                    'size': {'type': 'select', 'options': ['small', 'medium', 'large', 'full'], 'default': 'medium'},
                    'border_radius': {'type': 'select', 'options': ['none', 'sm', 'md', 'lg', 'full'], 'default': 'md'},
                    'shadow': {'type': 'select', 'options': ['none', 'sm', 'md', 'lg'], 'default': 'none'},
                    'link': {'type': 'url', 'default': ''}
                }
            },
            'video': {
                'name': 'Video',
                'description': 'Video player with controls',
                'icon': 'video',
                'category': 'content',
                'settings': {
                    'src': {'type': 'video', 'default': ''},
                    'poster': {'type': 'image', 'default': ''},
                    'controls': {'type': 'boolean', 'default': True},
                    'autoplay': {'type': 'boolean', 'default': False},
                    'loop': {'type': 'boolean', 'default': False},
                    'muted': {'type': 'boolean', 'default': False},
                    'aspect_ratio': {'type': 'select', 'options': ['16:9', '4:3', '1:1'], 'default': '16:9'}
                }
            },
            'button': {
                'name': 'Button',
                'description': 'Call-to-action button',
                'icon': 'mouse-pointer',
                'category': 'content',
                'settings': {
                    'text': {'type': 'text', 'default': 'Click Me'},
                    'link': {'type': 'url', 'default': '#'},
                    'target': {'type': 'select', 'options': ['_self', '_blank'], 'default': '_self'},
                    'style': {'type': 'select', 'options': ['primary', 'secondary', 'outline', 'ghost'], 'default': 'primary'},
                    'size': {'type': 'select', 'options': ['sm', 'md', 'lg'], 'default': 'md'},
                    'alignment': {'type': 'select', 'options': ['left', 'center', 'right'], 'default': 'left'},
                    'full_width': {'type': 'boolean', 'default': False},
                    'icon': {'type': 'icon', 'default': ''},
                    'icon_position': {'type': 'select', 'options': ['left', 'right'], 'default': 'left'}
                }
            },
            'spacer': {
                'name': 'Spacer',
                'description': 'Empty space for layout',
                'icon': 'minus',
                'category': 'content',
                'settings': {
                    'height': {'type': 'spacing', 'default': 'xl'},
                    'mobile_height': {'type': 'spacing', 'default': 'lg'}
                }
            }
        },
        'media': {
            'gallery': {
                'name': 'Image Gallery',
                'description': 'Grid of images with lightbox',
                'icon': 'grid',
                'category': 'media',
                'settings': {
                    'images': {'type': 'image_array', 'default': []},
                    'columns': {'type': 'number', 'min': 1, 'max': 6, 'default': 3},
                    'gap': {'type': 'spacing', 'default': 'md'},
                    'lightbox': {'type': 'boolean', 'default': True},
                    'captions': {'type': 'boolean', 'default': False}
                }
            },
            'slider': {
                'name': 'Image Slider',
                'description': 'Carousel of images',
                'icon': 'chevrons-right',
                'category': 'media',
                'settings': {
                    'images': {'type': 'image_array', 'default': []},
                    'autoplay': {'type': 'boolean', 'default': True},
                    'autoplay_speed': {'type': 'number', 'default': 5000},
                    'navigation': {'type': 'boolean', 'default': True},
                    'pagination': {'type': 'boolean', 'default': True},
                    'loop': {'type': 'boolean', 'default': True}
                }
            },
            'audio': {
                'name': 'Audio Player',
                'description': 'Audio player with controls',
                'icon': 'volume-2',
                'category': 'media',
                'settings': {
                    'src': {'type': 'audio', 'default': ''},
                    'title': {'type': 'text', 'default': 'Audio Track'},
                    'artist': {'type': 'text', 'default': ''},
                    'cover': {'type': 'image', 'default': ''},
                    'autoplay': {'type': 'boolean', 'default': False},
                    'loop': {'type': 'boolean', 'default': False}
                }
            }
        },
        'forms': {
            'contact_form': {
                'name': 'Contact Form',
                'description': 'Contact form with customizable fields',
                'icon': 'mail',
                'category': 'forms',
                'settings': {
                    'title': {'type': 'text', 'default': 'Contact Us'},
                    'fields': {
                        'type': 'field_array',
                        'default': [
                            {'type': 'text', 'name': 'name', 'label': 'Name', 'required': True},
                            {'type': 'email', 'name': 'email', 'label': 'Email', 'required': True},
                            {'type': 'textarea', 'name': 'message', 'label': 'Message', 'required': True}
                        ]
                    },
                    'submit_text': {'type': 'text', 'default': 'Send Message'},
                    'success_message': {'type': 'text', 'default': 'Thank you for your message!'},
                    'email_to': {'type': 'email', 'default': ''},
                    'redirect_url': {'type': 'url', 'default': ''}
                }
            },
            'newsletter': {
                'name': 'Newsletter Signup',
                'description': 'Email newsletter subscription form',
                'icon': 'mail-plus',
       
(Content truncated due to size limit. Use line ranges to read in chunks)
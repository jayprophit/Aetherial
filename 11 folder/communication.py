"""
Communication Platform API - WhatsApp/Telegram/Discord/Zoom Features
Complete communication suite with messaging, voice/video calls, and collaboration
"""

from flask import Blueprint, request, jsonify
import random
import time
from datetime import datetime, timedelta

communication_bp = Blueprint('communication', __name__)

# Mock data for demonstration
CHAT_ROOMS = {
    "room001": {
        "room_id": "room001",
        "name": "AI Development Team",
        "description": "Discussion about AI and machine learning projects",
        "type": "group",  # group, direct, channel
        "privacy": "private",  # public, private, invite_only
        "created_by": "user001",
        "created_at": "2024-01-15T10:00:00Z",
        "member_count": 15,
        "members": [
            {
                "user_id": "user001",
                "username": "john_doe",
                "display_name": "John Doe",
                "role": "admin",
                "joined_at": "2024-01-15T10:00:00Z",
                "last_seen": "2024-01-27T12:30:00Z",
                "status": "online"
            },
            {
                "user_id": "user002",
                "username": "sarah_tech",
                "display_name": "Sarah Johnson",
                "role": "moderator",
                "joined_at": "2024-01-15T10:05:00Z",
                "last_seen": "2024-01-27T12:25:00Z",
                "status": "online"
            }
        ],
        "settings": {
            "allow_file_sharing": True,
            "allow_voice_messages": True,
            "allow_video_calls": True,
            "message_history_visible": True,
            "invite_permissions": "admins_only"
        },
        "avatar": "/images/rooms/ai_team_avatar.jpg",
        "pinned_messages": [],
        "tags": ["AI", "Development", "Team"]
    },
    "room002": {
        "room_id": "room002",
        "name": "Supply Chain Innovation",
        "description": "Discussing supply chain automation and optimization",
        "type": "channel",
        "privacy": "public",
        "created_by": "user003",
        "created_at": "2024-01-20T14:30:00Z",
        "member_count": 234,
        "members": [],  # Simplified for demo
        "settings": {
            "allow_file_sharing": True,
            "allow_voice_messages": True,
            "allow_video_calls": False,
            "message_history_visible": True,
            "invite_permissions": "everyone"
        },
        "avatar": "/images/rooms/supply_chain_avatar.jpg",
        "pinned_messages": [],
        "tags": ["SupplyChain", "Innovation", "Business"]
    }
}

MESSAGES_DATABASE = [
    {
        "message_id": "msg001",
        "room_id": "room001",
        "sender_id": "user001",
        "sender_info": {
            "username": "john_doe",
            "display_name": "John Doe",
            "avatar": "/images/profiles/john.jpg"
        },
        "content": "Hey team! I've just finished implementing the new AI algorithm for supply chain optimization. The results are incredible - we're seeing 25% cost reduction!",
        "message_type": "text",
        "timestamp": "2024-01-27T10:30:00Z",
        "edited": False,
        "reactions": {
            "👍": ["user002", "user003"],
            "🚀": ["user002"],
            "❤️": ["user004"]
        },
        "replies_count": 3,
        "thread_id": None,
        "attachments": [],
        "mentions": [],
        "read_by": ["user001", "user002", "user003"]
    },
    {
        "message_id": "msg002",
        "room_id": "room001",
        "sender_id": "user002",
        "sender_info": {
            "username": "sarah_tech",
            "display_name": "Sarah Johnson",
            "avatar": "/images/profiles/sarah.jpg"
        },
        "content": "That's amazing, John! Can you share the technical details? I'd love to integrate this with our robotics platform.",
        "message_type": "text",
        "timestamp": "2024-01-27T10:32:00Z",
        "edited": False,
        "reactions": {
            "👍": ["user001"]
        },
        "replies_count": 0,
        "thread_id": "msg001",
        "attachments": [],
        "mentions": ["user001"],
        "read_by": ["user001", "user002"]
    },
    {
        "message_id": "msg003",
        "room_id": "room001",
        "sender_id": "user001",
        "sender_info": {
            "username": "john_doe",
            "display_name": "John Doe",
            "avatar": "/images/profiles/john.jpg"
        },
        "content": "",
        "message_type": "file",
        "timestamp": "2024-01-27T10:35:00Z",
        "edited": False,
        "reactions": {},
        "replies_count": 0,
        "thread_id": None,
        "attachments": [
            {
                "file_id": "file001",
                "filename": "ai_algorithm_specs.pdf",
                "file_type": "application/pdf",
                "file_size": 2048576,
                "url": "/files/ai_algorithm_specs.pdf",
                "thumbnail": "/thumbnails/pdf_thumb.jpg"
            }
        ],
        "mentions": [],
        "read_by": ["user001"]
    }
]

VOICE_CALLS = {}
VIDEO_CALLS = {}

@communication_bp.route('/api/communication/rooms', methods=['GET'])
def get_chat_rooms():
    """
    Get user's chat rooms and channels
    """
    user_id = request.args.get('user_id', 'user001')
    room_type = request.args.get('type', 'all')  # all, group, direct, channel
    
    # Filter rooms based on user membership and type
    user_rooms = []
    for room_id, room in CHAT_ROOMS.items():
        # Check if user is member (simplified check)
        is_member = any(member['user_id'] == user_id for member in room['members']) or room['privacy'] == 'public'
        
        if is_member:
            if room_type == 'all' or room['type'] == room_type:
                # Add unread message count
                room_copy = room.copy()
                room_copy['unread_count'] = random.randint(0, 5)
                room_copy['last_message'] = {
                    "content": "Hey team! I've just finished implementing...",
                    "sender": "John Doe",
                    "timestamp": "2024-01-27T10:30:00Z"
                }
                user_rooms.append(room_copy)
    
    # Sort by last activity
    user_rooms.sort(key=lambda x: x.get('last_message', {}).get('timestamp', ''), reverse=True)
    
    return jsonify({
        "status": "success",
        "rooms": user_rooms,
        "summary": {
            "total_rooms": len(user_rooms),
            "unread_total": sum(room['unread_count'] for room in user_rooms),
            "active_calls": 2,
            "online_friends": 15
        }
    })

@communication_bp.route('/api/communication/rooms/create', methods=['POST'])
def create_chat_room():
    """
    Create a new chat room or channel
    """
    data = request.get_json()
    
    name = data.get('name', '')
    description = data.get('description', '')
    room_type = data.get('type', 'group')  # group, channel
    privacy = data.get('privacy', 'private')
    creator_id = data.get('creator_id')
    initial_members = data.get('members', [])
    
    room_id = f"room{int(time.time())}"
    new_room = {
        "room_id": room_id,
        "name": name,
        "description": description,
        "type": room_type,
        "privacy": privacy,
        "created_by": creator_id,
        "created_at": datetime.now().isoformat() + "Z",
        "member_count": len(initial_members) + 1,  # +1 for creator
        "members": [
            {
                "user_id": creator_id,
                "role": "admin",
                "joined_at": datetime.now().isoformat() + "Z",
                "status": "online"
            }
        ] + [
            {
                "user_id": member_id,
                "role": "member",
                "joined_at": datetime.now().isoformat() + "Z",
                "status": "offline"
            } for member_id in initial_members
        ],
        "settings": {
            "allow_file_sharing": True,
            "allow_voice_messages": True,
            "allow_video_calls": True,
            "message_history_visible": True,
            "invite_permissions": "admins_only" if room_type == "group" else "everyone"
        },
        "avatar": f"/images/rooms/default_{room_type}.jpg",
        "pinned_messages": [],
        "tags": data.get('tags', [])
    }
    
    # Add to database
    CHAT_ROOMS[room_id] = new_room
    
    return jsonify({
        "status": "success",
        "message": f"{room_type.title()} created successfully",
        "room": new_room
    })

@communication_bp.route('/api/communication/rooms/<room_id>/messages', methods=['GET', 'POST'])
def handle_messages(room_id):
    """
    Get messages from a room or send a new message
    """
    if request.method == 'GET':
        # Get messages for room
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 50))
        
        room_messages = [msg for msg in MESSAGES_DATABASE if msg['room_id'] == room_id]
        room_messages.sort(key=lambda x: x['timestamp'], reverse=True)
        
        # Pagination
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        paginated_messages = room_messages[start_idx:end_idx]
        
        # Reverse to show oldest first
        paginated_messages.reverse()
        
        return jsonify({
            "status": "success",
            "room_id": room_id,
            "messages": paginated_messages,
            "pagination": {
                "current_page": page,
                "per_page": limit,
                "total_messages": len(room_messages),
                "has_more": end_idx < len(room_messages)
            }
        })
    
    elif request.method == 'POST':
        # Send new message
        data = request.get_json()
        
        sender_id = data.get('sender_id')
        content = data.get('content', '')
        message_type = data.get('message_type', 'text')  # text, image, video, file, voice
        attachments = data.get('attachments', [])
        mentions = data.get('mentions', [])
        reply_to = data.get('reply_to')  # message_id for replies
        
        message_id = f"msg{int(time.time())}"
        new_message = {
            "message_id": message_id,
            "room_id": room_id,
            "sender_id": sender_id,
            "sender_info": {
                "username": "user_" + sender_id[-3:],
                "display_name": f"User {sender_id[-3:]}",
                "avatar": f"/images/profiles/user{sender_id[-3:]}.jpg"
            },
            "content": content,
            "message_type": message_type,
            "timestamp": datetime.now().isoformat() + "Z",
            "edited": False,
            "reactions": {},
            "replies_count": 0,
            "thread_id": reply_to,
            "attachments": attachments,
            "mentions": mentions,
            "read_by": [sender_id]
        }
        
        # Add to database
        MESSAGES_DATABASE.append(new_message)
        
        # Update reply count if this is a reply
        if reply_to:
            parent_message = next((msg for msg in MESSAGES_DATABASE if msg['message_id'] == reply_to), None)
            if parent_message:
                parent_message['replies_count'] += 1
        
        return jsonify({
            "status": "success",
            "message": "Message sent successfully",
            "message_data": new_message
        })

@communication_bp.route('/api/communication/messages/<message_id>/react', methods=['POST'])
def react_to_message(message_id):
    """
    Add reaction to a message
    """
    data = request.get_json()
    
    user_id = data.get('user_id')
    emoji = data.get('emoji', '👍')
    
    message = next((msg for msg in MESSAGES_DATABASE if msg['message_id'] == message_id), None)
    if not message:
        return jsonify({"status": "error", "message": "Message not found"}), 404
    
    # Add or remove reaction
    if emoji not in message['reactions']:
        message['reactions'][emoji] = []
    
    if user_id in message['reactions'][emoji]:
        message['reactions'][emoji].remove(user_id)
        if not message['reactions'][emoji]:
            del message['reactions'][emoji]
        action = "removed"
    else:
        message['reactions'][emoji].append(user_id)
        action = "added"
    
    return jsonify({
        "status": "success",
        "message": f"Reaction {action}",
        "reactions": message['reactions']
    })

@communication_bp.route('/api/communication/calls/voice/start', methods=['POST'])
def start_voice_call():
    """
    Start a voice call
    """
    data = request.get_json()
    
    caller_id = data.get('caller_id')
    room_id = data.get('room_id')
    participants = data.get('participants', [])
    
    call_id = f"voice{int(time.time())}"
    voice_call = {
        "call_id": call_id,
        "call_type": "voice",
        "room_id": room_id,
        "caller_id": caller_id,
        "participants": participants,
        "status": "ringing",
        "started_at": datetime.now().isoformat() + "Z",
        "duration": 0,
        "quality": "HD",
        "settings": {
            "mute_on_join": False,
            "recording_enabled": False,
            "noise_cancellation": True
        }
    }
    
    VOICE_CALLS[call_id] = voice_call
    
    return jsonify({
        "status": "success",
        "message": "Voice call initiated",
        "call": voice_call,
        "join_url": f"/calls/voice/{call_id}",
        "dial_in_number": "+1-555-CALL-123"
    })

@communication_bp.route('/api/communication/calls/video/start', methods=['POST'])
def start_video_call():
    """
    Start a video call (Zoom-like functionality)
    """
    data = request.get_json()
    
    host_id = data.get('host_id')
    room_id = data.get('room_id')
    participants = data.get('participants', [])
    meeting_title = data.get('title', 'Video Meeting')
    scheduled_time = data.get('scheduled_time')  # For scheduled meetings
    
    call_id = f"video{int(time.time())}"
    video_call = {
        "call_id": call_id,
        "call_type": "video",
        "meeting_title": meeting_title,
        "room_id": room_id,
        "host_id": host_id,
        "participants": participants,
        "status": "waiting" if scheduled_time else "active",
        "started_at": datetime.now().isoformat() + "Z",
        "scheduled_time": scheduled_time,
        "duration": 0,
        "max_participants": 100,
        "current_participants": 1,
        "settings": {
            "video_quality": "1080p",
            "audio_quality": "HD",
            "screen_sharing": True,
            "recording": False,
            "waiting_room": True,
            "mute_participants_on_join": True,
            "allow_chat": True,
            "allow_reactions": True
        },
        "features": {
            "breakout_rooms": True,
            "whiteboard": True,
            "polls": True,
            "hand_raising": True,
            "background_blur": True,
            "virtual_backgrounds": True
        }
    }
    
    VIDEO_CALLS[call_id] = video_call
    
    return jsonify({
        "status": "success",
        "message": "Video call created",
        "call": video_call,
        "join_url": f"/calls/video/{call_id}",
        "meeting_id": call_id,
        "passcode": "123456",
        "dial_in_numbers": [
            "+1-555-VIDEO-01",
            "+44-20-VIDEO-02",
            "+81-3-VIDEO-03"
        ]
    })

@communication_bp.route('/api/communication/calls/<call_id>/join', methods=['POST'])
def join_call(call_id):
    """
    Join an existing voice or video call
    """
    data = request.get_json()
    
    user_id = data.get('user_id')
    audio_enabled = data.get('audio_enabled', True)
    video_enabled = data.get('video_enabled', True)
    
    # Check voice calls first
    call = VOICE_CALLS.get(call_id) or VIDEO_CALLS.get(call_id)
    if not call:
        return jsonify({"status": "error", "message": "Call not found"}), 404
    
    # Add participant
    participant = {
        "user_id": user_id,
        "joined_at": datetime.now().isoformat() + "Z",
        "audio_enabled": audio_enabled,
        "video_enabled": video_enabled if call['call_type'] == 'video' else False,
        "screen_sharing": False,
        "hand_raised": False,
        "role": "participant"
    }
    
    call['participants'].append(participant)
    call['current_participants'] = len(call['participants'])
    call['status'] = "active"
    
    return jsonify({
        "status": "success",
        "message": "Joined call successfully",
        "call": call,
        "participant_info": participant,
        "connection_info": {
            "server": "media-server-01.platform.com",
            "ice_servers": [
                {"urls": "stun:stun.platform.com:3478"},
                {"urls": "turn:turn.platform.com:3478", "username": "user", "credential": "pass"}
            ]
        }
    })

@communication_bp.route('/api/communication/calls/<call_id>/control', methods=['POST'])
def control_call(call_id):
    """
    Control call features (mute, video, screen share, etc.)
    """
    data = request.get_json()
    
    user_id = data.get('user_id')
    action = data.get('action')  # mute, unmute, video_on, video_off, screen_share, stop_screen_share, raise_hand, lower_hand
    
    call = VOICE_CALLS.get(call_id) or VIDEO_CALLS.get(call_id)
    if not call:
        return jsonify({"status": "error", "message": "Call not found"}), 404
    
    # Find participant
    participant = next((p for p in call['participants'] if p['user_id'] == user_id), None)
    if not participant:
        return jsonify({"status": "error", "message": "Not in call"}), 404
    
    # Handle action
    if action == "mute":
        participant['audio_enabled'] = False
    elif action == "unmute":
        participant['audio_enabled'] = True
    elif action == "video_on":
        participant['video_enabled'] = True
    elif action == "video_off":
        participant['video_enabled'] = False
    elif action == "screen_share":
        participant['screen_sharing'] = True
    elif action == "stop_screen_share":
        participant['screen_sharing'] = False
    elif action == "raise_hand":
        participant['hand_raised'] = True
    elif action == "lower_hand":
        participant['hand_raised'] = False
    
    return jsonify({
        "status": "success",
        "message": f"Action '{action}' completed",
        "participant": participant
    })

@communication_bp.route('/api/communication/files/upload', methods=['POST'])
def upload_file():
    """
    Upload file for sharing in chat
    """
    # In real implementation, this would handle actual file upload
    data = request.get_json()
    
    filename = data.get('filename', 'document.pdf')
    file_size = data.get('file_size', 1024000)
    file_type = data.get('file_type', 'application/pdf')
    room_id = data.get('room_id')
    
    file_id = f"file{int(time.time())}"
    file_info = {
        "file_id": file_id,
        "filename": filename,
        "file_type": file_type,
        "file_size": file_size,
        "url": f"/files/{file_id}/{filename}",
        "thumbnail": f"/thumbnails/{file_id}.jpg" if file_type.startswith('image') else None,
        "uploaded_at": datetime.now().isoformat() + "Z",
        "virus_scan_status": "clean",
        "download_count": 0
    }
    
    return jsonify({
        "status": "success",
        "message": "File uploaded successfully",
        "file": file_info
    })

@communication_bp.route('/api/communication/analytics/usage', methods=['GET'])
def get_communication_analytics():
    """
    Get communication platform usage analytics
    """
    user_id = request.args.get('user_id')
    timeframe = request.args.get('timeframe', '7d')
    
    analytics = {
        "overview": {
            "total_messages_sent": 1250,
            "total_messages_received": 2340,
            "active_conversations": 15,
            "voice_call_minutes": 450,
            "video_call_minutes": 320,
            "files_shared": 89
        },
        "activity_trends": {
            "daily_messages": [45, 67, 89, 123, 98, 76, 134],
            "peak_hours": [9, 11, 14, 16, 19],
            "most_active_rooms": [
                {"room_id": "room001", "name": "AI Development Team", "message_count": 456},
                {"room_id": "room002", "name": "Supply Chain Innovation", "message_count": 234}
            ]
        },
        "call_statistics": {
            "total_calls": 45,
            "average_call_duration": 25.5,
            "call_quality_rating": 4.7,
            "most_used_features": ["Screen Sharing", "Chat", "Recording"]
        },
        "collaboration_metrics": {
            "files_shared": 89,
            "screen_shares": 23,
            "reactions_used": 567,
            "mentions_received": 45
        }
    }
    
    return jsonify({
        "status": "success",
        "analytics": analytics,
        "timeframe": timeframe,
        "generated_at": datetime.now().isoformat()
    })


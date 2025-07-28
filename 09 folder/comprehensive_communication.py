"""
Comprehensive Communication API Routes
Provides endpoints for all communication services including voice, messaging, email, Bluetooth, and satellite
"""

from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional

from ..services.comprehensive_communication_service import (
    ComprehensiveCommunicationService,
    CommunicationMessage,
    VoiceCall,
    EmailMessage,
    CommunicationType,
    NetworkGeneration,
    MessageStatus,
    ProviderType
)

# Initialize communication service
communication_service = ComprehensiveCommunicationService()

communication_bp = Blueprint('communication', __name__)

def run_async(coro):
    """Helper to run async functions in Flask routes"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()

@communication_bp.route('/api/communication/send-message', methods=['POST'])
@cross_origin()
def send_message():
    """Send a message using various communication methods"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['sender_id', 'recipient_id', 'message_type', 'content']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Create message object
        message = CommunicationMessage(
            id=data.get('id', f"msg_{datetime.utcnow().timestamp()}"),
            sender_id=data['sender_id'],
            recipient_id=data['recipient_id'],
            message_type=CommunicationType(data['message_type']),
            content=data['content'],
            metadata=data.get('metadata', {}),
            network_generation=NetworkGeneration(data['network_generation']) if data.get('network_generation') else None
        )
        
        # Send message
        success = run_async(communication_service.send_message(message))
        
        if success:
            return jsonify({
                'message_id': message.id,
                'status': 'sent',
                'sent_at': message.sent_at.isoformat() if message.sent_at else None,
                'provider': message.provider.value if message.provider else None
            })
        else:
            return jsonify({
                'message_id': message.id,
                'status': 'failed',
                'error': 'Failed to send message'
            }), 500
            
    except ValueError as e:
        return jsonify({'error': f'Invalid value: {str(e)}'}), 400
    except Exception as e:
        logging.error(f"Error sending message: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@communication_bp.route('/api/communication/voice-call', methods=['POST'])
@cross_origin()
def initiate_voice_call():
    """Initiate a voice call"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['caller_id', 'callee_id', 'network_generation']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Create call object
        call = VoiceCall(
            id="",  # Will be generated
            caller_id=data['caller_id'],
            callee_id=data['callee_id'],
            call_type=data.get('call_type', 'voice'),
            network_generation=NetworkGeneration(data['network_generation'])
        )
        
        # Initiate call
        call_id = run_async(communication_service.initiate_voice_call(call))
        
        if call_id:
            return jsonify({
                'call_id': call_id,
                'status': 'connecting',
                'network_generation': call.network_generation.value,
                'started_at': call.started_at.isoformat() if call.started_at else None
            })
        else:
            return jsonify({
                'error': 'Failed to initiate call'
            }), 500
            
    except ValueError as e:
        return jsonify({'error': f'Invalid value: {str(e)}'}), 400
    except Exception as e:
        logging.error(f"Error initiating voice call: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@communication_bp.route('/api/communication/bluetooth/discover', methods=['POST'])
@cross_origin()
def discover_bluetooth_devices():
    """Discover nearby Bluetooth devices"""
    try:
        devices = run_async(communication_service.discover_bluetooth_devices())
        
        device_list = []
        for device in devices:
            device_list.append({
                'id': device.id,
                'name': device.name,
                'address': device.address,
                'device_class': device.device_class,
                'services': device.services,
                'is_paired': device.is_paired,
                'is_connected': device.is_connected,
                'last_seen': device.last_seen.isoformat() if device.last_seen else None
            })
        
        return jsonify({
            'devices': device_list,
            'total_discovered': len(device_list),
            'discovered_at': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logging.error(f"Error discovering Bluetooth devices: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@communication_bp.route('/api/communication/bluetooth/pair', methods=['POST'])
@cross_origin()
def pair_bluetooth_device():
    """Pair with a Bluetooth device"""
    try:
        data = request.get_json()
        
        if not data or 'device_id' not in data:
            return jsonify({'error': 'Device ID required'}), 400
        
        success = run_async(communication_service.pair_bluetooth_device(data['device_id']))
        
        if success:
            return jsonify({
                'device_id': data['device_id'],
                'status': 'paired',
                'paired_at': datetime.utcnow().isoformat()
            })
        else:
            return jsonify({
                'device_id': data['device_id'],
                'status': 'failed',
                'error': 'Failed to pair device'
            }), 500
            
    except Exception as e:
        logging.error(f"Error pairing Bluetooth device: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@communication_bp.route('/api/communication/bluetooth/connect', methods=['POST'])
@cross_origin()
def connect_bluetooth_device():
    """Connect to a paired Bluetooth device"""
    try:
        data = request.get_json()
        
        if not data or 'device_id' not in data:
            return jsonify({'error': 'Device ID required'}), 400
        
        profile = data.get('profile', 'A2DP')
        success = run_async(communication_service.connect_bluetooth_device(data['device_id'], profile))
        
        if success:
            return jsonify({
                'device_id': data['device_id'],
                'profile': profile,
                'status': 'connected',
                'connected_at': datetime.utcnow().isoformat()
            })
        else:
            return jsonify({
                'device_id': data['device_id'],
                'status': 'failed',
                'error': 'Failed to connect device'
            }), 500
            
    except Exception as e:
        logging.error(f"Error connecting Bluetooth device: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@communication_bp.route('/api/communication/satellite/send', methods=['POST'])
@cross_origin()
def send_satellite_message():
    """Send message via satellite communication"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['sender_id', 'recipient_id', 'content']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Create satellite message
        message = CommunicationMessage(
            id=f"sat_{datetime.utcnow().timestamp()}",
            sender_id=data['sender_id'],
            recipient_id=data['recipient_id'],
            message_type=CommunicationType.SATELLITE,
            content=data['content'],
            metadata=data.get('metadata', {})
        )
        
        provider = data.get('provider', 'iridium')
        success = run_async(communication_service.send_satellite_message(message, provider))
        
        if success:
            return jsonify({
                'message_id': message.id,
                'status': 'sent',
                'provider': provider,
                'sent_at': message.sent_at.isoformat() if message.sent_at else None,
                'metadata': message.metadata
            })
        else:
            return jsonify({
                'message_id': message.id,
                'status': 'failed',
                'error': 'Failed to send satellite message'
            }), 500
            
    except Exception as e:
        logging.error(f"Error sending satellite message: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@communication_bp.route('/api/communication/network-coverage', methods=['GET'])
@cross_origin()
def get_network_coverage():
    """Get network coverage information"""
    try:
        latitude = request.args.get('latitude', type=float)
        longitude = request.args.get('longitude', type=float)
        generation = request.args.get('generation', '4g')
        
        if latitude is None or longitude is None:
            return jsonify({'error': 'Latitude and longitude required'}), 400
        
        location = {'latitude': latitude, 'longitude': longitude}
        network_gen = NetworkGeneration(generation)
        
        coverage = run_async(communication_service.get_network_coverage(location, network_gen))
        
        return jsonify(coverage)
        
    except ValueError as e:
        return jsonify({'error': f'Invalid value: {str(e)}'}), 400
    except Exception as e:
        logging.error(f"Error getting network coverage: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@communication_bp.route('/api/communication/analytics/<user_id>', methods=['GET'])
@cross_origin()
def get_communication_analytics(user_id: str):
    """Get communication analytics for a user"""
    try:
        days = request.args.get('days', 30, type=int)
        
        analytics = run_async(communication_service.get_communication_analytics(user_id, days))
        
        return jsonify(analytics)
        
    except Exception as e:
        logging.error(f"Error getting communication analytics: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@communication_bp.route('/api/communication/providers/status', methods=['GET'])
@cross_origin()
def get_provider_status():
    """Get status of all communication providers"""
    try:
        status = run_async(communication_service.check_provider_status())
        
        return jsonify(status)
        
    except Exception as e:
        logging.error(f"Error getting provider status: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@communication_bp.route('/api/communication/capabilities/<generation>', methods=['GET'])
@cross_origin()
def get_network_capabilities(generation: str):
    """Get capabilities for a specific network generation"""
    try:
        network_gen = NetworkGeneration(generation)
        capabilities = communication_service.network_capabilities.get(network_gen, {})
        
        return jsonify({
            'generation': generation,
            'capabilities': capabilities,
            'description': f"Capabilities for {generation.upper()} network"
        })
        
    except ValueError as e:
        return jsonify({'error': f'Invalid network generation: {generation}'}), 400
    except Exception as e:
        logging.error(f"Error getting network capabilities: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@communication_bp.route('/api/communication/send-email', methods=['POST'])
@cross_origin()
def send_email():
    """Send email message"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['sender_email', 'recipient_email', 'subject', 'body']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Create email message
        message = CommunicationMessage(
            id=f"email_{datetime.utcnow().timestamp()}",
            sender_id=data['sender_email'],
            recipient_id=data['recipient_email'],
            message_type=CommunicationType.EMAIL,
            content=data['body'],
            metadata={
                'sender_email': data['sender_email'],
                'subject': data['subject'],
                'html_body': data.get('html_body'),
                'attachments': data.get('attachments', []),
                'cc_emails': data.get('cc_emails', []),
                'bcc_emails': data.get('bcc_emails', []),
                'priority': data.get('priority', 'normal'),
                'smtp_server': data.get('smtp_server'),
                'smtp_port': data.get('smtp_port'),
                'smtp_username': data.get('smtp_username'),
                'smtp_password': data.get('smtp_password')
            }
        )
        
        # Send email
        success = run_async(communication_service.send_message(message))
        
        if success:
            return jsonify({
                'message_id': message.id,
                'status': 'sent',
                'sent_at': message.sent_at.isoformat() if message.sent_at else None,
                'recipient': data['recipient_email'],
                'subject': data['subject']
            })
        else:
            return jsonify({
                'message_id': message.id,
                'status': 'failed',
                'error': 'Failed to send email'
            }), 500
            
    except Exception as e:
        logging.error(f"Error sending email: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@communication_bp.route('/api/communication/instant-message', methods=['POST'])
@cross_origin()
def send_instant_message():
    """Send instant message via WebSocket or messaging platform"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['sender_id', 'recipient_id', 'content']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Create instant message
        message = CommunicationMessage(
            id=f"im_{datetime.utcnow().timestamp()}",
            sender_id=data['sender_id'],
            recipient_id=data['recipient_id'],
            message_type=CommunicationType.INSTANT_MESSAGE,
            content=data['content'],
            metadata={
                'platform': data.get('platform', 'websocket'),
                'websocket_url': data.get('websocket_url'),
                'mqtt_broker': da
(Content truncated due to size limit. Use line ranges to read in chunks)
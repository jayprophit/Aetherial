from flask import Blueprint, request, jsonify
import datetime
import uuid
import base64

kyc_bp = Blueprint('kyc', __name__)

# KYC verification statuses
KYC_STATUSES = {
    'not_started': 'KYC verification not started',
    'in_progress': 'KYC verification in progress',
    'pending_review': 'Documents submitted, pending manual review',
    'approved': 'KYC verification approved',
    'rejected': 'KYC verification rejected',
    'expired': 'KYC verification expired, re-verification required'
}

# Document types for verification
DOCUMENT_TYPES = {
    'identity': {
        'passport': 'Passport',
        'drivers_license': 'Driver\'s License',
        'national_id': 'National ID Card',
        'residence_permit': 'Residence Permit'
    },
    'address': {
        'utility_bill': 'Utility Bill',
        'bank_statement': 'Bank Statement',
        'lease_agreement': 'Lease Agreement',
        'government_letter': 'Government Letter',
        'insurance_statement': 'Insurance Statement'
    },
    'business': {
        'incorporation_certificate': 'Certificate of Incorporation',
        'business_license': 'Business License',
        'tax_certificate': 'Tax Registration Certificate',
        'vat_certificate': 'VAT Registration Certificate',
        'memorandum': 'Memorandum of Association'
    },
    'financial': {
        'bank_verification': 'Bank Account Verification',
        'financial_statement': 'Financial Statement',
        'audit_report': 'Audit Report'
    }
}

@kyc_bp.route('/start', methods=['POST'])
def start_kyc():
    """Start KYC verification process"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        kyc_type = data.get('kyc_type', 'individual')  # individual or business
        
        if not user_id:
            return jsonify({'error': 'User ID is required'}), 400
        
        if kyc_type not in ['individual', 'business']:
            return jsonify({'error': 'Invalid KYC type'}), 400
        
        kyc_session = {
            'kyc_id': str(uuid.uuid4()),
            'user_id': user_id,
            'kyc_type': kyc_type,
            'status': 'in_progress',
            'started_at': datetime.datetime.utcnow().isoformat(),
            'steps_completed': [],
            'documents_uploaded': [],
            'verification_level': 'none',
            'estimated_completion': (datetime.datetime.utcnow() + datetime.timedelta(hours=24)).isoformat()
        }
        
        # Define required steps based on KYC type
        if kyc_type == 'individual':
            required_steps = [
                'personal_information',
                'identity_verification',
                'address_verification',
                'selfie_verification',
                'source_of_funds'
            ]
        else:  # business
            required_steps = [
                'business_information',
                'business_registration',
                'director_verification',
                'beneficial_ownership',
                'business_address',
                'financial_information'
            ]
        
        kyc_session['required_steps'] = required_steps
        kyc_session['current_step'] = required_steps[0]
        
        return jsonify({
            'message': 'KYC verification started',
            'kyc_session': kyc_session
        }), 201
        
    except Exception as e:
        return jsonify({'error': 'Failed to start KYC', 'details': str(e)}), 500

@kyc_bp.route('/submit-step', methods=['POST'])
def submit_kyc_step():
    """Submit a KYC verification step"""
    try:
        data = request.get_json()
        kyc_id = data.get('kyc_id')
        step_name = data.get('step_name')
        step_data = data.get('step_data', {})
        
        if not all([kyc_id, step_name]):
            return jsonify({'error': 'KYC ID and step name are required'}), 400
        
        # Validate step data based on step type
        validation_result = validate_step_data(step_name, step_data)
        if not validation_result['valid']:
            return jsonify({'error': validation_result['message']}), 400
        
        step_submission = {
            'step_id': str(uuid.uuid4()),
            'kyc_id': kyc_id,
            'step_name': step_name,
            'step_data': step_data,
            'submitted_at': datetime.datetime.utcnow().isoformat(),
            'status': 'submitted',
            'validation_score': validation_result.get('score', 0)
        }
        
        return jsonify({
            'message': 'Step submitted successfully',
            'step_submission': step_submission,
            'next_step': get_next_step(step_name)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to submit step', 'details': str(e)}), 500

@kyc_bp.route('/upload-document', methods=['POST'])
def upload_document():
    """Upload KYC verification document"""
    try:
        data = request.get_json()
        kyc_id = data.get('kyc_id')
        document_type = data.get('document_type')
        document_category = data.get('document_category')
        document_data = data.get('document_data')  # Base64 encoded
        document_name = data.get('document_name')
        
        if not all([kyc_id, document_type, document_category, document_data]):
            return jsonify({'error': 'All document fields are required'}), 400
        
        # Validate document type
        if document_category not in DOCUMENT_TYPES:
            return jsonify({'error': 'Invalid document category'}), 400
        
        if document_type not in DOCUMENT_TYPES[document_category]:
            return jsonify({'error': 'Invalid document type for category'}), 400
        
        # Simulate document processing
        document_analysis = analyze_document(document_data, document_type)
        
        document_record = {
            'document_id': str(uuid.uuid4()),
            'kyc_id': kyc_id,
            'document_type': document_type,
            'document_category': document_category,
            'document_name': document_name,
            'uploaded_at': datetime.datetime.utcnow().isoformat(),
            'file_size': len(document_data),
            'analysis_result': document_analysis,
            'verification_status': document_analysis['status']
        }
        
        return jsonify({
            'message': 'Document uploaded successfully',
            'document_record': document_record
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to upload document', 'details': str(e)}), 500

@kyc_bp.route('/status/<kyc_id>', methods=['GET'])
def get_kyc_status(kyc_id):
    """Get KYC verification status"""
    try:
        # In a real application, fetch from database
        # For demo, return mock data
        kyc_status = {
            'kyc_id': kyc_id,
            'status': 'pending_review',
            'kyc_type': 'individual',
            'progress_percentage': 85,
            'steps_completed': [
                'personal_information',
                'identity_verification',
                'address_verification',
                'selfie_verification'
            ],
            'current_step': 'source_of_funds',
            'documents_uploaded': [
                {
                    'type': 'passport',
                    'status': 'verified',
                    'uploaded_at': '2025-06-27T10:30:00Z'
                },
                {
                    'type': 'utility_bill',
                    'status': 'verified',
                    'uploaded_at': '2025-06-27T10:45:00Z'
                },
                {
                    'type': 'selfie',
                    'status': 'verified',
                    'uploaded_at': '2025-06-27T11:00:00Z'
                }
            ],
            'estimated_completion': '2025-06-28T12:00:00Z',
            'verification_level': 'kyc_individual',
            'rejection_reasons': [],
            'next_actions': [
                'Complete source of funds declaration',
                'Wait for final review'
            ]
        }
        
        return jsonify(kyc_status), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get KYC status', 'details': str(e)}), 500

@kyc_bp.route('/resubmit', methods=['POST'])
def resubmit_kyc():
    """Resubmit rejected KYC verification"""
    try:
        data = request.get_json()
        kyc_id = data.get('kyc_id')
        resubmission_notes = data.get('notes', '')
        
        if not kyc_id:
            return jsonify({'error': 'KYC ID is required'}), 400
        
        resubmission = {
            'resubmission_id': str(uuid.uuid4()),
            'kyc_id': kyc_id,
            'resubmitted_at': datetime.datetime.utcnow().isoformat(),
            'notes': resubmission_notes,
            'status': 'in_progress',
            'previous_rejection_addressed': True
        }
        
        return jsonify({
            'message': 'KYC resubmitted successfully',
            'resubmission': resubmission
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to resubmit KYC', 'details': str(e)}), 500

def validate_step_data(step_name, step_data):
    """Validate KYC step data"""
    validation_rules = {
        'personal_information': {
            'required_fields': ['first_name', 'last_name', 'date_of_birth', 'nationality'],
            'score_weight': 20
        },
        'business_information': {
            'required_fields': ['business_name', 'registration_number', 'business_type', 'incorporation_date'],
            'score_weight': 25
        },
        'identity_verification': {
            'required_fields': ['document_type', 'document_number', 'expiry_date'],
            'score_weight': 30
        },
        'address_verification': {
            'required_fields': ['street_address', 'city', 'postal_code', 'country'],
            'score_weight': 20
        }
    }
    
    if step_name not in validation_rules:
        return {'valid': False, 'message': 'Invalid step name'}
    
    rules = validation_rules[step_name]
    missing_fields = []
    
    for field in rules['required_fields']:
        if field not in step_data or not step_data[field]:
            missing_fields.append(field)
    
    if missing_fields:
        return {
            'valid': False,
            'message': f'Missing required fields: {", ".join(missing_fields)}'
        }
    
    return {
        'valid': True,
        'score': rules['score_weight'],
        'message': 'Step data validated successfully'
    }

def analyze_document(document_data, document_type):
    """Analyze uploaded document (mock implementation)"""
    # In a real implementation, this would use OCR and document verification services
    analysis = {
        'status': 'verified',
        'confidence_score': 0.95,
        'extracted_data': {
            'document_number': 'A12345678',
            'expiry_date': '2030-12-31',
            'name': 'John Doe',
            'date_of_birth': '1990-01-01'
        },
        'security_features': {
            'watermark_detected': True,
            'security_thread_detected': True,
            'hologram_detected': True
        },
        'quality_checks': {
            'image_quality': 'high',
            'text_clarity': 'excellent',
            'document_completeness': 'complete'
        },
        'fraud_indicators': [],
        'processing_time_ms': 1250
    }
    
    return analysis

def get_next_step(current_step):
    """Get the next step in KYC process"""
    individual_steps = [
        'personal_information',
        'identity_verification',
        'address_verification',
        'selfie_verification',
        'source_of_funds'
    ]
    
    business_steps = [
        'business_information',
        'business_registration',
        'director_verification',
        'beneficial_ownership',
        'business_address',
        'financial_information'
    ]
    
    # Determine which flow we're in
    if current_step in individual_steps:
        steps = individual_steps
    else:
        steps = business_steps
    
    try:
        current_index = steps.index(current_step)
        if current_index < len(steps) - 1:
            return steps[current_index + 1]
        else:
            return 'completed'
    except ValueError:
        return None

@kyc_bp.route('/document-types', methods=['GET'])
def get_document_types():
    """Get available document types for KYC"""
    return jsonify({
        'document_types': DOCUMENT_TYPES,
        'upload_requirements': {
            'max_file_size_mb': 10,
            'supported_formats': ['PDF', 'JPG', 'PNG'],
            'image_requirements': {
                'min_resolution': '300x300',
                'max_resolution': '4000x4000',
                'color_mode': 'RGB or Grayscale'
            }
        }
    }), 200


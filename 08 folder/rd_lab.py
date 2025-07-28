from flask import Blueprint, request, jsonify
import datetime
import uuid
import hashlib
import json

rd_lab_bp = Blueprint('rd_lab', __name__)

# Research categories and fields
RESEARCH_CATEGORIES = {
    'artificial_intelligence': {
        'name': 'Artificial Intelligence',
        'subcategories': ['Machine Learning', 'Deep Learning', 'Natural Language Processing', 'Computer Vision', 'Robotics']
    },
    'biotechnology': {
        'name': 'Biotechnology',
        'subcategories': ['Genetics', 'Bioengineering', 'Pharmaceuticals', 'Medical Devices', 'Bioinformatics']
    },
    'quantum_computing': {
        'name': 'Quantum Computing',
        'subcategories': ['Quantum Algorithms', 'Quantum Hardware', 'Quantum Cryptography', 'Quantum Simulation']
    },
    'renewable_energy': {
        'name': 'Renewable Energy',
        'subcategories': ['Solar Technology', 'Wind Energy', 'Energy Storage', 'Smart Grid', 'Fusion Energy']
    },
    'space_technology': {
        'name': 'Space Technology',
        'subcategories': ['Propulsion Systems', 'Satellite Technology', 'Space Materials', 'Life Support Systems']
    },
    'materials_science': {
        'name': 'Materials Science',
        'subcategories': ['Nanotechnology', 'Smart Materials', 'Composites', 'Semiconductors', 'Superconductors']
    },
    'environmental_science': {
        'name': 'Environmental Science',
        'subcategories': ['Climate Change', 'Pollution Control', 'Sustainability', 'Conservation', 'Green Chemistry']
    },
    'neuroscience': {
        'name': 'Neuroscience',
        'subcategories': ['Brain-Computer Interfaces', 'Neuroplasticity', 'Cognitive Science', 'Neurodegenerative Diseases']
    }
}

# Funding tiers and rewards
FUNDING_TIERS = {
    'seed': {
        'min_amount': 100,
        'max_amount': 5000,
        'duration_days': 30,
        'min_votes': 50,
        'approval_threshold': 60  # percentage
    },
    'development': {
        'min_amount': 5000,
        'max_amount': 50000,
        'duration_days': 60,
        'min_votes': 200,
        'approval_threshold': 65
    },
    'scale': {
        'min_amount': 50000,
        'max_amount': 500000,
        'duration_days': 90,
        'min_votes': 1000,
        'approval_threshold': 70
    },
    'breakthrough': {
        'min_amount': 500000,
        'max_amount': 5000000,
        'duration_days': 120,
        'min_votes': 5000,
        'approval_threshold': 75
    }
}

@rd_lab_bp.route('/submit-research', methods=['POST'])
def submit_research():
    """Submit new research project for community review"""
    try:
        data = request.get_json()
        
        # Required fields
        required_fields = ['title', 'abstract', 'category', 'funding_goal', 'researcher_id']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Validate category
        if data['category'] not in RESEARCH_CATEGORIES:
            return jsonify({'error': 'Invalid research category'}), 400
        
        # Determine funding tier
        funding_goal = float(data['funding_goal'])
        funding_tier = determine_funding_tier(funding_goal)
        
        if not funding_tier:
            return jsonify({'error': 'Funding goal outside acceptable range'}), 400
        
        # Create research project
        research_project = {
            'project_id': str(uuid.uuid4()),
            'title': data['title'],
            'abstract': data['abstract'],
            'category': data['category'],
            'subcategory': data.get('subcategory'),
            'researcher_id': data['researcher_id'],
            'researcher_name': data.get('researcher_name', 'Anonymous'),
            'institution': data.get('institution'),
            'funding_goal': funding_goal,
            'funding_tier': funding_tier,
            'current_funding': 0,
            'backers_count': 0,
            'status': 'under_review',
            'submission_date': datetime.datetime.utcnow().isoformat(),
            'review_deadline': (datetime.datetime.utcnow() + 
                              datetime.timedelta(days=FUNDING_TIERS[funding_tier]['duration_days'])).isoformat(),
            
            # Research details
            'methodology': data.get('methodology', ''),
            'expected_outcomes': data.get('expected_outcomes', ''),
            'timeline': data.get('timeline', ''),
            'budget_breakdown': data.get('budget_breakdown', {}),
            'team_members': data.get('team_members', []),
            'references': data.get('references', []),
            'attachments': data.get('attachments', []),
            
            # Voting and community metrics
            'votes': {
                'total_votes': 0,
                'upvotes': 0,
                'downvotes': 0,
                'approval_rating': 0,
                'community_score': 0
            },
            
            # Blockchain integration
            'blockchain_hash': generate_research_hash(data),
            'smart_contract_address': None,  # Will be set when funding starts
            'token_rewards': calculate_token_rewards(funding_goal, funding_tier)
        }
        
        return jsonify({
            'message': 'Research project submitted successfully',
            'project': research_project,
            'next_steps': [
                'Community review period started',
                f'Voting open for {FUNDING_TIERS[funding_tier]["duration_days"]} days',
                f'Minimum {FUNDING_TIERS[funding_tier]["min_votes"]} votes required',
                f'{FUNDING_TIERS[funding_tier]["approval_threshold"]}% approval needed for funding'
            ]
        }), 201
        
    except Exception as e:
        return jsonify({'error': 'Research submission failed', 'details': str(e)}), 500

@rd_lab_bp.route('/vote', methods=['POST'])
def vote_on_research():
    """Vote on research project using earned rewards"""
    try:
        data = request.get_json()
        
        required_fields = ['project_id', 'voter_id', 'vote_type', 'stake_amount']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        project_id = data['project_id']
        voter_id = data['voter_id']
        vote_type = data['vote_type']  # 'upvote', 'downvote'
        stake_amount = float(data['stake_amount'])
        reasoning = data.get('reasoning', '')
        
        if vote_type not in ['upvote', 'downvote']:
            return jsonify({'error': 'Invalid vote type'}), 400
        
        # Validate voter has sufficient tokens
        voter_balance = get_voter_token_balance(voter_id)
        if voter_balance < stake_amount:
            return jsonify({'error': 'Insufficient token balance'}), 400
        
        # Create vote record
        vote_record = {
            'vote_id': str(uuid.uuid4()),
            'project_id': project_id,
            'voter_id': voter_id,
            'vote_type': vote_type,
            'stake_amount': stake_amount,
            'reasoning': reasoning,
            'timestamp': datetime.datetime.utcnow().isoformat(),
            'voter_reputation': get_voter_reputation(voter_id),
            'weighted_vote_power': calculate_vote_weight(stake_amount, get_voter_reputation(voter_id)),
            'blockchain_tx_hash': generate_vote_hash(data)
        }
        
        # Update project voting metrics
        updated_metrics = update_project_votes(project_id, vote_record)
        
        return jsonify({
            'message': 'Vote recorded successfully',
            'vote_record': vote_record,
            'updated_project_metrics': updated_metrics,
            'voter_new_balance': voter_balance - stake_amount
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Voting failed', 'details': str(e)}), 500

@rd_lab_bp.route('/fund-project', methods=['POST'])
def fund_research_project():
    """Fund approved research project with digital assets"""
    try:
        data = request.get_json()
        
        required_fields = ['project_id', 'funder_id', 'funding_amount']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        project_id = data['project_id']
        funder_id = data['funder_id']
        funding_amount = float(data['funding_amount'])
        funding_type = data.get('funding_type', 'tokens')  # tokens, cryptocurrency, fiat
        
        # Validate project is approved for funding
        project_status = get_project_status(project_id)
        if project_status != 'approved_for_funding':
            return jsonify({'error': 'Project not approved for funding'}), 400
        
        # Validate funder has sufficient balance
        funder_balance = get_funder_balance(funder_id, funding_type)
        if funder_balance < funding_amount:
            return jsonify({'error': 'Insufficient balance'}), 400
        
        # Create funding record
        funding_record = {
            'funding_id': str(uuid.uuid4()),
            'project_id': project_id,
            'funder_id': funder_id,
            'funding_amount': funding_amount,
            'funding_type': funding_type,
            'timestamp': datetime.datetime.utcnow().isoformat(),
            'transaction_hash': generate_funding_hash(data),
            'smart_contract_address': get_project_contract_address(project_id),
            'milestone_release': data.get('milestone_release', False),
            'expected_returns': calculate_funding_returns(funding_amount, project_id)
        }
        
        # Update project funding
        updated_project = update_project_funding(project_id, funding_record)
        
        # Issue funder rewards/tokens
        funder_rewards = issue_funder_rewards(funder_id, funding_amount, project_id)
        
        return jsonify({
            'message': 'Funding successful',
            'funding_record': funding_record,
            'updated_project': updated_project,
            'funder_rewards': funder_rewards
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Funding failed', 'details': str(e)}), 500

@rd_lab_bp.route('/projects', methods=['GET'])
def get_research_projects():
    """Get list of research projects with filtering and sorting"""
    try:
        # Query parameters
        category = request.args.get('category')
        status = request.args.get('status')
        sort_by = request.args.get('sort_by', 'submission_date')
        order = request.args.get('order', 'desc')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        
        # Mock data - in real implementation, query database
        projects = generate_mock_projects()
        
        # Apply filters
        if category:
            projects = [p for p in projects if p['category'] == category]
        if status:
            projects = [p for p in projects if p['status'] == status]
        
        # Sort projects
        reverse = order == 'desc'
        if sort_by == 'funding_progress':
            projects.sort(key=lambda x: x['current_funding'] / x['funding_goal'], reverse=reverse)
        elif sort_by == 'community_score':
            projects.sort(key=lambda x: x['votes']['community_score'], reverse=reverse)
        else:
            projects.sort(key=lambda x: x.get(sort_by, ''), reverse=reverse)
        
        # Pagination
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_projects = projects[start_idx:end_idx]
        
        return jsonify({
            'projects': paginated_projects,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total_projects': len(projects),
                'total_pages': (len(projects) + per_page - 1) // per_page
            },
            'filters': {
                'categories': list(RESEARCH_CATEGORIES.keys()),
                'statuses': ['under_review', 'approved_for_funding', 'funded', 'in_progress', 'completed', 'rejected']
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get projects', 'details': str(e)}), 500

@rd_lab_bp.route('/project/<project_id>', methods=['GET'])
def get_project_details(project_id):
    """Get detailed information about a specific research project"""
    try:
        # Mock project details - in real implementation, fetch from database
        project = {
            'project_id': project_id,
            'title': 'Quantum-Enhanced Machine Learning for Drug Discovery',
            'abstract': 'This research aims to develop novel quantum machine learning algorithms to accelerate drug discovery processes by simulating molecular interactions at unprecedented scales.',
            'category': 'quantum_computing',
            'subcategory': 'Quantum Algorithms',
            'researcher_id': 'RES001',
            'researcher_name': 'Dr. Sarah Chen',
            'institution': 'MIT Quantum Research Lab',
            'funding_goal': 150000,
            'funding_tier': 'development',
            'current_funding': 87500,
            'backers_count': 234,
            'status': 'approved_for_funding',
            'submission_date': '2025-01-01T10:00:00Z',
            'review_deadline': '2025-03-01T23:59:59Z',
            
            # Detailed research information
            'methodology': 'We will implement variational quantum eigensolvers (VQE) combined with classical neural networks to create hybrid quantum-classical models for molecular property prediction.',
            'expected_outcomes': [
                '50% reduction in computational time for molecular simulations',
                'Novel quantum algorithms for drug-target interaction prediction',
                'Open-source quantum ML library for pharmaceutical research',
                'Publication in top-tier scientific journals'
            ],
            'timeline': {
                'phase_1': {'duration': '3 months', 'description': 'Algorithm development and initial testing'},
                'phase_2': {'duration': '4 months', 'description': 'Implementation and optimization'},
                'phase_3': {'duration': '3 months', 'description': 'Validation and publication'},
                'phase_4': {'duration': '2 months', 'description': 'Open-source release and documentation'}
            },
            'budget_breakdown': {
                'personnel': 90000,
                'equipment': 35000,
                'cloud_computing': 15000,
                'travel_conferences': 8000,
                'publication_fees': 2000
            },
            'team_members': [
                {'name': 'Dr. Sarah Chen', 'role': 'Principal Investigator', 'expertise': 'Quantum Computing'},
                {'name': 'Dr. Michael Rodriguez', 'role': 'Co-Investigator', 'expertise': 'Machine Learning'},
                {'name': 'Lisa Wang', 'role': 'PhD Student', 'expertise': 'Computational Chemistry'},
                {'name': 'James Thompson', 'role': 'Research Engineer', 'expertise': 'Software Development'}
            ],
            
            # Community engagement
            'votes': {
                'total_votes': 1247,
                'upvotes': 1089,
                'downvotes': 158,
                'approval_rating': 87.3,
                'community_score': 92.1
            },
            'comments': generate_mock_comments(),
            'updates': generate_mock_updates(),
            
            # Blockchain and tokenomics
            'blockchain_hash': 'QmX7Y8Z9...',
            'smart_contract_address': '0x742d35Cc6634C0532925a3b8D4C9db4C4b8b8b8b',
            'token_rewards': {
                'total_tokens': 15000,
(Content truncated due to size limit. Use line ranges to read in chunks)
from flask import Blueprint, request, jsonify
import datetime
import uuid
import hashlib
import random

consensus_rewards_bp = Blueprint('consensus_rewards', __name__)

# Consensus mechanisms and reward structures
CONSENSUS_TYPES = {
    'proof_of_work': {
        'name': 'Proof of Work',
        'description': 'Computational work for research validation',
        'base_reward': 10,
        'difficulty_adjustment': True,
        'energy_cost': 'high'
    },
    'proof_of_stake': {
        'name': 'Proof of Stake',
        'description': 'Stake tokens to validate research',
        'base_reward': 8,
        'minimum_stake': 100,
        'energy_cost': 'low'
    },
    'proof_of_research': {
        'name': 'Proof of Research',
        'description': 'Contribute research data or peer review',
        'base_reward': 15,
        'quality_multiplier': True,
        'energy_cost': 'minimal'
    },
    'proof_of_community': {
        'name': 'Proof of Community',
        'description': 'Community engagement and governance participation',
        'base_reward': 5,
        'engagement_multiplier': True,
        'energy_cost': 'minimal'
    }
}

# Reward categories and multipliers
REWARD_CATEGORIES = {
    'research_submission': {
        'base_reward': 100,
        'quality_bonus': [0, 25, 50, 100, 200],  # Based on peer review scores
        'innovation_bonus': [0, 50, 100, 250, 500],  # Based on novelty assessment
        'impact_bonus': [0, 30, 75, 150, 300]  # Based on potential impact
    },
    'peer_review': {
        'base_reward': 25,
        'thoroughness_bonus': [0, 10, 20, 40],  # Based on review quality
        'timeliness_bonus': [0, 5, 10, 15],  # Based on review speed
        'accuracy_bonus': [0, 15, 30, 50]  # Based on review accuracy vs consensus
    },
    'community_voting': {
        'base_reward': 2,
        'stake_multiplier': 0.1,  # Reward = base + (stake_amount * multiplier)
        'accuracy_bonus': [0, 5, 10, 20],  # Based on voting accuracy
        'early_voter_bonus': 3  # Bonus for early participation
    },
    'data_contribution': {
        'base_reward': 50,
        'data_quality_bonus': [0, 20, 40, 80, 160],  # Based on data validation
        'uniqueness_bonus': [0, 25, 50, 100],  # Based on data rarity
        'usage_bonus': 0.5  # Per use by other researchers
    },
    'funding_contribution': {
        'base_reward': 1,  # Per dollar funded
        'early_backer_bonus': 0.5,  # Additional per dollar for early backers
        'risk_bonus': [0, 0.2, 0.5, 1.0],  # Based on project risk level
        'loyalty_bonus': 0.1  # Per previous successful funding
    }
}

@consensus_rewards_bp.route('/participate-consensus', methods=['POST'])
def participate_in_consensus():
    """Participate in consensus mechanism to earn rewards"""
    try:
        data = request.get_json()
        
        required_fields = ['user_id', 'consensus_type', 'contribution_type']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        user_id = data['user_id']
        consensus_type = data['consensus_type']
        contribution_type = data['contribution_type']
        contribution_data = data.get('contribution_data', {})
        
        if consensus_type not in CONSENSUS_TYPES:
            return jsonify({'error': 'Invalid consensus type'}), 400
        
        # Process different types of consensus participation
        if consensus_type == 'proof_of_work':
            result = process_proof_of_work(user_id, contribution_data)
        elif consensus_type == 'proof_of_stake':
            result = process_proof_of_stake(user_id, contribution_data)
        elif consensus_type == 'proof_of_research':
            result = process_proof_of_research(user_id, contribution_type, contribution_data)
        elif consensus_type == 'proof_of_community':
            result = process_proof_of_community(user_id, contribution_type, contribution_data)
        
        # Record consensus participation
        participation_record = {
            'participation_id': str(uuid.uuid4()),
            'user_id': user_id,
            'consensus_type': consensus_type,
            'contribution_type': contribution_type,
            'contribution_data': contribution_data,
            'timestamp': datetime.datetime.utcnow().isoformat(),
            'rewards_earned': result['rewards'],
            'reputation_gained': result['reputation'],
            'blockchain_hash': generate_consensus_hash(data),
            'validation_status': result['status']
        }
        
        return jsonify({
            'message': 'Consensus participation recorded',
            'participation_record': participation_record,
            'user_stats': get_updated_user_stats(user_id, result)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Consensus participation failed', 'details': str(e)}), 500

@consensus_rewards_bp.route('/submit-research-data', methods=['POST'])
def submit_research_data():
    """Submit research data for community validation and rewards"""
    try:
        data = request.get_json()
        
        required_fields = ['user_id', 'data_type', 'data_content', 'research_field']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        user_id = data['user_id']
        data_type = data['data_type']  # dataset, code, methodology, results, analysis
        data_content = data['data_content']
        research_field = data['research_field']
        metadata = data.get('metadata', {})
        
        # Validate and process research data
        validation_result = validate_research_data(data_content, data_type, research_field)
        
        # Calculate rewards based on data quality and uniqueness
        rewards = calculate_data_contribution_rewards(validation_result, data_type, user_id)
        
        # Create data submission record
        submission_record = {
            'submission_id': str(uuid.uuid4()),
            'user_id': user_id,
            'data_type': data_type,
            'research_field': research_field,
            'data_hash': hashlib.sha256(str(data_content).encode()).hexdigest(),
            'metadata': metadata,
            'validation_score': validation_result['score'],
            'uniqueness_score': validation_result['uniqueness'],
            'quality_rating': validation_result['quality'],
            'rewards_earned': rewards['total_rewards'],
            'reputation_gained': rewards['reputation_points'],
            'submission_date': datetime.datetime.utcnow().isoformat(),
            'status': 'pending_community_review',
            'blockchain_hash': generate_data_hash(data)
        }
        
        return jsonify({
            'message': 'Research data submitted successfully',
            'submission_record': submission_record,
            'validation_result': validation_result,
            'rewards_breakdown': rewards
        }), 201
        
    except Exception as e:
        return jsonify({'error': 'Data submission failed', 'details': str(e)}), 500

@consensus_rewards_bp.route('/peer-review', methods=['POST'])
def submit_peer_review():
    """Submit peer review for research project or data"""
    try:
        data = request.get_json()
        
        required_fields = ['reviewer_id', 'target_id', 'target_type', 'review_content']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        reviewer_id = data['reviewer_id']
        target_id = data['target_id']  # project_id or data_submission_id
        target_type = data['target_type']  # 'research_project' or 'data_submission'
        review_content = data['review_content']
        
        # Validate reviewer qualifications
        reviewer_qualifications = get_reviewer_qualifications(reviewer_id)
        if not is_qualified_reviewer(reviewer_qualifications, target_type):
            return jsonify({'error': 'Insufficient qualifications for review'}), 400
        
        # Process peer review
        review_analysis = analyze_review_quality(review_content, target_type)
        rewards = calculate_peer_review_rewards(review_analysis, reviewer_qualifications)
        
        # Create review record
        review_record = {
            'review_id': str(uuid.uuid4()),
            'reviewer_id': reviewer_id,
            'target_id': target_id,
            'target_type': target_type,
            'review_content': review_content,
            'review_score': review_analysis['score'],
            'thoroughness_rating': review_analysis['thoroughness'],
            'constructiveness_rating': review_analysis['constructiveness'],
            'technical_accuracy': review_analysis['technical_accuracy'],
            'rewards_earned': rewards['total_rewards'],
            'reputation_gained': rewards['reputation_points'],
            'review_date': datetime.datetime.utcnow().isoformat(),
            'status': 'submitted',
            'blockchain_hash': generate_review_hash(data)
        }
        
        return jsonify({
            'message': 'Peer review submitted successfully',
            'review_record': review_record,
            'rewards_breakdown': rewards,
            'reviewer_stats': get_reviewer_stats(reviewer_id)
        }), 201
        
    except Exception as e:
        return jsonify({'error': 'Peer review submission failed', 'details': str(e)}), 500

@consensus_rewards_bp.route('/claim-rewards', methods=['POST'])
def claim_earned_rewards():
    """Claim accumulated rewards from various activities"""
    try:
        data = request.get_json()
        
        user_id = data.get('user_id')
        if not user_id:
            return jsonify({'error': 'User ID is required'}), 400
        
        # Get user's unclaimed rewards
        unclaimed_rewards = get_unclaimed_rewards(user_id)
        
        if unclaimed_rewards['total_amount'] == 0:
            return jsonify({'message': 'No rewards to claim', 'current_balance': get_user_balance(user_id)}), 200
        
        # Process reward claim
        claim_transaction = {
            'claim_id': str(uuid.uuid4()),
            'user_id': user_id,
            'claimed_amount': unclaimed_rewards['total_amount'],
            'reward_breakdown': unclaimed_rewards['breakdown'],
            'claim_date': datetime.datetime.utcnow().isoformat(),
            'transaction_hash': generate_claim_hash(user_id, unclaimed_rewards),
            'status': 'completed'
        }
        
        # Update user balance
        new_balance = update_user_balance(user_id, unclaimed_rewards['total_amount'])
        
        return jsonify({
            'message': 'Rewards claimed successfully',
            'claim_transaction': claim_transaction,
            'new_balance': new_balance,
            'next_claim_available': calculate_next_claim_time(user_id)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Reward claim failed', 'details': str(e)}), 500

@consensus_rewards_bp.route('/user-stats/<user_id>', methods=['GET'])
def get_user_consensus_stats(user_id):
    """Get user's consensus participation and reward statistics"""
    try:
        stats = {
            'user_id': user_id,
            'total_rewards_earned': 15847,
            'total_reputation': 2456,
            'current_balance': 8923,
            'participation_level': 'Expert Contributor',
            
            # Consensus participation
            'consensus_participation': {
                'proof_of_work': {
                    'participations': 45,
                    'rewards_earned': 4500,
                    'success_rate': 89.2,
                    'average_difficulty': 7.3
                },
                'proof_of_stake': {
                    'participations': 123,
                    'rewards_earned': 3690,
                    'total_staked': 12000,
                    'staking_efficiency': 92.1
                },
                'proof_of_research': {
                    'participations': 67,
                    'rewards_earned': 6234,
                    'data_contributions': 23,
                    'peer_reviews': 44,
                    'average_quality_score': 8.7
                },
                'proof_of_community': {
                    'participations': 234,
                    'rewards_earned': 1423,
                    'votes_cast': 189,
                    'governance_proposals': 12,
                    'community_score': 94.3
                }
            },
            
            # Activity breakdown
            'activity_breakdown': {
                'research_submissions': 8,
                'data_contributions': 23,
                'peer_reviews_completed': 44,
                'community_votes': 189,
                'funding_contributions': 15,
                'governance_participation': 12
            },
            
            # Achievements and badges
            'achievements': [
                {'badge': 'Research Pioneer', 'earned_date': '2024-11-15', 'description': 'First research submission'},
                {'badge': 'Data Validator', 'earned_date': '2024-12-01', 'description': '10+ data contributions'},
                {'badge': 'Peer Review Expert', 'earned_date': '2024-12-20', 'description': '25+ peer reviews'},
                {'badge': 'Community Leader', 'earned_date': '2025-01-05', 'description': 'Top 1% community participation'}
            ],
            
            # Performance metrics
            'performance_metrics': {
                'research_success_rate': 87.5,  # Percentage of successful research projects
                'review_accuracy': 91.2,  # Accuracy of peer reviews vs consensus
                'voting_accuracy': 84.7,  # Accuracy of community votes
                'data_quality_score': 8.9,  # Average quality of data contributions
                'community_impact_score': 94.3  # Overall community impact
            },
            
            # Rewards history (last 30 days)
            'recent_rewards': [
                {
                    'date': '2025-01-08',
                    'activity': 'Peer Review',
                    'target': 'Quantum ML Research',
                    'rewards': 45,
                    'reputation': 15
                },
                {
                    'date': '2025-01-07',
                    'activity': 'Data Contribution',
                    'target': 'Climate Dataset',
                    'rewards': 120,
                    'reputation': 25
                },
                {
                    'date': '2025-01-06',
                    'activity': 'Community Voting',
                    'target': 'Research Proposal #234',
                    'rewards': 8,
                    'reputation': 3
                }
            ]
        }
        
        return jsonify(stats), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get user stats', 'details': str(e)}), 500

@consensus_rewards_bp.route('/leaderboard/consensus', methods=['GET'])
def get_consensus_leaderboard():
    """Get leaderboard for consensus participation and rewards"""
    try:
        leaderboard_type = request.args.get('type', 'overall')  # overall, pow, pos, por, poc
        period = request.args.get('period', 'all_time')  # all_time, monthly, weekly
        
        leaderboard = {
            'leaderboard_type': leaderboard_type,
            'period': period,
            'updated_at': datetime.datetime.utcnow().isoformat(),
            
            'top_contributors': [
                {
                    'rank': 1,
                    'user_id': 'USER001',
                    'username': 'QuantumResearcher',
                    'total_rewards':
(Content truncated due to size limit. Use line ranges to read in chunks)
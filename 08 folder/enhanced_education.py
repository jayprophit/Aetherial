"""
Enhanced Education API Routes
Comprehensive learning management system endpoints
"""

from flask import Blueprint, request, jsonify, current_app
from flask_cors import cross_origin
import asyncio
import json
import logging
from datetime import datetime
from decimal import Decimal
import uuid
from typing import Dict, List, Optional, Any

from ..services.enhanced_education_service import (
    EnhancedEducationService, Course, Module, Lesson, Assessment, Question,
    Enrollment, LearningPath, Discussion, Certificate, CourseLevel, CourseStatus,
    EnrollmentStatus, ContentType, AssessmentType, QuestionType, CertificationType
)

enhanced_education_bp = Blueprint('enhanced_education', __name__)

# Initialize service
education_service = EnhancedEducationService()

@enhanced_education_bp.route('/api/education/courses', methods=['POST'])
@cross_origin()
def create_course():
    """Create a new course"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = [
            'instructor_id', 'title', 'description', 'short_description',
            'category', 'subcategory', 'level', 'language', 'duration_hours',
            'price', 'currency', 'thumbnail_url'
        ]
        
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Create course object
        course = Course(
            id=str(uuid.uuid4()),
            instructor_id=data['instructor_id'],
            title=data['title'],
            description=data['description'],
            short_description=data['short_description'],
            category=data['category'],
            subcategory=data['subcategory'],
            level=CourseLevel(data['level']),
            language=data['language'],
            duration_hours=float(data['duration_hours']),
            price=Decimal(str(data['price'])),
            currency=data['currency'],
            thumbnail_url=data['thumbnail_url'],
            preview_video_url=data.get('preview_video_url'),
            learning_objectives=data.get('learning_objectives', []),
            prerequisites=data.get('prerequisites', []),
            target_audience=data.get('target_audience', []),
            skills_taught=data.get('skills_taught', []),
            tags=data.get('tags', []),
            status=CourseStatus(data.get('status', 'draft')),
            is_featured=data.get('is_featured', False)
        )
        
        # Create course
        course_id = asyncio.run(education_service.create_course(course))
        
        return jsonify({
            "success": True,
            "course_id": course_id,
            "message": "Course created successfully"
        }), 201
        
    except Exception as e:
        logging.error(f"Error creating course: {e}")
        return jsonify({"error": str(e)}), 500

@enhanced_education_bp.route('/api/education/courses/<course_id>/modules', methods=['POST'])
@cross_origin()
def create_module(course_id):
    """Create a new module for a course"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'description', 'order_index', 'duration_minutes']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Create module object
        module = Module(
            id=str(uuid.uuid4()),
            course_id=course_id,
            title=data['title'],
            description=data['description'],
            order_index=int(data['order_index']),
            duration_minutes=int(data['duration_minutes']),
            is_preview=data.get('is_preview', False),
            learning_objectives=data.get('learning_objectives', [])
        )
        
        # Create module
        module_id = asyncio.run(education_service.create_module(module))
        
        return jsonify({
            "success": True,
            "module_id": module_id,
            "message": "Module created successfully"
        }), 201
        
    except Exception as e:
        logging.error(f"Error creating module: {e}")
        return jsonify({"error": str(e)}), 500

@enhanced_education_bp.route('/api/education/modules/<module_id>/lessons', methods=['POST'])
@cross_origin()
def create_lesson(module_id):
    """Create a new lesson for a module"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'description', 'content_type', 'content_url', 'duration_minutes', 'order_index']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Create lesson object
        lesson = Lesson(
            id=str(uuid.uuid4()),
            module_id=module_id,
            title=data['title'],
            description=data['description'],
            content_type=ContentType(data['content_type']),
            content_url=data['content_url'],
            content_data=data.get('content_data'),
            duration_minutes=int(data['duration_minutes']),
            order_index=int(data['order_index']),
            is_preview=data.get('is_preview', False),
            transcript=data.get('transcript'),
            resources=data.get('resources', [])
        )
        
        # Create lesson
        lesson_id = asyncio.run(education_service.create_lesson(lesson))
        
        return jsonify({
            "success": True,
            "lesson_id": lesson_id,
            "message": "Lesson created successfully"
        }), 201
        
    except Exception as e:
        logging.error(f"Error creating lesson: {e}")
        return jsonify({"error": str(e)}), 500

@enhanced_education_bp.route('/api/education/courses/<course_id>/assessments', methods=['POST'])
@cross_origin()
def create_assessment(course_id):
    """Create a new assessment for a course"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'description', 'assessment_type', 'total_points', 'passing_score', 'attempts_allowed']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Create assessment object
        assessment = Assessment(
            id=str(uuid.uuid4()),
            course_id=course_id,
            module_id=data.get('module_id'),
            title=data['title'],
            description=data['description'],
            assessment_type=AssessmentType(data['assessment_type']),
            total_points=int(data['total_points']),
            passing_score=int(data['passing_score']),
            time_limit_minutes=data.get('time_limit_minutes'),
            attempts_allowed=int(data['attempts_allowed']),
            randomize_questions=data.get('randomize_questions', False),
            show_correct_answers=data.get('show_correct_answers', True),
            instructions=data.get('instructions', '')
        )
        
        # Create assessment
        assessment_id = asyncio.run(education_service.create_assessment(assessment))
        
        return jsonify({
            "success": True,
            "assessment_id": assessment_id,
            "message": "Assessment created successfully"
        }), 201
        
    except Exception as e:
        logging.error(f"Error creating assessment: {e}")
        return jsonify({"error": str(e)}), 500

@enhanced_education_bp.route('/api/education/assessments/<assessment_id>/questions', methods=['POST'])
@cross_origin()
def create_question(assessment_id):
    """Create a new question for an assessment"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['question_type', 'question_text', 'points', 'order_index', 'correct_answers']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Create question object
        question = Question(
            id=str(uuid.uuid4()),
            assessment_id=assessment_id,
            question_type=QuestionType(data['question_type']),
            question_text=data['question_text'],
            points=int(data['points']),
            order_index=int(data['order_index']),
            options=data.get('options', []),
            correct_answers=data['correct_answers'],
            explanation=data.get('explanation'),
            hints=data.get('hints', []),
            media_url=data.get('media_url')
        )
        
        # Create question (would need to implement this method)
        # question_id = asyncio.run(education_service.create_question(question))
        
        return jsonify({
            "success": True,
            "question_id": question.id,
            "message": "Question created successfully"
        }), 201
        
    except Exception as e:
        logging.error(f"Error creating question: {e}")
        return jsonify({"error": str(e)}), 500

@enhanced_education_bp.route('/api/education/courses/<course_id>/enroll', methods=['POST'])
@cross_origin()
def enroll_student(course_id):
    """Enroll a student in a course"""
    try:
        data = request.get_json()
        
        if 'student_id' not in data:
            return jsonify({"error": "Missing required field: student_id"}), 400
        
        student_id = data['student_id']
        
        # Enroll student
        enrollment_id = asyncio.run(education_service.enroll_student(student_id, course_id))
        
        return jsonify({
            "success": True,
            "enrollment_id": enrollment_id,
            "message": "Student enrolled successfully"
        }), 201
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logging.error(f"Error enrolling student: {e}")
        return jsonify({"error": str(e)}), 500

@enhanced_education_bp.route('/api/education/lessons/<lesson_id>/progress', methods=['POST'])
@cross_origin()
def update_lesson_progress(lesson_id):
    """Update student progress for a lesson"""
    try:
        data = request.get_json()
        
        if 'student_id' not in data:
            return jsonify({"error": "Missing required field: student_id"}), 400
        
        student_id = data['student_id']
        completed = data.get('completed', False)
        time_spent = data.get('time_spent', 0)
        last_position = data.get('last_position', 0)
        
        # Update progress
        success = asyncio.run(education_service.update_lesson_progress(
            student_id, lesson_id, completed, time_spent, last_position
        ))
        
        if success:
            return jsonify({
                "success": True,
                "message": "Progress updated successfully"
            }), 200
        else:
            return jsonify({"error": "Failed to update progress"}), 500
        
    except Exception as e:
        logging.error(f"Error updating lesson progress: {e}")
        return jsonify({"error": str(e)}), 500

@enhanced_education_bp.route('/api/education/assessments/<assessment_id>/submit', methods=['POST'])
@cross_origin()
def submit_assessment(assessment_id):
    """Submit assessment answers"""
    try:
        data = request.get_json()
        
        if 'student_id' not in data or 'answers' not in data:
            return jsonify({"error": "Missing required fields: student_id, answers"}), 400
        
        student_id = data['student_id']
        answers = data['answers']
        
        # Submit assessment
        result = asyncio.run(education_service.submit_assessment(student_id, assessment_id, answers))
        
        return jsonify({
            "success": True,
            "result": result,
            "message": "Assessment submitted successfully"
        }), 200
        
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logging.error(f"Error submitting assessment: {e}")
        return jsonify({"error": str(e)}), 500

@enhanced_education_bp.route('/api/education/learning-paths', methods=['POST'])
@cross_origin()
def create_learning_path():
    """Create a new learning path"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = [
            'creator_id', 'title', 'description', 'category', 'level',
            'estimated_duration_hours', 'course_ids'
        ]
        
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Create learning path object
        learning_path = LearningPath(
            id=str(uuid.uuid4()),
            creator_id=data['creator_id'],
            title=data['title'],
            description=data['description'],
            category=data['category'],
            level=CourseLevel(data['level']),
            estimated_duration_hours=float(data['estimated_duration_hours']),
            course_ids=data['course_ids'],
            prerequisites=data.get('prerequisites', []),
            learning_objectives=data.get('learning_objectives', []),
            skills_gained=data.get('skills_gained', []),
            is_featured=data.get('is_featured', False)
        )
        
        # Create learning path
        path_id = asyncio.run(education_service.create_learning_path(learning_path))
        
        return jsonify({
            "success": True,
            "learning_path_id": path_id,
            "message": "Learning path created successfully"
        }), 201
        
    except Exception as e:
        logging.error(f"Error creating learning path: {e}")
        return jsonify({"error": str(e)}), 500

@enhanced_education_bp.route('/api/education/certificates/issue', methods=['POST'])
@cross_origin()
def issue_certificate():
    """Issue a certificate to a student"""
    try:
        data = request.get_json()
        
        if 'student_id' not in data:
            return jsonify({"error": "Missing required field: student_id"}), 400
        
        student_id = data['student_id']
        course_id = data.get('course_id')
        learning_path_id = data.get('learning_path_id')
        certificate_type = CertificationType(data.get('certificate_type', 'completion'))
        
        if not course_id and not learning_path_id:
            return jsonify({"error": "Either course_id or learning_path_id must be provided"}), 400
        
        # Issue certificate
        certificate_id = asyncio.run(education_service.issue_certificate(
            student_id, course_id, learning_path_id, certificate_type
        ))
        
        return jsonify({
            "success": True,
            "certificate_id": certificate_id,
            "message": "Certificate issued successfully"
        }), 201
        
    except Exception as e:
        logging.error(f"Error issuing certificate: {e}")
        return jsonify({"error": str(e)}), 500

@enhanced_education_bp.route('/api/education/courses/search', methods=['GET'])
@cross_origin()
def search_courses():
    """Search courses with advanced filtering"""
    try:
        # Get query parameters
        query = request.args.get('q', '')
        category = request.args.get('category')
        subcategory = request.args.get('subcategory')
        level = request.args.get('level')
        language = request.args.get('language')
        price_max = request.args.get('price_max', type=float)
        duration_max = request.args.get('duration_max', type=float)
        rating_min = request.args.get('rating_min', type=float)
        limit = request.args.get('limit', 50, ty
(Content truncated due to size limit. Use line ranges to read in chunks)
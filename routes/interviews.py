from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from models import db
from models.user import User
from models.career import Career
from models.interview import InterviewQuestion, InterviewAttempt
from models.notification import Notification
from routes.auth import login_required, get_current_user
from services.ai_service import evaluate_interview_answer

interviews_bp = Blueprint('interviews', __name__)

@interviews_bp.route('/interviews')
@login_required
def index():
    user = get_current_user()
    category = request.args.get('category', 'Technical')
    role_tag = request.args.get('role_tag')

    query = InterviewQuestion.query
    if category != 'All':
        query = query.filter_by(category=category)
    if role_tag:
        query = query.filter_by(role_tag=role_tag)

    questions = query.all()
    user_attempts = InterviewAttempt.query.filter_by(user_id=user.id).order_by(InterviewAttempt.created_at.desc()).all()
    
    # Calculate stats
    total_attempts = len(user_attempts)
    avg_score = int(round(sum(a.score for a in user_attempts) / total_attempts)) if total_attempts > 0 else 0

    return render_template(
        'interviews.html',
        user=user,
        questions=questions,
        user_attempts=user_attempts,
        total_attempts=total_attempts,
        avg_score=avg_score,
        active_category=category,
        active_role=role_tag
    )


@interviews_bp.route('/api/interviews/submit-answer', methods=['POST'])
@login_required
def submit_answer():
    user = get_current_user()
    data = request.get_json() or {}
    question_id = data.get('question_id')
    user_answer = data.get('answer', '').strip()

    if not question_id or not user_answer:
        return jsonify({'success': False, 'message': 'Question ID and answer text are required.'}), 400

    question = InterviewQuestion.query.get_or_404(question_id)

    # Evaluate answer using transparent evaluation rubric
    eval_result = evaluate_interview_answer(question.question, user_answer, question.category)

    # Persist attempt to database
    attempt = InterviewAttempt(
        user_id=user.id,
        question_id=question.id,
        user_answer=user_answer,
        score=eval_result['score'],
        feedback=eval_result['feedback']
    )
    attempt.criteria_breakdown = eval_result['criteria']
    db.session.add(attempt)

    # Add notification for high performance
    if eval_result['score'] >= 80:
        notif = Notification(
            user_id=user.id,
            title="Great Mock Interview Score!",
            message=f"You achieved {eval_result['score']}% on: '{question.question[:50]}...'",
            notification_type="success",
            link="/interviews"
        )
        db.session.add(notif)

    db.session.commit()

    return jsonify({
        'success': True,
        'score': eval_result['score'],
        'feedback': eval_result['feedback'],
        'criteria': eval_result['criteria'],
        'disclaimer': eval_result['disclaimer'],
        'sample_answer': question.sample_answer,
        'explanation': question.explanation
    })


@interviews_bp.route('/api/interviews/check-quiz', methods=['POST'])
@login_required
def check_quiz():
    data = request.get_json() or {}
    question_id = data.get('question_id')
    selected_option = data.get('selected_option', '').strip()

    question = InterviewQuestion.query.get_or_404(question_id)
    is_correct = (selected_option.lower() == (question.correct_answer or '').lower())

    return jsonify({
        'success': True,
        'is_correct': is_correct,
        'correct_answer': question.correct_answer,
        'explanation': question.explanation
    })

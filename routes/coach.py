from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from models.user import User
from routes.auth import login_required, get_current_user
from services.ai_service import ask_career_coach, get_ai_status

coach_bp = Blueprint('coach', __name__)

@coach_bp.route('/coach')
@login_required
def index():
    user = get_current_user()
    status = get_ai_status()
    
    suggested_prompts = [
        "Which career suits my current skills?",
        "What should I learn next?",
        "Suggest a beginner project for my career goal.",
        "Help me prepare for a Data Science interview.",
        "Review my learning roadmap."
    ]

    return render_template(
        'coach.html',
        user=user,
        ai_status=status,
        suggested_prompts=suggested_prompts
    )


@coach_bp.route('/api/coach/ask', methods=['POST'])
@login_required
def ask():
    user = get_current_user()
    data = request.get_json() or {}
    message = data.get('message', '').strip()
    history = data.get('history', [])

    if not message:
        return jsonify({'success': False, 'message': 'Message cannot be empty.'}), 400

    response_data = ask_career_coach(message, user, history)

    return jsonify({
        'success': True,
        'reply': response_data['reply'],
        'source': response_data['source'],
        'mode': response_data['mode']
    })

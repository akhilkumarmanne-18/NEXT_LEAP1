from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from models import db
from models.career import Career
from models.user import User
from routes.auth import login_required, get_current_user
from services.career_engine import calculate_career_matches, compare_two_careers
from services.roadmap_engine import generate_personalized_roadmap

careers_bp = Blueprint('careers', __name__)

@careers_bp.route('/careers')
@login_required
def index():
    user = get_current_user()
    user_skills = user.skills.all()
    user_profile = {
        'interests': user.interests,
        'education_level': user.education_level,
        'current_course': user.current_course,
        'learning_style': user.learning_style
    }

    # Match careers based on profile and skills
    matches = calculate_career_matches(user_profile, user_skills)
    all_careers = Career.query.all()

    return render_template(
        'careers.html',
        user=user,
        matches=matches,
        careers=all_careers,
        target_career_id=user.target_career_id
    )


@careers_bp.route('/careers/<slug>')
@login_required
def detail(slug):
    user = get_current_user()
    career = Career.query.filter_by(slug=slug).first_or_404()
    user_skills = user.skills.all()
    user_skill_names = {s.skill_name.lower().strip() for s in user_skills}

    # Check which skills user has vs lacks
    skills_status = []
    for cs in career.skills_required:
        has_skill = cs.skill_name.lower().strip() in user_skill_names
        skills_status.append({
            'skill': cs,
            'acquired': has_skill
        })

    is_target = (user.target_career_id == career.id) or (user.preferred_career_goal == career.title)

    return render_template(
        'career_detail.html',
        user=user,
        career=career,
        skills_status=skills_status,
        is_target=is_target
    )


@careers_bp.route('/api/careers/set-target/<int:career_id>', methods=['POST'])
@login_required
def set_target_career(career_id):
    user = get_current_user()
    career = Career.query.get_or_404(career_id)

    user.target_career_id = career.id
    user.preferred_career_goal = career.title
    db.session.commit()

    # Automatically generate or activate corresponding personalized roadmap!
    generate_personalized_roadmap(user, career)

    return jsonify({
        'success': True,
        'message': f"Target career successfully set to {career.title}! Your roadmap has been calibrated.",
        'career_title': career.title
    })


@careers_bp.route('/api/careers/compare', methods=['GET'])
@login_required
def compare():
    id1 = request.args.get('c1', type=int)
    id2 = request.args.get('c2', type=int)
    if not id1 or not id2:
        return jsonify({'success': False, 'message': 'Two career IDs required for comparison'}), 400

    user = get_current_user()
    comparison_data = compare_two_careers(id1, id2, user.skills.all())
    if not comparison_data:
        return jsonify({'success': False, 'message': 'Careers not found'}), 404

    return jsonify({'success': True, 'data': comparison_data})


@careers_bp.route('/api/careers/discovery-quiz', methods=['POST'])
@login_required
def discovery_quiz():
    user = get_current_user()
    data = request.get_json() or {}

    interests = data.get('interests', '')
    course = data.get('course', '')
    style = data.get('learning_style', '')
    skills_input = data.get('skills', [])

    temp_profile = {
        'interests': interests,
        'current_course': course,
        'learning_style': style
    }

    # Format skills
    temp_skills = []
    for s in skills_input:
        temp_skills.append({'skill_name': s, 'proficiency': 'Intermediate'})

    matches = calculate_career_matches(temp_profile, temp_skills)
    return jsonify({'success': True, 'matches': matches})

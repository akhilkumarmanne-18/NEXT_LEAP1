from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from models import db
from models.user import User
from models.career import Career
from models.skill import Skill, UserSkill
from routes.auth import login_required, get_current_user
from services.skill_gap_engine import analyze_skill_gap

skills_bp = Blueprint('skills', __name__)

@skills_bp.route('/skill-gap')
@login_required
def index():
    user = get_current_user()
    all_careers = Career.query.all()
    
    # Selected career from query parameter or default to user target career
    selected_career_id = request.args.get('career_id', type=int)
    target_career = None
    if selected_career_id:
        target_career = Career.query.get(selected_career_id)
    if not target_career and user.target_career_id:
        target_career = Career.query.get(user.target_career_id)
    if not target_career and user.preferred_career_goal:
        target_career = Career.query.filter(Career.title.ilike(f"%{user.preferred_career_goal}%")).first()
    if not target_career:
        target_career = Career.query.first()

    user_skills = user.skills.all()
    gap_result = analyze_skill_gap(target_career, user_skills)
    catalog_skills = Skill.query.order_by(Skill.name).all()

    return render_template(
        'skill_gap.html',
        user=user,
        careers=all_careers,
        selected_career=target_career,
        gap=gap_result,
        catalog_skills=catalog_skills,
        user_skills=user_skills
    )


@skills_bp.route('/api/skills/add', methods=['POST'])
@login_required
def add_skill():
    user = get_current_user()
    data = request.get_json() or {}
    skill_name = data.get('skill_name', '').strip()
    proficiency = data.get('proficiency', 'Beginner')
    category = data.get('category', 'Technical')
    notes = data.get('notes', '')

    if not skill_name:
        return jsonify({'success': False, 'message': 'Skill name is required'}), 400

    # Check if already present
    existing = UserSkill.query.filter_by(user_id=user.id, skill_name=skill_name).first()
    if existing:
        existing.proficiency = proficiency
        existing.category = category
        if notes:
            existing.notes = notes
        db.session.commit()
        return jsonify({
            'success': True,
            'message': f"Updated {skill_name} proficiency to {proficiency}.",
            'skill': existing.to_dict()
        })

    new_skill = UserSkill(
        user_id=user.id,
        skill_name=skill_name,
        category=category,
        proficiency=proficiency,
        notes=notes
    )
    db.session.add(new_skill)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': f"Added {skill_name} ({proficiency}) to your skills.",
        'skill': new_skill.to_dict()
    })


@skills_bp.route('/api/skills/update/<int:skill_id>', methods=['POST'])
@login_required
def update_skill(skill_id):
    user = get_current_user()
    skill = UserSkill.query.filter_by(id=skill_id, user_id=user.id).first()
    if not skill:
        return jsonify({'success': False, 'message': 'Skill not found'}), 404

    data = request.get_json() or {}
    if 'proficiency' in data:
        skill.proficiency = data['proficiency']
    if 'notes' in data:
        skill.notes = data['notes']

    db.session.commit()
    return jsonify({
        'success': True,
        'message': f"Proficiency updated to {skill.proficiency}.",
        'skill': skill.to_dict()
    })


@skills_bp.route('/api/skills/delete/<int:skill_id>', methods=['POST', 'DELETE'])
@login_required
def delete_skill(skill_id):
    user = get_current_user()
    skill = UserSkill.query.filter_by(id=skill_id, user_id=user.id).first()
    if not skill:
        return jsonify({'success': False, 'message': 'Skill not found'}), 404

    skill_name = skill.skill_name
    db.session.delete(skill)
    db.session.commit()
    return jsonify({
        'success': True,
        'message': f"Removed {skill_name} from your profile."
    })


@skills_bp.route('/api/skills/gap-data', methods=['GET'])
@login_required
def get_gap_data():
    user = get_current_user()
    career_id = request.args.get('career_id', type=int)
    career = Career.query.get(career_id) if career_id else None
    if not career and user.target_career_id:
        career = Career.query.get(user.target_career_id)

    gap = analyze_skill_gap(career, user.skills.all())
    return jsonify({'success': True, 'gap': gap})

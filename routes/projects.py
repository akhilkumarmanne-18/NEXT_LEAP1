from datetime import datetime
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from models import db
from models.user import User
from models.career import Career
from models.project import Project, UserProject
from models.notification import Notification
from routes.auth import login_required, get_current_user

projects_bp = Blueprint('projects', __name__)

@projects_bp.route('/projects')
@login_required
def index():
    user = get_current_user()
    difficulty = request.args.get('difficulty')
    category = request.args.get('category')
    
    query = Project.query
    if difficulty:
        query = query.filter_by(difficulty=difficulty)
    if category:
        query = query.filter_by(category=category)

    catalog_projects = query.all()
    user_projects = user.projects.all()
    user_project_map = {up.project_id: up for up in user_projects if up.project_id}

    return render_template(
        'projects.html',
        user=user,
        catalog_projects=catalog_projects,
        user_projects=user_projects,
        user_project_map=user_project_map,
        active_difficulty=difficulty,
        active_category=category
    )


@projects_bp.route('/portfolio')
@login_required
def portfolio():
    user = get_current_user()
    # Portfolio projects are those where in_portfolio is True or status is Completed
    portfolio_projects = UserProject.query.filter_by(user_id=user.id, in_portfolio=True).all()
    user_skills = user.skills.all()

    return render_template(
        'portfolio.html',
        user=user,
        portfolio_projects=portfolio_projects,
        user_skills=user_skills
    )


@projects_bp.route('/api/projects/start/<int:project_id>', methods=['POST'])
@login_required
def start_project(project_id):
    user = get_current_user()
    project = Project.query.get_or_404(project_id)

    # Check if already started
    existing = UserProject.query.filter_by(user_id=user.id, project_id=project.id).first()
    if existing:
        return jsonify({
            'success': True,
            'message': 'Project is already active in your studio.',
            'user_project': existing.to_dict()
        })

    up = UserProject(
        user_id=user.id,
        project_id=project.id,
        status="In Progress",
        progress_percent=10,
        notes="Started project from catalog."
    )
    db.session.add(up)

    notif = Notification(
        user_id=user.id,
        title="Project Started!",
        message=f"You started working on '{project.title}'. Happy building!",
        notification_type="info",
        link="/projects"
    )
    db.session.add(notif)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': f"Started '{project.title}'! Track your progress below.",
        'user_project': up.to_dict()
    })


@projects_bp.route('/api/projects/update/<int:user_project_id>', methods=['POST'])
@login_required
def update_user_project(user_project_id):
    user = get_current_user()
    up = UserProject.query.filter_by(id=user_project_id, user_id=user.id).first_or_404()

    data = request.get_json() or {}
    if 'progress_percent' in data:
        up.progress_percent = max(0, min(100, int(data['progress_percent'])))
        if up.progress_percent == 100 and up.status != 'Completed':
            up.status = 'Completed'
            up.completed_at = datetime.utcnow()
            up.in_portfolio = True
    if 'status' in data:
        up.status = data['status']
        if up.status == 'Completed':
            up.progress_percent = 100
            up.completed_at = datetime.utcnow()
            up.in_portfolio = True
    if 'notes' in data:
        up.notes = data['notes']
    if 'repo_url' in data:
        up.repo_url = data['repo_url']
    if 'live_url' in data:
        up.live_url = data['live_url']
    if 'in_portfolio' in data:
        up.in_portfolio = bool(data['in_portfolio'])

    db.session.commit()
    return jsonify({
        'success': True,
        'message': 'Project details saved.',
        'user_project': up.to_dict()
    })


@projects_bp.route('/api/projects/toggle-portfolio/<int:user_project_id>', methods=['POST'])
@login_required
def toggle_portfolio(user_project_id):
    user = get_current_user()
    up = UserProject.query.filter_by(id=user_project_id, user_id=user.id).first_or_404()
    
    up.in_portfolio = not up.in_portfolio
    db.session.commit()

    status_str = "added to" if up.in_portfolio else "removed from"
    return jsonify({
        'success': True,
        'in_portfolio': up.in_portfolio,
        'message': f"Project {status_str} your public portfolio."
    })

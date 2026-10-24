from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from models import db
from models.user import User
from models.career import Career
from models.roadmap import Roadmap, RoadmapTask
from models.project import Project, UserProject
from models.interview import InterviewAttempt
from models.notification import Notification
from routes.auth import login_required, get_current_user
from services.skill_gap_engine import analyze_skill_gap
from services.next_action_engine import determine_next_action, complete_next_action

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def index():
    user = get_current_user()
    if not user:
        return redirect(url_for('auth.login'))

    # Retrieve target career
    target_career = None
    if user.target_career_id:
        target_career = Career.query.get(user.target_career_id)
    if not target_career and user.preferred_career_goal:
        target_career = Career.query.filter(Career.title.ilike(f"%{user.preferred_career_goal}%")).first()
    if not target_career:
        target_career = Career.query.first()

    # Skills count and skill gap
    user_skills = user.skills.all()
    skills_count = len(user_skills)
    skill_gap_result = analyze_skill_gap(target_career, user_skills)

    # Active roadmap and progress
    active_roadmap = Roadmap.query.filter_by(user_id=user.id, is_active=True).first()
    roadmap_progress = active_roadmap.progress_percent if active_roadmap else 0

    # Projects completed
    user_projects = user.projects.all()
    completed_projects_count = sum(1 for p in user_projects if p.status == 'Completed')

    # Signature Feature: Your Next LEAP Action
    next_action = determine_next_action(user)

    # Upcoming roadmap tasks
    upcoming_tasks = []
    if active_roadmap:
        for phase in active_roadmap.phases:
            for task in phase.tasks:
                if task.status in ['Pending', 'In Progress']:
                    upcoming_tasks.append(task)
                if len(upcoming_tasks) >= 4:
                    break
            if len(upcoming_tasks) >= 4:
                break

    # Recommended projects from catalog
    recommended_projects = Project.query.filter(
        (Project.career_id == (target_career.id if target_career else None)) | (Project.career_id == None)
    ).limit(3).all()

    # Recent activities (completed tasks, interview attempts, project updates)
    recent_activities = []
    # Fetch recent completed tasks
    if active_roadmap:
        for phase in active_roadmap.phases:
            for task in phase.tasks:
                if task.status == 'Completed' and task.completed_at:
                    recent_activities.append({
                        'title': f"Completed Task: {task.title}",
                        'category': 'Roadmap',
                        'timestamp': task.completed_at.strftime("%b %d, %H:%M"),
                        'icon': 'check-circle'
                    })
    # Fetch recent interview attempts
    recent_attempts = InterviewAttempt.query.filter_by(user_id=user.id).order_by(InterviewAttempt.created_at.desc()).limit(3).all()
    for att in recent_attempts:
        recent_activities.append({
            'title': f"Interview Practice: Scored {att.score}%",
            'category': 'Interview',
            'timestamp': att.created_at.strftime("%b %d, %H:%M") if att.created_at else "Recently",
            'icon': 'award'
        })
    # Sort activities by timestamp desc (or limit to 4)
    recent_activities = recent_activities[:4]

    # Weekly learning data for Chart.js
    weekly_hours_target = user.weekly_hours or 12
    weekly_data = {
        'days': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        'actual_hours': [1.5, 2.0, 1.0, 2.5, 3.0, 2.0, 1.5],
        'target_hours': [weekly_hours_target / 7] * 7
    }

    # Unread notifications
    notifications = Notification.query.filter_by(user_id=user.id, is_read=False).order_by(Notification.created_at.desc()).all()

    return render_template(
        'dashboard.html',
        user=user,
        target_career=target_career,
        skills_count=skills_count,
        roadmap_progress=roadmap_progress,
        completed_projects_count=completed_projects_count,
        skill_gap=skill_gap_result,
        next_action=next_action,
        upcoming_tasks=upcoming_tasks,
        recommended_projects=recommended_projects,
        recent_activities=recent_activities,
        weekly_data=weekly_data,
        notifications=notifications
    )


@dashboard_bp.route('/api/next-action/complete', methods=['POST'])
@login_required
def api_complete_next_action():
    user = get_current_user()
    data = request.get_json() or {}
    action_id = data.get('action_id')
    
    if not action_id:
        return jsonify({'success': False, 'message': 'Missing action ID'}), 400

    success, message = complete_next_action(user, action_id)
    # Recalculate next action immediately
    new_action = determine_next_action(user)

    return jsonify({
        'success': success,
        'message': message,
        'next_action': new_action
    })


@dashboard_bp.route('/api/notifications/mark-read/<int:notif_id>', methods=['POST'])
@login_required
def mark_notification_read(notif_id):
    user = get_current_user()
    notif = Notification.query.filter_by(id=notif_id, user_id=user.id).first()
    if notif:
        notif.is_read = True
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'Notification not found'}), 404

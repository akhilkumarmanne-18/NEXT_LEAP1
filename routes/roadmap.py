from datetime import datetime
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from models import db
from models.user import User
from models.career import Career
from models.roadmap import Roadmap, RoadmapPhase, RoadmapTask
from models.notification import Notification
from routes.auth import login_required, get_current_user
from services.roadmap_engine import generate_personalized_roadmap

roadmap_bp = Blueprint('roadmap', __name__)

@roadmap_bp.route('/roadmap')
@login_required
def index():
    user = get_current_user()
    
    # Active roadmap
    active_roadmap = Roadmap.query.filter_by(user_id=user.id, is_active=True).first()
    
    # If no active roadmap, generate one based on target career
    if not active_roadmap:
        target_career = None
        if user.target_career_id:
            target_career = Career.query.get(user.target_career_id)
        if not target_career and user.preferred_career_goal:
            target_career = Career.query.filter(Career.title.ilike(f"%{user.preferred_career_goal}%")).first()
        if not target_career:
            target_career = Career.query.first()

        if target_career:
            active_roadmap = generate_personalized_roadmap(user, target_career)

    all_careers = Career.query.all()

    return render_template(
        'roadmap.html',
        user=user,
        roadmap=active_roadmap,
        careers=all_careers
    )


@roadmap_bp.route('/api/roadmap/task/toggle/<int:task_id>', methods=['POST'])
@login_required
def toggle_task(task_id):
    user = get_current_user()
    task = RoadmapTask.query.get_or_404(task_id)
    
    # Verify task ownership through phase -> roadmap -> user
    if task.phase.roadmap.user_id != user.id:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403

    if task.status == 'Completed':
        task.status = 'Pending'
        task.completed_at = None
    else:
        task.status = 'Completed'
        task.completed_at = datetime.utcnow()
        # Add notification for celebration
        notif = Notification(
            user_id=user.id,
            title="Milestone Completed!",
            message=f"You marked '{task.title}' as completed. Keep up the great momentum!",
            notification_type="success",
            link="/roadmap"
        )
        db.session.add(notif)

    db.session.commit()

    roadmap = task.phase.roadmap
    return jsonify({
        'success': True,
        'task_id': task.id,
        'new_status': task.status,
        'phase_progress': task.phase.progress_percent,
        'roadmap_progress': roadmap.progress_percent,
        'completed_tasks': roadmap.completed_tasks,
        'total_tasks': roadmap.total_tasks
    })


@roadmap_bp.route('/api/roadmap/task/add', methods=['POST'])
@login_required
def add_custom_task():
    user = get_current_user()
    data = request.get_json() or {}
    phase_id = data.get('phase_id')
    title = data.get('title', '').strip()
    description = data.get('description', '').strip()
    skills_involved = data.get('skills_involved', '').strip()
    estimated_hours = data.get('estimated_hours', 5)
    target_date = data.get('target_date', '')

    if not title or not phase_id:
        return jsonify({'success': False, 'message': 'Title and Phase are required'}), 400

    phase = RoadmapPhase.query.get_or_404(phase_id)
    if phase.roadmap.user_id != user.id:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403

    new_task = RoadmapTask(
        phase_id=phase.id,
        title=title,
        description=description,
        skills_involved=skills_involved,
        estimated_hours=int(estimated_hours),
        target_date=target_date or "Flexible",
        status='Pending',
        is_custom=True,
        order_index=len(phase.tasks) + 1
    )
    db.session.add(new_task)
    db.session.commit()

    roadmap = phase.roadmap
    return jsonify({
        'success': True,
        'message': f"Added custom task: '{title}'",
        'task': new_task.to_dict(),
        'roadmap_progress': roadmap.progress_percent
    })


@roadmap_bp.route('/api/roadmap/task/delete/<int:task_id>', methods=['POST', 'DELETE'])
@login_required
def delete_task(task_id):
    user = get_current_user()
    task = RoadmapTask.query.get_or_404(task_id)
    if task.phase.roadmap.user_id != user.id:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403

    roadmap = task.phase.roadmap
    db.session.delete(task)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Task removed.',
        'roadmap_progress': roadmap.progress_percent
    })


@roadmap_bp.route('/api/roadmap/regenerate', methods=['POST'])
@login_required
def regenerate_roadmap():
    user = get_current_user()
    data = request.get_json() or {}
    career_id = data.get('career_id') or user.target_career_id
    
    career = Career.query.get(career_id) if career_id else Career.query.first()
    if not career:
        return jsonify({'success': False, 'message': 'Career not found'}), 404

    # Delete existing roadmaps for this user
    Roadmap.query.filter_by(user_id=user.id).delete()
    db.session.commit()

    # Generate fresh personalized roadmap
    new_roadmap = generate_personalized_roadmap(user, career)
    return jsonify({
        'success': True,
        'message': f"New personalized roadmap created for {career.title}!",
        'roadmap': new_roadmap.to_dict()
    })

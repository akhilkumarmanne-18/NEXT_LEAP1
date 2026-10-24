import os
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from models import db
from models.user import User
from models.career import Career
from models.skill import UserSkill
from routes.auth import login_required, get_current_user
from services.seed_service import seed_database
from services.ai_service import get_ai_status

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = get_current_user()
    careers = Career.query.all()
    user_skills = user.skills.all()

    if request.method == 'POST':
        user.full_name = request.form.get('full_name', user.full_name).strip()
        user.education_level = request.form.get('education_level', user.education_level)
        user.current_course = request.form.get('current_course', user.current_course).strip()
        user.interests = request.form.get('interests', user.interests).strip()
        user.preferred_career_goal = request.form.get('preferred_career_goal', user.preferred_career_goal)
        
        target_cid = request.form.get('target_career_id', type=int)
        if target_cid:
            user.target_career_id = target_cid

        user.learning_style = request.form.get('learning_style', user.learning_style)
        user.weekly_hours = request.form.get('weekly_hours', type=int) or user.weekly_hours
        user.bio = request.form.get('bio', user.bio)
        user.github_url = request.form.get('github_url', user.github_url)
        user.linkedin_url = request.form.get('linkedin_url', user.linkedin_url)
        user.portfolio_url = request.form.get('portfolio_url', user.portfolio_url)

        db.session.commit()
        flash("Your profile information has been successfully updated.", "success")
        return redirect(url_for('profile.profile'))

    return render_template('profile.html', user=user, careers=careers, user_skills=user_skills)


@profile_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    user = get_current_user()
    status = get_ai_status()

    if request.method == 'POST':
        theme = request.form.get('theme', 'dark')
        user.theme_preference = theme
        db.session.commit()
        flash("Theme and platform preferences updated.", "success")
        return redirect(url_for('profile.settings'))

    return render_template('settings.html', user=user, ai_status=status)


@profile_bp.route('/api/settings/theme', methods=['POST'])
@login_required
def toggle_theme():
    user = get_current_user()
    data = request.get_json() or {}
    new_theme = data.get('theme', 'dark')
    if new_theme in ['dark', 'light']:
        user.theme_preference = new_theme
        db.session.commit()
        return jsonify({'success': True, 'theme': new_theme})
    return jsonify({'success': False, 'message': 'Invalid theme'}), 400


@profile_bp.route('/api/settings/reset-demo', methods=['POST'])
@login_required
def reset_demo():
    """Resets the demo environment and repopulates clean Data Science sample data."""
    try:
        from models.roadmap import Roadmap
        from models.project import UserProject
        from models.interview import InterviewAttempt
        from models.notification import Notification

        user = get_current_user()
        
        # Clear user's transactional data
        Roadmap.query.filter_by(user_id=user.id).delete()
        UserProject.query.filter_by(user_id=user.id).delete()
        UserSkill.query.filter_by(user_id=user.id).delete()
        InterviewAttempt.query.filter_by(user_id=user.id).delete()
        Notification.query.filter_by(user_id=user.id).delete()
        db.session.commit()

        # Re-populate demo data for this user
        ds_career = Career.query.filter_by(slug='data-scientist').first()
        if ds_career:
            user.target_career_id = ds_career.id
            user.preferred_career_goal = ds_career.title

        demo_skills = [
            ("Python", "Programming", "Intermediate", True, "Comfortable with Pandas, NumPy, and OOP scripts."),
            ("Statistics", "Mathematics", "Beginner", False, "Studying probability distributions and hypothesis testing."),
            ("Data Visualization", "Data", "Beginner", False, "Created basic charts in Matplotlib and Seaborn."),
            ("Problem Solving", "Soft Skills", "Intermediate", True, "Solved 120+ algorithmic challenges.")
        ]
        for s_name, s_cat, s_prof, s_ver, s_notes in demo_skills:
            us = UserSkill(
                user_id=user.id,
                skill_name=s_name,
                category=s_cat,
                proficiency=s_prof,
                is_verified=s_ver,
                notes=s_notes
            )
            db.session.add(us)

        from services.roadmap_engine import generate_personalized_roadmap
        if ds_career:
            generate_personalized_roadmap(user, ds_career)

        from models.project import Project
        sample_proj_1 = Project.query.filter_by(slug="customer-churn-prediction").first()
        if sample_proj_1:
            up1 = UserProject(
                user_id=user.id,
                project_id=sample_proj_1.id,
                status="Completed",
                progress_percent=100,
                notes="Implemented Random Forest and XGBoost with 84% ROC-AUC score. Published Streamlit interactive demo.",
                repo_url="https://github.com/alexchen-demo/customer-churn-predictor",
                live_url="https://customer-churn-demo.streamlit.app",
                in_portfolio=True
            )
            db.session.add(up1)

        db.session.commit()
        return jsonify({'success': True, 'message': 'Demo dataset has been restored successfully!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

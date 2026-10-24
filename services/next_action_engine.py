from models import db
from models.career import Career
from models.roadmap import Roadmap, RoadmapTask
from models.project import UserProject
from models.interview import InterviewAttempt
from models.notification import Notification
from services.skill_gap_engine import analyze_skill_gap

def determine_next_action(user):
    """
    Determines the single most impactful 'Next LEAP' action for the user.
    Uses deterministic priority rules based on:
    - Career goal & skill gaps
    - Active roadmap tasks
    - Active projects
    - Interview preparedness
    """
    if not user:
        return None

    # Find target career
    target_career = None
    if user.target_career_id:
        target_career = Career.query.get(user.target_career_id)
    if not target_career and user.preferred_career_goal:
        target_career = Career.query.filter(Career.title.ilike(f"%{user.preferred_career_goal}%")).first()
    if not target_career:
        target_career = Career.query.first()

    if not target_career:
        return {
            'id': 'action_choose_career',
            'title': 'Discover and select your target career goal',
            'reason': 'Defining your target career allows NEXT LEAP to formulate your personalized skill map and learning path.',
            'category': 'Career Direction',
            'priority': 'Urgent',
            'estimated_effort': '10 mins',
            'cta_url': '/careers',
            'cta_label': 'Explore Careers',
            'badge': 'Step 1'
        }

    # 1. Skill Gap Analysis
    user_skills = user.skills.all()
    gap_data = analyze_skill_gap(target_career, user_skills)
    missing_urgent = [s for s in gap_data['missing_skills'] if s['priority'] in ['Urgent', 'High']]
    level_up_urgent = [s for s in gap_data['level_up_skills'] if s['priority'] == 'High']

    # 2. Roadmap inspection
    active_roadmap = Roadmap.query.filter_by(user_id=user.id, is_active=True).first()
    earliest_pending_task = None
    if active_roadmap:
        for phase in active_roadmap.phases:
            for task in phase.tasks:
                if task.status in ['Pending', 'In Progress']:
                    earliest_pending_task = task
                    break
            if earliest_pending_task:
                break

    # 3. Project in-progress inspection
    active_project = UserProject.query.filter_by(user_id=user.id, status='In Progress').first()

    # 4. Interview preparation inspection
    interview_count = InterviewAttempt.query.filter_by(user_id=user.id).count()

    # DECISION MATRIX:
    # Rule 1: If there is an active roadmap task matching an urgent missing skill, recommend that!
    if earliest_pending_task and missing_urgent:
        top_missing = missing_urgent[0]['name'].lower()
        if top_missing in (earliest_pending_task.skills_involved.lower() + " " + earliest_pending_task.title.lower()):
            return {
                'id': f'task_{earliest_pending_task.id}',
                'task_id': earliest_pending_task.id,
                'title': earliest_pending_task.title,
                'reason': f"This directly addresses {missing_urgent[0]['name']}, an essential requirement for your target goal of {target_career.title}.",
                'category': 'Roadmap Milestone',
                'priority': 'High Priority',
                'estimated_effort': f"{earliest_pending_task.estimated_hours} hours",
                'cta_url': '/roadmap',
                'cta_label': 'Open in Roadmap',
                'badge': 'High Impact',
                'target_career': target_career.title,
                'related_skill': missing_urgent[0]['name']
            }

    # Rule 2: If there's an urgent missing skill with high weight (e.g. SQL for Data Scientist)
    if missing_urgent:
        top_skill = missing_urgent[0]
        return {
            'id': f'skill_gap_{top_skill["name"].lower().replace(" ", "_")}',
            'title': f"Master {top_skill['name']} Fundamentals & Practical Exercises",
            'reason': f"{top_skill['name']} is rated as {top_skill['importance']} for {target_career.title}. {top_skill['why']}",
            'category': 'Skill Gap',
            'priority': 'Urgent',
            'estimated_effort': '45 mins',
            'cta_url': '/skill-gap',
            'cta_label': 'Review Skill Gap',
            'badge': 'Critical Gap',
            'target_career': target_career.title,
            'related_skill': top_skill['name']
        }

    # Rule 3: If user has a project in progress with good momentum, finish it!
    if active_project:
        return {
            'id': f'project_{active_project.id}',
            'project_id': active_project.id,
            'title': f"Continue Milestone: {active_project.display_title}",
            'reason': f"Your project is currently at {active_project.progress_percent}% progress. Completing and publishing this project significantly boosts your portfolio credibility.",
            'category': 'Project Studio',
            'priority': 'High Priority',
            'estimated_effort': '1.5 hours',
            'cta_url': '/projects',
            'cta_label': 'Go to Project Studio',
            'badge': 'Portfolio Builder',
            'target_career': target_career.title
        }

    # Rule 4: If roadmap task is available
    if earliest_pending_task:
        return {
            'id': f'task_{earliest_pending_task.id}',
            'task_id': earliest_pending_task.id,
            'title': earliest_pending_task.title,
            'reason': f"Next sequential step in your {active_roadmap.title}. {earliest_pending_task.description}",
            'category': 'Curriculum',
            'priority': 'Recommended',
            'estimated_effort': f"{earliest_pending_task.estimated_hours} hours",
            'cta_url': '/roadmap',
            'cta_label': 'Continue Learning',
            'badge': 'Next Milestone',
            'target_career': target_career.title
        }

    # Rule 5: If skills are mostly ready (> 65% readiness) but few interview attempts, prepare for interviews!
    if gap_data['readiness_score'] >= 60 and interview_count < 3:
        return {
            'id': 'action_mock_interview',
            'title': f"Take a Mock Technical Interview for {target_career.title}",
            'reason': f"Your skill readiness is strong at {gap_data['readiness_score']}%. Validating your technical articulation in mock questions will solidify your job readiness.",
            'category': 'Interview Readiness',
            'priority': 'Recommended',
            'estimated_effort': '20 mins',
            'cta_url': '/interviews',
            'cta_label': 'Start Mock Interview',
            'badge': 'Interview Prep',
            'target_career': target_career.title
        }

    # Default fallback: level-up skill or explore advanced project
    return {
        'id': 'action_general_advance',
        'title': f"Deepen Technical Portfolio for {target_career.title}",
        'reason': "Explore advanced projects and sharpen your competitive advantage with hands-on development.",
        'category': 'Skill Polish',
        'priority': 'Recommended',
        'estimated_effort': '1 hour',
        'cta_url': '/projects',
        'cta_label': 'View Projects',
        'badge': 'Level Up',
        'target_career': target_career.title
    }


def complete_next_action(user, action_id):
    """
    Marks the corresponding action as completed and updates application state.
    """
    if not user:
        return False, "User not found"

    # If it's a roadmap task
    if action_id.startswith('task_'):
        task_id = int(action_id.split('_')[1])
        task = RoadmapTask.query.get(task_id)
        if task and task.phase.roadmap.user_id == user.id:
            from datetime import datetime
            task.status = 'Completed'
            task.completed_at = datetime.utcnow()
            
            notif = Notification(
                user_id=user.id,
                title="Next LEAP Action Completed!",
                message=f"Great job finishing: '{task.title}'. Your roadmap and readiness have updated.",
                notification_type="success",
                link="/roadmap"
            )
            db.session.add(notif)
            db.session.commit()
            return True, "Action completed and roadmap updated."

    # If it's a skill gap action
    if action_id.startswith('skill_gap_'):
        skill_clean = action_id.replace('skill_gap_', '').replace('_', ' ').title()
        # Add or update user skill
        from models.skill import UserSkill
        existing_skill = UserSkill.query.filter_by(user_id=user.id, skill_name=skill_clean).first()
        if existing_skill:
            existing_skill.proficiency = 'Intermediate'
        else:
            new_skill = UserSkill(
                user_id=user.id,
                skill_name=skill_clean,
                proficiency='Intermediate',
                notes="Completed via Next LEAP signature action"
            )
            db.session.add(new_skill)

        notif = Notification(
            user_id=user.id,
            title="Skill Upgraded!",
            message=f"You updated proficiency in {skill_clean} to Intermediate. Skill gap score recalculated.",
            notification_type="success",
            link="/skill-gap"
        )
        db.session.add(notif)
        db.session.commit()
        return True, f"Skill {skill_clean} updated to Intermediate."

    # Generic completion notification
    notif = Notification(
        user_id=user.id,
        title="Action Milestone Reached!",
        message="You successfully completed your scheduled Next LEAP recommendation.",
        notification_type="success",
        link="/dashboard"
    )
    db.session.add(notif)
    db.session.commit()
    return True, "Action completed successfully."

from models.career import Career, CareerSkill

def analyze_skill_gap(target_career, user_skills):
    """
    Performs comprehensive skill gap analysis for a user against a target career.
    target_career: Career instance
    user_skills: list of UserSkill instances
    """
    if not target_career:
        return None

    # Map user skills: name_lower -> UserSkill
    user_skill_map = {}
    for us in user_skills:
        user_skill_map[us.skill_name.lower().strip()] = us

    required_skills = target_career.skills_required
    total_skills = len(required_skills)
    
    prof_rank = {'Beginner': 1, 'Intermediate': 2, 'Advanced': 3}

    acquired_skills = []
    level_up_skills = []
    missing_skills = []
    
    total_target_points = 0
    total_earned_points = 0

    for req in required_skills:
        req_norm = req.skill_name.lower().strip()
        min_rank = prof_rank.get(req.minimum_proficiency, 2)
        weight = req.weight or 5
        target_pts = min_rank * weight
        total_target_points += target_pts

        if req_norm in user_skill_map:
            us = user_skill_map[req_norm]
            user_rank = prof_rank.get(us.proficiency, 1)
            earned_pts = min(min_rank, user_rank) * weight
            total_earned_points += earned_pts

            gap_level = min_rank - user_rank
            if gap_level <= 0:
                acquired_skills.append({
                    'name': req.skill_name,
                    'user_proficiency': us.proficiency,
                    'required_proficiency': req.minimum_proficiency,
                    'importance': req.importance_level,
                    'status': 'Mastered',
                    'why': req.why_recommended
                })
            else:
                level_up_skills.append({
                    'name': req.skill_name,
                    'user_proficiency': us.proficiency,
                    'required_proficiency': req.minimum_proficiency,
                    'gap_steps': gap_level,
                    'importance': req.importance_level,
                    'priority': 'High' if req.importance_level == 'Required' else 'Medium',
                    'status': 'Level-Up Needed',
                    'why': req.why_recommended,
                    'action': f"Advance {req.skill_name} from {us.proficiency} to {req.minimum_proficiency}"
                })
        else:
            priority = 'Urgent' if req.importance_level == 'Required' and req.weight >= 8 else (
                'High' if req.importance_level == 'Required' else 'Medium'
            )
            missing_skills.append({
                'name': req.skill_name,
                'user_proficiency': 'None',
                'required_proficiency': req.minimum_proficiency,
                'importance': req.importance_level,
                'priority': priority,
                'status': 'Missing',
                'weight': weight,
                'why': req.why_recommended,
                'action': f"Learn {req.skill_name} fundamentals and reach {req.minimum_proficiency} level"
            })

    # Sort missing skills by priority/weight
    missing_skills.sort(key=lambda x: (0 if x['priority'] == 'Urgent' else (1 if x['priority'] == 'High' else 2), -x['weight']))

    readiness_score = int(round((total_earned_points / (total_target_points or 1)) * 100))
    readiness_score = min(100, max(5, readiness_score))

    # Prepare chart data for Chart.js radar / bar
    labels = []
    user_data = []
    target_data = []

    for req in required_skills:
        labels.append(req.skill_name)
        req_norm = req.skill_name.lower().strip()
        target_val = prof_rank.get(req.minimum_proficiency, 2)
        target_data.append(target_val)
        
        if req_norm in user_skill_map:
            user_data.append(prof_rank.get(user_skill_map[req_norm].proficiency, 1))
        else:
            user_data.append(0)

    # Readiness level descriptor
    if readiness_score >= 80:
        readiness_badge = "Job-Ready Candidate"
        readiness_desc = "Strong foundation! Focus on portfolio polishing and mock interviews."
    elif readiness_score >= 50:
        readiness_badge = "Intermediate Bridge"
        readiness_desc = "Solid core skills. Close key high-priority technical gaps to achieve market readiness."
    else:
        readiness_badge = "Early Explorer"
        readiness_desc = "Great starting point. Follow your customized roadmap to build core competencies systematically."

    return {
        'target_career': target_career.to_dict(),
        'readiness_score': readiness_score,
        'readiness_badge': readiness_badge,
        'readiness_desc': readiness_desc,
        'total_required': total_skills,
        'mastered_count': len(acquired_skills),
        'level_up_count': len(level_up_skills),
        'missing_count': len(missing_skills),
        'acquired_skills': acquired_skills,
        'level_up_skills': level_up_skills,
        'missing_skills': missing_skills,
        'chart': {
            'labels': labels,
            'user_data': user_data,
            'target_data': target_data
        }
    }

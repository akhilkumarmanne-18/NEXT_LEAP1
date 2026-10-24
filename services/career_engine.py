import re
from models.career import Career, CareerSkill

def calculate_career_matches(user_profile, user_skills):
    """
    Computes match percentages for all careers against the user's profile and skills.
    user_profile: dict with interests, education_level, current_course, learning_style, work_style
    user_skills: list of dicts or UserSkill objects with skill_name, proficiency
    """
    all_careers = Career.query.all()
    user_skill_dict = {}
    for s in user_skills:
        name = s.skill_name.lower().strip() if hasattr(s, 'skill_name') else s.get('skill_name', '').lower().strip()
        prof = s.proficiency if hasattr(s, 'proficiency') else s.get('proficiency', 'Beginner')
        user_skill_dict[name] = prof

    user_interests_str = (user_profile.get('interests') or '').lower()
    user_course_str = (user_profile.get('current_course') or '').lower()
    
    results = []

    for career in all_careers:
        required_skills = career.skills_required
        total_weight = sum(cs.weight for cs in required_skills) or 1
        skill_score = 0
        matched_skills = []
        missing_skills = []

        for cs in required_skills:
            c_skill_norm = cs.skill_name.lower().strip()
            if c_skill_norm in user_skill_dict:
                user_prof = user_skill_dict[c_skill_norm]
                # Compare proficiency
                prof_multipliers = {'Beginner': 0.6, 'Intermediate': 0.85, 'Advanced': 1.0}
                mult = prof_multipliers.get(user_prof, 0.6)
                earned = cs.weight * mult
                skill_score += earned
                matched_skills.append({
                    'name': cs.skill_name,
                    'user_proficiency': user_prof,
                    'required_proficiency': cs.minimum_proficiency,
                    'importance': cs.importance_level
                })
            else:
                missing_skills.append({
                    'name': cs.skill_name,
                    'importance': cs.importance_level,
                    'why': cs.why_recommended
                })

        skill_match_pct = (skill_score / total_weight) * 100

        # Interest & Course Alignment Score (0-100)
        interest_score = 50  # baseline
        career_keywords = [
            career.title.lower(),
            career.category.lower(),
            career.slug.lower()
        ]
        # Check title/category words in interests
        for kw in career_keywords:
            if kw in user_interests_str or kw in user_course_str:
                interest_score += 25
        
        # Check skill overlap in interests
        for cs in required_skills:
            if cs.skill_name.lower() in user_interests_str:
                interest_score += 8
        interest_score = min(100, interest_score)

        # Weighted final score: 65% skill overlap, 35% interests & background
        overall_match = int(round((0.65 * skill_match_pct) + (0.35 * interest_score)))
        overall_match = max(15, min(98, overall_match))  # Realistic bounds

        results.append({
            'career': career.to_dict(),
            'match_score': overall_match,
            'skill_match_pct': int(round(skill_match_pct)),
            'interest_score': int(round(interest_score)),
            'matched_skills_count': len(matched_skills),
            'total_skills_count': len(required_skills),
            'matched_skills': matched_skills,
            'missing_skills': missing_skills[:4],
            'recommendation_tag': 'Top Match' if overall_match >= 75 else ('Good Fit' if overall_match >= 55 else 'Growth Path')
        })

    # Sort descending by match score
    results.sort(key=lambda x: x['match_score'], reverse=True)
    return results


def compare_two_careers(career_id_1, career_id_2, user_skills):
    """
    Detailed side-by-side comparison of two careers for the user.
    """
    c1 = Career.query.get(career_id_1)
    c2 = Career.query.get(career_id_2)
    if not c1 or not c2:
        return None

    user_skill_names = {s.skill_name.lower().strip() for s in user_skills}

    def build_summary(c):
        req = c.skills_required
        matched = [s.skill_name for s in req if s.skill_name.lower().strip() in user_skill_names]
        missing = [s.skill_name for s in req if s.skill_name.lower().strip() not in user_skill_names]
        readiness = int(round((len(matched) / (len(req) or 1)) * 100))
        return {
            'career': c.to_dict(),
            'readiness': readiness,
            'matched_skills': matched,
            'missing_skills': missing
        }

    return {
        'career_1': build_summary(c1),
        'career_2': build_summary(c2)
    }

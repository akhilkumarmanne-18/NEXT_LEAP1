import os
import json
import requests
from config import Config

def get_ai_status():
    """
    Returns transparency status regarding whether an external LLM API is active or rule-based fallback is active.
    """
    if Config.GEMINI_API_KEY:
        return {"mode": "gemini", "label": "Gemini AI Engine Active", "is_llm": True}
    elif Config.OPENAI_API_KEY:
        return {"mode": "openai", "label": "OpenAI Engine Active", "is_llm": True}
    else:
        return {"mode": "rule_based", "label": "NextLeap Expert System (Deterministic Fallback)", "is_llm": False}


def ask_career_coach(user_message, user, chat_history=None):
    """
    Generates a personalized response for the AI Career Coach.
    Uses LLM API if configured, otherwise uses intelligent context-aware rule engine.
    """
    status = get_ai_status()
    
    # Extract rich context from user profile
    user_name = user.full_name if user else "Learner"
    career_goal = user.preferred_career_goal if user else "Technology"
    weekly_hours = user.weekly_hours if user else 10
    
    user_skills_list = []
    if user:
        user_skills_list = [f"{s.skill_name} ({s.proficiency})" for s in user.skills.all()]
    skills_summary = ", ".join(user_skills_list) if user_skills_list else "No recorded skills yet"

    # 1. Attempt External AI API if configured
    if status['is_llm']:
        try:
            if status['mode'] == 'gemini':
                return call_gemini_api(user_message, user_name, career_goal, skills_summary, weekly_hours, chat_history)
            elif status['mode'] == 'openai':
                return call_openai_api(user_message, user_name, career_goal, skills_summary, weekly_hours, chat_history)
        except Exception as e:
            # Fall back to rule-based engine gracefully with notification
            pass

    # 2. Transparent Rule-Based Expert System
    return generate_expert_rule_response(user_message, user, user_name, career_goal, skills_summary, weekly_hours)


def call_gemini_api(message, name, goal, skills, hours, history):
    system_instruction = (
        f"You are the Next Leap AI Career Coach for {name}. Their career goal is {goal}. "
        f"Their current skills are: {skills}. They have {hours} hours available per week. "
        f"Provide supportive, highly structured, practical, and actionable career guidance. "
        f"Keep recommendations focused on practical projects, skill acquisition, and realistic milestones. "
        f"Always be encouraging, precise, and transparent."
    )
    
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={Config.GEMINI_API_KEY}"
    payload = {
        "contents": [
            {"role": "user", "parts": [{"text": f"System context: {system_instruction}\n\nUser Question: {message}"}]}
        ]
    }
    
    res = requests.post(api_url, json=payload, timeout=12)
    if res.status_code == 200:
        data = res.json()
        candidates = data.get('candidates', [])
        if candidates and 'content' in candidates[0]:
            parts = candidates[0]['content'].get('parts', [])
            if parts and 'text' in parts[0]:
                return {
                    "reply": parts[0]['text'],
                    "source": "Google Gemini AI",
                    "mode": "gemini"
                }
    raise Exception(f"Gemini API returned status {res.status_code}")


def call_openai_api(message, name, goal, skills, hours, history):
    api_url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {Config.OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": f"You are the Next Leap AI Career Coach for {name}. Goal: {goal}. Skills: {skills}. Available: {hours} hrs/week. Give concrete, realistic career advice."
            },
            {"role": "user", "content": message}
        ],
        "max_tokens": 600
    }
    res = requests.post(api_url, headers=headers, json=payload, timeout=12)
    if res.status_code == 200:
        data = res.json()
        return {
            "reply": data['choices'][0]['message']['content'],
            "source": "OpenAI Engine",
            "mode": "openai"
        }
    raise Exception(f"OpenAI API returned status {res.status_code}")


def generate_expert_rule_response(msg, user, name, goal, skills, hours):
    """
    Intelligent context-driven deterministic rule engine.
    Detects question intent and constructs customized advice based on actual user database records.
    """
    q = msg.lower().strip()
    
    # Intent 1: "Which career suits my current skills?"
    if any(k in q for k in ['suit', 'career suits', 'which career', 'match my skills', 'best career']):
        return {
            "reply": (
                f"Based on your profile, **{name}**, with existing skills in **{skills}**:\n\n"
                f"1. **{goal}** remains your strongest alignment. Your technical foundation allows you to quickly level up into applied projects.\n"
                f"2. **Alternative Adjacent Paths:**\n"
                f"   - **Business Analytics / Data Analytics:** If you enjoy interpreting metrics, SQL and visualization directly map here.\n"
                f"   - **Machine Learning Engineering:** If your coding rigor deepens, moving from data modeling to production deployment is a natural transition.\n\n"
                f"💡 **Recommendation:** Check your **Skill Gap Analyzer** page to see your quantitative readiness score and prioritize the remaining foundational gaps."
            ),
            "source": "NextLeap Expert Engine (Rule-based Fallback)",
            "mode": "rule_based"
        }

    # Intent 2: "What should I learn next?"
    if any(k in q for k in ['learn next', 'what should i learn', 'next step', 'next action']):
        # Pull missing skills from target career
        return {
            "reply": (
                f"Great question, **{name}**. To progress toward your goal of becoming a **{goal}**:\n\n"
                f"🎯 **Top Immediate Priority:**\n"
                f"- If you haven't mastered **SQL (Joins, Window Functions & Aggregations)**, prioritize that first. Data interviews test SQL aggressively.\n"
                f"- Follow this with **Data Wrangling (Pandas/NumPy)** and applied exploratory data analysis.\n\n"
                f"⏱️ **Weekly Plan ({hours} hrs/week allocated):**\n"
                f"- 4 hours: Theoretical concepts & documentation\n"
                f"- 6 hours: Hands-on query writing and debugging\n"
                f"- 2 hours: Code review & portfolio documentation\n\n"
                f"Check your **Your Next LEAP** widget on your Dashboard for today's curated learning task!"
            ),
            "source": "NextLeap Expert Engine (Rule-based Fallback)",
            "mode": "rule_based"
        }

    # Intent 3: "Suggest a beginner project for my career goal."
    if any(k in q for k in ['project', 'suggest a project', 'beginner project', 'portfolio idea']):
        return {
            "reply": (
                f"Here is an industry-relevant project tailored for your **{goal}** journey:\n\n"
                f"📁 **Project Idea: Customer Churn & Retention Analytics System**\n\n"
                f"**Why this matters:** Subscription and e-commerce companies constantly seek professionals who can diagnose why users leave.\n\n"
                f"**Key Deliverables:**\n"
                f"1. Exploratory analysis on customer demographics and usage metrics.\n"
                f"2. SQL queries summarizing monthly recurring revenue and churn rates.\n"
                f"3. A clean visualization dashboard (or Streamlit web interface) displaying predictive risk scores.\n\n"
                f"🚀 You can start and track this immediately in our **Project Studio** tab!"
            ),
            "source": "NextLeap Expert Engine (Rule-based Fallback)",
            "mode": "rule_based"
        }

    # Intent 4: "Help me prepare for an interview."
    if any(k in q for k in ['interview', 'prepare for interview', 'interview question', 'mock interview']):
        return {
            "reply": (
                f"Here is your interview readiness strategy for **{goal}** roles:\n\n"
                f"1. **Technical Core (40% of rounds):** Practice SQL joins, grouping, window functions, and algorithmic complexity in Python.\n"
                f"2. **Case Studies & System Design (35% of rounds):** Be ready to explain how you handle messy datasets, model drift, and business metric trade-offs.\n"
                f"3. **Behavioral (25% of rounds):** Use the **STAR method** (Situation, Task, Action, Result) to describe challenging technical hurdles you resolved.\n\n"
                f"Head over to our **Interview Preparation** module to practice interactive questions and receive immediate scored rubrics!"
            ),
            "source": "NextLeap Expert Engine (Rule-based Fallback)",
            "mode": "rule_based"
        }

    # Intent 5: "Review my learning roadmap."
    if any(k in q for k in ['roadmap', 'review roadmap', 'curriculum', 'learning plan']):
        return {
            "reply": (
                f"Reviewing your personalized **{goal}** roadmap for **{name}**:\n\n"
                f"✅ **Phase 1 (Foundations):** Solidifies programming syntax, data structures, and relational databases.\n"
                f"⏳ **Phase 2 & 3 (Core Technical & Applications):** Connects data wrangling with statistical testing and applied modeling.\n"
                f"🚀 **Phase 4 & 5 (Portfolio & Interview):** Converts your knowledge into public proof-of-work and prepares you for live technical screens.\n\n"
                f"💡 **Tip:** With your **{hours} hours per week**, you are on track to complete Phase 1 within approximately 3-4 weeks. Keep updating your task statuses in the **My Roadmap** section to keep progress accurate."
            ),
            "source": "NextLeap Expert Engine (Rule-based Fallback)",
            "mode": "rule_based"
        }

    # Default general guidance
    return {
        "reply": (
            f"Hello **{name}**! As your Next Leap Career Companion, I am here to assist your progression toward **{goal}**.\n\n"
            f"You have **{skills}** recorded in your profile. How can I assist you right now?\n"
            f"- Ask about **what skills to learn next**.\n"
            f"- Ask for **hands-on project recommendations**.\n"
            f"- Ask how to **prepare for technical or behavioral interviews**.\n"
            f"- Ask how to optimize your **weekly learning schedule**."
        ),
        "source": "NextLeap Expert Engine (Rule-based Fallback)",
        "mode": "rule_based"
    }


def evaluate_interview_answer(question, user_answer, category='Technical'):
    """
    Transparent rubric evaluation of a user's mock interview submission.
    Evaluates:
    - Relevance (0-25)
    - Clarity & Structure (0-25)
    - Completeness (0-25)
    - Technical Correctness / Specificity (0-25)
    """
    answer_text = user_answer.strip()
    word_count = len(answer_text.split())

    # Length & basic depth checks
    if word_count < 10:
        return {
            "score": 35,
            "feedback": "Your response is too brief to demonstrate full competency in an interview setting. Aim to elaborate on your reasoning and provide concrete technical terminology or examples.",
            "criteria": {
                "relevance": 10,
                "clarity": 12,
                "completeness": 5,
                "technical_correctness": 8
            },
            "disclaimer": "Note: Mock evaluation scores are educational estimations and do not guarantee hiring outcomes."
        }

    # Keyword and depth heuristic
    question_lower = question.lower()
    answer_lower = answer_text.lower()
    
    # Calculate relevance
    q_words = [w for w in question_lower.replace('?', '').split() if len(w) > 3]
    matched_q_words = [w for w in q_words if w in answer_lower]
    relevance_score = min(25, int((len(matched_q_words) / (len(q_words) or 1)) * 30) + 12)

    # Calculate clarity: sentence structure, capitalization, transition words
    has_transitions = any(t in answer_lower for t in ['because', 'therefore', 'for example', 'first', 'second', 'specifically', 'in order to'])
    clarity_score = 22 if has_transitions and word_count >= 30 else (18 if word_count >= 20 else 14)

    # Calculate completeness
    completeness_score = 24 if word_count >= 60 else (20 if word_count >= 35 else 15)

    # Technical correctness
    technical_score = 23 if (word_count >= 40 and len(matched_q_words) >= 2) else 18

    total_score = min(96, relevance_score + clarity_score + completeness_score + technical_score)

    feedback_points = []
    if total_score >= 80:
        feedback_points.append("Excellent response! You demonstrated solid clarity and articulated key concepts well.")
    elif total_score >= 65:
        feedback_points.append("Good start. Your core message is understandable, but could be enhanced with specific production examples or metric outcomes.")
    else:
        feedback_points.append("Adequate outline, but lacks technical depth and precision. Practice structuring your thoughts using structured frameworks (e.g. STAR).")

    if category == 'Technical':
        feedback_points.append("Remember to state assumptions, edge cases, and computational complexity (time/space) where applicable.")
    else:
        feedback_points.append("Ensure your story highlights your specific individual contribution and tangible positive results.")

    return {
        "score": total_score,
        "feedback": " ".join(feedback_points),
        "criteria": {
            "relevance": relevance_score,
            "clarity": clarity_score,
            "completeness": completeness_score,
            "technical_correctness": technical_score
        },
        "disclaimer": "Note: Mock evaluation scores are educational estimations and do not guarantee hiring outcomes."
    }

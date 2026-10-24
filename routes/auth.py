from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g, jsonify
from models import db
from models.user import User
from models.career import Career
from services.seed_service import seed_database

auth_bp = Blueprint('auth', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    user_id = session.get('user_id')
    if user_id:
        return User.query.get(user_id)
    return None

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('user_id'):
        return redirect(url_for('dashboard.index'))

    careers = Career.query.all()
    if not careers:
        seed_database()
        careers = Career.query.all()

    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        education_level = request.form.get('education_level', 'Undergraduate')
        current_course = request.form.get('current_course', '').strip()
        interests = request.form.get('interests', '').strip()
        preferred_career_goal = request.form.get('preferred_career_goal', 'Data Scientist')

        # Form validation
        if not full_name or not email or not password:
            flash("Full name, email, and password are required.", "danger")
            return render_template('register.html', careers=careers, form=request.form)

        if len(password) < 6:
            flash("Password must be at least 6 characters long.", "danger")
            return render_template('register.html', careers=careers, form=request.form)

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("An account with this email address already exists.", "danger")
            return render_template('register.html', careers=careers, form=request.form)

        # Match career goal to ID if possible
        matched_career = Career.query.filter(Career.title.ilike(f"%{preferred_career_goal}%")).first()

        new_user = User(
            full_name=full_name,
            email=email,
            education_level=education_level,
            current_course=current_course,
            interests=interests,
            preferred_career_goal=preferred_career_goal,
            target_career_id=matched_career.id if matched_career else None
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        # Generate initial roadmap for chosen career
        if matched_career:
            from services.roadmap_engine import generate_personalized_roadmap
            generate_personalized_roadmap(new_user, matched_career)

        session['user_id'] = new_user.id
        session['user_name'] = new_user.full_name
        flash(f"Welcome to NEXT LEAP 2.0, {new_user.full_name}! Your career journey begins.", "success")
        return redirect(url_for('dashboard.index'))

    return render_template('register.html', careers=careers)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user_id'):
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        if not email or not password:
            flash("Please enter both email and password.", "danger")
            return render_template('login.html')

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            flash("Invalid email or password. Please try again.", "danger")
            return render_template('login.html')

        session['user_id'] = user.id
        session['user_name'] = user.full_name
        flash(f"Welcome back, {user.full_name}!", "success")
        
        next_page = request.args.get('next')
        return redirect(next_page or url_for('dashboard.index'))

    return render_template('login.html')


@auth_bp.route('/demo-login')
def demo_login():
    """One-click instant login as the pre-configured Data Science demo user Alex Chen."""
    demo_user = User.query.filter_by(email="alex.chen@nextleap.demo").first()
    if not demo_user:
        seed_database()
        demo_user = User.query.filter_by(email="alex.chen@nextleap.demo").first()

    if demo_user:
        session['user_id'] = demo_user.id
        session['user_name'] = demo_user.full_name
        flash("Logged in as Data Science Demo User (Alex Chen). Explore all active platform features!", "info")
        return redirect(url_for('dashboard.index'))
    
    flash("Demo user could not be initialized.", "danger")
    return redirect(url_for('auth.login'))


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("You have been signed out safely. Come back soon to continue your leap!", "info")
    return redirect(url_for('landing'))

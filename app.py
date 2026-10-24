import os
from flask import Flask, render_template, session, redirect, url_for
from config import Config
from models import db
from models.user import User
from models.career import Career
from models.notification import Notification

from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.careers import careers_bp
from routes.skills import skills_bp
from routes.roadmap import roadmap_bp
from routes.projects import projects_bp
from routes.interviews import interviews_bp
from routes.coach import coach_bp
from routes.user_profile import profile_bp

from services.seed_service import seed_database

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(careers_bp)
    app.register_blueprint(skills_bp)
    app.register_blueprint(roadmap_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(interviews_bp)
    app.register_blueprint(coach_bp)
    app.register_blueprint(profile_bp)

    # Global context processor
    @app.context_processor
    def inject_global_vars():
        user = None
        unread_notifs = 0
        if 'user_id' in session:
            user = User.query.get(session['user_id'])
            if user:
                unread_notifs = Notification.query.filter_by(user_id=user.id, is_read=False).count()
        return {
            'current_user': user,
            'unread_notifications_count': unread_notifs,
            'app_name': 'NEXT LEAP 2.0',
            'app_tagline': 'Discover Your Potential. Build Your Skills. Shape Your Future.'
        }

    # Root landing page route
    @app.route('/')
    def landing():
        careers = Career.query.limit(6).all()
        return render_template('landing.html', careers=careers)

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('base.html', content="<div class='container my-5 text-center'><h2>404 - Page Not Found</h2><p>The page you requested could not be located.</p><a href='/' class='btn btn-primary'>Return Home</a></div>"), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('base.html', content="<div class='container my-5 text-center'><h2>500 - Server Error</h2><p>An unexpected error occurred. Please try again.</p><a href='/' class='btn btn-primary'>Return Home</a></div>"), 500

    # Initialize database tables and seed sample data
    with app.app_context():
        # Ensure database directory exists for SQLite
        db_uri = app.config['SQLALCHEMY_DATABASE_URI']
        if db_uri.startswith('sqlite:///'):
            db_file = db_uri.replace('sqlite:///', '')
            os.makedirs(os.path.dirname(os.path.abspath(db_file)), exist_ok=True)
            
        db.create_all()
        try:
            seed_database()
        except Exception as e:
            print(f"Warning during seed check: {e}")

    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

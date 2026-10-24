from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    
    # Profile & Educational background
    education_level = db.Column(db.String(100), default="Undergraduate")
    current_course = db.Column(db.String(150), default="Computer Science & Engineering")
    interests = db.Column(db.String(500), default="Artificial Intelligence, Data Science, Web Development")
    preferred_career_goal = db.Column(db.String(100), default="Data Scientist")
    target_career_id = db.Column(db.Integer, nullable=True)
    
    # Learning preferences
    learning_style = db.Column(db.String(50), default="Hands-on Project Building")
    weekly_hours = db.Column(db.Integer, default=12)
    bio = db.Column(db.Text, nullable=True)
    github_url = db.Column(db.String(250), nullable=True)
    linkedin_url = db.Column(db.String(250), nullable=True)
    portfolio_url = db.Column(db.String(250), nullable=True)
    theme_preference = db.Column(db.String(20), default="dark")
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    skills = db.relationship('UserSkill', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    roadmaps = db.relationship('Roadmap', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    projects = db.relationship('UserProject', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    interview_attempts = db.relationship('InterviewAttempt', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    notifications = db.relationship('Notification', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'education_level': self.education_level,
            'current_course': self.current_course,
            'interests': self.interests,
            'preferred_career_goal': self.preferred_career_goal,
            'target_career_id': self.target_career_id,
            'learning_style': self.learning_style,
            'weekly_hours': self.weekly_hours,
            'bio': self.bio,
            'github_url': self.github_url,
            'linkedin_url': self.linkedin_url,
            'portfolio_url': self.portfolio_url,
            'theme_preference': self.theme_preference
        }

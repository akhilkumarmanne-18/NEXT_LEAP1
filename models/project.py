import json
from datetime import datetime
from . import db

class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)
    title = db.Column(db.String(150), nullable=False)
    career_id = db.Column(db.Integer, db.ForeignKey('careers.id', ondelete='SET NULL'), nullable=True)
    category = db.Column(db.String(80), default="Technical")
    difficulty = db.Column(db.String(30), default="Beginner")  # Beginner, Intermediate, Advanced
    description = db.Column(db.Text, nullable=False)
    
    # JSON-encoded lists
    required_skills_json = db.Column(db.Text, default="[]")
    suggested_tools_json = db.Column(db.Text, default="[]")
    milestones_json = db.Column(db.Text, default="[]")
    deliverables_json = db.Column(db.Text, default="[]")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user_projects = db.relationship('UserProject', backref='project', lazy='dynamic')

    @property
    def required_skills(self):
        try:
            return json.loads(self.required_skills_json or "[]")
        except:
            return []

    @required_skills.setter
    def required_skills(self, val):
        self.required_skills_json = json.dumps(val)

    @property
    def suggested_tools(self):
        try:
            return json.loads(self.suggested_tools_json or "[]")
        except:
            return []

    @suggested_tools.setter
    def suggested_tools(self, val):
        self.suggested_tools_json = json.dumps(val)

    @property
    def milestones(self):
        try:
            return json.loads(self.milestones_json or "[]")
        except:
            return []

    @milestones.setter
    def milestones(self, val):
        self.milestones_json = json.dumps(val)

    @property
    def deliverables(self):
        try:
            return json.loads(self.deliverables_json or "[]")
        except:
            return []

    @deliverables.setter
    def deliverables(self, val):
        self.deliverables_json = json.dumps(val)

    def to_dict(self):
        return {
            'id': self.id,
            'slug': self.slug,
            'title': self.title,
            'career_id': self.career_id,
            'category': self.category,
            'difficulty': self.difficulty,
            'description': self.description,
            'required_skills': self.required_skills,
            'suggested_tools': self.suggested_tools,
            'milestones': self.milestones,
            'deliverables': self.deliverables
        }


class UserProject(db.Model):
    __tablename__ = 'user_projects'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete='SET NULL'), nullable=True)
    custom_title = db.Column(db.String(150), nullable=True)
    status = db.Column(db.String(30), default="In Progress")  # In Progress, Completed
    progress_percent = db.Column(db.Integer, default=0)
    notes = db.Column(db.Text, nullable=True)
    repo_url = db.Column(db.String(255), nullable=True)
    live_url = db.Column(db.String(255), nullable=True)
    in_portfolio = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)

    @property
    def display_title(self):
        if self.custom_title:
            return self.custom_title
        if self.project:
            return self.project.title
        return "Untitled Project"

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'project_id': self.project_id,
            'display_title': self.display_title,
            'status': self.status,
            'progress_percent': self.progress_percent,
            'notes': self.notes,
            'repo_url': self.repo_url,
            'live_url': self.live_url,
            'in_portfolio': self.in_portfolio,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'project': self.project.to_dict() if self.project else None
        }

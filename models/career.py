import json
from datetime import datetime
from . import db

class Career(db.Model):
    __tablename__ = 'careers'

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(80), unique=True, nullable=False, index=True)
    title = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(80), nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    salary_range = db.Column(db.String(80), default="$75,000 - $135,000 / yr")
    market_outlook = db.Column(db.String(80), default="High Demand (+23% Growth)")
    
    # JSON-encoded lists
    responsibilities_json = db.Column(db.Text, default="[]")
    entry_roles_json = db.Column(db.Text, default="[]")
    learning_resources_json = db.Column(db.Text, default="[]")
    recommended_beginner_projects_json = db.Column(db.Text, default="[]")
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    skills_required = db.relationship('CareerSkill', backref='career', lazy='joined', cascade='all, delete-orphan')
    roadmaps = db.relationship('Roadmap', backref='career', lazy='dynamic')
    projects = db.relationship('Project', backref='career', lazy='dynamic')

    @property
    def responsibilities(self):
        try:
            return json.loads(self.responsibilities_json or "[]")
        except:
            return []

    @responsibilities.setter
    def responsibilities(self, val):
        self.responsibilities_json = json.dumps(val)

    @property
    def entry_roles(self):
        try:
            return json.loads(self.entry_roles_json or "[]")
        except:
            return []

    @entry_roles.setter
    def entry_roles(self, val):
        self.entry_roles_json = json.dumps(val)

    @property
    def learning_resources(self):
        try:
            return json.loads(self.learning_resources_json or "[]")
        except:
            return []

    @learning_resources.setter
    def learning_resources(self, val):
        self.learning_resources_json = json.dumps(val)

    @property
    def recommended_beginner_projects(self):
        try:
            return json.loads(self.recommended_beginner_projects_json or "[]")
        except:
            return []

    @recommended_beginner_projects.setter
    def recommended_beginner_projects(self, val):
        self.recommended_beginner_projects_json = json.dumps(val)

    def to_dict(self):
        return {
            'id': self.id,
            'slug': self.slug,
            'title': self.title,
            'category': self.category,
            'description': self.description,
            'salary_range': self.salary_range,
            'market_outlook': self.market_outlook,
            'responsibilities': self.responsibilities,
            'entry_roles': self.entry_roles,
            'learning_resources': self.learning_resources,
            'recommended_beginner_projects': self.recommended_beginner_projects,
            'skills': [cs.to_dict() for cs in self.skills_required]
        }


class CareerSkill(db.Model):
    __tablename__ = 'career_skills'

    id = db.Column(db.Integer, primary_key=True)
    career_id = db.Column(db.Integer, db.ForeignKey('careers.id', ondelete='CASCADE'), nullable=False)
    skill_name = db.Column(db.String(100), nullable=False)
    importance_level = db.Column(db.String(20), default="Required")  # Required, Preferred, Bonus
    minimum_proficiency = db.Column(db.String(20), default="Intermediate")  # Beginner, Intermediate, Advanced
    why_recommended = db.Column(db.Text, nullable=False)
    weight = db.Column(db.Integer, default=5)  # 1 to 10 scale for scoring

    def to_dict(self):
        return {
            'id': self.id,
            'career_id': self.career_id,
            'skill_name': self.skill_name,
            'importance_level': self.importance_level,
            'minimum_proficiency': self.minimum_proficiency,
            'why_recommended': self.why_recommended,
            'weight': self.weight
        }

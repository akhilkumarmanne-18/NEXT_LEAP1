from datetime import datetime
from . import db

class Skill(db.Model):
    __tablename__ = 'skills'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    category = db.Column(db.String(80), nullable=False, default="General")
    description = db.Column(db.Text, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'description': self.description
        }


class UserSkill(db.Model):
    __tablename__ = 'user_skills'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    skill_name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(80), default="Technical")
    proficiency = db.Column(db.String(30), default="Beginner")  # Beginner, Intermediate, Advanced
    is_verified = db.Column(db.Boolean, default=False)
    notes = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Convert proficiency to numeric 1-3 for calculations
    @property
    def level_score(self):
        scores = {'Beginner': 1, 'Intermediate': 2, 'Advanced': 3}
        return scores.get(self.proficiency, 1)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'skill_name': self.skill_name,
            'category': self.category,
            'proficiency': self.proficiency,
            'level_score': self.level_score,
            'is_verified': self.is_verified,
            'notes': self.notes,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

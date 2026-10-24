import json
from datetime import datetime
from . import db

class InterviewQuestion(db.Model):
    __tablename__ = 'interview_questions'

    id = db.Column(db.Integer, primary_key=True)
    career_id = db.Column(db.Integer, db.ForeignKey('careers.id', ondelete='SET NULL'), nullable=True)
    category = db.Column(db.String(50), nullable=False, default="Technical")  # Technical, Behavioral, Role-Specific, Quiz
    role_tag = db.Column(db.String(80), default="Data Science")
    difficulty = db.Column(db.String(30), default="Medium")  # Easy, Medium, Hard
    question = db.Column(db.Text, nullable=False)
    
    options_json = db.Column(db.Text, default="[]")  # For MCQs
    correct_answer = db.Column(db.String(255), nullable=True)
    sample_answer = db.Column(db.Text, nullable=True)
    rubric_json = db.Column(db.Text, default="{}")
    explanation = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    attempts = db.relationship('InterviewAttempt', backref='question_ref', lazy='dynamic')

    @property
    def options(self):
        try:
            return json.loads(self.options_json or "[]")
        except:
            return []

    @options.setter
    def options(self, val):
        self.options_json = json.dumps(val)

    @property
    def rubric(self):
        try:
            return json.loads(self.rubric_json or "{}")
        except:
            return {}

    @rubric.setter
    def rubric(self, val):
        self.rubric_json = json.dumps(val)

    def to_dict(self):
        return {
            'id': self.id,
            'career_id': self.career_id,
            'category': self.category,
            'role_tag': self.role_tag,
            'difficulty': self.difficulty,
            'question': self.question,
            'options': self.options,
            'correct_answer': self.correct_answer,
            'sample_answer': self.sample_answer,
            'rubric': self.rubric,
            'explanation': self.explanation
        }


class InterviewAttempt(db.Model):
    __tablename__ = 'interview_attempts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('interview_questions.id', ondelete='CASCADE'), nullable=False)
    user_answer = db.Column(db.Text, nullable=False)
    score = db.Column(db.Integer, default=0)
    feedback = db.Column(db.Text, nullable=True)
    criteria_breakdown_json = db.Column(db.Text, default="{}")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def criteria_breakdown(self):
        try:
            return json.loads(self.criteria_breakdown_json or "{}")
        except:
            return {}

    @criteria_breakdown.setter
    def criteria_breakdown(self, val):
        self.criteria_breakdown_json = json.dumps(val)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'question_id': self.question_id,
            'user_answer': self.user_answer,
            'score': self.score,
            'feedback': self.feedback,
            'criteria_breakdown': self.criteria_breakdown,
            'created_at': self.created_at.strftime("%b %d, %Y %H:%M") if self.created_at else None,
            'question': self.question_ref.question if self.question_ref else None,
            'role_tag': self.question_ref.role_tag if self.question_ref else None
        }

from datetime import datetime
from . import db

class Roadmap(db.Model):
    __tablename__ = 'roadmaps'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    career_id = db.Column(db.Integer, db.ForeignKey('careers.id', ondelete='SET NULL'), nullable=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    phases = db.relationship('RoadmapPhase', backref='roadmap', lazy='joined', cascade='all, delete-orphan', order_by='RoadmapPhase.phase_number')

    @property
    def total_tasks(self):
        count = 0
        for phase in self.phases:
            count += len(phase.tasks)
        return count

    @property
    def completed_tasks(self):
        count = 0
        for phase in self.phases:
            for task in phase.tasks:
                if task.status == 'Completed':
                    count += 1
        return count

    @property
    def progress_percent(self):
        total = self.total_tasks
        if total == 0:
            return 0
        return int(round((self.completed_tasks / total) * 100))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'career_id': self.career_id,
            'title': self.title,
            'description': self.description,
            'is_active': self.is_active,
            'total_tasks': self.total_tasks,
            'completed_tasks': self.completed_tasks,
            'progress_percent': self.progress_percent,
            'phases': [phase.to_dict() for phase in self.phases]
        }


class RoadmapPhase(db.Model):
    __tablename__ = 'roadmap_phases'

    id = db.Column(db.Integer, primary_key=True)
    roadmap_id = db.Column(db.Integer, db.ForeignKey('roadmaps.id', ondelete='CASCADE'), nullable=False)
    phase_number = db.Column(db.Integer, nullable=False, default=1)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)

    # Relationships
    tasks = db.relationship('RoadmapTask', backref='phase', lazy='joined', cascade='all, delete-orphan', order_by='RoadmapTask.order_index')

    @property
    def progress_percent(self):
        total = len(self.tasks)
        if total == 0:
            return 0
        completed = sum(1 for t in self.tasks if t.status == 'Completed')
        return int(round((completed / total) * 100))

    def to_dict(self):
        return {
            'id': self.id,
            'roadmap_id': self.roadmap_id,
            'phase_number': self.phase_number,
            'title': self.title,
            'description': self.description,
            'progress_percent': self.progress_percent,
            'tasks': [t.to_dict() for t in self.tasks]
        }


class RoadmapTask(db.Model):
    __tablename__ = 'roadmap_tasks'

    id = db.Column(db.Integer, primary_key=True)
    phase_id = db.Column(db.Integer, db.ForeignKey('roadmap_phases.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    skills_involved = db.Column(db.String(255), default="")
    estimated_hours = db.Column(db.Integer, default=5)
    target_date = db.Column(db.String(50), nullable=True)
    status = db.Column(db.String(30), default='Pending')  # Pending, In Progress, Completed
    is_custom = db.Column(db.Boolean, default=False)
    order_index = db.Column(db.Integer, default=0)
    completed_at = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'phase_id': self.phase_id,
            'title': self.title,
            'description': self.description,
            'skills_involved': self.skills_involved,
            'estimated_hours': self.estimated_hours,
            'target_date': self.target_date,
            'status': self.status,
            'is_custom': self.is_custom,
            'order_index': self.order_index,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

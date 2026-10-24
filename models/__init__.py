from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .career import Career, CareerSkill
from .skill import Skill, UserSkill
from .roadmap import Roadmap, RoadmapPhase, RoadmapTask
from .project import Project, UserProject
from .interview import InterviewQuestion, InterviewAttempt
from .notification import Notification

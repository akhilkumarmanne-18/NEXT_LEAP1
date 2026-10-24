from datetime import datetime, timedelta
from models import db
from models.roadmap import Roadmap, RoadmapPhase, RoadmapTask
from models.career import Career

def generate_personalized_roadmap(user, career):
    """
    Generates a tailored 5-phase learning roadmap for the user based on career and current skills.
    """
    if not career:
        return None

    # Check if user already has an active roadmap for this career
    existing = Roadmap.query.filter_by(user_id=user.id, career_id=career.id).first()
    if existing:
        return existing

    # Archive any previous active roadmaps
    Roadmap.query.filter_by(user_id=user.id, is_active=True).update({'is_active': False})

    user_skills_dict = {s.skill_name.lower().strip(): s.proficiency for s in user.skills.all()}

    roadmap = Roadmap(
        user_id=user.id,
        career_id=career.id,
        title=f"{career.title} Mastery Pathway",
        description=f"Tailored step-by-step curriculum customized for {user.full_name} to achieve job readiness in {career.title}.",
        is_active=True
    )
    db.session.add(roadmap)
    db.session.flush()

    # Pre-defined roadmap templates customized by category/career
    career_slug = career.slug
    
    phases_data = get_roadmap_template(career_slug, career.title, user_skills_dict)

    base_date = datetime.utcnow()
    for p_idx, p_data in enumerate(phases_data, start=1):
        phase = RoadmapPhase(
            roadmap_id=roadmap.id,
            phase_number=p_idx,
            title=p_data['title'],
            description=p_data['description']
        )
        db.session.add(phase)
        db.session.flush()

        for t_idx, t_data in enumerate(p_data['tasks'], start=1):
            target_dt = base_date + timedelta(days=t_data.get('days_offset', 7 * t_idx))
            task = RoadmapTask(
                phase_id=phase.id,
                title=t_data['title'],
                description=t_data['description'],
                skills_involved=t_data.get('skills_involved', ''),
                estimated_hours=t_data.get('hours', 6),
                target_date=target_dt.strftime('%b %d, %Y'),
                status=t_data.get('status', 'Pending'),
                is_custom=False,
                order_index=t_idx,
                completed_at=datetime.utcnow() if t_data.get('status') == 'Completed' else None
            )
            db.session.add(task)

    db.session.commit()
    return roadmap


def get_roadmap_template(slug, career_title, user_skills):
    """
    Returns tailored 5-phase data structure taking user's existing skills into account.
    """
    knows_python = 'python' in user_skills
    python_prof = user_skills.get('python', 'None')
    knows_sql = 'sql' in user_skills
    knows_git = 'git' in user_skills or 'version control' in user_skills

    if 'data' in slug or 'analyst' in slug or 'ai' in slug:
        return [
            {
                'title': 'Phase 1: Foundations & Analytical Tooling',
                'description': 'Master core programming, mathematical intuition, and foundational data querying.',
                'tasks': [
                    {
                        'title': 'Python Fundamentals & Data Structures' if not knows_python else 'Advanced Python & Functional Programming',
                        'description': 'Control flow, lists, dicts, OOP, and data pipelines.' if not knows_python else 'Generators, decorators, multiprocessing, and performant Python idioms.',
                        'skills_involved': 'Python',
                        'hours': 8 if not knows_python else 4,
                        'days_offset': 5,
                        'status': 'Completed' if knows_python and python_prof in ['Intermediate', 'Advanced'] else 'In Progress'
                    },
                    {
                        'title': 'SQL Mastery: Aggregations, Window Functions & Joins',
                        'description': 'Writing complex queries, CTEs, self-joins, and query performance optimization.',
                        'skills_involved': 'SQL, Relational Databases',
                        'hours': 10,
                        'days_offset': 12,
                        'status': 'Completed' if knows_sql else 'Pending'
                    },
                    {
                        'title': 'Git, GitHub & Reproducible Environments',
                        'description': 'Version control, feature branches, pull requests, virtual environments and container basics.',
                        'skills_involved': 'Git, GitHub, Terminal',
                        'hours': 4,
                        'days_offset': 18,
                        'status': 'Completed' if knows_git else 'Pending'
                    }
                ]
            },
            {
                'title': 'Phase 2: Core Technical & Algorithmic Skills',
                'description': 'Data wrangling, statistical hypothesis testing, and exploratory data visualization.',
                'tasks': [
                    {
                        'title': 'Data Wrangling with Pandas & NumPy',
                        'description': 'Handling missing data, grouping, reshaping, time series, and vectorized operations.',
                        'skills_involved': 'Pandas, NumPy, Data Cleaning',
                        'hours': 12,
                        'days_offset': 26,
                        'status': 'Pending'
                    },
                    {
                        'title': 'Statistical Inference & Hypothesis Testing',
                        'description': 'Probability distributions, p-values, A/B test formulation, confidence intervals, and ANOVA.',
                        'skills_involved': 'Applied Statistics, Probability',
                        'hours': 10,
                        'days_offset': 34,
                        'status': 'Pending'
                    },
                    {
                        'title': 'Visual Storytelling with Seaborn, Matplotlib & BI Dashboards',
                        'description': 'Creating executive charts, interactive plots, and business metric presentation.',
                        'skills_involved': 'Data Visualization, Tableau/PowerBI',
                        'hours': 8,
                        'days_offset': 42,
                        'status': 'Pending'
                    }
                ]
            },
            {
                'title': 'Phase 3: Machine Learning & Practical Applications',
                'description': 'Supervised and unsupervised models, feature engineering, and cross-validation pipelines.',
                'tasks': [
                    {
                        'title': 'Supervised Learning: Regression & Classification',
                        'description': 'Linear models, decision trees, Random Forests, XGBoost, and ROC-AUC evaluation.',
                        'skills_involved': 'Scikit-Learn, Machine Learning',
                        'hours': 14,
                        'days_offset': 52,
                        'status': 'Pending'
                    },
                    {
                        'title': 'Unsupervised Learning & Clustering',
                        'description': 'K-Means, PCA dimensional reduction, and anomaly detection algorithms.',
                        'skills_involved': 'Clustering, PCA, Feature Engineering',
                        'hours': 8,
                        'days_offset': 60,
                        'status': 'Pending'
                    },
                    {
                        'title': 'Model Evaluation, Bias-Variance Tradeoff & Tuning',
                        'description': 'Stratified K-fold cross validation, hyperparameter grid search, and explainability (SHAP).',
                        'skills_involved': 'Model Validation, Hyperparameter Tuning',
                        'hours': 7,
                        'days_offset': 68,
                        'status': 'Pending'
                    }
                ]
            },
            {
                'title': 'Phase 4: Capstone Portfolio Projects',
                'description': 'Ship production-grade, end-to-end data pipelines and models to GitHub and public cloud.',
                'tasks': [
                    {
                        'title': 'Customer Lifetime Value & Churn Prediction System',
                        'description': 'Full machine learning pipeline with automated data ingestion, model serving, and Streamlit dashboard.',
                        'skills_involved': 'ML, Python, Streamlit, Docker',
                        'hours': 16,
                        'days_offset': 80,
                        'status': 'Pending'
                    },
                    {
                        'title': 'Interactive Executive Analytics Dashboard',
                        'description': 'Multi-page analytical dashboard connecting SQL database with automated KPIs and insights.',
                        'skills_involved': 'SQL, BI Tools, Dashboard Design',
                        'hours': 12,
                        'days_offset': 92,
                        'status': 'Pending'
                    }
                ]
            },
            {
                'title': 'Phase 5: Technical Interviews & Job Readiness',
                'description': 'Cracking live coding challenges, system design, case studies, and behavioral rounds.',
                'tasks': [
                    {
                        'title': 'SQL Live Query Drills & Edge Case Challenges',
                        'description': 'Speed practice on medium/hard LeetCode and HackerRank SQL questions under time limits.',
                        'skills_involved': 'Live SQL, Performance Tuning',
                        'hours': 8,
                        'days_offset': 100,
                        'status': 'Pending'
                    },
                    {
                        'title': 'Machine Learning System Design & Case Studies',
                        'description': 'Architecture design for recommendation systems, search ranking, and fraud detection.',
                        'skills_involved': 'System Design, Architecture',
                        'hours': 10,
                        'days_offset': 108,
                        'status': 'Pending'
                    },
                    {
                        'title': 'Mock Behavioral & STAR Methodology Rehearsals',
                        'description': 'Rehearse leadership, conflict resolution, and impact-driven project walkthroughs.',
                        'skills_involved': 'Behavioral Interviews, STAR Framework',
                        'hours': 5,
                        'days_offset': 114,
                        'status': 'Pending'
                    }
                ]
            }
        ]
    else:
        # Default modern software engineering pathway
        return [
            {
                'title': 'Phase 1: Foundations & Architecture Principles',
                'description': f'Core engineering fundamentals, clean code, and environments for {career_title}.',
                'tasks': [
                    {
                        'title': 'Programming Language Core & Data Structures',
                        'description': 'Syntax, algorithms, memory management, and clean architecture fundamentals.',
                        'skills_involved': 'Programming Fundamentals',
                        'hours': 10,
                        'days_offset': 7,
                        'status': 'In Progress'
                    },
                    {
                        'title': 'Version Control, Git Workflows & CI/CD Basics',
                        'description': 'Branching strategies, Git rebase, code reviews, and GitHub Actions.',
                        'skills_involved': 'Git, CI/CD',
                        'hours': 6,
                        'days_offset': 14,
                        'status': 'Pending'
                    }
                ]
            },
            {
                'title': 'Phase 2: Core Domain Tooling & Frameworks',
                'description': 'Building production modules with modern domain-specific libraries and databases.',
                'tasks': [
                    {
                        'title': 'Database Modeling & API Design',
                        'description': 'Relational schema design, RESTful principles, serialization, and auth security.',
                        'skills_involved': 'REST APIs, Databases',
                        'hours': 12,
                        'days_offset': 28,
                        'status': 'Pending'
                    },
                    {
                        'title': 'Automated Unit & Integration Testing',
                        'description': 'Writing test suites, mocking external dependencies, and achieving test coverage.',
                        'skills_involved': 'Testing, Quality Assurance',
                        'hours': 8,
                        'days_offset': 38,
                        'status': 'Pending'
                    }
                ]
            },
            {
                'title': 'Phase 3: Practical Application & Cloud Deployment',
                'description': 'Containerization, deployment, and cloud infrastructure.',
                'tasks': [
                    {
                        'title': 'Docker Containerization & Orchestration',
                        'description': 'Writing Dockerfiles, multi-stage builds, Docker Compose, and environment secrets.',
                        'skills_involved': 'Docker, Containers',
                        'hours': 8,
                        'days_offset': 50,
                        'status': 'Pending'
                    },
                    {
                        'title': 'Cloud Hosting & Observability',
                        'description': 'Deploying microservices, logging, error monitoring, and metrics dashboards.',
                        'skills_involved': 'Cloud, Monitoring',
                        'hours': 10,
                        'days_offset': 62,
                        'status': 'Pending'
                    }
                ]
            },
            {
                'title': 'Phase 4: Production Portfolio Project',
                'description': 'Architecting and deploying a showcase full-stack application.',
                'tasks': [
                    {
                        'title': 'Full-Scale Capstone Application Build',
                        'description': 'Design, code, test, and deploy a live project with documentation and live demo link.',
                        'skills_involved': 'Full-Stack, Cloud Deployment',
                        'hours': 18,
                        'days_offset': 78,
                        'status': 'Pending'
                    }
                ]
            },
            {
                'title': 'Phase 5: Technical Interviews & System Design',
                'description': 'Data structures, coding challenges, system design, and behavioral excellence.',
                'tasks': [
                    {
                        'title': 'Coding Challenges & Algorithm Optimization',
                        'description': 'Arrays, Hash Maps, Trees, Graphs, and Dynamic Programming practice.',
                        'skills_involved': 'Algorithms, Data Structures',
                        'hours': 12,
                        'days_offset': 90,
                        'status': 'Pending'
                    },
                    {
                        'title': 'System Design & Scalability Walkthroughs',
                        'description': 'Load balancing, caching, sharding, message queues, and high availability.',
                        'skills_involved': 'System Design',
                        'hours': 10,
                        'days_offset': 100,
                        'status': 'Pending'
                    }
                ]
            }
        ]

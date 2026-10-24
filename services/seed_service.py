import json
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
from models import db
from models.user import User
from models.career import Career, CareerSkill
from models.skill import Skill, UserSkill
from models.roadmap import Roadmap, RoadmapPhase, RoadmapTask
from models.project import Project, UserProject
from models.interview import InterviewQuestion, InterviewAttempt
from models.notification import Notification

def seed_database():
    """Populates initial reference data and demo user if empty."""
    # Check if already seeded
    if Career.query.first():
        return

    print("--- Seeding NEXT LEAP 2.0 Database ---")

    # 1. Seed Skills Catalog
    skills_data = [
        ("Python", "Programming", "Versatile language for backend, automation, and data."),
        ("SQL", "Database", "Structured query language for relational databases."),
        ("Statistics", "Mathematics", "Probability, distributions, hypothesis testing."),
        ("Machine Learning", "AI/ML", "Supervised, unsupervised, regression, classification."),
        ("Data Visualization", "Data", "Matplotlib, Seaborn, Tableau, PowerBI storytelling."),
        ("Data Cleaning", "Data", "Handling missing values, outlier detection, normalization."),
        ("Problem Solving", "Soft Skills", "Algorithmic thinking and breaking down challenges."),
        ("Project Development", "Engineering", "Translating requirements into production code."),
        ("JavaScript", "Frontend", "Interactive web frontends and asynchronous workflows."),
        ("React", "Frontend", "Component-based user interface engineering."),
        ("Docker", "DevOps", "Containerization and local reproducible environments."),
        ("AWS", "Cloud", "Amazon Web Services compute, storage, and networking."),
        ("Git", "Tools", "Version control, branching, PRs, and collaborative repos."),
        ("Network Security", "Cybersecurity", "Protocols, firewalls, threat modeling."),
        ("Figma", "Design", "UI design, prototyping, typography, wireframes."),
        ("UX Research", "Design", "User interviews, persona synthesis, usability audits."),
        ("Product Strategy", "Management", "Roadmapping, prioritization, metrics, OKRs.")
    ]
    for name, cat, desc in skills_data:
        s = Skill(name=name, category=cat, description=desc)
        db.session.add(s)
    db.session.flush()

    # 2. Seed Careers
    careers_data = [
        {
            "slug": "data-scientist",
            "title": "Data Scientist",
            "category": "Data Science",
            "description": "Analyzes complex datasets to extract actionable insights, build predictive models, and optimize business decisions through data-driven intelligence.",
            "salary_range": "$95,000 - $155,000 / yr",
            "market_outlook": "Very High (+26% Growth)",
            "responsibilities": [
                "Formulate business questions into statistical hypotheses and analytical frameworks.",
                "Extract, clean, and integrate high-volume multi-source data using SQL and Python.",
                "Develop, validate, and fine-tune supervised and unsupervised machine learning models.",
                "Communicate insights and strategic recommendations to cross-functional stakeholders through visual dashboards."
            ],
            "entry_roles": ["Junior Data Scientist", "Data Science Associate", "Quantitative Analyst", "Associate ML Specialist"],
            "learning_resources": [
                {"title": "Kaggle Micro-Courses", "type": "Interactive Coding", "url": "https://kaggle.com/learn"},
                {"title": "StatQuest with Josh Starmer", "type": "Video Explanations", "url": "https://youtube.com/@statquest"},
                {"title": "Fast.ai Practical Deep Learning", "type": "Open Curriculum", "url": "https://course.fast.ai"}
            ],
            "recommended_beginner_projects": [
                "Customer Churn Classification with Scikit-Learn",
                "E-Commerce Exploratory Sales Insights Dashboard",
                "Real Estate Price Prediction Model with Feature Engineering"
            ],
            "skills": [
                ("Python", "Required", "Intermediate", "Primary programming environment for scientific computing and modeling.", 9),
                ("SQL", "Required", "Intermediate", "Essential for querying enterprise databases and aggregating data.", 9),
                ("Statistics", "Required", "Intermediate", "Underpins experimental design, confidence intervals, and hypothesis tests.", 8),
                ("Machine Learning", "Required", "Intermediate", "Core algorithmic foundation for predictive modeling and pattern recognition.", 8),
                ("Data Visualization", "Required", "Beginner", "Communicating results effectively to non-technical business partners.", 7),
                ("Data Cleaning", "Required", "Intermediate", "Real-world data is messy; cleaning represents majority of workflow time.", 8),
                ("Problem Solving", "Preferred", "Intermediate", "Formulating ambiguous business problems into crisp quantitative models.", 7),
                ("Git", "Preferred", "Beginner", "Ensuring reproducibility and team version control for analytical code.", 6)
            ]
        },
        {
            "slug": "software-engineer",
            "title": "Software Engineer",
            "category": "Software Development",
            "description": "Architects, develops, tests, and maintains modern web, cloud, and distributed software systems with focus on scalability, maintainability, and clean code.",
            "salary_range": "$85,000 - $145,000 / yr",
            "market_outlook": "High Demand (+22% Growth)",
            "responsibilities": [
                "Write clean, testable, and well-documented code following modern design patterns.",
                "Build scalable RESTful and GraphQL APIs for client applications.",
                "Collaborate with product managers and designers to translate product specs into features.",
                "Debug production incidents and participate in architecture code reviews."
            ],
            "entry_roles": ["Associate Software Engineer", "Junior Backend Developer", "Full Stack Developer I"],
            "learning_resources": [
                {"title": "The Odin Project", "type": "Curriculum", "url": "https://theodinproject.com"},
                {"title": "CS50 Introduction to Computer Science", "type": "Course", "url": "https://cs50.harvard.edu"},
                {"title": "Roadmap.sh Full-Stack Guide", "type": "Visual Guide", "url": "https://roadmap.sh"}
            ],
            "recommended_beginner_projects": [
                "RESTful Task Management API with Auth & JWT",
                "Full-Stack Collaborative Markdown Notes App",
                "URL Shortener Microservice with Redis Caching"
            ],
            "skills": [
                ("Python", "Required", "Intermediate", "Backend scripting, server development, and automation.", 8),
                ("JavaScript", "Required", "Intermediate", "Dynamic client-side functionality and modern UI frameworks.", 8),
                ("SQL", "Required", "Intermediate", "Relational database schema modeling, queries, and migrations.", 7),
                ("Git", "Required", "Intermediate", "Branching, rebasing, pull requests, and CI/CD triggers.", 7),
                ("Docker", "Preferred", "Beginner", "Creating consistent environments and isolated microservices.", 6),
                ("Problem Solving", "Required", "Intermediate", "Data structures and algorithm optimization under time limits.", 8)
            ]
        },
        {
            "slug": "ai-ml-engineer",
            "title": "AI & Machine Learning Engineer",
            "category": "Artificial Intelligence",
            "description": "Bridges the gap between research models and production systems, designing scalable ML pipelines, LLM architectures, and real-time inference engines.",
            "salary_range": "$110,000 - $175,000 / yr",
            "market_outlook": "Explosive Demand (+38% Growth)",
            "responsibilities": [
                "Design and deploy production machine learning pipelines and vector search indexes.",
                "Fine-tune pre-trained foundation models and optimize inference latency with ONNX/TensorRT.",
                "Monitor model drift, latency, and data quality in production environments.",
                "Integrate retrieval-augmented generation (RAG) frameworks with enterprise databases."
            ],
            "entry_roles": ["Junior ML Engineer", "AI Associate", "Applied AI Developer"],
            "learning_resources": [
                {"title": "DeepLearning.AI Short Courses", "type": "Applied Courses", "url": "https://deeplearning.ai"},
                {"title": "Hugging Face NLP Course", "type": "Open Tutorials", "url": "https://huggingface.co/learn"}
            ],
            "recommended_beginner_projects": [
                "RAG Document Assistant with ChromaDB & LangChain",
                "Real-Time Image Classification API using FastAPI & PyTorch",
                "Sentiment Analysis Pipeline with Model Explainability"
            ],
            "skills": [
                ("Python", "Required", "Advanced", "Primary language for PyTorch, transformers, and model inference.", 10),
                ("Machine Learning", "Required", "Advanced", "Deep learning, attention mechanisms, loss functions, evaluation.", 9),
                ("Docker", "Required", "Intermediate", "Packaging models into deterministic deployable containers.", 8),
                ("Statistics", "Required", "Intermediate", "Mathematical validation, loss landscape intuition, probability.", 8),
                ("Git", "Required", "Intermediate", "Experiment versioning and pipeline orchestration.", 7)
            ]
        },
        {
            "slug": "cybersecurity-analyst",
            "title": "Cybersecurity Analyst",
            "category": "Cybersecurity",
            "description": "Protects organizational infrastructure, networks, and confidential data from cyber threats, vulnerabilities, and unauthorized access.",
            "salary_range": "$80,000 - $130,000 / yr",
            "market_outlook": "High Demand (+32% Growth)",
            "responsibilities": [
                "Monitor SIEM alerts and investigate potential security breaches or anomalies.",
                "Conduct vulnerability assessments and penetration testing on web applications.",
                "Configure firewalls, zero-trust policies, and multi-factor authentication systems.",
                "Create incident response playbooks and security awareness documentation."
            ],
            "entry_roles": ["SOC Analyst Tier 1", "Junior Security Analyst", "Information Security Specialist"],
            "learning_resources": [
                {"title": "TryHackMe Hands-on Labs", "type": "Simulations", "url": "https://tryhackme.com"},
                {"title": "OWASP Top 10 Security Guide", "type": "Documentation", "url": "https://owasp.org"}
            ],
            "recommended_beginner_projects": [
                "Home Lab Network SIEM Monitoring Setup with Wazuh",
                "Automated Python Port Scanner & Vulnerability Auditing Script",
                "OWASP Juice Shop Vulnerability Exploitation & Remediation Report"
            ],
            "skills": [
                ("Network Security", "Required", "Intermediate", "TCP/IP, packet analysis, Wireshark, routing, firewalls.", 9),
                ("Python", "Preferred", "Intermediate", "Security scripting, log parsing, and task automation.", 7),
                ("Git", "Preferred", "Beginner", "Security as code and configuration management.", 5),
                ("Problem Solving", "Required", "Intermediate", "Root cause forensics and threat modeling.", 8)
            ]
        },
        {
            "slug": "cloud-architect",
            "title": "Cloud Computing Engineer",
            "category": "Cloud Computing",
            "description": "Architects resilient, secure, and cost-optimized cloud infrastructure using modern cloud providers, infrastructure-as-code, and serverless architectures.",
            "salary_range": "$100,000 - $160,000 / yr",
            "market_outlook": "Very High (+27% Growth)",
            "responsibilities": [
                "Provision cloud infrastructure using Terraform and CloudFormation.",
                "Optimize cloud spend, compute autoscaling, and cross-region disaster recovery.",
                "Implement zero-downtime CI/CD deployment pipelines on Kubernetes."
            ],
            "entry_roles": ["Junior Cloud Engineer", "DevOps Associate", "Cloud Infrastructure Specialist"],
            "learning_resources": [
                {"title": "AWS Skill Builder", "type": "Vendor Labs", "url": "https://explore.skillbuilder.aws"}
            ],
            "recommended_beginner_projects": [
                "Terraform-Automated High-Availability Web Cluster on AWS",
                "Serverless Image Processing Pipeline with S3 and Lambda",
                "Kubernetes Multi-Tier Microservice Deployment"
            ],
            "skills": [
                ("AWS", "Required", "Intermediate", "VPC, EC2, S3, IAM, CloudWatch, Lambda architecture.", 9),
                ("Docker", "Required", "Intermediate", "Container builds, registries, and microservice networking.", 8),
                ("Python", "Preferred", "Intermediate", "Boto3 scripting and infrastructure automation.", 7),
                ("Git", "Required", "Intermediate", "GitOps and continuous deployment pipelines.", 7)
            ]
        },
        {
            "slug": "ui-ux-designer",
            "title": "UI/UX Product Designer",
            "category": "UI/UX Design",
            "description": "Creates intuitive, accessible, and delightful digital user experiences by combining user research, wireframing, interactive prototyping, and design systems.",
            "salary_range": "$75,000 - $125,000 / yr",
            "market_outlook": "Steady (+16% Growth)",
            "responsibilities": [
                "Conduct user interviews, synthesize personas, and map user journey flows.",
                "Build low-fidelity wireframes and interactive high-fidelity prototypes in Figma.",
                "Maintain reusable UI component libraries and design tokens.",
                "Conduct usability testing to validate product hypotheses before code implementation."
            ],
            "entry_roles": ["Junior UI Designer", "Associate Product Designer", "UX Researcher"],
            "learning_resources": [
                {"title": "Figma Community Tutorials", "type": "Design Files", "url": "https://figma.com/@community"},
                {"title": "Nielsen Norman Group UX Articles", "type": "Research", "url": "https://nngroup.com"}
            ],
            "recommended_beginner_projects": [
                "Redesign of a Complex FinTech Mobile App Onboarding Flow",
                "Comprehensive Design System with Responsive Component Tokens",
                "End-to-End E-Commerce Checkout Usability Audit and Redesign"
            ],
            "skills": [
                ("Figma", "Required", "Advanced", "Component variants, auto-layout, interactive prototypes, design tokens.", 10),
                ("UX Research", "Required", "Intermediate", "Formative interviews, heuristic evaluations, usability benchmarks.", 9),
                ("Problem Solving", "Required", "Intermediate", "Simplifying convoluted workflows into intuitive interactions.", 8)
            ]
        },
        {
            "slug": "business-analyst",
            "title": "Business Intelligence Analyst",
            "category": "Business Analytics",
            "description": "Transforms raw transactional data into business intelligence, KPI scorecards, and interactive dashboards to steer executive decisions.",
            "salary_range": "$70,000 - $115,000 / yr",
            "market_outlook": "High Demand (+20% Growth)",
            "responsibilities": [
                "Write complex SQL queries to extract commercial and operational metrics.",
                "Design real-time executive KPI dashboards in Tableau / PowerBI.",
                "Collaborate with department leads to define north-star business metrics."
            ],
            "entry_roles": ["Junior BI Analyst", "Commercial Operations Analyst", "Reporting Specialist"],
            "learning_resources": [
                {"title": "Microsoft PowerBI Guided Learning", "type": "Course", "url": "https://learn.microsoft.com"}
            ],
            "recommended_beginner_projects": [
                "Executive Sales & Inventory KPI Dashboard",
                "Customer Acquisition Funnel & Marketing Attribution Model"
            ],
            "skills": [
                ("SQL", "Required", "Intermediate", "Data extraction, aggregations, CTEs, and window functions.", 9),
                ("Data Visualization", "Required", "Intermediate", "Executive chart hygiene, visual hierarchy, dashboard usability.", 8),
                ("Problem Solving", "Required", "Intermediate", "Connecting numbers to practical operational actions.", 8)
            ]
        },
        {
            "slug": "digital-marketer",
            "title": "Digital Growth Strategist",
            "category": "Digital Marketing",
            "description": "Drives user acquisition, retention, and brand visibility through SEO, performance marketing, content strategy, and conversion rate optimization.",
            "salary_range": "$65,000 - $110,000 / yr",
            "market_outlook": "Moderate (+14% Growth)",
            "responsibilities": [
                "Manage paid acquisition campaigns across search and social channels.",
                "Optimize technical SEO, keyword distribution, and content funnels.",
                "Analyze Google Analytics 4 data to optimize conversion funnels."
            ],
            "entry_roles": ["Growth Marketing Associate", "SEO Specialist", "Digital Marketing Coordinator"],
            "learning_resources": [
                {"title": "Google Analytics Skillshop", "type": "Certification", "url": "https://skillshop.withgoogle.com"}
            ],
            "recommended_beginner_projects": [
                "Comprehensive SEO Audit & Content Strategy for a SaaS Brand",
                "High-Converting Landing Page & Lead Magnet Campaign"
            ],
            "skills": [
                ("Data Visualization", "Preferred", "Beginner", "Communicating campaign ROAS and conversion rates.", 6),
                ("Problem Solving", "Required", "Intermediate", "A/B testing optimization and funnel debugging.", 8)
            ]
        },
        {
            "slug": "product-manager",
            "title": "Technical Product Manager",
            "category": "Product Management",
            "description": "Guides the vision, execution, and launch of technology products, aligning engineering, design, and business teams to deliver high customer value.",
            "salary_range": "$95,000 - $160,000 / yr",
            "market_outlook": "High Demand (+18% Growth)",
            "responsibilities": [
                "Define product roadmaps, user stories, and acceptance criteria.",
                "Prioritize backlog items based on user value and engineering feasibility.",
                "Analyze user retention, telemetry metrics, and customer feedback."
            ],
            "entry_roles": ["Associate Product Manager (APM)", "Junior Product Specialist", "Product Analyst"],
            "learning_resources": [
                {"title": "Product School Resources", "type": "Guides", "url": "https://productschool.com"}
            ],
            "recommended_beginner_projects": [
                "PRD (Product Requirement Document) for an AI Workflow Feature",
                "Product Teardown & Feature Prioritization Matrix (RICE)"
            ],
            "skills": [
                ("Product Strategy", "Required", "Intermediate", "Defining OKRs, feature scopes, and roadmap prioritization.", 9),
                ("UX Research", "Preferred", "Intermediate", "User discovery interviews and problem statement validation.", 7),
                ("Problem Solving", "Required", "Advanced", "Navigating technical tradeoffs and cross-functional alignment.", 9)
            ]
        }
    ]

    career_id_map = {}
    for c_item in careers_data:
        career = Career(
            slug=c_item["slug"],
            title=c_item["title"],
            category=c_item["category"],
            description=c_item["description"],
            salary_range=c_item["salary_range"],
            market_outlook=c_item["market_outlook"]
        )
        career.responsibilities = c_item["responsibilities"]
        career.entry_roles = c_item["entry_roles"]
        career.learning_resources = c_item["learning_resources"]
        career.recommended_beginner_projects = c_item["recommended_beginner_projects"]
        db.session.add(career)
        db.session.flush()
        career_id_map[c_item["slug"]] = career.id

        # Add skills
        for s_name, imp, min_prof, why, weight in c_item["skills"]:
            cs = CareerSkill(
                career_id=career.id,
                skill_name=s_name,
                importance_level=imp,
                minimum_proficiency=min_prof,
                why_recommended=why,
                weight=weight
            )
            db.session.add(cs)

    # 3. Seed Projects
    projects_data = [
        {
            "slug": "customer-churn-prediction",
            "title": "Customer Churn Prediction with Python & Scikit-Learn",
            "career_slug": "data-scientist",
            "category": "Data Science",
            "difficulty": "Intermediate",
            "description": "Build an end-to-end machine learning pipeline that identifies subscription customers at risk of churn and generates retention recommendations.",
            "required_skills": ["Python", "Pandas", "Scikit-Learn", "Machine Learning", "Data Cleaning"],
            "suggested_tools": ["Jupyter Lab", "VS Code", "Matplotlib", "Seaborn"],
            "milestones": [
                "Phase 1: Exploratory data analysis, correlation matrix, and demographic profiling.",
                "Phase 2: Data preprocessing, missing value imputation, one-hot encoding, and feature scaling.",
                "Phase 3: Model training with Logistic Regression, Random Forest, and XGBoost with Stratified K-Fold.",
                "Phase 4: Hyperparameter tuning and model explainability via SHAP feature importance.",
                "Phase 5: Deploying an interactive prediction dashboard with Streamlit."
            ],
            "deliverables": [
                "Clean GitHub repository with README, requirements.txt, and setup instructions.",
                "Jupyter notebook demonstrating rigorous data analysis and baseline comparisons.",
                "Interactive Streamlit app allowing users to input customer traits and get churn probability."
            ]
        },
        {
            "slug": "ecommerce-sales-insights",
            "title": "E-Commerce Sales Insights Dashboard with SQL & Tableau",
            "career_slug": "data-scientist",
            "category": "Data Science",
            "difficulty": "Beginner",
            "description": "Analyze multi-year retail transactions using relational SQL queries and construct a commercial dashboard for executive decision making.",
            "required_skills": ["SQL", "Data Visualization", "Data Cleaning"],
            "suggested_tools": ["PostgreSQL/MySQL", "Tableau Public", "DBeaver"],
            "milestones": [
                "Phase 1: Design database schema and import raw CSV records into relational tables.",
                "Phase 2: Formulate SQL queries with CTEs and window functions to compute Month-over-Month growth.",
                "Phase 3: Identify top 10% high-margin products and customer cohorts.",
                "Phase 4: Design executive dashboard layout following visual hierarchy best practices."
            ],
            "deliverables": [
                "Set of documented SQL script files with performance indexing.",
                "Interactive Tableau Public workbook link with filters and drill-down KPIs."
            ]
        },
        {
            "slug": "end-to-end-llm-rag-pipeline",
            "title": "Enterprise RAG Document Q&A System with Vector DB",
            "career_slug": "ai-ml-engineer",
            "category": "Artificial Intelligence",
            "difficulty": "Advanced",
            "description": "Architect a Retrieval-Augmented Generation (RAG) assistant that indexes technical documentation into a vector database and answers queries with citations.",
            "required_skills": ["Python", "Machine Learning", "Docker", "Git"],
            "suggested_tools": ["FastAPI", "LangChain", "ChromaDB", "Docker"],
            "milestones": [
                "Phase 1: Document chunking, recursive text splitting, and token count optimization.",
                "Phase 2: Generating dense semantic embeddings and storing them in ChromaDB.",
                "Phase 3: Hybrid search retrieval combining BM25 keyword search with vector cosine similarity.",
                "Phase 4: Building FastAPI backend with prompt defense and streaming LLM responses.",
                "Phase 5: Containerizing backend and frontend with Docker Compose."
            ],
            "deliverables": [
                "Production-ready Dockerized microservice repository.",
                "Live demonstration video and automated evaluation benchmark report."
            ]
        },
        {
            "slug": "task-management-api",
            "title": "Secure Microservice API with JWT Authentication & CI/CD",
            "career_slug": "software-engineer",
            "category": "Software Development",
            "difficulty": "Beginner",
            "description": "Design and build a robust backend REST API featuring user registration, rate limiting, token refresh flows, and automated GitHub Actions test pipelines.",
            "required_skills": ["Python", "SQL", "Git", "Docker"],
            "suggested_tools": ["Flask/FastAPI", "PostgreSQL", "GitHub Actions", "Postman"],
            "milestones": [
                "Phase 1: Database relational schema design and migration setup.",
                "Phase 2: Implement password hashing, JWT generation, and token revocation.",
                "Phase 3: CRUD endpoints with input validation and HTTP status codes.",
                "Phase 4: Writing unit and integration tests with 85%+ coverage.",
                "Phase 5: Configuring GitHub Actions CI workflow to run linter and test suite on push."
            ],
            "deliverables": [
                "GitHub repository with green CI badge and Swagger/OpenAPI documentation.",
                "Postman API collection with sample request payloads."
            ]
        }
    ]

    for p in projects_data:
        c_id = career_id_map.get(p["career_slug"])
        proj = Project(
            slug=p["slug"],
            title=p["title"],
            career_id=c_id,
            category=p["category"],
            difficulty=p["difficulty"],
            description=p["description"]
        )
        proj.required_skills = p["required_skills"]
        proj.suggested_tools = p["suggested_tools"]
        proj.milestones = p["milestones"]
        proj.deliverables = p["deliverables"]
        db.session.add(proj)

    # 4. Seed Interview Questions & Quizzes
    questions_data = [
        # Technical Questions
        {
            "career_slug": "data-scientist",
            "category": "Technical",
            "role_tag": "Data Science",
            "difficulty": "Medium",
            "question": "Explain the difference between bagging and boosting ensemble techniques. When would you prefer Random Forest over XGBoost?",
            "sample_answer": "Bagging (Bootstrap Aggregating) trains multiple base estimators in parallel on random bootstrap samples of the training data and averages their predictions to reduce variance without increasing bias. Random Forest is a prime example. Boosting trains models sequentially, where each new tree focuses on the residual errors of preceding trees to reduce both bias and variance (e.g., XGBoost, LightGBM). I prefer Random Forest when I want a quick, robust baseline that is relatively immune to overfitting and requires minimal hyperparameter tuning. I prefer XGBoost when maximizing predictive performance on tabular data and when computing resources allow careful tuning of learning rates and regularization.",
            "rubric": {
                "relevance": 25,
                "clarity": 25,
                "completeness": 25,
                "technical_correctness": 25
            },
            "explanation": "Clear distinction between parallel vs sequential training, variance vs bias impact, and practical deployment considerations."
        },
        {
            "career_slug": "data-scientist",
            "category": "Technical",
            "role_tag": "Data Science",
            "difficulty": "Medium",
            "question": "How do you detect and handle multicollinearity in regression models, and what problems does it cause?",
            "sample_answer": "Multicollinearity occurs when two or more independent predictor variables in a multiple regression model are highly linearly correlated. It inflates the variance of coefficient estimates, making them unstable and difficult to interpret. We detect it using correlation matrices (e.g. Pearson r > 0.8) and calculating Variance Inflation Factor (VIF > 5-10 indicates problematic collinearity). We handle it by: 1) Dropping redundant features, 2) Combining collinear features using dimensionality reduction (PCA), or 3) Applying L2 Ridge regularization which shrinks coefficients toward zero without dropping them.",
            "rubric": {
                "relevance": 25,
                "clarity": 25,
                "completeness": 25,
                "technical_correctness": 25
            },
            "explanation": "Evaluates understanding of statistical diagnostics, VIF metrics, and remediation strategies."
        },
        # Multiple Choice Quiz Questions
        {
            "career_slug": "data-scientist",
            "category": "Quiz",
            "role_tag": "Data Science",
            "difficulty": "Easy",
            "question": "Which SQL clause is executed FIRST in logical query processing order?",
            "options": ["SELECT", "WHERE", "FROM", "HAVING"],
            "correct_answer": "FROM",
            "sample_answer": "FROM is processed first to determine the working dataset and table joins.",
            "rubric": {},
            "explanation": "Logical SQL execution order begins with FROM / JOIN, followed by WHERE, GROUP BY, HAVING, SELECT, and finally ORDER BY / LIMIT."
        },
        {
            "career_slug": "data-scientist",
            "category": "Quiz",
            "role_tag": "Data Science",
            "difficulty": "Medium",
            "question": "When evaluating an imbalanced classification problem where false negatives are far more costly than false positives (e.g. cancer detection), which metric should you prioritize?",
            "options": ["Accuracy", "Precision", "Recall (Sensitivity)", "Specificity"],
            "correct_answer": "Recall (Sensitivity)",
            "sample_answer": "Recall measures the proportion of actual positives correctly identified.",
            "rubric": {},
            "explanation": "Recall = TP / (TP + FN). When false negatives are catastrophic, maximizing recall ensures as few actual positive cases as possible slip through undetected."
        },
        # Behavioral Questions
        {
            "career_slug": "data-scientist",
            "category": "Behavioral",
            "role_tag": "All Careers",
            "difficulty": "Medium",
            "question": "Tell me about a time when a project or model didn't yield the results you or your team expected. How did you handle it?",
            "sample_answer": "In our e-commerce recommendation project, our initial collaborative filtering model failed to improve click-through rates during preliminary A/B testing because of severe cold-start issues for newly listed items. Recognizing the bottleneck, I organized a sprint to pivot our architecture to a hybrid model incorporating content-based metadata (tags, categories, price). I communicated the issue transparently to our product manager with data visualizations of the distribution gap. Within two weeks, the hybrid model improved cold-start item engagement by 34% and we launched the update safely.",
            "rubric": {
                "relevance": 25,
                "clarity": 25,
                "completeness": 25,
                "technical_correctness": 25
            },
            "explanation": "Look for honest reflection, analytical root-cause diagnosis, structured STAR format, and constructive resolution."
        }
    ]

    for q in questions_data:
        c_id = career_id_map.get(q.get("career_slug"))
        iq = InterviewQuestion(
            career_id=c_id,
            category=q["category"],
            role_tag=q["role_tag"],
            difficulty=q["difficulty"],
            question=q["question"],
            correct_answer=q.get("correct_answer"),
            sample_answer=q.get("sample_answer"),
            explanation=q.get("explanation")
        )
        iq.options = q.get("options", [])
        iq.rubric = q.get("rubric", {})
        db.session.add(iq)

    db.session.flush()

    # 5. Seed Demonstration User: Alex Chen pursuing Data Science
    ds_career_id = career_id_map.get("data-scientist")

    demo_user = User(
        full_name="Alex Chen",
        email="alex.chen@nextleap.demo",
        education_level="Bachelor of Science in Computer Science (Junior Year)",
        current_course="Data Structures & Algorithms, Database Systems",
        interests="Data Science, Machine Learning, Python, Applied Statistics",
        preferred_career_goal="Data Scientist",
        target_career_id=ds_career_id,
        learning_style="Hands-on Project Building & Interactive Coding",
        weekly_hours=14,
        bio="Aspiring Data Scientist passionate about converting unstructured data into actionable predictive insights. Building open-source projects in Python and statistical modeling.",
        github_url="https://github.com/alexchen-demo",
        linkedin_url="https://linkedin.com/in/alexchen-demo",
        portfolio_url="https://alexchen.dev",
        theme_preference="dark"
    )
    demo_user.set_password("demo_password123")
    db.session.add(demo_user)
    db.session.flush()

    # Seed User Skills for Alex Chen
    demo_skills = [
        ("Python", "Programming", "Intermediate", True, "Comfortable with Pandas, NumPy, and OOP scripts."),
        ("Statistics", "Mathematics", "Beginner", False, "Studying probability distributions and hypothesis testing."),
        ("Data Visualization", "Data", "Beginner", False, "Created basic charts in Matplotlib and Seaborn."),
        ("Problem Solving", "Soft Skills", "Intermediate", True, "Solved 120+ algorithmic challenges.")
    ]
    for s_name, s_cat, s_prof, s_ver, s_notes in demo_skills:
        us = UserSkill(
            user_id=demo_user.id,
            skill_name=s_name,
            category=s_cat,
            proficiency=s_prof,
            is_verified=s_ver,
            notes=s_notes
        )
        db.session.add(us)

    # Seed Personalized Roadmap for Alex Chen
    from services.roadmap_engine import generate_personalized_roadmap
    ds_career = Career.query.get(ds_career_id)
    if ds_career:
        roadmap = generate_personalized_roadmap(demo_user, ds_career)

    # Seed User Project for Alex Chen
    sample_proj_1 = Project.query.filter_by(slug="customer-churn-prediction").first()
    if sample_proj_1:
        up1 = UserProject(
            user_id=demo_user.id,
            project_id=sample_proj_1.id,
            status="Completed",
            progress_percent=100,
            notes="Implemented Random Forest and XGBoost with 84% ROC-AUC score. Published Streamlit interactive demo.",
            repo_url="https://github.com/alexchen-demo/customer-churn-predictor",
            live_url="https://customer-churn-demo.streamlit.app",
            in_portfolio=True,
            completed_at=datetime.utcnow() - timedelta(days=5)
        )
        db.session.add(up1)

    sample_proj_2 = Project.query.filter_by(slug="ecommerce-sales-insights").first()
    if sample_proj_2:
        up2 = UserProject(
            user_id=demo_user.id,
            project_id=sample_proj_2.id,
            status="In Progress",
            progress_percent=55,
            notes="Finished SQL data cleaning queries and window function metrics. Now connecting to Tableau Public.",
            repo_url="https://github.com/alexchen-demo/ecommerce-sales-insights",
            in_portfolio=False
        )
        db.session.add(up2)

    # Seed Sample Interview Attempt
    first_q = InterviewQuestion.query.filter_by(category="Technical").first()
    if first_q:
        attempt = InterviewAttempt(
            user_id=demo_user.id,
            question_id=first_q.id,
            user_answer="Bagging trains several models independently in parallel on bootstrap samples of training data to reduce variance, like in Random Forests. Boosting trains models sequentially where each new model tries to correct the errors of previous models, like XGBoost. I would pick Random Forest for high stability and ease of tuning.",
            score=86,
            feedback="Great answer! You clearly differentiated parallel vs sequential training and highlighted variance reduction. For even higher scores, mention bias reduction in boosting and specific hyperparameter tuning considerations.",
            created_at=datetime.utcnow() - timedelta(days=2)
        )
        attempt.criteria_breakdown = {
            "relevance": 23,
            "clarity": 22,
            "completeness": 20,
            "technical_correctness": 21
        }
        db.session.add(attempt)

    # Seed Welcome Notifications
    notifs = [
        Notification(
            user_id=demo_user.id,
            title="Welcome to NEXT LEAP 2.0!",
            message="Your Data Science personalized roadmap and skill gap analyzer are primed and ready.",
            notification_type="success",
            link="/dashboard"
        ),
        Notification(
            user_id=demo_user.id,
            title="Next LEAP Recommended Action",
            message="Your skill gap highlights SQL as a critical missing competency. Complete SQL JOIN drills to unlock your next milestone.",
            notification_type="action",
            link="/skill-gap"
        )
    ]
    for n in notifs:
        db.session.add(n)

    db.session.commit()
    print("--- Database Seeding Completed Successfully! ---")

# NEXT LEAP 2.0
> **"Discover Your Potential. Build Your Skills. Shape Your Future."**

An AI-powered, full-stack career development platform architected for students, graduates, and career changers. NEXT LEAP 2.0 guides users from high-level career discovery down to the single most impactful learning action to take today.

---

## 🌟 Core Product Principle

> *"NEXT LEAP doesn't just tell you where you could go. It helps you decide what to do next."*

---

## 🚀 Key Modules & Features

1. **Brand Identity & SaaS Interface**
   - Premium SaaS aesthetic with Deep Navy (`#0B1020`), Electric Blue (`#4F7CFF`), and Violet (`#8B5CF6`).
   - Dynamic dark mode & clean light mode toggle.
   - Fully responsive on desktop, tablet, and mobile.

2. **Hero Landing Page**
   - Live interactive dashboard preview widget.
   - Structured walkthrough: Methodology, Discovery, Skill Gaps, Roadmap, Projects, Interviews, and FAQs.

3. **Authentication & User Profile Management**
   - User registration with education level, course, interests, and target career.
   - Secure server-side password hashing (Werkzeug PBKDF2/SHA256).
   - Instant **1-Click Hackathon Demo Mode** (log in directly as Alex Chen).
   - Editable student profile, learning preferences, and weekly hours.

4. **Main Student Dashboard**
   - Summary Metric Cards: Target Career, Skills Recorded, Roadmap Progress %, Completed Projects.
   - **"Your Next LEAP" Signature Engine**: Prioritizes the highest-leverage immediate action with estimated effort, reason, and one-click completion.
   - Interactive Chart.js visualizations: Career Readiness Radar & Weekly Learning Hours.
   - Upcoming Milestones checklist & Recent Activities feed.

5. **AI Career Discovery**
   - Covers 9 core domains: Data Science, Software Development, AI & ML, Cybersecurity, Cloud Computing, UI/UX Design, Business Analytics, Digital Marketing, Product Management.
   - Multi-factor match scoring based on user profile and skills.
   - Side-by-side career comparison tool.
   - One-click target career calibration.

6. **Skill Gap Analyzer**
   - Quantifies readiness against industry requirements.
   - Categorizes competencies into **Mastered**, **Level-Up Needed**, and **Critical Missing Gaps**.
   - Interactive radar charts comparing user proficiencies against benchmarks.
   - Add/update skills with instant recalculation.

7. **Personalized 5-Phase Learning Roadmap**
   - Phase 1: Fundamentals
   - Phase 2: Core Technical Skills
   - Phase 3: Practical Applications
   - Phase 4: Portfolio Projects
   - Phase 5: Interview Preparation
   - Interactive checkboxes auto-recalculate progress percentages.
   - Custom milestone creation (set title, description, hours, target dates).

8. **Project Studio & Public Portfolio**
   - Tiered project catalog (Beginner, Intermediate, Advanced) with milestones and deliverables.
   - Workspace tracker with progress sliders, GitHub repository URLs, live demo URLs, and architecture notes.
   - Shareable student portfolio page for recruiters and mentors.

9. **Interview Preparation Arena**
   - Technical questions, behavioral questions (STAR method), and multiple-choice quizzes.
   - Interactive Mock Interview submission evaluated with a transparent 4-factor rubric:
     - Relevance (0-25)
     - Clarity (0-25)
     - Completeness (0-25)
     - Technical Rigor (0-25)
   - Exemplary model answers and quiz explanations.

10. **AI Career Coach**
    - Context-aware career assistant calibrated to the user's active goals, skills, and weekly availability.
    - Quick prompt pills for fast guidance.
    - **Hybrid Architecture**: Connects to Google Gemini or OpenAI when API keys are configured; otherwise uses our deterministic expert engine with complete transparency.

---

## 🛠️ Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+), Chart.js, Lucide Icons
- **Backend**: Python 3.12+, Flask 3.x, Flask-SQLAlchemy, Werkzeug
- **Database**: 
  - **MySQL 8.0+** (fully supported via PyMySQL with provided `schema.sql` and `seed.sql`)
  - **SQLite** (pre-configured default for immediate zero-friction execution)

---

## 📂 Project Structure

```
next-leap/
│
├── app.py                     # Application entry point & factory
├── config.py                  # Database & environment configuration
├── requirements.txt           # Python dependencies
├── .env.example               # Template environment variables
├── .env                       # Active environment configuration
├── README.md                  # Comprehensive documentation
│
├── routes/
│   ├── auth.py                # Register, login, logout, demo login
│   ├── dashboard.py           # Dashboard overview, next action API
│   ├── careers.py             # Career discovery, matching & comparison
│   ├── skills.py              # Skill gap analyzer & competency management
│   ├── roadmap.py             # 5-phase curriculum & milestone tracking
│   ├── projects.py            # Project studio & public portfolio
│   ├── interviews.py          # Technical questions, MCQs & mock rubric scoring
│   ├── coach.py               # AI Career Coach chat endpoints
│   └── user_profile.py        # Profile editing, settings & demo reset
│
├── services/
│   ├── career_engine.py       # Career matching & comparison logic
│   ├── skill_gap_engine.py    # Readiness score & gap analysis algorithm
│   ├── roadmap_engine.py      # 5-phase personalized curriculum generator
│   ├── next_action_engine.py  # Signature Next LEAP recommendation engine
│   ├── ai_service.py          # LLM integrations (Gemini/OpenAI) + expert fallback
│   └── seed_service.py        # Automated reference & demo dataset populator
│
├── models/
│   ├── __init__.py            # SQLAlchemy database instance
│   ├── user.py                # User account & preferences model
│   ├── career.py              # Career & CareerSkill models
│   ├── skill.py               # Skill catalog & UserSkill models
│   ├── roadmap.py             # Roadmap, RoadmapPhase & RoadmapTask models
│   ├── project.py             # Project & UserProject models
│   ├── interview.py           # InterviewQuestion & InterviewAttempt models
│   └── notification.py        # User notifications model
│
├── templates/
│   ├── base.html              # Core layout shell & navigation
│   ├── landing.html           # Landing page with live preview & sections
│   ├── login.html             # Login form with 1-click demo button
│   ├── register.html          # Registration form
│   ├── dashboard.html         # Main student dashboard
│   ├── careers.html           # Career discovery catalog & compare modal
│   ├── career_detail.html     # Deep-dive career page
│   ├── skill_gap.html         # Skill gap analyzer & radar charts
│   ├── roadmap.html           # Visual 5-phase curriculum timeline
│   ├── projects.html          # Project studio & active tracker
│   ├── portfolio.html         # Verified public student portfolio
│   ├── interviews.html        # Mock interviews & quizzes
│   ├── coach.html             # AI Career Coach chat interface
│   ├── profile.html           # Profile settings & skill management
│   └── settings.html          # Platform settings & demo reset
│
├── static/
│   ├── css/
│   │   ├── style.css          # Design system & landing styling
│   │   └── dashboard.css      # SaaS dashboard & component styling
│   └── js/
│       ├── app.js             # Global utilities & theme toggle
│       ├── dashboard.js       # Chart.js graphs & Next Action handlers
│       ├── careers.js         # Career filters & comparison modals
│       ├── roadmap.js         # Milestone checkboxes & custom task modal
│       ├── projects.js        # Progress sliders & portfolio toggles
│       └── interviews.js      # Mock answer rubrics & quiz checks
│
└── database/
    ├── schema.sql             # Relational DDL schema
    ├── seed.sql               # Reference SQL data
    └── nextleap.db            # Auto-generated SQLite instance
```

---

## ⚡ Quick Start Guide

### 1. Prerequisites
- Python 3.10+ installed
- (Optional) MySQL 8.0+ if choosing to use MySQL

### 2. Installation
Navigate to the project directory:
```bash
cd next-leap
```

Install the dependencies:
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
Copy the example environment file:
```bash
cp .env.example .env
```

To run with default SQLite (zero setup required):
Leave `DATABASE_URL` commented out.

To connect to MySQL:
Uncomment and set `DATABASE_URL` in `.env`:
```env
DATABASE_URL=mysql+pymysql://root:yourpassword@localhost:3306/nextleap_db
```

### 4. Running the Application
Start the Flask development server:
```bash
python app.py
```
Open your browser and navigate to:
```
http://localhost:5000
```

---

## 🎯 Hackathon Demonstration Workflow

1. **Landing Page**: Visit `http://localhost:5000` to inspect the value proposition, live preview card, and feature sections.
2. **Instant Demo Login**: Click **"Demo Mode"** in the top navigation or on the login page to immediately sign in as **Alex Chen** (`alex.chen@nextleap.demo`).
3. **Overview Dashboard**:
   - Inspect the **"Your Next LEAP"** signature card.
   - Click **"Mark Done & Next"** to watch the recommendation engine dynamically update.
   - View the **Career Readiness Radar** and **Weekly Learning Pace** charts.
4. **Skill Gap Analyzer**: Navigate to `/skill-gap` to see the breakdown of Mastered, Level-Up, and Missing skills. Click **"Mark Learned"** on a missing skill to observe instant score recalculation.
5. **My Roadmap**: Navigate to `/roadmap`. Check off tasks to watch the phase and overall progress bars update smoothly in real time. Click **"Add Task"** to add a custom milestone.
6. **Project Studio**: Navigate to `/projects`. Adjust progress sliders on active projects, add GitHub URLs, and toggle **"Add to Portfolio"**.
7. **Interview Prep**: Navigate to `/interviews`.
   - Take the Multiple Choice Quiz to test instant answer validation.
   - Submit an answer to a technical mock question to receive a scored 4-criteria rubric evaluation.
8. **AI Career Coach**: Navigate to `/coach`. Click any suggested prompt pill (e.g. *"What should I learn next?"*) to see context-aware responses incorporating your active profile.
9. **Theme Toggle**: Click the Moon/Sun icon in the top navigation to switch between Dark Navy and Clean Light mode.

---

## 🛡️ Security Features
- **Password Protection**: Passwords are hashed using salted PBKDF2 with SHA-256 before persistence.
- **Session Security**: Session cookies configured with `HttpOnly` and `SameSite=Lax`.
- **Authorization Guards**: Authenticated routes enforce `@login_required` decorators.
- **Data Isolation**: Users can only modify their own roadmap tasks, projects, skills, and attempts.
- **Secret Hygiene**: Sensitive credentials stored strictly in environment variables.

---

## 🤝 Troubleshooting

- **Port in Use**: If port 5000 is occupied, run with a custom port: `PORT=5050 python app.py`.
- **Resetting Demo Data**: If sample data is deleted or modified during testing, go to `/settings` and click **"Restore Data Science Demo Dataset"**.
#   N E X T _ L E A P  
 
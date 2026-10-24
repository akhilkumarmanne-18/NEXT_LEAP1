-- NEXT LEAP 2.0 Database Schema
-- Compatible with MySQL 8.0+ and SQLite

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(120) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    education_level VARCHAR(100) DEFAULT 'Undergraduate',
    current_course VARCHAR(150) DEFAULT 'Computer Science',
    interests VARCHAR(500) DEFAULT 'Artificial Intelligence, Data Science',
    preferred_career_goal VARCHAR(100) DEFAULT 'Data Scientist',
    target_career_id INT NULL,
    learning_style VARCHAR(50) DEFAULT 'Hands-on Project Building',
    weekly_hours INT DEFAULT 12,
    bio TEXT NULL,
    github_url VARCHAR(250) NULL,
    linkedin_url VARCHAR(250) NULL,
    portfolio_url VARCHAR(250) NULL,
    theme_preference VARCHAR(20) DEFAULT 'dark',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_user_email (email)
);

CREATE TABLE IF NOT EXISTS careers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    slug VARCHAR(80) UNIQUE NOT NULL,
    title VARCHAR(120) NOT NULL,
    category VARCHAR(80) NOT NULL,
    description TEXT NOT NULL,
    salary_range VARCHAR(80) DEFAULT '$75,000 - $135,000 / yr',
    market_outlook VARCHAR(80) DEFAULT 'High Demand (+23% Growth)',
    responsibilities_json TEXT,
    entry_roles_json TEXT,
    learning_resources_json TEXT,
    recommended_beginner_projects_json TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_career_slug (slug),
    INDEX idx_career_category (category)
);

CREATE TABLE IF NOT EXISTS skills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    category VARCHAR(80) DEFAULT 'General',
    description TEXT,
    INDEX idx_skill_name (name)
);

CREATE TABLE IF NOT EXISTS career_skills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    career_id INT NOT NULL,
    skill_name VARCHAR(100) NOT NULL,
    importance_level VARCHAR(20) DEFAULT 'Required',
    minimum_proficiency VARCHAR(20) DEFAULT 'Intermediate',
    why_recommended TEXT NOT NULL,
    weight INT DEFAULT 5,
    FOREIGN KEY (career_id) REFERENCES careers(id) ON DELETE CASCADE,
    INDEX idx_cs_career (career_id)
);

CREATE TABLE IF NOT EXISTS user_skills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    skill_name VARCHAR(100) NOT NULL,
    category VARCHAR(80) DEFAULT 'Technical',
    proficiency VARCHAR(30) DEFAULT 'Beginner',
    is_verified BOOLEAN DEFAULT FALSE,
    notes VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_us_user (user_id)
);

CREATE TABLE IF NOT EXISTS roadmaps (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    career_id INT NULL,
    title VARCHAR(150) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (career_id) REFERENCES careers(id) ON DELETE SET NULL,
    INDEX idx_rm_user (user_id)
);

CREATE TABLE IF NOT EXISTS roadmap_phases (
    id INT AUTO_INCREMENT PRIMARY KEY,
    roadmap_id INT NOT NULL,
    phase_number INT NOT NULL DEFAULT 1,
    title VARCHAR(120) NOT NULL,
    description TEXT,
    FOREIGN KEY (roadmap_id) REFERENCES roadmaps(id) ON DELETE CASCADE,
    INDEX idx_rp_roadmap (roadmap_id)
);

CREATE TABLE IF NOT EXISTS roadmap_tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    phase_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    skills_involved VARCHAR(255) DEFAULT '',
    estimated_hours INT DEFAULT 5,
    target_date VARCHAR(50),
    status VARCHAR(30) DEFAULT 'Pending',
    is_custom BOOLEAN DEFAULT FALSE,
    order_index INT DEFAULT 0,
    completed_at DATETIME NULL,
    FOREIGN KEY (phase_id) REFERENCES roadmap_phases(id) ON DELETE CASCADE,
    INDEX idx_rt_phase (phase_id)
);

CREATE TABLE IF NOT EXISTS projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    slug VARCHAR(100) UNIQUE NOT NULL,
    title VARCHAR(150) NOT NULL,
    career_id INT NULL,
    category VARCHAR(80) DEFAULT 'Technical',
    difficulty VARCHAR(30) DEFAULT 'Beginner',
    description TEXT NOT NULL,
    required_skills_json TEXT,
    suggested_tools_json TEXT,
    milestones_json TEXT,
    deliverables_json TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (career_id) REFERENCES careers(id) ON DELETE SET NULL,
    INDEX idx_proj_slug (slug)
);

CREATE TABLE IF NOT EXISTS user_projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    project_id INT NULL,
    custom_title VARCHAR(150) NULL,
    status VARCHAR(30) DEFAULT 'In Progress',
    progress_percent INT DEFAULT 0,
    notes TEXT,
    repo_url VARCHAR(255),
    live_url VARCHAR(255),
    in_portfolio BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE SET NULL,
    INDEX idx_up_user (user_id)
);

CREATE TABLE IF NOT EXISTS interview_questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    career_id INT NULL,
    category VARCHAR(50) NOT NULL DEFAULT 'Technical',
    role_tag VARCHAR(80) DEFAULT 'Data Science',
    difficulty VARCHAR(30) DEFAULT 'Medium',
    question TEXT NOT NULL,
    options_json TEXT,
    correct_answer VARCHAR(255),
    sample_answer TEXT,
    rubric_json TEXT,
    explanation TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (career_id) REFERENCES careers(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS interview_attempts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    question_id INT NOT NULL,
    user_answer TEXT NOT NULL,
    score INT DEFAULT 0,
    feedback TEXT,
    criteria_breakdown_json TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES interview_questions(id) ON DELETE CASCADE,
    INDEX idx_ia_user (user_id)
);

CREATE TABLE IF NOT EXISTS notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(120) NOT NULL,
    message TEXT NOT NULL,
    notification_type VARCHAR(30) DEFAULT 'info',
    link VARCHAR(255),
    is_read BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_notif_user (user_id)
);

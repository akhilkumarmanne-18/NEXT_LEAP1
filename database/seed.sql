-- NEXT LEAP 2.0 Sample Data Seeding
-- For MySQL installations

INSERT INTO skills (name, category, description) VALUES
('Python', 'Programming', 'Versatile language for backend, automation, and data.'),
('SQL', 'Database', 'Structured query language for relational databases.'),
('Statistics', 'Mathematics', 'Probability, distributions, hypothesis testing.'),
('Machine Learning', 'AI/ML', 'Supervised, unsupervised, regression, classification.'),
('Data Visualization', 'Data', 'Matplotlib, Seaborn, Tableau, PowerBI storytelling.'),
('Data Cleaning', 'Data', 'Handling missing values, outlier detection, normalization.'),
('Problem Solving', 'Soft Skills', 'Algorithmic thinking and breaking down challenges.'),
('JavaScript', 'Frontend', 'Interactive web frontends and asynchronous workflows.'),
('React', 'Frontend', 'Component-based user interface engineering.'),
('Docker', 'DevOps', 'Containerization and local reproducible environments.'),
('AWS', 'Cloud', 'Amazon Web Services compute, storage, and networking.'),
('Git', 'Tools', 'Version control, branching, PRs, and collaborative repos.');

INSERT INTO careers (slug, title, category, description, salary_range, market_outlook, responsibilities_json, entry_roles_json, learning_resources_json, recommended_beginner_projects_json) VALUES
('data-scientist', 'Data Scientist', 'Data Science', 'Analyzes complex datasets to extract actionable insights, build predictive models, and optimize business decisions through data-driven intelligence.', '$95,000 - $155,000 / yr', 'Very High (+26% Growth)', '["Formulate business questions into statistical hypotheses.", "Extract, clean, and integrate data using SQL and Python.", "Develop and fine-tune machine learning models."]', '["Junior Data Scientist", "Data Analyst", "Quantitative Analyst"]', '[{"title": "Kaggle Learn", "url": "https://kaggle.com/learn"}]', '["Customer Churn Prediction", "Sales Analytics Dashboard"]'),
('software-engineer', 'Software Engineer', 'Software Development', 'Architects, develops, tests, and maintains modern web, cloud, and distributed software systems.', '$85,000 - $145,000 / yr', 'High Demand (+22% Growth)', '["Write clean, testable code.", "Build scalable RESTful APIs.", "Collaborate across teams."]', '["Associate Software Engineer", "Junior Backend Developer"]', '[{"title": "The Odin Project", "url": "https://theodinproject.com"}]', '["Task Management API", "Collaborative Notes App"]');

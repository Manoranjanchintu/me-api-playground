-- Seed the Profile
INSERT INTO profiles (name, email, education, work_links)
VALUES (
    'Manoranjan Sahoo', 
    'manoranjansahoo1313@example.com', 
    'MCA at Candigarh University', 
    '{"github": "https://github.com/Manoranjanchintu", "linkedin": "https://www.linkedin.com/in/manoranjansahoo1319/", "portfolio": "https://www.behance.net/manoranjansahoo8"}'
);

-- Seed Skills
INSERT INTO skills (name, proficiency, is_top, profile_id) VALUES 
('Python', 'Expert', true, 1),
('React', 'Advanced', true, 1),
('Docker', 'Intermediate', true, 1),
('FastAPI', 'Expert', false, 1),
('PostgreSQL', 'Advanced', false, 1);

-- Seed Projects
INSERT INTO projects (title, description, links, profile_id) VALUES 
(
    'Me-API Playground', 
    'A personal API playground with FastAPI and React.', 
    '{"repo": "https://github.com/manor/me-api-playground"}',
    1
),
(
    'Task Master', 
    'A task management application built with Django.', 
    '{"demo": "https://taskmaster.demo"}',
    1
);

-- Seed Project Skills (Linking projects to skills)
-- Python(1), React(2), Docker(3), FastAPI(4), Postgres(5)
-- Me-API Playground(1) uses Python, React, Docker, FastAPI
INSERT INTO project_skills (project_id, skill_id) VALUES 
(1, 1), (1, 2), (1, 3), (1, 4),
(2, 1);

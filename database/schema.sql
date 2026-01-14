-- profiles table
CREATE TABLE IF NOT EXISTS profiles (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    education TEXT,
    work_links TEXT
);

-- skills table
CREATE TABLE IF NOT EXISTS skills (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    proficiency VARCHAR,
    is_top BOOLEAN DEFAULT FALSE,
    profile_id INTEGER REFERENCES profiles(id)
);

-- projects table
CREATE TABLE IF NOT EXISTS projects (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    description TEXT,
    links TEXT,
    profile_id INTEGER REFERENCES profiles(id)
);

-- project_skills join table
CREATE TABLE IF NOT EXISTS project_skills (
    project_id INTEGER REFERENCES projects(id),
    skill_id INTEGER REFERENCES skills(id),
    PRIMARY KEY (project_id, skill_id)
);

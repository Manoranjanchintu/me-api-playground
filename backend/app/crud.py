from sqlalchemy.orm import Session
from . import models, schemas
import json

# -----------------------------
# Profile CRUD
# -----------------------------
def get_profile(db: Session):
    return db.query(models.Profile).first()

def create_profile(db: Session, profile: schemas.ProfileCreate):
    # Check if profile exists
    existing = get_profile(db)
    if existing:
        return existing
    
    db_profile = models.Profile(
        name=profile.name,
        education=profile.education,
        work_links=profile.work_links  # JSON as text
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

def update_profile(db: Session, profile: schemas.ProfileCreate):
    db_profile = get_profile(db)
    if not db_profile:
        return create_profile(db, profile)
    
    db_profile.name = profile.name
    db_profile.education = profile.education
    db_profile.work_links = profile.work_links
    
    db.commit()
    db.refresh(db_profile)
    return db_profile

def delete_profile(db: Session):
    db_profile = get_profile(db)
    if db_profile:
        db.delete(db_profile)
        db.commit()
    return {"message": "Profile deleted"}

# -----------------------------
# Skills CRUD
# -----------------------------
def get_skills(db: Session, top: bool = False):
    query = db.query(models.Skill)
    if top:
        query = query.filter(models.Skill.is_top == True)
    return query.all()

def create_skill(db: Session, skill: schemas.SkillCreate, profile_id: int):
    # Check if exists
    db_skill = db.query(models.Skill).filter(
        models.Skill.name == skill.name, 
        models.Skill.profile_id == profile_id
    ).first()
    if db_skill:
        return db_skill
        
    db_skill = models.Skill(**skill.dict(), profile_id=profile_id)
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill

# -----------------------------
# Projects CRUD
# -----------------------------
def get_projects(db: Session, skill_name: str = None):
    if skill_name:
        return db.query(models.Project).join(models.Project.skills).filter(
            models.Skill.name.ilike(f"%{skill_name}%")
        ).all()
    return db.query(models.Project).all()

def create_project(db: Session, project: schemas.ProjectCreate, profile_id: int):
    # Handle skills
    skills = []
    for s_name in project.skill_names:
        s = db.query(models.Skill).filter(
            models.Skill.name == s_name, 
            models.Skill.profile_id == profile_id
        ).first()
        if not s:
            s = models.Skill(name=s_name, profile_id=profile_id)
            db.add(s)
        skills.append(s)
    
    db_project = models.Project(
        title=project.title,
        description=project.description,
        links=project.links,
        profile_id=profile_id
    )
    db_project.skills = skills
    
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

# -----------------------------
# Search helper
# -----------------------------
def search(db: Session, query: str):
    projects = db.query(models.Project).filter(
        (models.Project.title.ilike(f"%{query}%")) | 
        (models.Project.description.ilike(f"%{query}%"))
    ).all()
    
    skills = db.query(models.Skill).filter(
        models.Skill.name.ilike(f"%{query}%")
    ).all()
    
    return {"projects": projects, "skills": skills}

# -----------------------------
# Seed / Reset helpers
# -----------------------------
def seed_database(db: Session):
    # Create profile
    profile_data = schemas.ProfileCreate(
        name="Manoranjan Sahoo",
        education="MCA in AI & ML",
        work_links=json.dumps({
            "github": "https://github.com/Manoranjanchintu",
            "linkedin": "https://linkedin.com/in/manoranjansahoo"
        })
    )
    profile = create_profile(db, profile_data)
    
    # Create skills
    skill_names = ["Python", "React", "FastAPI", "SQL", "Machine Learning"]
    for name in skill_names:
        skill_data = schemas.SkillCreate(
            name=name,
            proficiency="Expert" if name in ["Python", "SQL"] else "Intermediate",
            is_top=True if name in ["Python", "SQL"] else False
        )
        create_skill(db, skill_data, profile.id)
    
    # Create projects
    project_samples = [
        {
            "title": "Smart Headcount",
            "description": "Project to manage employee headcount",
            "links": json.dumps({
                "demo": "",
                "repo": "https://github.com/Manoranjanchintu/smart-headcount"
            }),
            "skill_names": ["Python", "SQL"]
        },
        {
            "title": "Fitnex App",
            "description": "Preventive Health & Wellness App UI",
            "links": json.dumps({
                "demo": "",
                "repo": "https://github.com/Manoranjanchintu/fitnex"
            }),
            "skill_names": ["React", "FastAPI"]
        }
    ]
    
    for p in project_samples:
        project_data = schemas.ProjectCreate(
            title=p["title"],
            description=p["description"],
            links=p["links"],
            skill_names=p["skill_names"]
        )
        create_project(db, project_data, profile.id)
    
    return {"status": "seed completed"}

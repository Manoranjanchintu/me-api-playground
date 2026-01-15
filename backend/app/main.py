from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from . import models, database, crud
from .routers import profile, projects, skills

# Create tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Me-API Playground")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(profile.router)
app.include_router(projects.router)
app.include_router(skills.router)

@app.get("/")
def root():
    return {"message": "Welcome to Me-API Playground"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/search")
def search(q: str, db: Session = Depends(database.get_db)):
    return crud.search(db, query=q)

# ----------------------------
# DATABASE UTILITIES
# ----------------------------

@app.post("/reset-db")
def reset_db(db: Session = Depends(database.get_db)):
    try:
        db.execute(text("DROP TABLE IF EXISTS project_skills CASCADE"))
        db.execute(text("DROP TABLE IF EXISTS projects CASCADE"))
        db.execute(text("DROP TABLE IF EXISTS skills CASCADE"))
        db.execute(text("DROP TABLE IF EXISTS profiles CASCADE"))
        db.commit()

        models.Base.metadata.create_all(bind=database.engine)

        return {"status": "database reset complete"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}


@app.post("/seed")
def seed_db(db: Session = Depends(database.get_db)):
    try:
        # Create profile
        profile = models.Profile(
            name="Manoranjan Sahoo",
            email="manoranjan@example.com",
            education="MCA in AI & ML",
            work_links='{"github": "https://github.com/Manoranjanchintu"}'
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)

        # Create skills
        skill1 = models.Skill(name="Python", proficiency="Expert", is_top=True, profile_id=profile.id)
        skill2 = models.Skill(name="FastAPI", proficiency="Intermediate", is_top=True, profile_id=profile.id)
        skill3 = models.Skill(name="React", proficiency="Intermediate", is_top=False, profile_id=profile.id)

        db.add_all([skill1, skill2, skill3])
        db.commit()

        # Create projects
        project1 = models.Project(
            title="Me API Playground",
            description="Personal portfolio API with FastAPI and PostgreSQL",
            links='{"repo": "https://github.com/Manoranjanchintu"}',
            profile_id=profile.id
        )

        project1.skills = [skill1, skill2]

        db.add(project1)
        db.commit()

        return {"status": "database seeded"}

    except Exception as e:
        return {"status": "error", "detail": str(e)}

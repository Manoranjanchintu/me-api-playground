from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text

from . import models, database, crud
from .routers import profile, projects, skills


# Create DB tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Me-API Playground")


# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routers
app.include_router(profile.router)
app.include_router(projects.router)
app.include_router(skills.router)


# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to Me-API Playground API"}


# Health check
@app.get("/health")
def health_check():
    return {"status": "ok"}


# Database test
@app.get("/db-test")
def db_test(db: Session = Depends(database.get_db)):
    try:
        result = db.execute(text("SELECT 1")).fetchone()
        return {"database_result": result[0], "status": "connected"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}


# Search endpoint
@app.get("/search")
def search(q: str, db: Session = Depends(database.get_db)):
    return crud.search(db, query=q)


# Seed database with sample data
@app.post("/seed")
def seed_database(db: Session = Depends(database.get_db)):
    try:
        # Insert sample skills
        db.execute(text("""
            INSERT INTO skills (name, level)
            VALUES 
            ('Python', 'Advanced'),
            ('FastAPI', 'Intermediate'),
            ('React', 'Beginner')
        """))

        # Insert sample projects
        db.execute(text("""
            INSERT INTO projects (title, description)
            VALUES
            ('Smart Headcount System', 'AI based crowd counting system'),
            ('Me API Playground', 'Personal profile API using FastAPI')
        """))

        db.commit()
        return {"status": "success", "message": "Database seeded successfully"}

    except Exception as e:
        db.rollback()
        return {"status": "error", "detail": str(e)}

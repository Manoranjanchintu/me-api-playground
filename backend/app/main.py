from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, database, crud
from .routers import profile, projects, skills

# Create tables is not usually done here in prod (migrations preferable), but per req minimal setup:
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Me-API Playground")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, specify domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(profile.router)
app.include_router(projects.router)
app.include_router(skills.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/search")
def search(q: str, db: Session = Depends(database.get_db)):
    return crud.search(db, query=q)

@app.get("/")
def root():
    return {"message": "Welcome to Me-API Playground"}

@app.get("/db-test")
def db_test(db: Session = Depends(database.get_db)):
    try:
        # Simple query to check connection
        result = db.execute("SELECT 1").fetchone()
        return {"database_result": result[0], "status": "connected"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from . import models, database, crud

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
        return crud.seed_database(db)
    except Exception as e:
        return {"status": "error", "detail": str(e)}

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import crud, schemas, database

router = APIRouter(
    prefix="/projects",
    tags=["projects"]
)

@router.get("/", response_model=List[schemas.Project])
def read_projects(skill: Optional[str] = None, db: Session = Depends(database.get_db)):
    return crud.get_projects(db, skill_name=skill)

@router.post("/", response_model=schemas.Project)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(database.get_db)):
    # Assuming profile exists, pick the first one as "me"
    profile = crud.get_profile(db)
    if not profile:
        raise HTTPException(status_code=400, detail="Profile must exist before creating projects")
    return crud.create_project(db, project, profile_id=profile.id)

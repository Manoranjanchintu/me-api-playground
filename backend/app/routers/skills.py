from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas, database

router = APIRouter(
    prefix="/skills",
    tags=["skills"]
)

@router.get("/top", response_model=List[schemas.Skill])
def read_top_skills(db: Session = Depends(database.get_db)):
    return crud.get_skills(db, top=True)

@router.get("/", response_model=List[schemas.Skill])
def read_skills(db: Session = Depends(database.get_db)):
    return crud.get_skills(db)

@router.post("/", response_model=schemas.Skill)
def create_skill(skill: schemas.SkillCreate, db: Session = Depends(database.get_db)):
    profile = crud.get_profile(db)
    if not profile:
        raise HTTPException(status_code=400, detail="Profile must exist before creating skills")
    return crud.create_skill(db, skill, profile_id=profile.id)

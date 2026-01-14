from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, database

router = APIRouter(
    prefix="/profile",
    tags=["profile"]
)

@router.get("/", response_model=schemas.Profile)
def read_profile(db: Session = Depends(database.get_db)):
    profile = crud.get_profile(db)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.post("/", response_model=schemas.Profile)
def create_profile(profile: schemas.ProfileCreate, db: Session = Depends(database.get_db)):
    return crud.create_profile(db, profile)

@router.put("/", response_model=schemas.Profile)
def update_profile(profile: schemas.ProfileCreate, db: Session = Depends(database.get_db)):
    return crud.update_profile(db, profile)

@router.delete("/")
def delete_profile(db: Session = Depends(database.get_db)):
    return crud.delete_profile(db)

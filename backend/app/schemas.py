from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Json

# Skill Schemas
class SkillBase(BaseModel):
    name: str
    proficiency: Optional[str] = None
    is_top: bool = False

class SkillCreate(SkillBase):
    pass

class Skill(SkillBase):
    id: int
    
    class Config:
        orm_mode = True

# Project Schemas
class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None
    links: Optional[str] = None # JSON string or plain text representation
    # Could use Dict if we handle serialization manually, but keeping it simple for now as per minimal reqs

class ProjectCreate(ProjectBase):
    skill_names: List[str] = [] # List of skill names to associate

class Project(ProjectBase):
    id: int
    skills: List[Skill] = []

    class Config:
        orm_mode = True

# Profile Schemas
class ProfileBase(BaseModel):
    name: str
    email: str
    education: Optional[str] = None
    work_links: Optional[str] = None # JSON string

class ProfileCreate(ProfileBase):
    pass

class Profile(ProfileBase):
    id: int
    projects: List[Project] = []
    skills: List[Skill] = []

    class Config:
        orm_mode = True

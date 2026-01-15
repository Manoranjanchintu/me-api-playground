from typing import List, Optional
from pydantic import BaseModel

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
    links: Optional[str] = None  # JSON string

class ProjectCreate(ProjectBase):
    skill_names: List[str] = []

class Project(ProjectBase):
    id: int
    skills: List[Skill] = []
    class Config:
        orm_mode = True

# Profile Schemas
class ProfileBase(BaseModel):
    name: str
    email: Optional[str] = None
    education: Optional[str] = None
    work_links: Optional[str] = None  # JSON string

class ProfileCreate(ProfileBase):
    pass

class Profile(ProfileBase):
    id: int
    skills: List[Skill] = []
    projects: List[Project] = []
    class Config:
        orm_mode = True

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base

# Many-to-Many relationship between Projects and Skills
project_skills = Table(
    "project_skills",
    Base.metadata,
    Column("project_id", Integer, ForeignKey("projects.id")),
    Column("skill_id", Integer, ForeignKey("skills.id"))
)

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    education = Column(Text, nullable=True)
    work_links = Column(Text, nullable=True)  # JSON stored as text

    skills = relationship("Skill", back_populates="profile", cascade="all, delete-orphan")
    projects = relationship("Project", back_populates="profile", cascade="all, delete-orphan")

class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    proficiency = Column(String, nullable=True)
    is_top = Column(Boolean, default=False)
    profile_id = Column(Integer, ForeignKey("profiles.id"))

    profile = relationship("Profile", back_populates="skills")
    projects = relationship("Project", secondary=project_skills, back_populates="skills")

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    links = Column(Text, nullable=True)  # JSON as text
    profile_id = Column(Integer, ForeignKey("profiles.id"))

    profile = relationship("Profile", back_populates="projects")
    skills = relationship("Skill", secondary=project_skills, back_populates="projects")

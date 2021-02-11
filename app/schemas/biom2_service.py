from typing import List, Optional

from pydantic import BaseModel


class ProjectBase(BaseModel):
    name: str


class ProjectCreate(ProjectBase):
    pass


class Project(ProjectBase):
    id: int

    class Config:
        orm_mode = True


class Biom2ServiceBase(BaseModel):
    name: str
    major_version: Optional[int] = 0
    minor_version: Optional[int] = 0
    patch_version: Optional[int] = 1
    url: Optional[str] = ''
    type: Optional[str] = ''
    environment: Optional[str] = ''
    friendly_name: Optional[str] = ''
    description: Optional[str] = ''
    icon_url: Optional[str] = ''
    source_link: Optional[str] = ''
    docs_link: Optional[str] = ''


class Biom2ServiceCreate(Biom2ServiceBase):
    pass


class Biom2Service(Biom2ServiceBase):
    id: int
    projects: List[Project] = []

    class Config:
        orm_mode = True



from typing import List

from pydantic import BaseModel


class Biom2ServiceBase(BaseModel):
    id: str
    name: str
    major_version: int
    minor_version: int
    patch_version: int
    url: str
    type: str
    environment: str
    projects: List[str]
    friendly_name: str
    description: str
    icon_url: str
    source_link: str
    docs_link: str

    class Config:
        orm_mode = True


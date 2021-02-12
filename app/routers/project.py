from fastapi import APIRouter, Depends
from fastapi_versioning import version
from sqlalchemy.orm import Session

from dependencies.database import get_db
from repositories.biom2_service_repository import get_projects

router = APIRouter(tags=["project"])


@router.get("/projects")
@version(1)
async def read_project(db: Session = Depends(get_db)):
    projects = get_projects(db)

    return {"projects": [projects]}

from typing import Optional

from fastapi import APIRouter, Depends
from fastapi_versioning import version
from sqlalchemy.orm import Session

from dependencies.database import get_db
from repositories.pod_service_repository import *

router = APIRouter(tags=["endpoint"])


@router.get("/endpoints")
@version(1)
async def read_service_endpoint(type: Optional[str] = None, environment: Optional[str] = None,
                                project: Optional[str] = None, db: Session = Depends(get_db)):

    if project is not None:
        services = get_pod_services_by_project(db, project)
    else:
        services = get_pod_services(db)

    if type is not None:
        services = list(filter(lambda service: service.type == type, services))

    if environment is not None:
        services = list(filter(lambda service: service.environment == environment, services))

    return {"items": [services]}

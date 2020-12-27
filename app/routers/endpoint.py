from fastapi import APIRouter, Depends
from fastapi_versioning import version
from sqlalchemy.orm import Session

from dependencies.database import get_db
from repositories.biom2_service_repository import get_biom2_services

router = APIRouter(tags=["endpoint"])


@router.get("/endpoints")
@version(1)
async def read_service_endpoint(db: Session = Depends(get_db)):
    services = get_biom2_services(db)
    return {"items": [services]}

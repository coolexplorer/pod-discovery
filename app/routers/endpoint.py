from fastapi import APIRouter
from fastapi_versioning import version

from app.schemas.biom2_service import Biom2Service
from app.utils.logger import logger

router = APIRouter()


@router.get("/endpoints", response_model=Biom2Service)
@version(1)
async def read_service_endpoint():
    logger.debug("/endpoints")
    return {"items": []}

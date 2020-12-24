import logging

from fastapi import APIRouter
from fastapi_versioning import version


logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/endpoints")
@version(1)
async def read_service_endpoint():
    return {"items": []}

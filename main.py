import logging

import uvicorn
from fastapi import FastAPI
from fastapi_versioning import VersionedFastAPI

from config.configuration import Configuration
from routers import endpoint, root

# log
from services.service_accounts import ServiceAccounts

logger = logging.getLogger(__name__)

# FastAPI
app = FastAPI(
    title="biom2-discovery",
    description="BioMetrics2 App and Service discovery service under the kubernetes"
)

# routers
app.include_router(root.router, tags=["root"])
app.include_router(endpoint.router, tags=["endpoint"])

# Versioned_FastAPI
app = VersionedFastAPI(app,
                       prefix_format='/v{major}',
                       version_format='{major}')

# Service Account
config = Configuration()
config.read_env()
service_accounts = ServiceAccounts(config)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)

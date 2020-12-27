import logging

import uvicorn
from fastapi import FastAPI, Depends
from fastapi_versioning import VersionedFastAPI

from app.config.configuration import Configuration
from app.routers import root
from app.routers import endpoint

# log
from app.schedules.schedule import Schedule
from app.services.service_accounts import ServiceAccounts

logger = logging.getLogger(__name__)

# FastAPI
app = FastAPI(
    title="biom2-discovery",
    description="BioMetrics2 App and Service discovery service under the kubernetes"
)

# Service Account
config = Configuration()
config.read_env()
service_accounts = ServiceAccounts(config)

# Schedule
schedule = Schedule(service_accounts.k8s)
schedule.add_discovery_cron_job('*/10', 'search_biom2_pod')
schedule.start()


# routers
def get_k8s_service_account():
    return service_accounts.k8s


app.include_router(root.router, tags=["root"])
app.include_router(endpoint.router, tags=["endpoint"], dependencies=[Depends(get_k8s_service_account)])

# Versioned_FastAPI
app = VersionedFastAPI(app,
                       prefix_format='/v{major}',
                       version_format='{major}')


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)

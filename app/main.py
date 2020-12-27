import logging

import uvicorn
from fastapi import FastAPI, Depends
from fastapi_versioning import VersionedFastAPI

from app import models
from app.config.configuration import Configuration
from app.database.database import engine, SessionLocal, Base
from app.routers import root
from app.routers import endpoint

# log
from app.schedules.schedule import Schedule
from app.services.service_accounts import ServiceAccounts


Base.metadata.create_all(bind=engine)


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
schedule.add_discovery_cron_job('*/20', 'search_biom2_pod')
schedule.start()


# routers
app.include_router(root.router)
app.include_router(endpoint.router)

# Versioned_FastAPI
app = VersionedFastAPI(app,
                       prefix_format='/v{major}',
                       version_format='{major}')


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)

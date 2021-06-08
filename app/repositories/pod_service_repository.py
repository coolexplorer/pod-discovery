from sqlalchemy.orm import Session

from models.pod_service import PodService, Project, services_projects
from utils.logger import logger


def get_pod_services(db: Session):
    return db.query(PodService).all()


def get_pod_services_by_project(db: Session, project):
    return db.query(PodService).filter(PodService.projects.any(name=project)).all()


def create_pod_service(db: Session, pod_service, projects):
    db_pod_service = PodService(
        name=pod_service.name,
        major_version=pod_service.major_version,
        minor_version=pod_service.minor_version,
        patch_version=pod_service.patch_version,
        url=pod_service.url,
        type=pod_service.type,
        environment=pod_service.environment,
        friendly_name=pod_service.friendly_name,
        description=pod_service.description,
        icon_url=pod_service.icon_url,
        source_link=pod_service.source_link,
        docs_link=pod_service.docs_link
    )

    # make relationship with project
    if len(projects) != 0:
        for project in projects:
            pro = get_project(db, project)
            if pro is None:
                insert_project(db, project)

            pro = get_project(db, project)
            db_pod_service.projects.append(pro)

    return db_pod_service


def insert_project(db: Session, project):
    db.add(Project(name=project))
    db.commit()


def get_project(db: Session, project):
    return db.query(Project).filter(Project.name == project).first()


def get_projects(db: Session):
    return db.query(Project).all()


def insert_services(db: Session, pod_services):
    db.add_all(pod_services)
    db.commit()


def delete_service_all_rows(db: Session):
    try:
        # delete all rows
        services = db.query(PodService).all()

        for service in services:
            for project in service.projects:
                db.delete(project)
            db.delete(service)
        db.commit()
    except Exception:
        logger.debug("Deletion failed")
        db.rollback()

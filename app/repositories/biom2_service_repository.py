from sqlalchemy.orm import Session

from models.biom2_service import Biom2Service


def get_biom2_services(db: Session):
    return db.query(Biom2Service).all()


def get_biom2_services_by_project(db: Session, project):
    return db.query(Biom2Service).filter(Biom2Service.projects.name == project)

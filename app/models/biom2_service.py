from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref

from database.database import Base

services_projects = Table('services_projects', Base.metadata,
                          Column('service_id', Integer, ForeignKey('biom2services.id')),
                          Column('project_id', Integer, ForeignKey('projects.id'))
                          )


class Biom2Service(Base):
    __tablename__ = "biom2services"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    major_version = Column(Integer)
    minor_version = Column(Integer)
    patch_version = Column(Integer)
    url = Column(String)
    type = Column(String)
    environment = Column(String)
    friendly_name = Column(String)
    description = Column(String)
    icon_url = Column(String)
    source_link = Column(String)
    docs_link = Column(String)
    projects = relationship("Project", secondary=services_projects, backref="biom2services", lazy="dynamic")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    def __repr__(self):
        return "<Project('%s')>" % self.name

from sqlalchemy import Column, Integer, String, ARRAY

from app.database.database import Base


class Biom2Service(Base):
    __tablename__ = "biom2services"

    id = Column(Integer, primary_key=True, index=True)
    name: Column(String, unique=True)
    major_version: Column(Integer)
    minor_version: Column(Integer)
    patch_version: Column(Integer)
    url: Column(String)
    type: Column(String)
    projects: Column(ARRAY(String))
    environment: Column(String)
    friendly_name: Column(String)
    description: Column(String)
    icon_url: Column(String)
    source_link: Column(String)
    docs_link: Column(String)

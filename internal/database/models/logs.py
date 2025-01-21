import uuid

from sqlalchemy import Column, DateTime, JSON, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Logs(Base):
    __tablename__ = 'logs'
    id = Column(String(255), primary_key=True, default=lambda: str(uuid.uuid4()))
    json = Column(JSON, nullable=False)
    time = Column(DateTime, nullable=False)

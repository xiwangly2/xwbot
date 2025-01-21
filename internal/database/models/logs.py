from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Logs(Base):
    __tablename__ = 'logs'
    id = Column(String(255), primary_key=True)
    json = Column(String(255), nullable=False)
    time = Column(String(255), nullable=False)

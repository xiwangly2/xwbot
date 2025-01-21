from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Switch(Base):
    __tablename__ = 'switch'
    group_id = Column(String(255), primary_key=True)
    switch = Column(String(255), primary_key=True, nullable=False)
    time = Column(String(255), nullable=False)

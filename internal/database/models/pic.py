import uuid

from sqlalchemy import Column, String, LargeBinary
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Pic(Base):
    __tablename__ = 'pic'
    id = Column(String(255), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False)
    bin = Column(LargeBinary, nullable=False)
    sha256 = Column(String(255), nullable=False)
    md5 = Column(String(255), nullable=False)

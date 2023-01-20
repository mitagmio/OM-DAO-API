from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import JSONB

from app.config.database import Base


class Config(Base):
    __tablename__ = 'config'
    id = Column(Integer, primary_key=True)
    data = Column(JSONB, default={})

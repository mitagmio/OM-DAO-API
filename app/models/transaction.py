from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import JSONB

from app.config.database import Base


class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    data = Column(JSONB, default={})

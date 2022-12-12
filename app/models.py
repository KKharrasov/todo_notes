from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from core.db import Base
from user.models import User


class Note(Base):
    __tablename__ = 'note'
    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String)
    description = Column(String(10000))
    user_id = Column(Integer, ForeignKey('user.id'))
    created_timestamp = Column(DateTime)
    updated_timestamp = Column(DateTime)
    status = Column(String)

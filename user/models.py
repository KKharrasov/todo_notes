from sqlalchemy import Column, String, Integer, DateTime
from core.db import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    created_timestamp = Column(DateTime)
    updated_timestamp = Column(DateTime)

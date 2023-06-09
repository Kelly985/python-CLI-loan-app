from sqlalchemy import Column, Integer, String, DateTime, Boolean
from database import Base
from datetime import datetime


class Admin(Base):
    __tablename__ = 'admins'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    

    def __init__(self, username, password):
        self.username = username
        self.password = password
      
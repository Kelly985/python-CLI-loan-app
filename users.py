from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    loans_rel = relationship('Loan', back_populates='user_rel')
    payments_rel = relationship('Payment', back_populates='user_rel')

    def __init__(self, username, password):
        # Initialize the User object with the provided username and password
        self.username = username
        self.password = password

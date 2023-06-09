from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Payment(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True)
    pay_amount = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'))
    user_rel = relationship('User', back_populates='payments_rel')
    loan_id = Column(Integer, ForeignKey('loans.id'))
    loan_rel = relationship('Loan', back_populates='payments_rel')

    def __init__(self, pay_amount, user_rel, loan_rel):
        self.pay_amount = pay_amount
        self.user_rel = user_rel
        self.loan_rel = loan_rel

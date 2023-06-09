from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime, timedelta

class Loan(Base):
    __tablename__ = 'loans'
    id = Column(Integer, primary_key=True)
    loan_type = Column(Integer)
    amount = Column(Float)
    amount_to_pay = Column(Float)
    expected_payment_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'))
    user_rel = relationship('User', back_populates='loans_rel')
    payments_rel = relationship('Payment', back_populates='loan_rel')

    def __init__(self, loan_type, amount, amount_to_pay, user_rel):
        # Initialize the Loan object with the provided attributes
        self.loan_type = loan_type
        self.amount = amount
        self.amount_to_pay = amount_to_pay
        self.expected_payment_date = self.calculate_expected_payment_date()
        self.user_rel = user_rel

    def calculate_expected_payment_date(self):
        # Calculate the expected payment date based on the loan type
        if self.loan_type == 1:  # Week-long plan
            return datetime.utcnow() + timedelta(days=7)
        elif self.loan_type == 2:  # Monthly plan
            return datetime.utcnow() + timedelta(days=30)
        elif self.loan_type == 3:  # 3-month long plan
            return datetime.utcnow() + timedelta(days=90)
        elif self.loan_type == 4:  # 6-month long plan
            return datetime.utcnow() + timedelta(days=180)
        elif self.loan_type == 5:  # Yearly plan
            return datetime.utcnow() + timedelta(days=365)
        else:
            return None

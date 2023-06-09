from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from users import User
from loans import Loan
from payments import Payment
from faker import Faker
import random


def seed_data():
    engine = create_engine('sqlite:///loans.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    # Seeding logic
    fake = Faker()

    users = []
    # Create fake users
    for _ in range(10):
        username = fake.user_name()
        password = fake.password(length=8)
        masked_password = '*' * len(password)  # Generate asterisks of the same length
        user = User(username=username, password=masked_password)
        session.add(user)
        users.append(user)  # Append the user object to the 'users' list


    # Create fake loans
    for _ in range(20):
        loan_type = fake.random_int(min=1, max=5)
        loan_amount = fake.random_int(min=1000, max=10000)
        user = random.choice(users)  # Assuming 'users' is a list of User objects
        interest_rate = random.uniform(0.05, 0.25)  # Random interest rate between 5% and 25%
        amount_to_pay = loan_amount * (1 + interest_rate)  # Calculate amount to pay
        loan = Loan(loan_type=loan_type, amount=loan_amount, amount_to_pay=amount_to_pay, user_rel=user)

        session.add(loan)

    session.commit()

if __name__ == "__main__":
    seed_data()

from getpass import getpass
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exists
from database import Base
from users import User
from admins import Admin
from loans import Loan
from payments import Payment

# Create the database engine
engine = create_engine('sqlite:///loans.db')

# Create a session factory
Session = sessionmaker(bind=engine)

# Create a session
session = Session()

# Create the tables
Base.metadata.create_all(engine)


def sign_up():
    while True:
        user_type = input("Enter user type (1 for User, 2 for Admin): ")
        username = input("Enter a username: ")
        existing_user = session.query(User).filter_by(username=username).first()
        if existing_user:
            print("Username already exists. Please choose a different username.")
        else:
            break

    password = getpass("Enter a password: ")
    # Save the password as asterisks
    password = "*" * len(password)

    if user_type == "1":
        # Create a new user
        user = User(username=username, password=password)
    elif user_type == "2":
        # Create a new admin
        user = Admin(username=username, password=password)
    else:
        print("Invalid user type.")
        return

    session.add(user)
    session.commit()
    print("Sign up successful!")







def user_sign_in():
    # Prompt the user to enter their username and password
    username = input("Enter your username: ")
    password = getpass("Enter your password: ")

    # Query the database to find a user with the given username and password
    user = session.query(User).filter_by(username=username, password="*" * len(password)).first()

    # If a user is found, the sign-in is successful
    if user:
        print("User sign in successful!")
        return user

    # If no user is found, the sign-in is unsuccessful
    print("Invalid username or password.")
    return None

def admin_sign_in():
    # Prompt the admin to enter their username and password
    username = input("Enter your username: ")
    password = getpass("Enter your password: ")

    # Query the database to find an admin with the given username and password
    admin = session.query(Admin).filter_by(username=username, password="*" * len(password)).first()

    # If an admin is found, the sign-in is successful
    if admin:
        print("Admin sign in successful!")
        return admin

    # If no admin is found, the sign-in is unsuccessful
    print("Invalid username or password.")
    return None






def borrow_loan(user):
    # Display the available loan types to the user
    print("Available loan types:")
    print("1. Week-long plan (5% interest)")
    print("2. Monthly plan (10% interest)")
    print("3. 3-month long plan (15% interest)")
    print("4. 6-month long plan (20% interest)")
    print("5. Yearly plan (25% interest)")

    # Prompt the user to choose a loan type and enter the loan amount
    loan_type = int(input("Choose a loan type (1-5): "))
    loan_amount = float(input("Enter the loan amount: "))

    # Determine the interest rate based on the chosen loan type
    if loan_type == 1:
        interest_rate = 0.05
    elif loan_type == 2:
        interest_rate = 0.10
    elif loan_type == 3:
        interest_rate = 0.15
    elif loan_type == 4:
        interest_rate = 0.20
    elif loan_type == 5:
        interest_rate = 0.25
    else:
        # If an invalid loan type is entered, display an error message and return
        print("Invalid loan type.")
        return

    # Calculate the total payment including the loan amount and interest
    total_payment = loan_amount * (1 + interest_rate)
    print("Total payment:", total_payment)

    # Create a Loan object with the chosen loan type, loan amount, total payment, and user relationship
    loan = Loan(loan_type=loan_type, amount=loan_amount, amount_to_pay=total_payment, user_rel=user)

    # Add the loan object to the session and commit the changes to the database
    session.add(loan)
    session.commit()

    # Display a success message to indicate that the loan has been borrowed successfully
    print("Loan borrowed successfully!")



def pay_loan(user):
    # Prompt the user to enter the loan ID and payment amount
    loan_id = int(input("Enter the loan ID: "))
    payment_amount = float(input("Enter the payment amount: "))

    # Retrieve the loan from the database based on the loan ID and user relationship
    loan = session.query(Loan).filter_by(id=loan_id, user_rel=user).first()
    if loan:
        # If the loan is found, calculate the remaining loan amount after the payment
        total_payment = loan.amount_to_pay
        remaining_amount = total_payment - payment_amount
        print("Remaining loan amount:", remaining_amount)

        # Create a Payment object with the payment amount, user relationship, and loan relationship
        payment = Payment(pay_amount=payment_amount, user_rel=user, loan_rel=loan)

        # Add the payment object to the session and commit the changes to the database
        session.add(payment)
        session.commit()
    else:
        # If the loan is not found or the user does not have access to the loan, display an error message
        print("Invalid loan ID or you do not have access to this loan.")



def view_loan_history(user):
    # Retrieve all loans associated with the user from the database
    loans = session.query(Loan).filter_by(user_rel=user).all()
    loan_details = []

    # Iterate over each loan and gather relevant loan information
    for loan in loans:
        loan_type = loan.loan_type
        loan_amount = loan.amount
        interest_rates = {1: 0.05, 2: 0.10, 3: 0.15, 4: 0.20, 5: 0.25}

        # Check if the loan type is valid and retrieve the corresponding interest rate
        if loan_type in interest_rates:
            interest_rate = interest_rates[loan_type]
        else:
            print("Invalid loan type.")
            continue

        # Calculate the total payment and remaining amount based on the loan amount and interest rate
        total_payment = loan_amount * (1 + interest_rate)
        remaining_amount = total_payment - sum(payment.pay_amount for payment in loan.payments_rel)
        expected_payment_date = loan.expected_payment_date.strftime("%Y-%m-%d %H:%M:%S")

        # Store the loan information in a dictionary
        loan_info = {
            "Loan ID": loan.id,
            "Loan Type": loan_type,
            "Loan Amount": loan_amount,
            "Total Payment": total_payment,
            "Remaining Amount": remaining_amount,
            "Expected Payment Date": expected_payment_date
        }
        loan_details.append(loan_info)

    # Display the loan history
    print("Loan History:")
    if loan_details:
        for loan_info in loan_details:
            print("{")
            for key, value in loan_info.items():
                print(f"  {key}: {value}")
            print("}")
            print("-----------------------------")
    else:
        print("No loan history found.")




def analysis_of_loans():
    # Define loan types and initialize dictionaries to store loan totals and counts
    loan_types = {
        1: "Week-long plan",
        2: "Monthly plan",
        3: "3-month long plan",
        4: "6-month long plan",
        5: "Yearly plan"
    }
    loan_totals = {loan_type: 0 for loan_type in loan_types}
    loan_counts = {loan_type: 0 for loan_type in loan_types}

    # Retrieve all loans from the database
    loans = session.query(Loan).all()

    # Iterate over each loan and calculate loan totals and counts for each loan type
    for loan in loans:
        loan_type = loan.loan_type
        loan_amount = loan.amount
        loan_totals[loan_type] += loan_amount
        loan_counts[loan_type] += 1

    # Calculate the grand total of all loans
    grand_total = sum(loan_totals.values())

    # Display the analysis of loans as tuples
    print("Analysis of Loans:")
    for loan_type, loan_name in loan_types.items():
        total_amount = loan_totals[loan_type]
        loan_count = loan_counts[loan_type]
        loan_info = (
            ("Loan Type", loan_name),
            ("Total Amount", total_amount),
            ("Loan Count", loan_count)
        )
        print(tuple(f"({key}, {value})" for key, value in loan_info))
        print("-----------------------------")

    # Calculate and display the average loan amount and grand total
    loan_count = sum(loan_counts.values())  # Total number of loans
    average_loan_amount = grand_total / loan_count  # Calculate average loan amount
    average_info = (("Average Loan Amount", average_loan_amount),)
    grand_total_info = (("Grand Total", grand_total),)

    print(tuple(f"({key}, {value})" for key, value in average_info))
    print(tuple(f"({key}, {value})" for key, value in grand_total_info))




def profit_analysis():
    # Define loan types and initialize dictionaries to store borrowed and expected totals
    loan_types = {
        1: "Week-long plan",
        2: "Monthly plan",
        3: "3-month long plan",
        4: "6-month long plan",
        5: "Yearly plan"
    }
    borrowed_totals = {loan_type: 0 for loan_type in loan_types}
    expected_totals = {loan_type: 0 for loan_type in loan_types}

    # Retrieve all loans from the database
    loans = session.query(Loan).all()

    # Iterate over each loan and calculate borrowed and expected totals for each loan type
    for loan in loans:
        loan_type = loan.loan_type
        loan_amount = loan.amount
        interest_rate = 0.05 + (loan_type - 1) * 0.05
        expected_amount = loan_amount * (1 + interest_rate)

        borrowed_totals[loan_type] += loan_amount
        expected_totals[loan_type] += expected_amount

    # Calculate the grand totals of borrowed and expected amounts
    grand_borrowed_total = sum(borrowed_totals.values())
    grand_expected_total = sum(expected_totals.values())

    # Display the profit analysis
    print("Profit Analysis:")
    for loan_type, loan_name in loan_types.items():
        borrowed_amount = borrowed_totals[loan_type]
        expected_amount = expected_totals[loan_type]
        profit = expected_amount - borrowed_amount

        print(f"{loan_name}:")
        print("Borrowed Amount:", borrowed_amount)
        print("Expected Amount:", expected_amount)
        print("Profit:", profit)
        print("-----------------------------")

    # Display the grand totals
    print("Grand Total:")
    print("Borrowed Amount:", grand_borrowed_total)
    print("Expected Amount:", grand_expected_total)
    print("Profit:", grand_expected_total - grand_borrowed_total)


def list_borrowers():
    users = session.query(User).all()
    borrower_list = [user.username for user in users]
    print("List of Borrowers:")
    print(borrower_list)




def admin_section():
    # Display the admin section header
    print("Admin Section")
    
    while True:
        # Display available commands
        print("Available commands:")
        print("1. Sign Up")
        print("2. Sign In")
        print("3. Exit")
        option = input("Choose an option (1-3): ")

        if option == "1":
            sign_up()  # Call the sign_up function to register a new admin
        elif option == "2":
            user = admin_sign_in()  # Call the admin_sign_in function to sign in an admin
            if user:
                break  # Break the loop if the admin sign-in is successful
        elif option == "3":
            print("Exiting the program...")
            return  # Exit the admin_section function, returning to the main function
        else:
            print("Invalid option.")

    while True:
        # Display admin options
        print("Admin Options:")
        print("1. Analysis of Loans")
        print("2. Profit Analysis")
        print("3. List of Borrowers")
        print("4. Exit")
        option = input("Choose an option (1-4): ")

        if option == "1":
            analysis_of_loans()  # Call the analysis_of_loans function to perform loan analysis
        elif option == "2":
            profit_analysis()  # Call the profit_analysis function to perform profit analysis
        elif option == "3":
            list_borrowers()  # Call the list_borrowers function to display a list of borrowers
        elif option == "4":
            print("Exiting the admin section...")
            return  # Exit the admin_section function, returning to the main function
        else:
            print("Invalid option.")



def main():
    # Display a welcome message
    print("Welcome!")

    while True:
        # Display available commands
        print("Available commands:")
        print("1. User Section")
        print("2. Admin Section")
        print("3. Exit")
        option = input("Choose an option (1-3): ")

        if option == "1":
            while True:
                # Enter the user section
                print("User Section")
                print("Available commands:")
                print("1. Sign Up")
                print("2. Sign In")
                print("3. Exit")
                user_option = input("Choose an option (1-3): ")

                if user_option == "1":
                    sign_up()  # Call the sign_up function to register a new user
                elif user_option == "2":
                    user = user_sign_in()  # Call the user_sign_in function to sign in a user
                    if user:
                        while True:
                            # Enter the user actions section
                            print("User Actions")
                            print("Available commands:")
                            print("1. Borrow Loan")
                            print("2. Pay Loan")
                            print("3. View Loan History")
                            print("4. Exit")
                            user_action = input("Choose an option (1-4): ")

                            if user_action == "1":
                                borrow_loan(user)  # Call the borrow_loan function to borrow a loan
                            elif user_action == "2":
                                pay_loan(user)  # Call the pay_loan function to make a loan payment
                            elif user_action == "3":
                                view_loan_history(user)  # Call the view_loan_history function to view loan history
                            elif user_action == "4":
                                print("Exiting the user section...")
                                break  # Exit the inner while loop, returning to the main while loop
                            else:
                                print("Invalid option.")
                elif user_option == "3":
                    print("Exiting the program...")
                    break  # Exit the inner while loop, returning to the main while loop
                else:
                    print("Invalid option.")

        elif option == "2":
            admin_section()  # Call the admin_section function to enter the admin section
        elif option == "3":
            print("Exiting the program...")
            break  # Exit the main while loop, terminating the program
        else:
            print("Invalid option.")




if __name__ == "__main__":
    main()

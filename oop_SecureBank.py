
import random
import datetime

# Account Class to handle account details and PIN verification
class Account:
    def __init__(self, pin="1234", balance=1000):
        self.pin = pin
        self.balance = balance
    
    def verify_pin(self, entered_pin):
        """Verify if the entered PIN is correct."""
        return entered_pin == self.pin
    
    def check_balance(self):
        """Return the current balance."""
        return self.balance
    
    def withdraw(self, amount):
        """Withdraw a specific amount if the balance allows it."""
        if amount <= self.balance:
            self.balance -= amount
            return True
        return False
    
    def change_pin(self, new_pin):
        """Change the account PIN."""
        if len(new_pin) == 4 and new_pin.isdigit():
            self.pin = new_pin
            return True
        return False

# Transaction Class to manage different types of transactions
class Transaction:
    def __init__(self, account):
        self.account = account
        self.withdrawal_amount = 0
    
    def select_withdrawal_amount(self, amount):
        """Set the withdrawal amount after validating it."""
        self.withdrawal_amount = amount
        if self.withdrawal_amount <= 0:
            print("Please enter a valid amount.")
            return False
        elif self.withdrawal_amount > self.account.check_balance():
            print("Insufficient balance. Please choose a smaller amount.")
            return False
        return True

    def execute_withdrawal(self):
        """Perform the withdrawal and return True if successful."""
        if self.account.withdraw(self.withdrawal_amount):
            return True
        else:
            print("Withdrawal failed.")
            return False

# Receipt Class to generate and print a transaction receipt
class Receipt:
    def __init__(self, transaction, remaining_balance):
        self.transaction = transaction
        self.remaining_balance = remaining_balance

    def generate_receipt(self):
        """Print the receipt with transaction details."""
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M:%S")
        return f"""
        SecureBank
        Branch: Eastwood Alley Branch
        Date: {date}
        Time: {time}
        Amount Withdrawn: €{self.transaction.withdrawal_amount}
        Currency: EUR
        Balance: €{self.remaining_balance}
        """

# ATM Class to manage overall ATM workflow
class ATM:
    def __init__(self):
        self.account = Account()
        self.transaction = Transaction(self.account)
        self.names = ["Alice", "Bob", "Charlie", "Diana", "Edward"]
        self.is_card_inserted = False

    def insert_card(self):
        if not self.is_card_inserted:
            self.is_card_inserted = True
            print("Reading Card... Please Wait")
            self.prompt_pin()

    def prompt_pin(self):
        pin = input("Enter Your PIN: ")
        if self.account.verify_pin(pin):
            self.show_transaction_interface()
        else:
            print("Incorrect PIN. Try Again.")
            self.prompt_pin()

    def show_transaction_interface(self):
        user_name = random.choice(self.names)
        print(f"Welcome to SecureBank, {user_name}!")
        print("Choose a transaction:\n1. Withdrawal\n2. Check Balance\n3. Change PIN")
        choice = input("Enter your choice (1-3): ")
        self.handle_transaction_choice(choice)

    def handle_transaction_choice(self, choice):
        if choice == "1":
            self.withdrawal_options()
        elif choice == "2":
            self.show_balance()
        elif choice == "3":
            self.change_pin()
        else:
            print("Invalid choice, try again.")
            self.show_transaction_interface()

    def show_balance(self):
        balance = self.account.check_balance()
        print(f"Your current balance is: €{balance}")
        self.show_transaction_interface()

    def change_pin(self):
        new_pin = input("Enter new 4-digit PIN: ")
        if self.account.change_pin(new_pin):
            print("PIN changed successfully.")
        else:
            print("Invalid PIN format.")
        self.show_transaction_interface()

    def withdrawal_options(self):
        print("Choose Withdrawal Amount:\n1. €50\n2. €100\n3. €200\n4. €300\n5. Enter custom amount")
        choice = input("Enter your choice (1-5): ")
        if choice == "1":
            amount = 50
        elif choice == "2":
            amount = 100
        elif choice == "3":
            amount = 200
        elif choice == "4":
            amount = 300
        elif choice == "5":
            amount = int(input("Enter custom amount: €"))
        else:
            print("Invalid choice, returning to main menu.")
            self.show_transaction_interface()
            return

        if self.transaction.select_withdrawal_amount(amount):
            self.confirm_receipt_option()

    def confirm_receipt_option(self):
        choice = input(f"Withdrawal Amount: €{self.transaction.withdrawal_amount}. Would you like a receipt? (y/n): ")
        if choice.lower() == 'y':
            self.complete_transaction(print_receipt=True)
        else:
            self.complete_transaction(print_receipt=False)

    def complete_transaction(self, print_receipt):
        if self.transaction.execute_withdrawal():
            if print_receipt:
                receipt = Receipt(self.transaction, self.account.check_balance())
                print(receipt.generate_receipt())
            self.finish_transaction()
        else:
            print("Transaction failed.")

    def finish_transaction(self):
        print(f"Dispensing €{self.transaction.withdrawal_amount}...")
        print("Transaction Complete. Please retrieve your card.")
        self.is_card_inserted = False
        self.reset_atm()

    def reset_atm(self):
        self.transaction.withdrawal_amount = 0
        print("\nATM ready for next transaction.")

# Running the ATM simulation
if __name__ == "__main__":
    atm = ATM()
    atm.insert_card()
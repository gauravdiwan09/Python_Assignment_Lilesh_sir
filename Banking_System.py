import random
import mysql.connector
import re

# Database setup
def setup_database():
    conn = None
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Gaurav@123"
        )
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS banking_system")
        conn.close()

        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Gaurav@123",
            database="banking_system"
        )
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            name VARCHAR(255),
                            account_number VARCHAR(10) UNIQUE,
                            dob DATE,
                            city VARCHAR(255),
                            password VARCHAR(255),
                            balance FLOAT,
                            contact_number VARCHAR(10),
                            email VARCHAR(255),
                            address TEXT,
                            active BOOLEAN DEFAULT TRUE)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            account_number VARCHAR(10),
                            type VARCHAR(255),
                            amount FLOAT,
                            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn and conn.is_connected():
            conn.close()

setup_database()

# Utility functions
def generate_account_number():
    return str(random.randint(10**9, 10**10 - 1))

# Banking functions
def validate_password(password):
    # Password must be at least 8 characters, contain both uppercase and lowercase, and a number
    if len(password) < 8 or not re.search("[a-z]", password) or not re.search("[A-Z]", password) or not re.search("[0-9]", password):
        print("Password must be at least 8 characters, include an uppercase letter, a lowercase letter, and a number.")
        return False
    return True

def add_user():
    name = input("Enter name: ")
    dob = input("Enter DOB (YYYY-MM-DD): ")
    city = input("Enter city: ")
    password = input("Enter password: ")
    while not validate_password(password):
        password = input("Enter password: ")
    
    balance = float(input("Enter initial balance (>= 2000): "))
    while balance < 2000:
        print("Minimum balance must be 2000.")
        balance = float(input("Enter initial balance (>= 2000): "))
    
    contact_number = input("Enter contact number: ")
    while len(contact_number) != 10 or not contact_number.isdigit():
        print("Invalid contact number.")
        contact_number = input("Enter contact number: ")

    email = input("Enter email: ")
    while not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        print("Invalid email format.")
        email = input("Enter email: ")
    
    address = input("Enter address: ")

    account_number = generate_account_number()
    conn = None
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Gaurav@123",
            database="banking_system"
        )
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO users (name, account_number, dob, city, password, balance, contact_number, email, address)
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                       (name, account_number, dob, city, password, balance, contact_number, email, address))
        conn.commit()
        print(f"User added. Account Number: {account_number}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn and conn.is_connected():
            conn.close()

def show_user():
    conn = None
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Gaurav@123",
            database="banking_system"
        )
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        for user in users:
            print(f"ID: {user[0]}, Name: {user[1]}, Account: {user[2]}, DOB: {user[3]}, City: {user[4]}, Balance: {user[6]}, Contact: {user[7]}, Email: {user[8]}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn and conn.is_connected():
            conn.close()

def login():
    account_number = input("Enter account number: ")
    password = input("Enter password: ")
    conn = None
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Gaurav@123",
            database="banking_system"
        )
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE account_number = %s AND password = %s', (account_number, password))
        user = cursor.fetchone()
        if user:
            print("Login successful.")
            manage_account(account_number, user[5])  # user[5] contains current balance
        else:
            print("Invalid credentials.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn and conn.is_connected():
            conn.close()

def manage_account(account_number, balance):
    while True:
        print(f"Balance: {balance}")
        print("1. Credit Amount")
        print("2. Debit Amount")
        print("3. Transfer Amount")
        print("4. Show Transactions")
        print("5. Change Password")
        print("6. Update Profile")
        print("7. Deactivate Account")
        print("8. Logout")
        choice = input("Enter choice: ")
        
        if choice == '1':
            amount = float(input("Enter amount to credit: "))
            credit_amount(account_number, amount)
        elif choice == '2':
            amount = float(input("Enter amount to debit: "))
            debit_amount(account_number, amount)
        elif choice == '3':
            amount = float(input("Enter amount to transfer: "))
            transfer_amount(account_number, amount)
        elif choice == '4':
            show_transactions(account_number)
        elif choice == '5':
            change_password(account_number)
        elif choice == '6':
            update_profile(account_number)
        elif choice == '7':
            deactivate_account(account_number)
        elif choice == '8':
            break
        else:
            print("Invalid choice.")

def credit_amount(account_number, amount):
    conn = None
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Gaurav@123",
            database="banking_system"
        )
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET balance = balance + %s WHERE account_number = %s", (amount, account_number))
        cursor.execute("INSERT INTO transactions (account_number, type, amount) VALUES (%s, %s, %s)", (account_number, 'Credit', amount))
        conn.commit()
        print("Amount credited successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn and conn.is_connected():
            conn.close()

def debit_amount(account_number, amount):
    conn = None
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Gaurav@123",
            database="banking_system"
        )
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET balance = balance - %s WHERE account_number = %s", (amount, account_number))
        cursor.execute("INSERT INTO transactions (account_number, type, amount) VALUES (%s, %s, %s)", (account_number, 'Debit', amount))
        conn.commit()
        print("Amount debited successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn and conn.is_connected():
            conn.close()

def transfer_amount(account_number, amount):
    to_account = input("Enter the account number to transfer to: ")
    conn = None
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Gaurav@123",
            database="banking_system"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM users WHERE account_number = %s", (account_number,))
        balance = cursor.fetchone()[0]
        
        if balance >= amount:
            cursor.execute("UPDATE users SET balance = balance - %s WHERE account_number = %s", (amount, account_number))
            cursor.execute("UPDATE users SET balance = balance + %s WHERE account_number = %s", (amount, to_account))
            cursor.execute("INSERT INTO transactions (account_number, type, amount) VALUES (%s, %s, %s)", (account_number, 'Transfer', amount))
            conn.commit()
            print("Amount transferred successfully.")
        else:
            print("Insufficient balance.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn and conn.is_connected():
            conn.close()

def show_transactions(account_number):
    conn = None
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Gaurav@123",
            database="banking_system"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transactions WHERE account_number = %s", (account_number,))
        transactions = cursor.fetchall()
        for transaction in transactions:
            print(f"ID: {transaction[0]}, Type: {transaction[2]}, Amount: {transaction[3]}, Date: {transaction[4]}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn and conn.is_connected():
            conn.close()

def change_password(account_number):
    new_password = input("Enter new password: ")
    while not validate_password(new_password):
        new_password = input("Enter new password: ")
    conn = None
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Gaurav@123",
            database="banking_system"
        )
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET password = %s WHERE account_number = %s", (new_password, account_number))
        conn.commit()
        print("Password changed successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn and conn.is_connected():
            conn.close()

def update_profile(account_number):
    name = input("Enter new name: ")
    city = input("Enter new city: ")
    email = input("Enter new email: ")
    address = input("Enter new address: ")
    contact_number = input("Enter new contact number: ")

    conn = None
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Gaurav@123",
            database="banking_system"
        )
        cursor = conn.cursor()
        cursor.execute('''UPDATE users
                          SET name = %s, city = %s, email = %s, address = %s, contact_number = %s
                          WHERE account_number = %s''',
                       (name, city, email, address, contact_number, account_number))
        conn.commit()
        print("Profile updated successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn and conn.is_connected():
            conn.close()

def deactivate_account(account_number):
    conn = None
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Gaurav@123",
            database="banking_system"
        )
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET active = FALSE WHERE account_number = %s", (account_number,))
        conn.commit()
        print("Account deactivated successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn and conn.is_connected():
            conn.close()

def main():
    while True:
        print("1. Add User")
        print("2. Show User")
        print("3. Login")
        print("4. Exit")
        choice = input("Enter choice: ")
        if choice == '1':
            add_user()
        elif choice == '2':
            show_user()
        elif choice == '3':
            login()
        elif choice == '4':
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()

import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",      
    password="Gaurav@123",      
    database="quiz_app"
)
cursor = conn.cursor()

# Registration system
def register():
    name = input("Enter your name: ")
    username = input("Enter your username: ")
    phone_no = input("Enter your 10-digit phone number: ")
    if len(phone_no) == 10:
        password = input("Enter your password: ")
        enrollment_no = input("Enter your enrollment number: ")

        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            print("Username already exists. Please try a different one.")
        else:
            cursor.execute(
                "INSERT INTO users (name, username, phone_no, password, enrollment_no) VALUES (%s, %s, %s, %s, %s)",
                (name, username, phone_no, password, enrollment_no)
            )
            conn.commit()
            print("Registration successful!")
    else:
        print("Enter a 10-digit phone number!")
        register()

# Login system
def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    if cursor.fetchone():
        print("Login successful!")
        return username
    else:
        print("Invalid credentials. Try again.")

# Quiz attempt
def attempt_quiz(username):
    print("Available sections: 1. DSA 2. DBMS 3. Python")
    section = input("Choose a section to attempt: ")

    if section == '1':
        section = 'DSA'
    elif section == '2':
        section = 'DBMS'
    elif section == '3':
        section = 'Python'
    else:
        print("Invalid section!")
        return

    cursor.execute("SELECT * FROM questions WHERE section = %s", (section,))
    questions = cursor.fetchall()

    if not questions:
        print("No questions available for this section.")
        return

    score = 0
    for i, q in enumerate(questions):
        print(f"Q{i + 1}: {q[2]}")  
        print(f"1. {q[3]}")        
        print(f"2. {q[4]}")        
        print(f"3. {q[5]}")       
        answer = int(input("Enter the correct option number: "))
        if answer == q[6]:
            score += 10

    cursor.execute(
        "INSERT INTO scores (username, section, score) VALUES (%s, %s, %s)",
        (username, section, score)
    )
    conn.commit()

    print(f"Your score is: {score}/50")

# Show results
def show_result(username):
    cursor.execute("SELECT section, score FROM scores WHERE username = %s", (username,))
    results = cursor.fetchall()
    if results:
        for section, score in results:
            print(f"Section: {section}, Score: {score}/50")
    else:
        print("You haven't attempted any quiz yet.")

# Main menu
def main_menu():
    while True:
        print("\nMenu:\n1. Register\n2. Login\n3. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            register()
        elif choice == '2':
            username = login()
            if username:
                while True:
                    print("\nLogged in as", username)
                    print("1. Attempt Quiz\n2. Show Result\n3. Logout")
                    user_choice = input("Choose an option: ")

                    if user_choice == '1':
                        attempt_quiz(username)
                    elif user_choice == '2':
                        show_result(username)
                    elif user_choice == '3':
                        print("Logging out...")
                        break
                    else:
                        print("Invalid option. Try again.")
        elif choice == '3':
            print("Exiting...")
            conn.close()
            exit()
        else:
            print("Invalid choice. Try again.")

# Starting point
main_menu()

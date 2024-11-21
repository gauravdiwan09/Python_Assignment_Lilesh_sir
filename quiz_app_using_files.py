import json

# File paths
USERS_FILE = "users.json"
SCORES_FILE = "scores.json"

def load_data(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_data(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Registration system
def register():
    users = load_data(USERS_FILE)
    name = input("Enter your name: ")
    username = input("Enter your username: ")
    phone_no = input("Enter your 10-digit phone number: ")
    if len(phone_no) == 10:
        password = input("Enter your password: ")
        enrollment_no = input("Enter your enrollment number: ")
        if username in users:
            print("Username already exists. Please try a different one.")
        else:
            users[username] = {'name': name, 'phone_no': phone_no, 'password': password, 'enrollment_no': enrollment_no}
            save_data(USERS_FILE, users)
            print("Registration successful!")
    else:
        print("Enter a 10-digit phone number!")
        register()

# Login system
def login():
    users = load_data(USERS_FILE)
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    if username in users and users[username]['password'] == password:
        print("Login successful!")
        return username
    else:
        print("Invalid credentials. Try again.")

# Quiz attempt
def attempt_quiz(username):
    questions = {
        'DSA': [
            {"question": "What is a stack?", "options": ["FIFO", "LIFO", "None"], "answer": 2},
            {"question": "What is a queue?", "options": ["FIFO", "LIFO", "None"], "answer": 1},
        ],
        'DBMS': [
            {"question": "What is SQL?", "options": ["Language", "Protocol", "None"], "answer": 1},
        ],
        'Python': [
            {"question": "What is Python?", "options": ["Snake", "Language", "IDE"], "answer": 2},
        ],
    }
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

    score = 0
    for i, q in enumerate(questions[section]):
        print(f"Q{i + 1}: {q['question']}")
        for j, option in enumerate(q['options']):
            print(f"{j + 1}. {option}")
        answer = int(input("Enter the correct option number: "))
        if answer == q['answer']:
            score += 10

    scores = load_data(SCORES_FILE)
    scores[username] = {'section': section, 'score': score}
    save_data(SCORES_FILE, scores)

    print(f"Your score is: {score}/50")

# Show results
def show_result(username):
    scores = load_data(SCORES_FILE)
    if username in scores:
        result = scores[username]
        print(f"----------\nSection: {result['section']}\nScore: {result['score']}/50\n----------")
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
            exit()
        else:
            print("Invalid choice. Try again.")

# Starting point
main_menu()

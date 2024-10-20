from questions import questions

#regirstration system
users = {}  # Dictionary to store user data

def register():
    name = input("Enter your name: ")
    username = input("Enter your username: ")
    phone_no = input("Enter your 10 digit phone number: ")
    if len(phone_no) == 10:
      password = input("Enter your password: ")
      enrollment_no = input("Enter your enrollment number: ")
      if username in users:
          print("Username already exists. Please try a different one.")
      else:
          users[username] = {'name': name, 'phone_no': phone_no, 'password': password, 'enrollment_no': enrollment_no}
          print("Registration successful!")
    else:
      print("enter a 10 digit phone number!")
      register()

#login
def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    if username in users and users[username]['password'] == password:
        print("Login successful!")
        return username
    else:
        print("Invalid credentials. Try again.")

#quizes
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

    score = 0
    for i, q in enumerate(questions[section]):
        print(f"Q{i+1}: {q['question']}")
        for j, option in enumerate(q['options']):
            print(f"{j+1}. {option}")
        answer = int(input("Enter the correct option number: "))
        if answer == q['answer']:
            score += 10

    users[username]['score'] = score
    print(f"{users[username]['name']} ({users[username]['enrollment_no']}), your score is: {users[username]['score']}/50")

#results
def show_result(username):
    if 'score' in users[username]:
        print(f"{users[username]['name']} ({users[username]['enrollment_no']}), your score is: {users[username]['score']}/50")
    else:
        print("You haven't attempted any quiz yet.")

#main menu
def main_menu():
    while True: #to continuosly display the main menu!
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


#starting point!
main_menu()
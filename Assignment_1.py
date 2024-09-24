print("""         1 ----> Registration
         2 ----> Login       
         3 ----> Forgot Password
         4 ----> Exit the service """)

user_list = []
user_db = {}
user_login = None

while True:
  number = input("enter the number associated with the service you want to use! ")
  if number == '1':
    # registration
    user_reg = input("enter your name: ").lower()
    pwd_reg = input("enter your password: ")
    dob = input("enter your dob! (format '12/11/2003') It will use at time of password recovery: ")

    user_list.append(user_reg)
    user_db[user_reg] = {pwd_reg: dob}

    print(f"{user_reg}, you have been registered successfully!")

  elif number == '2':
    # login
    user_login = input("enter your name: ").lower()
    if user_login in user_list:
      pwd_login = input("enter your password: ")
      if pwd_login in user_db[user_login]:
        print(f"welcome {user_login}, you have been logged in successfully!")
      else:
        print("wrong password!")
    else:
      print("Incorrect username!")
      print("not registered? register first!")

  elif number == '3':
    # forgot password
    if user_login is None:
      print("You need to log in first to recover your password.")
    else:
      pwd_recover_with_dob = input("enter your dob same as you entered at the time of registration! ")
      if pwd_recover_with_dob in user_db[user_login].values():
        new_pwd = input("enter your new password! ")
        user_db[user_login][new_pwd] = pwd_recover_with_dob
        print(f"{user_login}, your password has been updated successfully!")
      else:
        print("Incorrect dob!")
        print("enter again or create a new account!")

  else:
    print("Exiting the service!")
    break

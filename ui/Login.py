# ui/login.py

def ask_username():
    username = input("Enter your username: ")
    return username

def ask_password():
    password = input("Enter your password: ")
    return password

def display_success_message(username):
    print("Login successful! Welcome " + username + ".")

def login_screen():
    print("\n--- LOGIN SCREEN ---")
    username = ask_username()
    password = ask_password()
    display_success_message(username)
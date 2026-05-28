from Logic.Auth import authenticate_user, create_user


def ask_username():
    return input("Enter a username: ").strip()


def ask_password():
    return input("Enter a password: ").strip()


def display_login_success(username):
    print(f"Login successful. Welcome, {username}.")


def display_login_failure():
    print("Login failed. Please check your username and password.")


def display_account_created(username):
    print(f"Account created successfully for {username}.")


def display_account_error():
    print("Could not create the account. The username may already exist.")


def ask_auth_choice():
    print("\n--- Account Menu ---")
    print("1. Login")
    print("2. Create a new account")
    return input("Choose 1 or 2: ").strip()


def login_screen():
    print("\n--- Login ---")
    username = ask_username()
    password = ask_password()
    user = authenticate_user(username, password)

    if user:
        display_login_success(username)
        return user

    display_login_failure()
    return None


def create_account_screen():
    print("\n--- Create a New Account ---")
    username = ask_username()
    password = ask_password()

    if create_user(username, password):
        display_account_created(username)
        return authenticate_user(username, password)

    display_account_error()
    return None


def auth_screen():
    choice = ask_auth_choice()

    if choice == "1":
        return login_screen()

    if choice == "2":
        return create_account_screen()

    print("Invalid choice. Please select 1 or 2.")
    return None
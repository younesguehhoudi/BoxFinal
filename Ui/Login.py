from Logic.Auth import authenticate_user, create_user


def ask_username():
    """Prompt the user for a username."""
    return input("Enter a username: ").strip()


def ask_password():
    """Prompt the user for a password."""
    return input("Enter a password: ").strip()


def display_login_success(username):
    """Display a successful login message."""
    print(f"Login successful. Welcome, {username}.")


def display_login_failure():
    """Display a login failure message."""
    print("Login failed. Please check your username and password.")


def display_account_created(username):
    """Display a successful account creation message."""
    print(f"Account created successfully for {username}.")


def display_account_error():
    """Display an account creation error message."""
    print("Could not create the account. The username may already exist.")


def ask_auth_choice():
    """Prompt the user to choose between login and account creation."""
    print("\n--- Account Menu ---")
    print("1. Login")
    print("2. Create a new account")
    return input("Choose 1 or 2: ").strip()


def login_screen():
    """Handle the login flow in the console."""
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
    """Handle the account creation flow in the console."""
    print("\n--- Create a New Account ---")
    username = ask_username()
    password = ask_password()

    if create_user(username, password):
        display_account_created(username)
        return authenticate_user(username, password)

    display_account_error()
    return None


def auth_screen():
    """Display the authentication menu and return the authenticated user."""
    choice = ask_auth_choice()

    if choice == "1":
        return login_screen()

    if choice == "2":
        return create_account_screen()

    print("Invalid choice. Please select 1 or 2.")
    return None
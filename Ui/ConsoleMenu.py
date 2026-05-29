# Ui/ConsoleMenu.py

from Logic.Auth import authenticate_user, create_user
from Logic.Place import add_place, get_places_by_user


class ConsoleMenu:
    def __init__(self):
        self.current_user = None

    def display_title(self):
        print("\n=== TRAVEL PLANNER — MAIN MENU ===")
        if self.current_user:
            print(f"  Logged in as: {self.current_user['username']}")

    def display_options(self):
        if not self.current_user:
            print("1. Login")
            print("2. Register")
            print("3. Quit")
        else:
            print("1. Add a place manually")
            print("2. Display my places")
            print("3. Display tour (current order)")
            print("4. Logout")
            print("5. Quit")

    def ask_choice(self):
        if not self.current_user:
            return input("Your choice (1-3): ")
        return input("Your choice (1-5): ")

    def login_ui(self):
        print("\n--- LOGIN ---")
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        user = authenticate_user(username, password)
        if user:
            self.current_user = user
            print(f"Welcome back, {user['username']}!")
        else:
            print("Invalid username or password. Please try again.")

    def register_ui(self):
        print("\n--- REGISTER ---")
        username = input("Choose a username: ").strip()
        password = input("Choose a password: ").strip()
        success = create_user(username, password)
        if success:
            print(f"Account created for '{username}'. You can now log in.")
        else:
            print("Registration failed. That username may already be taken.")

    def logout_ui(self):
        print(f"Goodbye, {self.current_user['username']}!")
        self.current_user = None

    def add_place_ui(self):
        print("\n--- ADD A PLACE ---")
        name = input("Place name: ").strip()
        try:
            latitude = float(input("Latitude: ").strip())
            longitude = float(input("Longitude: ").strip())
        except ValueError:
            print("Invalid coordinates. Please enter numeric values.")
            return
        success = add_place(self.current_user["id"], name, latitude, longitude)
        if success:
            print(f"Place '{name}' added successfully.")
        else:
            print("Failed to add place.")

    def display_places_ui(self):
        print("\n--- MY PLACES ---")
        places = get_places_by_user(self.current_user["id"])
        if not places:
            print("You have no saved places yet.")
            return
        for place in places:
            print(f"  [{place['id']}] {place['name']} — lat: {place['latitude']}, lng: {place['longitude']}")

    def display_tour_ui(self):
        print("\n--- TOUR (current order) ---")
        places = get_places_by_user(self.current_user["id"])
        if len(places) < 2:
            print("You need at least 2 places to display a tour.")
            return
        for i, place in enumerate(places, start=1):
            print(f"  {i}. {place['name']}")

    def process_choice_guest(self, choice):
        if choice == "1":
            self.login_ui()
        elif choice == "2":
            self.register_ui()
        elif choice == "3":
            self.quit_application()
        else:
            print("Unknown choice. Please try again.")

    def process_choice_user(self, choice):
        if choice == "1":
            self.add_place_ui()
        elif choice == "2":
            self.display_places_ui()
        elif choice == "3":
            self.display_tour_ui()
        elif choice == "4":
            self.logout_ui()
        elif choice == "5":
            self.quit_application()
        else:
            print("Unknown choice. Please try again.")

    def quit_application(self):
        print("Exiting program. Goodbye!")
        exit()

    def run(self):
        while True:
            self.display_title()
            self.display_options()
            choice = self.ask_choice()
            if not self.current_user:
                self.process_choice_guest(choice)
            else:
                self.process_choice_user(choice)
from Ui.Login import auth_screen
from Ui.PlacePrinter import add_place_ui as place_add_ui, display_places_ui as place_display_ui

class ConsoleMenu:
    def __init__(self):
        self.current_user_id = None

    def display_title(self):
        print("\n=== MAIN MENU ===")

    def display_options(self):
        print("1. Login or create an account")
        print("2. Add a place")
        print("3. Display places")
        print("4. Display tour")
        print("5. Quit")

    def ask_choice(self):
        return input("Your choice (1-5): ")

    def login_ui(self):
        user = auth_screen()

        if user:
            self.current_user_id = user["id"]

    def add_place_ui(self):
        if self.current_user_id is None:
            print("Please log in first or create an account.")
            return

        place_add_ui(self.current_user_id)

    def display_places_ui(self):
        if self.current_user_id is None:
            print("Please log in first or create an account.")
            return

        place_display_ui(self.current_user_id)

    def display_tour_ui(self):
        print("Tour display is not implemented yet.")

    def quit_application(self):
        print("Exiting program. Goodbye!")
        exit()

    def process_choice(self, choice):
        if choice == "1":
            self.login_ui()
        elif choice == "2":
            self.add_place_ui()
        elif choice == "3":
            self.display_places_ui()
        elif choice == "4":
            self.display_tour_ui()
        elif choice == "5":
            self.quit_application()
        else:
            print("Unknown choice. Please try again.")

    def run(self):
        while True:
            self.display_title()
            self.display_options()
            choice = self.ask_choice()
            self.process_choice(choice)
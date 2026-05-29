from Logic.Algo import optimize_tour
from Logic.Place import get_places_by_user
from Ui.Login import auth_screen
from Ui.PlacePrinter import (
    add_place_ui as place_add_ui,
    display_places_ui as place_display_ui,
)
from Ui.TourPrinter import choose_places_for_tour, display_tour


class ConsoleMenu:
    def __init__(self):
        """Initialize the main console menu state."""
        self.current_user_id = None
        self.current_username = None

    def display_title(self):
        """Display the main menu title."""
        print("\n=== MAIN MENU ===")

    def display_options(self):
        """Display the available menu options."""
        if self.current_user_id is None:
            print("1. Login or create an account")
        else:
            print(f"1. Logout ({self.current_username})")
        print("2. Add a place")
        print("3. Display places")
        print("4. Display tour")
        print("5. Quit")

    def ask_choice(self):
        """Prompt the user for a menu choice."""
        return input("Your choice (1-5): ")

    def login_ui(self):
        """Launch the authentication flow and store the current user id."""
        user = auth_screen()

        if user:
            self.current_user_id = user["id"]
            self.current_username = user["username"]

    def logout_ui(self):
        """Log out the current user."""
        self.current_user_id = None
        self.current_username = None
        print("You have been logged out.")

    def add_place_ui(self):
        """Open the place creation flow for the current user."""
        if self.current_user_id is None:
            print("Please log in first or create an account.")
            return

        place_add_ui(self.current_user_id)

    def display_places_ui(self):
        """Display the places saved by the current user."""
        if self.current_user_id is None:
            print("Please log in first or create an account.")
            return

        place_display_ui(self.current_user_id)

    def display_tour_ui(self):
        """Display the optimized tour for the current user."""
        if self.current_user_id is None:
            print("Please log in first or create an account.")
            return

        places = get_places_by_user(self.current_user_id)

        if not places:
            print("No saved places.")
            return

        selected_places = choose_places_for_tour(places)
        if not selected_places:
            return

        print("Optimizing your tour, please wait...")
        tour = optimize_tour(selected_places, "my tour", "private")
        display_tour(tour)

    def quit_application(self):
        """Exit the application."""
        print("Exiting program. Goodbye!")
        exit()

    def process_choice(self, choice):
        """Run the action associated with the selected menu option."""
        if choice == "1":
            if self.current_user_id is None:
                self.login_ui()
            else:
                self.logout_ui()
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
        """Run the main console menu loop."""
        while True:
            self.display_title()
            self.display_options()
            choice = self.ask_choice()
            self.process_choice(choice)
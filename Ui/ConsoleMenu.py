from Logic.Algo import optimize_tour
from Logic.Place import get_places_by_user
from Ui.Login import auth_screen
from Ui.PlacePrinter import (
    add_place_ui as place_add_ui,
    display_places_ui as place_display_ui,
)
from Ui.TourPrinter import choose_places_for_tour, display_tour
from Ui.TourSharingPrinter import (
    save_tour_ui,
    list_my_tours_ui,
    access_shared_tour_ui,
)


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
        print("3. Display my places")
        print("4. Generate and save a tour")
        print("5. My saved tours")
        print("6. Access a shared tour (via token)")
        print("7. Quit")

    def ask_choice(self):
        """Prompt the user for a menu choice."""
        return input("Your choice (1-7): ").strip()

    # ── AUTH ──────────────────────────────────────────────────────────────────

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

    # ── PLACES ────────────────────────────────────────────────────────────────

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

    # ── TOURS ─────────────────────────────────────────────────────────────────

    def generate_and_save_tour_ui(self):
        """
        Let the user pick places, optimize the tour, display it, then
        optionally save it with a visibility setting and receive a share token.
        """
        if self.current_user_id is None:
            print("Please log in first or create an account.")
            return

        places = get_places_by_user(self.current_user_id)

        if not places:
            print("No saved places. Add some places first (option 2).")
            return

        selected_places = choose_places_for_tour(places)
        if not selected_places:
            return

        print("Optimizing your tour, please wait...")
        tour = optimize_tour(selected_places, "unnamed", "private")
        display_tour(tour)

        save = input("\nDo you want to save and share this tour? (y/n): ").strip().lower()
        if save == "y":
            save_tour_ui(self.current_user_id, tour)

    def list_my_tours_ui(self):
        """Display all tours saved by the current user."""
        if self.current_user_id is None:
            print("Please log in first or create an account.")
            return
        list_my_tours_ui(self.current_user_id)

    def access_shared_tour_ui(self):
        """
        Access a tour shared by another user via its token.
        Public tours do not require a login; private ones do.
        """
        access_shared_tour_ui(self.current_user_id)

    # ── ROUTING ───────────────────────────────────────────────────────────────

    def quit_application(self):
        """Exit the application."""
        print("Exiting program. Goodbye!")
        exit()

    def process_choice(self, choice):
        """Run the action associated with the selected menu option."""
        actions = {
            "1": lambda: self.login_ui() if self.current_user_id is None else self.logout_ui(),
            "2": self.add_place_ui,
            "3": self.display_places_ui,
            "4": self.generate_and_save_tour_ui,
            "5": self.list_my_tours_ui,
            "6": self.access_shared_tour_ui,
            "7": self.quit_application,
        }
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Unknown choice. Please try again.")

    def run(self):
        """Run the main console menu loop."""
        while True:
            self.display_title()
            self.display_options()
            choice = self.ask_choice()
            self.process_choice(choice)
class ConsoleMenu:
    def __init__(self):
        pass

    def display_title(self):
        print("\n=== MAIN MENU ===")

    def display_options(self):
        print("1. Login")
        print("2. Add a place manually")
        print("3. Display places")
        print("4. Display tour (current order)")
        print("5. Quit")

    def ask_choice(self):
        return input("Your choice (1-5): ")

    def login_ui(self):
        print("-> Login Section")

    def add_place_ui(self):
        print("-> Add Place Section")

    def display_places_ui(self):
        print("-> Display Places Section")

    def display_tour_ui(self):
        print("-> Display Tour Section")

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
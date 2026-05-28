# ui/consoleMenu.py

from Ui.Login import login_screen
from Ui.PlacePrinter import display_all_places
from Ui.Tour import display_tour

def display_title():
    print("\n=== MAIN MENU ===")

def display_options():
    print("1. Login")
    print("2. Add a place manually")
    print("3. Display places")
    print("4. Display tour (current order)")
    print("5. Quit")

def ask_choice():
    choice = input("Your choice (1-5): ")
    return choice

def ask_place_name():
    name = input("Name of the new place: ")
    return name

def ask_latitude():
    lat = input("Latitude: ")
    return lat

def ask_longitude():
    lon = input("Longitude: ")
    return lon

def add_place_ui(places_dictionary):
    name = ask_place_name()
    lat = ask_latitude()
    lon = ask_longitude()
    
    places_dictionary[name] = {
        "latitude": lat,
        "longitude": lon
    }
    print("Place added.")

def quit_application():
    print("Exiting program. Goodbye!")
    exit()

def process_choice(choice, places_dictionary):
    if choice == "1":
        login_screen()
    elif choice == "2":
        add_place_ui(places_dictionary)
    elif choice == "3":
        display_all_places(places_dictionary)
    elif choice == "4":
        display_tour(places_dictionary)
    elif choice == "5":
        quit_application()
    else:
        print("Unknown choice. Please try again.")

def run_menu(places_dictionary):
    while True:
        display_title()
        display_options()
        choice = ask_choice()
        process_choice(choice, places_dictionary)
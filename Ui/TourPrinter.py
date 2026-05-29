from Logic.Place import Place, fetch_coordinates
from Logic.Tour import Tour


def display_tour(tour: Tour):
    """Display the optimized tour in the console."""
    print("\n--- Optimized Tour ---")
    print(tour)
    print(f"Total distance: {tour.total_distance:.1f} km")


def display_places_list(places):
    """Display a numbered list of places."""
    print("\n--- Available places ---")
    for index, place in enumerate(places, start=1):
        print(f"{index}. {place}")


def ask_tour_source_choice():
    """Ask how the user wants to build the tour."""
    print("\n--- Build a tour ---")
    print("1. Use all saved places")
    print("2. Choose places from the saved list")
    print("3. Type custom place names")
    print("4. Cancel")
    return input("Choose 1-4: ").strip()


def choose_places_from_saved_list(places):
    """Let the user select saved places using their numbers."""
    while True:
        display_places_list(places)
        raw_choice = input(
            "Enter the numbers separated by commas (example: 1,3,4): "
        ).strip()

        if not raw_choice:
            print("Please enter at least one number.")
            continue

        tokens = [part.strip() for part in raw_choice.split(",") if part.strip()]
        if not tokens:
            print("Please enter valid numbers.")
            continue

        selected_places = []
        selected_indexes = set()
        invalid_input = False

        for token in tokens:
            if not token.isdigit():
                print(f"'{token}' is not a valid number.")
                invalid_input = True
                break

            index = int(token)
            if index < 1 or index > len(places):
                print(f"'{token}' is outside the available range.")
                invalid_input = True
                break

            if index not in selected_indexes:
                selected_places.append(places[index - 1])
                selected_indexes.add(index)

        if invalid_input:
            print("Please try again.")
            continue

        if not selected_places:
            print("Please select at least one place.")
            continue

        return selected_places


def choose_places_from_names():
    """Let the user type place names and resolve them with geocoding."""
    while True:
        print("\nType the place names separated by commas.")
        print("Example: Paris, Lyon, Marseille")
        raw_choice = input("Place names: ").strip()

        if not raw_choice:
            print("Please enter at least one place name.")
            continue

        tokens = [part.strip() for part in raw_choice.split(",") if part.strip()]
        if not tokens:
            print("Please enter valid place names.")
            continue

        selected_places = []
        selected_names = set()
        invalid_input = False

        for token in tokens:
            if token.isdigit():
                print(f"'{token}' is a number. Please type a place name.")
                invalid_input = True
                break

            key = token.lower()
            if key in selected_names:
                continue

            lat, lng = fetch_coordinates(token)
            if lat is None or lng is None:
                print(f"Unknown place: '{token}'.")
                invalid_input = True
                break

            selected_places.append(Place(name=token, lat=lat, lng=lng))
            selected_names.add(key)

        if invalid_input:
            print("Please try again.")
            continue

        if not selected_places:
            print("Please select at least one place.")
            continue

        return selected_places


def choose_places_for_tour(saved_places):
    """Return the list of places that will be used to build the tour."""
    if not saved_places:
        print("No saved places.")
        return []

    while True:
        choice = ask_tour_source_choice()

        if choice == "1":
            return saved_places

        if choice == "2":
            return choose_places_from_saved_list(saved_places)

        if choice == "3":
            return choose_places_from_names()

        if choice == "4":
            print("Tour creation cancelled.")
            return []

        print("Invalid choice. Please select 1, 2, 3 or 4.")
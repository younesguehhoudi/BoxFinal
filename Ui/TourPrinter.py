from Logic.Place import Place, fetch_coordinates
from Logic.Tour import Tour

# --- DISPLAY ---

def display_tour(tour: Tour):
    """
    Display the optimized tour and its total distance in the console.

    Args:
        tour (Tour): The optimized tour object to display.
    """
    print("\n--- Optimized Tour ---")
    print(tour)
    print(f"Total distance: {tour.total_distance:.1f} km")


def display_places_list(places):
    """
    Display a numbered list of available places.

    Args:
        places (list): A list of Place objects.
    """
    print("\n--- Available places ---")
    for index, place in enumerate(places, start=1):
        print(f"{index}. {place}")


def ask_tour_source_choice():
    """
    Ask the user how they want to build the tour.

    Returns:
        str: The user's menu choice, stripped of leading/trailing whitespace.
    """
    print("\n--- Build a tour ---")
    print("1. Use all saved places")
    print("2. Choose places from the saved list")
    print("3. Type custom place names")
    print("4. Cancel")
    return input("Choose 1-4: ").strip()


# --- INPUT READING AND PARSING ---

def get_tokens_from_input(prompt_message):
    """
    Prompt the user for input, split it by commas, and remove whitespace.

    Args:
        prompt_message (str): The message displayed to the user.

    Returns:
        list: A list of stripped strings entered by the user. Returns an empty 
              list if the input is empty.
    """
    raw_input = input(prompt_message).strip()
    if not raw_input:
        return []
    
    tokens = raw_input.split(",")
    return [part.strip() for part in tokens if part.strip()]


# --- SAVED LIST CHOICES PROCESSING ---

def validate_index(token, max_length):
    """
    Check if the provided text is a valid integer and falls within the list boundaries.

    Args:
        token (str): The string to validate as a number.
        max_length (int): The maximum valid index (inclusive).

    Returns:
        int: The validated index, or -1 if the token is invalid or out of bounds.
    """
    if not token.isdigit():
        print(f"'{token}' is not a valid number.")
        return -1
    
    index = int(token)
    if index < 1 or index > max_length:
        print(f"'{token}' is out of bounds.")
        return -1
        
    return index


def convert_tokens_to_saved_places(tokens, places):
    """
    Transform a list of numerical strings into a list of corresponding Place objects.

    Args:
        tokens (list): A list of strings representing numerical indexes.
        places (list): The list of available Place objects.

    Returns:
        list: A list of selected Place objects without duplicates. Returns an 
              empty list if any token is invalid.
    """
    selected_places = []
    selected_indexes = set()
    
    for token in tokens:
        index = validate_index(token, len(places))
        
        if index == -1:
            return [] 
        
        if index not in selected_indexes:
            selected_places.append(places[index - 1])
            selected_indexes.add(index)
            
    return selected_places


def choose_places_from_saved_list(places):
    """
    Manage the loop for selecting places from the saved list using numeric inputs.

    Args:
        places (list): The list of saved Place objects.

    Returns:
        list: A list of Place objects selected by the user.
    """
    while True:
        display_places_list(places)
        tokens = get_tokens_from_input("Enter the numbers separated by commas (example: 1,3,4): ")
        
        if not tokens:
            print("Please enter at least one number.")
            continue
            
        selected_places = convert_tokens_to_saved_places(tokens, places)
        
        if not selected_places:
            print("Please try again.")
            continue
            
        return selected_places


# --- NAME CHOICES PROCESSING ---

def create_place_from_name(name):
    """
    Check the provided name, fetch its geographic coordinates, and create a Place.

    Args:
        name (str): The name of the place to look up.

    Returns:
        Place: A new Place object with coordinates, or None if the name is 
               invalid or coordinates cannot be found.
    """
    if name.isdigit():
        print(f"'{name}' is a number. Please type a place name.")
        return None
        
    lat, lng = fetch_coordinates(name)
    if lat is None or lng is None:
        print(f"Unknown place: '{name}'.")
        return None
        
    return Place(name=name, lat=lat, lng=lng)


def convert_tokens_to_new_places(tokens):
    """
    Transform a list of location names into a list of Place objects after geocoding.

    Args:
        tokens (list): A list of strings representing place names.

    Returns:
        list: A list of selected Place objects without duplicates. Returns an 
              empty list if any place cannot be resolved.
    """
    selected_places = []
    selected_names = set()
    
    for token in tokens:
        key = token.lower()
        if key in selected_names:
            continue 
            
        place = create_place_from_name(token)
        if not place:
            return [] 
            
        selected_places.append(place)
        selected_names.add(key)
        
    return selected_places


def choose_places_from_names():
    """
    Manage the loop for selecting places by typing their names freely.

    Returns:
        list: A list of Place objects resolved from the user's text input.
    """
    while True:
        print("\nType the place names separated by commas.")
        print("Example: Paris, Lyon, Marseille")
        
        tokens = get_tokens_from_input("Place names: ")
        
        if not tokens:
            print("Please enter at least one place name.")
            continue
            
        selected_places = convert_tokens_to_new_places(tokens)
        
        if not selected_places:
            print("Please try again.")
            continue
            
        return selected_places


# --- MAIN ENTRY POINT ---

def choose_places_for_tour(saved_places):
    """
    Route the user to the correct tour creation method based on their choice.

    Args:
        saved_places (list): The list of currently saved Place objects.

    Returns:
        list: The final list of Place objects that will be used to build the tour, 
              or an empty list if cancelled or if no places are saved.
    """
    if not saved_places:
        print("No saved places.")
        return []

    while True:
        choice = ask_tour_source_choice()

        if choice == "1":
            return saved_places
            
        elif choice == "2":
            return choose_places_from_saved_list(saved_places)
            
        elif choice == "3":
            return choose_places_from_names()
            
        elif choice == "4":
            print("Tour creation cancelled.")
            return []
            
        else:
            print("Invalid choice. Please select 1, 2, 3 or 4.")
from Logic.Place import Place, fetch_coordinates, save_place, get_places_by_user

def add_place_ui(user_id: int):
    """Handle the user interaction for adding a place."""
    print("\n--- Add a place ---")
    name = input("Enter the place name: ").strip()
    
    print(f"Searching coordinates for '{name}'...")
    lat, lng = fetch_coordinates(name)
    
    if lat is not None and lng is not None:
        new_place = Place(name=name, latitude=lat, longitude=lng)
        success = save_place(user_id, new_place)
        
        if success:
            print(f"Success: {new_place} has been saved.")
        else:
            print("Error: unable to save the place in the database.")
    else:
        print("Error: unable to find coordinates for this place.")

def display_places_ui(user_id: int):
    """Display the list of a user's places."""
    print("\n--- Your places ---")
    places = get_places_by_user(user_id)
    
    if not places:
        print("No saved places.")
    else:
        for place in places:
            print(f"- {place}")
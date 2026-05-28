# ui/placePrinter.py

def display_places_header():
    print("\n--- List of saved places ---")

def check_if_empty(places_dictionary):
    if len(places_dictionary) == 0:
        return True
    return False

def display_empty_message():
    print("The dictionary contains no places.")

def display_single_place(place_name, coordinates):
    lat = coordinates["latitude"]
    lon = coordinates["longitude"]
    print("- " + place_name + " | Latitude: " + lat + " | Longitude: " + lon)

def display_all_places(places_dictionary):
    display_places_header()
    is_empty = check_if_empty(places_dictionary)
    
    if is_empty == True:
        display_empty_message()
    else:
        for name, coords in places_dictionary.items():
            display_single_place(name, coords)
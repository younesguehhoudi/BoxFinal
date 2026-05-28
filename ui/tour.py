# ui/tour.py

def display_tour_header():
    print("\n--- Tour Generation (Dictionary order) ---")

def display_step(number, place_name):
    print("Step " + str(number) + " : " + place_name)

def display_return_to_start(place_name):
    print("Return to starting point -> " + place_name)

def display_tour(places_dictionary):
    display_tour_header()
    
    if len(places_dictionary) == 0:
        print("Error: Cannot generate a tour with 0 places.")
        return

    counter = 1
    first_place = ""
    
    for name in places_dictionary.keys():
        if counter == 1:
            first_place = name
        display_step(counter, name)
        counter = counter + 1
        
    if first_place != "":
        display_return_to_start(first_place)
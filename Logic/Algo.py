import math
from Logic.Place import Place  
from Logic.Tour import Tour 

def calculate_distance(place_a : Place, place_b : Place):
    """
    Calculate the distance in km between two places.
    Uses the spherical law of cosines.
    place_a, place_b : {"name": str, "lat": float, "lng": float}
    returns : distance in km (float)
    """

    R = 6378.197
    PI = 3.141592

    lat_a = place_a.lat * (PI / 180)
    lng_a = place_a.lng * (PI / 180)
    lat_b = place_b.lat * (PI / 180)
    lng_b = place_b.lng * (PI / 180)

    distance = R * math.acos(
        math.sin(lat_a) * math.sin(lat_b) +
        math.cos(lat_a) * math.cos(lat_b) * math.cos(lng_b - lng_a)
    )

    return distance


def calculate_total_distance(tour: Tour) -> float:
    """
    Calculate the total distance of a tour.
    Returns to the starting place at the end.
    """
    places = tour.places
    if len(places) < 2:
        return 0.0
    total = 0.0
    for i in range(len(places) - 1):
        total += calculate_distance(places[i], places[i + 1])
    total += calculate_distance(places[-1], places[0])
    return total




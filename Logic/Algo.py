import math
from Logic.Place import Place
from Logic.Tour import Tour  

def calculate_distance(place_a: Place, place_b: Place) -> float:
    """
    Calculate the distance in km between two places.
    Uses the spherical law of cosines.
    """
    R = 6378.197
    PI = 3.141592

    lat_a = place_a.lat * (PI / 180)
    lng_a = place_a.lng * (PI / 180)
    lat_b = place_b.lat * (PI / 180)
    lng_b = place_b.lng * (PI / 180)

    return R * math.acos(
        math.sin(lat_a) * math.sin(lat_b) +
        math.cos(lat_a) * math.cos(lat_b) * math.cos(lng_b - lng_a)
    )


def calculate_total_distance(tour: Tour) -> float:
    """
    Calculate the total distance of a tour.
    Returns to the starting place at the end.
    """
    places = tour.places
    if len(places) < 2:
        return 0.0
    total = 0.0
    for i in range(len(places)):
        total += calculate_distance(places[i], places[(i + 1) % len(places)])
    return total


def find_nearest(current: Place, unvisited: list) -> Place:
    """
    Find the nearest place from current position among unvisited places.
    """
    nearest = unvisited[0]
    for i in unvisited:
        if calculate_distance(current, i) < calculate_distance(current, nearest):
            nearest = i
    return nearest


def nearest_neighbor_from(places: list, start: Place) -> list:
    """
    Build a tour from a given starting place using the Nearest Neighbour heuristic.
    Visits the closest unvisited place at each step.
    """
    tour = [start]
    visited = {start}
    current = start

    while len(visited) < len(places):
        unvisited = [i for i in places if i not in visited]    
        nearest = find_nearest(current, unvisited)
        tour.append(nearest)
        visited.add(nearest)
        current = nearest

    return tour

def best_nearest_neighbor(places: list, name: str, visibility: str) -> Tour:
    """
    Run Nearest Neighbour heuristic from every place as starting point.
    Returns the Tour with the shortest total distance.
    places     : list of all Place objects
    name       : name given to the resulting Tour
    visibility : visibility of the resulting Tour
    returns    : best Tour found
    """
    # starts with first place for starting best_tour and calculates total distance
    best_tour = Tour(name, nearest_neighbor_from(places, places[0]), visibility)
    best_tour.total_distance = calculate_total_distance(best_tour)

    #itterates to finds the tour with shortest distance
    for start in places[1:]:
        candidate = Tour(name, nearest_neighbor_from(places, start), visibility)
        candidate.total_distance = calculate_total_distance(candidate)
        if candidate.total_distance < best_tour.total_distance:
            best_tour = candidate

    return best_tour

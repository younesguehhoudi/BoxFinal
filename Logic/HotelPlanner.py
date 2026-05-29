from Logic.Algo import *
from Logic.Place import Place
from Logic.Tour import Tour


def nearest_centroid_index(place: Place, hotels: list) -> int:
    """
    Return the index of the nearest hotel to the given place.
    place  : Place object to assign
    hotels : list of Place objects representing current hotels
    returns: index of the nearest hotel
    """
    best_index = 0
    best_dist = calculate_distance(place, hotels[0])
    for i in range(1, len(hotels)):
        dist = calculate_distance(place, hotels[i])
        if dist < best_dist:
            best_dist = dist
            best_index = i
    return best_index


def get_hotel(cluster: list) -> Place:
    """
    Return the most central place in a cluster (the hotel).
    Computes the geographic centroid and returns the closest real place to it.
    cluster : list of Place objects
    returns : Place object chosen as hotel
    """
    lat_moy = sum(p.lat for p in cluster) / len(cluster)
    lng_moy = sum(p.lng for p in cluster) / len(cluster)
    centroid = Place("centroid", lat_moy, lng_moy)
    return min(cluster, key=lambda p: calculate_distance(p, centroid))


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


def kmeans(places: list, k: int) -> list:
    """
    Partition a list of places into k clusters using the K-Means algorithm.
    Hotels are always real places (closest to centroid), not abstract points.
    places : list of Place objects to cluster
    k      : number of clusters
    returns: list of k clusters, each cluster being a list of Place objects
    """
    hotels = places[:k]
    while True:
        clusters = [[] for _ in range(k)]
        for place in places:
            index = nearest_centroid_index(place, hotels)
            clusters[index].append(place)
        new_hotels = [get_hotel(cluster) for cluster in clusters if cluster]
        if all(new_hotels[i].name == hotels[i].name for i in range(len(new_hotels))):
            break
        hotels = new_hotels
    return clusters


def score_with_hotels(places: list, k: int) -> float:
    """
    Calculate the total travel distance for a given number of hotels k.
    Includes the optimized tour between hotels and all round trips from
    each hotel to its assigned cities.
    places : list of Place objects
    k      : number of hotels (clusters)
    returns: total distance in km as a float
    """
    total_distance = 0.0
    clusters = kmeans(places, k)
    hotels = [get_hotel(cluster) for cluster in clusters]
    tour_hotels = optimize_tour(hotels,"distance_hotel","private")
    for cluster in clusters :
        hotel = get_hotel(cluster)
        for place in cluster:
            if place != hotel:
                total_distance += 2 * calculate_distance(hotel, place)
    return total_distance + tour_hotels.total_distance

def find_best_k_optimal(places: list) -> int:
    """
    Find the optimal number of hotels that minimizes the total travel distance.
    Tests all values of k from 1 to len(places) and returns the k that produces
    the lowest total distance, including the inter-hotel tour and all round trips
    from each hotel to its assigned cities.
    Note: may return a high k value (up to one hotel per city) if that minimizes distance.
    places  : list of Place objects representing the cities to visit
    returns : integer k representing the optimal number of hotels
    """""
    for i in range(len(places)):
         
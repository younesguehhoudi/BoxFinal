from Logic.Algo import *
from Logic.Place import Place, Hotel
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


def get_hotel(cluster: list) -> Hotel:
    """
    Return the most central place in a cluster (the hotel).
    Computes the geographic centroid and returns the closest real place to it.
    cluster : list of Place objects
    returns : Hotel object chosen as the cluster's hotel, with its cities
    """
    lat_moy = sum(p.lat for p in cluster) / len(cluster)
    lng_moy = sum(p.lng for p in cluster) / len(cluster)
    centroid = Place("centroid", lat_moy, lng_moy)
    hotel_place = min(cluster, key=lambda p: calculate_distance(p, centroid))
    return Hotel(hotel_place, cluster)


def kmeans(places: list, k: int) -> list:
    clusters_init = [[] for _ in range(k)]
    for i, place in enumerate(places):
        clusters_init[i % k].append(place)
    hotels = [get_hotel(c) for c in clusters_init if c]
    
    while True:
        clusters = [[] for _ in range(k)]
        for place in places:
            index = nearest_centroid_index(place, hotels)
            clusters[index].append(place)
        new_hotels = [get_hotel(cluster) for cluster in clusters if cluster]
        if len(new_hotels) == len(hotels) and all(
            new_hotels[i].name == hotels[i].name for i in range(len(new_hotels))
        ):
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
    hotels = [get_hotel(cluster) for cluster in clusters if cluster]
    tour_hotels = optimize_tour(hotels, "distance_hotel", "private")
    for hotel in hotels:
        for place in hotel.cities:
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
    """
    best_k = 1
    best_score = score_with_hotels(places, 1)
    for i in range(2, len(places) + 1):
        new_score = score_with_hotels(places, i)
        if new_score < best_score:
            best_score = new_score
            best_k = i
    return best_k


def find_best_k_compromise(places: list, threshold: float = 0.05) -> int:
    """
    Find the optimal number of hotels using a gain threshold to avoid over-clustering.
    Starts from k=1 and increases k as long as the relative improvement in total
    distance exceeds the given threshold. Stops as soon as adding one more hotel
    does not reduce the distance by more than threshold percent.
    This avoids the degenerate case of one hotel per city by accepting a small
    distance trade-off in exchange for fewer hotels.
    places    : list of Place objects representing the cities to visit
    threshold : minimum relative gain to justify adding one more hotel (default 5%)
    returns   : integer k representing the compromise number of hotels
    """
    best_k = 1
    best_score = score_with_hotels(places, 1)
    for i in range(2, len(places) + 1):
        new_score = score_with_hotels(places, i)
        if best_score * (1 - threshold) > new_score:
            best_score = new_score
            best_k = i
        else:
            break
    return best_k

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from Logic.Place import Place
from Logic.HotelPlanner import kmeans, get_hotel, score_with_hotels

places = [
    Place("Paris", 48.8566, 2.3522),
    Place("Lyon", 45.7640, 4.8357),
    Place("Marseille", 43.2965, 5.3698),
    Place("Bordeaux", 44.8378, -0.5792),
]

def test_kmeans_k1():
    clusters = kmeans(places, 1)
    assert len(clusters) == 1, f"Expected 1 cluster, got {len(clusters)}"
    assert len(clusters[0]) == len(places), f"Expected {len(places)} places in cluster, got {len(clusters[0])}"
    hotel = get_hotel(clusters[0])
    assert hotel is not None
    assert hotel.name in [p.name for p in places]
    print(f"OK - 1 cluster, hotel choisi : {hotel.name}")
    print(f"     villes : {[p.name for p in hotel.cities]}")

def test_score_k1():
    score = score_with_hotels(places, 1)
    assert score > 0, "Score doit être > 0"
    print(f"OK - score k=1 : {score:.1f} km")

test_kmeans_k1()
test_score_k1()
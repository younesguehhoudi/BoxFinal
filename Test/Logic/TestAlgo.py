import sys
sys.path.append(".")
from Logic.Algo import *
from Logic.Place import Place
from Logic.Tour import Tour

tokyo   = Place("Tokyo",     35.6768601, 139.7638947)
osaka   = Place("Osaka",     34.6937569, 135.5014539)
kyoto   = Place("Kyoto",     35.0116363, 135.7680294)
nagoya  = Place("Nagoya",    35.1851045, 136.8998438)
hiroshima = Place("Hiroshima", 34.3917241, 132.4517589)

places = [tokyo, osaka, kyoto, nagoya, hiroshima]
no_places = []
tour = Tour("test", places, "public")
vide = Tour("vide",no_places,"public")
inverse = Tour("inverse", places[::-1], "public")

def test_distance_known_route():
    dist = calculate_distance(tokyo, osaka)
    assert 400 < dist < 450

def test_distance_same_place():
    dist = calculate_distance(osaka, osaka)
    assert dist < 0.01

def test_distance_symmetry():
    assert abs(calculate_distance(tokyo, osaka) - calculate_distance(osaka, tokyo)) < 0.01

def test_distance_total_known():
    dist = calculate_total_distance(tour)
    assert  1645 < dist < 1652

def test_distance_total_empty():
    dist = calculate_total_distance(vide)
    assert dist < 0.01

def test_distance_total_symmetry():
    assert abs(calculate_total_distance(tour) - calculate_total_distance(inverse)) < 0.01

def test_nearest_neighbor():
    result = nearest_neighbor_from(places,places[0])
    assert len(result) == len(places) # all places are still in result
    assert len(set(result)) == len(result) # checking duplicates 
    assert result[0] == tokyo # starting point did not changed

def test_best_nearest_neighbor_returns_tour():
    result = best_nearest_neighbor(places, "test", "public")
    assert isinstance(result, Tour)

def test_best_nearest_neighbor_distance():
    result = best_nearest_neighbor(places, "test", "public")
    assert result.total_distance > 0  

def test_two_opt():
    nn = best_nearest_neighbor(places, "test", "public")
    optimized = optimize_tour(places, "test", "public")
    assert optimized.total_distance <= nn.total_distance

if __name__ == "__main__":
    tests = [
        test_distance_known_route,
        test_distance_same_place,
        test_distance_symmetry,
        test_distance_total_known,
        test_distance_total_empty,
        test_distance_total_symmetry,
        test_nearest_neighbor,
        test_best_nearest_neighbor_returns_tour,
        test_best_nearest_neighbor_distance,
        test_two_opt
    ]
    for t in tests:
        t()
        print(f"  ✓ {t.__name__}")
    print("\nAll tests passed.")
    
    
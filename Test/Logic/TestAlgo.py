import sys
sys.path.append(".")
from Logic.Algo import calculate_distance
from Logic.Place import Place

tokyo = Place("Tokyo", 35.6768601, 139.7638947)
osaka = Place("Osaka", 34.6937569, 135.5014539)

if __name__ == "__main__":
    dist = calculate_distance(tokyo, osaka)
    print(f"Tokyo → Osaka : {dist:.1f} km")
    assert 400 < dist < 450
    print("OK")
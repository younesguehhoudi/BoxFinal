import math

def calculate_distance(place_a: dict, place_b: dict) -> float:
    """
    Calculate the distance in km between two places.
    Uses the spherical law of cosines (formula given in the subject).
    place_a, place_b : {"name": str, "lat": float, "lng": float}
    returns : distance in km (float)
    """

    R = 6378.197
    PI = 3.141592

    lat_a = place_a["lat"] * (PI / 180)
    lng_a = place_a["lng"] * (PI / 180)
    lat_b = place_b["lat"] * (PI / 180)
    lng_b = place_b["lng"] * (PI / 180)

    distance = R * math.acos(
        math.sin(lat_a) * math.sin(lat_b) +
        math.cos(lat_a) * math.cos(lat_b) * math.cos(lng_b - lng_a)
    )

    return distance


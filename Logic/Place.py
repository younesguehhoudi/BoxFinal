from typing import Optional

from geopy.geocoders import Nominatim
from geopy.exc import GeopyError
from Data.DataBase import get_connection

class Place:
    def __init__(
        self,
        name: str,
        lat: Optional[float] = None,
        lng: Optional[float] = None,
        place_id: Optional[int] = None,
    ):
        self.id = place_id
        self.name = name
        self.lat = lat
        self.lng = lng

    def __str__(self) -> str:
        return f"{self.name} ({self.lat}, {self.lng})"

def fetch_coordinates(place_name: str) -> tuple[Optional[float], Optional[float]]:
    geolocator = Nominatim(user_agent="TravelPlannerApp/1.0")
    try:
        location = geolocator.geocode(place_name)
        if location:
            return float(location.latitude), float(location.longitude)
        return None, None
    except GeopyError:
        return None, None

def save_place(user_id: int, place: Place) -> bool:
    if place.lat is None or place.lng is None:
        return False

    connection = get_connection()
    cursor = connection.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO places (user_id, name, latitude, longitude)
            VALUES (?, ?, ?, ?)
        """, (user_id, place.name, place.lat, place.lng))
        connection.commit()
        place.id = cursor.lastrowid
        return True
    except Exception:
        return False
    finally:
        connection.close()

def get_places_by_user(user_id: int) -> list[Place]:
    connection = get_connection()
    cursor = connection.cursor()
    
    cursor.execute("""
        SELECT id, name, latitude, longitude
        FROM places
        WHERE user_id = ?
    """, (user_id,))
    
    rows = cursor.fetchall()
    connection.close()

    return [Place(
        name=row["name"],
        lat=row["latitude"],
        lng=row["longitude"],
        place_id=row["id"]
    ) for row in rows]
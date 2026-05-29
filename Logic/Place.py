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
        """Create a place with optional coordinates and database identifier."""
        self.id = place_id
        self.name = name
        self.lat = lat
        self.lng = lng

    def __str__(self) -> str:
        """Return a readable representation of the place."""
        return f"{self.name} ({self.lat}, {self.lng})"

class Hotel(Place):
    def __init__(self, place: Place, cities: list):
        super().__init__(place.name, place.lat, place.lng)
        self.cities = cities


def fetch_coordinates(place_name: str) -> tuple[Optional[float], Optional[float]]:
    """Fetch latitude and longitude for a place name."""
    geolocator = Nominatim(user_agent="TravelPlannerApp/1.0")
    try:
        location = geolocator.geocode(place_name)
        if location:
            return float(location.latitude), float(location.longitude)
        return None, None
    except GeopyError:
        return None, None


def save_place(user_id: int, place: Place) -> bool:
    """Save a place for a user when coordinates are available."""
    if place.lat is None or place.lng is None:
        return False

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO places (user_id, name, latitude, longitude)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, place.name, place.lat, place.lng),
        )
        connection.commit()
        place.id = cursor.lastrowid
        return True
    except Exception:
        return False
    finally:
        connection.close()


def get_places_by_user(user_id: int) -> list[Place]:
    """Return all saved places for a given user."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, name, latitude, longitude
        FROM places
        WHERE user_id = ?
        """,
        (user_id,),
    )

    rows = cursor.fetchall()
    connection.close()

    return [
        Place(
            name=row["name"],
            lat=row["latitude"],
            lng=row["longitude"],
            place_id=row["id"],
        )
        for row in rows
    ]
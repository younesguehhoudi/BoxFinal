import uuid
from Data.DataBase import get_connection
from Logic.Tour import Tour
from Logic.Place import Place


def save_tour(user_id: int, tour: Tour) -> str | None:
    """
    Persist a Tour object to the database for the given user.
    Generates a unique share_token if the tour does not already have one.
    Returns the share_token on success, or None on failure.
    """
    if not tour.share_token:
        tour.share_token = str(uuid.uuid4())

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO tours (user_id, name, total_distance, visibility, share_token)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, tour.name, tour.total_distance, tour.visibility, tour.share_token),
        )
        tour_id = cursor.lastrowid

        for position, place in enumerate(tour.places):
            if place.id is None:
                raise ValueError(f"Place '{place.name}' has no database id. Save all places first.")
            cursor.execute(
                """
                INSERT INTO tour_places (tour_id, place_id, position)
                VALUES (?, ?, ?)
                """,
                (tour_id, place.id, position),
            )

        connection.commit()
        return tour.share_token

    except Exception as e:
        connection.rollback()
        print(f"[Error] Could not save tour: {e}")
        return None

    finally:
        connection.close()


def get_tours_by_user(user_id: int) -> list[dict]:
    """
    Return all tours (public and private) that belong to the given user,
    with their metadata (no places list — use get_tour_by_token for full detail).
    """
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, name, total_distance, visibility, share_token, created_at
        FROM tours
        WHERE user_id = ?
        ORDER BY created_at DESC
        """,
        (user_id,),
    )

    rows = cursor.fetchall()
    connection.close()

    return [dict(row) for row in rows]


def get_tour_by_token(token: str) -> dict | None:
    """
    Return a tour's full details (metadata + ordered list of Place objects)
    identified by its share_token. Returns None if the token does not exist.
    """
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT t.id, t.name, t.total_distance, t.visibility, t.share_token,
               t.created_at, t.user_id
        FROM tours t
        WHERE t.share_token = ?
        """,
        (token,),
    )

    tour_row = cursor.fetchone()

    if tour_row is None:
        connection.close()
        return None

    cursor.execute(
        """
        SELECT p.id, p.name, p.latitude, p.longitude
        FROM tour_places tp
        JOIN places p ON tp.place_id = p.id
        WHERE tp.tour_id = ?
        ORDER BY tp.position ASC
        """,
        (tour_row["id"],),
    )

    place_rows = cursor.fetchall()
    connection.close()

    places = [
        Place(name=r["name"], lat=r["latitude"], lng=r["longitude"], place_id=r["id"])
        for r in place_rows
    ]

    return {
        "id": tour_row["id"],
        "name": tour_row["name"],
        "total_distance": tour_row["total_distance"],
        "visibility": tour_row["visibility"],
        "share_token": tour_row["share_token"],
        "created_at": tour_row["created_at"],
        "user_id": tour_row["user_id"],
        "places": places,
    }
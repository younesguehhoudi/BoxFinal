# Logic/Place.py

from Data.DataBase import get_connection


def add_place(user_id, name, latitude, longitude):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO places (user_id, name, latitude, longitude)
            VALUES (?, ?, ?, ?)
            """,
            (user_id, name, float(latitude), float(longitude))
        )
        connection.commit()
        return True
    except Exception:
        return False
    finally:
        connection.close()


def get_places_by_user(user_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT id, name, latitude, longitude, created_at
        FROM places
        WHERE user_id = ?
        ORDER BY created_at ASC
        """,
        (user_id,)
    )
    places = cursor.fetchall()
    connection.close()
    return places


def delete_place(place_id, user_id):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "DELETE FROM places WHERE id = ? AND user_id = ?",
            (place_id, user_id)
        )
        connection.commit()
        return cursor.rowcount > 0
    except Exception:
        return False
    finally:
        connection.close()
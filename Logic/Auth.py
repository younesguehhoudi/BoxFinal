from werkzeug.security import check_password_hash, generate_password_hash
from Data.DataBase import get_connection

def create_user(username, password):
    """
    Create a user with hashed password for security, return True if it works and False otherwise
    """
    connection = get_connection()
    cursor = connection.cursor()

    hashed_password = generate_password_hash (password,
                                              method= "pbkdf2:sha256")

    try:
        cursor.execute("""
                       INSERT INTO users (username, password)
                       VALUES (?, ?)
                       """,
                       (username, hashed_password)
                       )
        connection.commit()
        return True
    except Exception:
        return False
    
    finally:
        connection.close()
  

def authenticate_user(username, password):
    """
    Check if the username and password are correct.
    Returns the user if authentication succeeds, otherwise None.
    """
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE username = ?
        """,
        (username,)
    )

    user = cursor.fetchone()
    connection.close()

    if user and check_password_hash(user["password"], password):
        return user

    return None


def get_user_by_id(user_id):
    """
    Get one user by id without returning the password.
    """
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, username, created_at
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    )

    user = cursor.fetchone()
    connection.close()

    return user
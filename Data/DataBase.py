import sqlite3

DATABASE_NAME = "travel_planner.db"

def get_connection():
    "a function that is used to send and return a connection to the database"
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


# Test/Logic/TestAuth.py

import unittest
import os
import sqlite3

import Data.DataBase as db_module
db_module.DATABASE_NAME = "test_travel_planner.db"

from Data.Models import initialize_database
from Logic.Auth import create_user, authenticate_user, get_user_by_id


class TestAuth(unittest.TestCase):

    def setUp(self):
        initialize_database()

    def tearDown(self):
        if os.path.exists("test_travel_planner.db"):
            os.remove("test_travel_planner.db")

    def test_create_user_success(self):
        result = create_user("abdallah", "securepass123")
        self.assertTrue(result)

    def test_create_user_duplicate_fails(self):
        create_user("abdallah", "securepass123")
        result = create_user("abdallah", "otherpass")
        self.assertFalse(result)

    def test_authenticate_user_success(self):
        create_user("abdallah", "securepass123")
        user = authenticate_user("abdallah", "securepass123")
        self.assertIsNotNone(user)
        self.assertEqual(user["username"], "abdallah")

    def test_authenticate_user_wrong_password(self):
        create_user("abdallah", "securepass123")
        user = authenticate_user("abdallah", "wrongpass")
        self.assertIsNone(user)

    def test_authenticate_unknown_user(self):
        user = authenticate_user("nobody", "anypass")
        self.assertIsNone(user)

    def test_get_user_by_id(self):
        create_user("abdallah", "securepass123")
        user = authenticate_user("abdallah", "securepass123")
        fetched = get_user_by_id(user["id"])
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched["username"], "abdallah")

    def test_password_not_stored_plain(self):
        create_user("abdallah", "securepass123")
        conn = sqlite3.connect("test_travel_planner.db")
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT password FROM users WHERE username = 'abdallah'")
        row = cur.fetchone()
        conn.close()
        self.assertNotEqual(row["password"], "securepass123")


if __name__ == "__main__":
    unittest.main()
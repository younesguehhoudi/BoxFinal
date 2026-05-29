# Test/Logic/TestPlace.py

import unittest
import os

import Data.DataBase as db_module
db_module.DATABASE_NAME = "test_travel_planner.db"

from Data.Models import initialize_database
from Logic.Auth import create_user, authenticate_user
from Logic.Place import Place, save_place, get_places_by_user


class TestPlace(unittest.TestCase):

    def setUp(self):
        initialize_database()
        create_user("testuser", "testpass")
        user = authenticate_user("testuser", "testpass")
        self.user_id = user["id"]

    def tearDown(self):
        if os.path.exists("test_travel_planner.db"):
            os.remove("test_travel_planner.db")

    def test_save_place_success(self):
        place = Place(name="Tokyo", lat=35.6820172, lng=139.76216)
        result = save_place(self.user_id, place)
        self.assertTrue(result)

    def test_save_place_without_coordinates_fails(self):
        place = Place(name="Unknown")
        result = save_place(self.user_id, place)
        self.assertFalse(result)

    def test_get_places_by_user_returns_saved(self):
        place = Place(name="Tokyo", lat=35.6820172, lng=139.76216)
        save_place(self.user_id, place)
        places = get_places_by_user(self.user_id)
        self.assertEqual(len(places), 1)
        self.assertEqual(places[0].name, "Tokyo")

    def test_places_isolated_between_users(self):
        create_user("otheruser", "otherpass")
        other = authenticate_user("otheruser", "otherpass")

        place = Place(name="Tokyo", lat=35.6820172, lng=139.76216)
        save_place(self.user_id, place)

        other_places = get_places_by_user(other["id"])
        self.assertEqual(len(other_places), 0)

    def test_get_places_empty_for_new_user(self):
        places = get_places_by_user(self.user_id)
        self.assertEqual(len(places), 0)


if __name__ == "__main__":
    unittest.main()
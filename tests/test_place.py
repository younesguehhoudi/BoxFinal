# tests/test_place.py

import unittest
from logic.place import build_api_url, extract_place_name, extract_latitude, extract_longitude

class TestPlaceFunctions(unittest.TestCase):

    def test_build_api_url(self):
        url = build_api_url("Lille")
        expected = "https://nominatim.openstreetmap.org/search?q=Lille&format=json&limit=1"
        self.assertEqual(url, expected)

    def test_extract_place_name(self):
        # Fake JSON data simulating the API response
        fake_data = [{"display_name": "Lille, Nord, France", "lat": "50.6365", "lon": "3.0635"}]
        name = extract_place_name(fake_data)
        self.assertEqual(name, "Lille, Nord, France")

    def test_extract_latitude(self):
        fake_data = [{"display_name": "Lille, Nord, France", "lat": "50.6365", "lon": "3.0635"}]
        lat = extract_latitude(fake_data)
        self.assertEqual(lat, "50.6365")

    def test_extract_longitude(self):
        fake_data = [{"display_name": "Lille, Nord, France", "lat": "50.6365", "lon": "3.0635"}]
        lon = extract_longitude(fake_data)
        self.assertEqual(lon, "3.0635")

    def test_extract_with_empty_data(self):
        # Simulating an API failure or no results
        empty_data = []
        name = extract_place_name(empty_data)
        lat = extract_latitude(empty_data)
        lon = extract_longitude(empty_data)
        
        self.assertEqual(name, None)
        self.assertEqual(lat, None)
        self.assertEqual(lon, None)

if __name__ == '__main__':
    unittest.main()
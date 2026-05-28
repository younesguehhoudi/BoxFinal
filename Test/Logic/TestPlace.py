"""Simple tests without classes."""

from Logic.Place import build_api_url, extract_place_name, extract_latitude, extract_longitude


def test_build_api_url():
	url = build_api_url("Lille")
	expected = "https://nominatim.openstreetmap.org/search?q=Lille&format=json&limit=1"
	assert url == expected


def test_extract_place_name():
	fake_data = [{"display_name": "Lille, Nord, France", "lat": "50.6365", "lon": "3.0635"}]
	name = extract_place_name(fake_data)
	assert name == "Lille, Nord, France"


def test_extract_latitude():
	fake_data = [{"display_name": "Lille, Nord, France", "lat": "50.6365", "lon": "3.0635"}]
	lat = extract_latitude(fake_data)
	assert lat == "50.6365"


def test_extract_longitude():
	fake_data = [{"display_name": "Lille, Nord, France", "lat": "50.6365", "lon": "3.0635"}]
	lon = extract_longitude(fake_data)
	assert lon == "3.0635"


def test_extract_with_empty_data():
	empty_data = []
	name = extract_place_name(empty_data)
	lat = extract_latitude(empty_data)
	lon = extract_longitude(empty_data)

	assert name is None
	assert lat is None
	assert lon is None
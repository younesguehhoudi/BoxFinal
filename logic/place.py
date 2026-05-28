# logic/place.py

import requests

def build_api_url(place_name):
    base_url = "https://nominatim.openstreetmap.org/search"
    url = base_url + "?q=" + place_name + "&format=json&limit=1"
    return url

def get_api_headers():
    headers = {
        "User-Agent": "TravelPlannerApp_StudentProject/1.0"
    }
    return headers

def execute_api_call(url, headers):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print("API Error: HTTP " + str(response.status_code))
            return []
    except requests.exceptions.RequestException as e:
        print("Network error: " + str(e))
        return []

def extract_place_name(json_data):
    if len(json_data) > 0:
        first_result = json_data[0]
        return first_result["display_name"]
    return None

def extract_latitude(json_data):
    if len(json_data) > 0:
        first_result = json_data[0]
        return first_result["lat"]
    return None

def extract_longitude(json_data):
    if len(json_data) > 0:
        first_result = json_data[0]
        return first_result["lon"]
    return None

def fetch_place_data_from_api(searched_name):
    print("Fetching data for " + searched_name + "...")
    
    url = build_api_url(searched_name)
    headers = get_api_headers()
    
    json_data = execute_api_call(url, headers)
    
    official_name = extract_place_name(json_data)
    latitude = extract_latitude(json_data)
    longitude = extract_longitude(json_data)
    
    return official_name, latitude, longitude
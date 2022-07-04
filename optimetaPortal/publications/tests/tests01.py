import requests

def test_get_location_check_status_code_equals_200():
     response = requests.get("http://localhost:8000/publications/api/publications/")
     assert response.status_code == 200

def test_get_locations_check_content_type_equals_json():
     response = requests.get("http://localhost:8000/publications/api/publications/")
     assert response.headers["Content-Type"] == "application/json"

def test_get_locations_for_us_90210_check_country_equals_united_states():
     response = requests.get("http://localhost:8000/publications/api/publications/")
     response_body = response.json()
     assert response_body["properties"]["name"] == "Example"


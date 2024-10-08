import pytest
import requests

# Base URL of the API
BASE_URL = "http://localhost:3000/api/v1"

# Test GET all item groups
def test_get_all_item_groups():
    response = requests.get(f"{BASE_URL}/item_groups", headers={"API_KEY":"a1b2c3d4e5"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for item_group in data:
        assert "id" in item_group
        assert "name" in item_group
        assert "description" in item_group
        assert "created_at" in item_group
        assert "updated_at" in item_group

# Test GET item group by ID
def test_get_item_group_by_id():
    item_group_id = 2  # Use an ID that exists in your item_groups.json
    response = requests.get(f"{BASE_URL}/item_groups/{item_group_id}", headers={"API_KEY":"a1b2c3d4e5"})
    assert response.status_code == 200
    item_group = response.json()
    assert item_group["id"] == item_group_id
    assert "name" in item_group
    assert "description" in item_group
    assert "created_at" in item_group
    assert "updated_at" in item_group

# Test PUT update item group
# To check it first make a put request, and to see it was changed make a get request
def test_update_item_group():
    updated_item_group = {
        "id": 3,
        "name": "Updated Stationeries",
        "description": "Updated description",
        "created_at": "1999-08-14 13:39:27",
        "updated_at": "2023-01-01 12:00:00"
    }
    
    item_group_id = 3
    
    # Update the item group using PUT request
    put_response = requests.put(f"{BASE_URL}/item_groups/{item_group_id}", json=updated_item_group, headers={"API_KEY":"a1b2c3d4e5"})
    
    # Ensure the update response is successful (200 OK)
    assert put_response.status_code == 200
    
    # Now make a GET request to verify the update
    get_response = requests.get(f"{BASE_URL}/item_groups/{item_group_id}", headers={"API_KEY":"a1b2c3d4e5"})
    
    # Ensure the GET response is successful (200 OK)
    assert get_response.status_code == 200
    
    # Check if the data was updated correctly
    data = get_response.json()
    assert data["name"] == "Updated Stationeries"
    assert data["description"] == "Updated description"

# Test DELETE item group by ID
def test_delete_item_group():
    item_group_id = 5  # Use an ID that exists in your item_groups.json
    response = requests.delete(f"{BASE_URL}/item_groups/{item_group_id}", headers={"API_KEY":"a1b2c3d4e5"})
    assert response.status_code == 200  # 200 No Content indicates successful deletion
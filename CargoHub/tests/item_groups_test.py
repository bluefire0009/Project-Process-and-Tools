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
    response = requests.get(f"{BASE_URL}/item_groups/{item_group_id}")
    assert response.status_code == 200
    item_group = response.json()
    assert item_group["id"] == item_group_id
    assert "name" in item_group
    assert "description" in item_group
    assert "created_at" in item_group
    assert "updated_at" in item_group

# Test POST new item group
def test_add_new_item_group():
    new_item_group = {
        "id": 6,
        "name": "Electronics",
        "description": "Electronic devices",
        "created_at": "2023-01-01 12:00:00",
        "updated_at": "2023-01-01 12:00:00"
    }
    response = requests.post(f"{BASE_URL}/item-groups", json=new_item_group)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 6
    assert data["name"] == "Electronics"

# Test PUT update item group
def test_update_item_group():
    updated_item_group = {
        "id": 2,
        "name": "Updated Stationery",
        "description": "Updated description",
        "created_at": "1999-08-14 13:39:27",
        "updated_at": "2023-01-01 12:00:00"
    }
    item_group_id = 2
    response = requests.put(f"{BASE_URL}/item_groups/{item_group_id}", json=updated_item_group)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Stationery"
    assert data["description"] == "Updated description"

# Test DELETE item group by ID
def test_delete_item_group():
    item_group_id = 5  # Use an ID that exists in your item_groups.json
    response = requests.delete(f"{BASE_URL}/item_groups/{item_group_id}")
    assert response.status_code == 204  # 204 No Content indicates successful deletion
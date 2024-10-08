import pytest
import requests

@pytest.fixture
def _DataPytestFixture():
    url = 'http://localhost:3000/api/v1'
    api_key = 'a1b2c3d4e5'
    return url, api_key

# Test GET all item groups
def test_get_all_item_groups(_DataPytestFixture):
    url, api_key = _DataPytestFixture
    response = requests.get(f"{url}/item_groups", headers={"API_KEY": api_key})
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
def test_get_item_group_by_id(_DataPytestFixture):
    url, api_key = _DataPytestFixture
    item_group_id = 2  # Use an ID that exists in your item_groups.json
    response = requests.get(f"{url}/item_groups/{item_group_id}", headers={"API_KEY": api_key})
    assert response.status_code == 200
    item_group = response.json()
    assert item_group["id"] == item_group_id
    assert "name" in item_group
    assert "description" in item_group
    assert "created_at" in item_group
    assert "updated_at" in item_group

# Test ADD new item group (currently no POST endpoint available)
def test_add_new_item_group_and_delete_new_item_group_afterwards(_DataPytestFixture):
    url, api_key = _DataPytestFixture
    new_item_group = {
        "id": 999999999,
        "name": "Electronics",
        "description": "Electronic devices",
        "created_at": "2023-01-01 12:00:00",
        "updated_at": "2023-01-01 12:00:00"
    }
    response = requests.post(f"{url}/item-groups", json=new_item_group, headers={"API_KEY": api_key})
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 999999999
    assert data["name"] == "Electronics"

    item_group_id = 999999999  # Use an ID that exists in your item_groups.json
    response = requests.delete(f"{url}/item_groups/{item_group_id}", headers={"API_KEY": api_key})
    assert response.status_code == 200  # 200 No Content indicates successful deletion

# Test PUT update item group
def test_update_item_group(_DataPytestFixture):
    url, api_key = _DataPytestFixture
    item_group_id = 99
    
    # Retrieve original data to restore later
    original_data = requests.get(f"{url}/item_groups/{item_group_id}", headers={"API_KEY": api_key}).json()
    
    updated_item_group = {
        "id": 100,
        "name": "Updated Stationeries",
        "description": "Updated description",
        "created_at": "1999-08-14 13:39:27",
        "updated_at": "2023-01-01 12:00:00"
    }
    
    # Update the item group using PUT request
    put_response = requests.put(f"{url}/item_groups/{item_group_id}", json=updated_item_group, headers={"API_KEY": api_key})
    
    # Ensure the update response is successful (200 OK)
    assert put_response.status_code == 200
    
    # Now make a GET request to verify the update
    get_response = requests.get(f"{url}/item_groups/{updated_item_group['id']}", headers={"API_KEY": api_key})
    
    # Ensure the GET response is successful (200 OK)
    assert get_response.status_code == 200
    
    # Check if the data was updated correctly
    data = get_response.json()
    assert data["name"] == "Updated Stationeries"
    assert data["description"] == "Updated description"

    # Restore the original data
    restore_response = requests.put(f"{url}/item_groups/{updated_item_group['id']}", json=original_data, headers={"API_KEY": api_key})
    assert restore_response.status_code == 200
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
    response = requests.get(
        f"{url}/item_groups/{item_group_id}", headers={"API_KEY": api_key})
    assert response.status_code == 200
    item_group = response.json()
    assert item_group["id"] == item_group_id
    assert "name" in item_group
    assert "description" in item_group
    assert "created_at" in item_group
    assert "updated_at" in item_group


# Test GET items by item group id
def test_get_items_by_item_group_id(_DataPytestFixture):
    url, api_key = _DataPytestFixture
    item_group_id = 73
    
    # Make the GET request to fetch items for a specific item group
    response = requests.get(f"{url}/item_groups/{item_group_id}/items", headers={"API_KEY": api_key})
    
    # Ensure the request was successful
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    
    # Parse the response JSON
    data = response.json()
    
    # Ensure the data is a list
    assert isinstance(data, list), "Expected a list of items"
    
    # Check each item in the list
    for item in data:
        assert "uid" in item
        assert "code" in item
        assert "description" in item
        assert "short_description" in item
        assert "upc_code" in item
        assert "model_number" in item
        assert "commodity_code" in item
        assert "item_line" in item
        assert "item_group" in item
        assert item["item_group"] == item_group_id  # Ensure the item belongs to the correct group
        assert "item_type" in item
        assert "unit_purchase_quantity" in item
        assert "unit_order_quantity" in item
        assert "pack_order_quantity" in item
        assert "supplier_id" in item
        assert "supplier_code" in item
        assert "supplier_part_number" in item
        assert "created_at" in item
        assert "updated_at" in item

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
    response = requests.post(
        f"{url}/item_groups", json=new_item_group, headers={"API_KEY": api_key})
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 999999999
    assert data["name"] == "Electronics"

    item_group_id = 999999999  # Use an ID that exists in your item_groups.json
    response = requests.delete(
        f"{url}/item_groups/{item_group_id}", headers={"API_KEY": api_key})
    assert response.status_code == 200  # 200 No Content indicates successful deletion

# Test PUT update item group
def test_update_item_group(_DataPytestFixture):
    url, api_key = _DataPytestFixture
    item_group_id = 99

    # Retrieve original data to restore later
    original_data = requests.get(
        f"{url}/item_groups/{item_group_id}", headers={"API_KEY": api_key}).json()

    updated_item_group = {
        "id": 100,
        "name": "Updated Stationeries",
        "description": "Updated description",
        "created_at": "1999-08-14 13:39:27",
        "updated_at": "2023-01-01 12:00:00"
    }

    # Update the item group using PUT request
    put_response = requests.put(
        f"{url}/item_groups/{item_group_id}", json=updated_item_group, headers={"API_KEY": api_key})

    # Ensure the update response is successful (200 OK)
    assert put_response.status_code == 200

    # Now make a GET request to verify the update
    get_response = requests.get(
        f"{url}/item_groups/{updated_item_group['id']}", headers={"API_KEY": api_key})

    # Ensure the GET response is successful (200 OK)
    assert get_response.status_code == 200

    # Check if the data was updated correctly
    data = get_response.json()
    assert data["name"] == "Updated Stationeries"
    assert data["description"] == "Updated description"

    # Restore the original data
    restore_response = requests.put(
        f"{url}/item_groups/{updated_item_group['id']}", json=original_data, headers={"API_KEY": api_key})
    assert restore_response.status_code == 200

# Test DELETE item group by ID
def test_delete_item_group_by_id(_DataPytestFixture):
    url, api_key = _DataPytestFixture
    new_item_group = {
        "id": 999999999,
        "name": "Electronics",
        "description": "Electronic devices",
        "created_at": "2023-01-01 12:00:00",
        "updated_at": "2023-01-01 12:00:00"
    }

    # Correcting the URL to match the API convention
    response = requests.post(
        f"{url}/item_groups", json=new_item_group, headers={"API_KEY": api_key})
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 999999999
    assert data["name"] == "Electronics"

    item_group_id = 999999999
    response = requests.delete(
        f"{url}/item_groups/{item_group_id}", headers={"API_KEY": api_key})
    assert response.status_code == 200  # 200 No Content indicates successful deletion

    # Verify the item group is actually deleted by trying to GET it
    get_response = requests.get(
        f"{url}/item_groups/{item_group_id}", headers={"API_KEY": api_key})
    assert get_response.status_code == 404  # 404 Not Found confirms it was deleted


def test_get_item_group_with_non_existent_id(_DataPytestFixture):
    url, api_key = _DataPytestFixture
    non_existent_item_group_id = 9999999999999  # An ID that does not exist in the database

    # Make the GET request with a non-existent item_group_id
    response = requests.get(f"{url}/item_groups/{non_existent_item_group_id}", headers={"API_KEY": api_key})

    # Log the response content for debugging
    print(response.text)

    # Expecting a 200 status code
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    # Check if the response is None
    response_json = response.json()
    assert response_json is None, "Expected response to be None for non-existent item groups"
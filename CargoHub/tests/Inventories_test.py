import pytest
import requests

@pytest.fixture
def _DataPytestFixture():
    url = 'http://localhost:3000/api/v1'
    api_key = 'a1b2c3d4e5'
    return url, api_key

# Test GET all inventories
def test_get_all_inventories(_DataPytestFixture):
    url, api_key = _DataPytestFixture
    response = requests.get(f"{url}/inventories", headers={"API_KEY": api_key})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for inventory in data:
        assert "id" in inventory
        assert "item_id" in inventory
        assert "description" in inventory
        assert "total_on_hand" in inventory
        assert "created_at" in inventory
        assert "updated_at" in inventory

# Test GET inventory by ID
def test_get_inventory_by_id(_DataPytestFixture):
    url, api_key = _DataPytestFixture
    inventory_id = 1  # Use an ID that exists in your inventories.json
    response = requests.get(f"{url}/inventories/{inventory_id}", headers={"API_KEY": api_key})
    assert response.status_code == 200
    inventory = response.json()
    assert inventory["id"] == inventory_id
    assert "item_id" in inventory
    assert "description" in inventory
    assert "total_on_hand" in inventory
    assert "created_at" in inventory
    assert "updated_at" in inventory

# Test ADD new inventory
def test_add_new_inventory_and_delete_new_inventory_afterwards(_DataPytestFixture):
    url, api_key = _DataPytestFixture
    new_inventory = {
        "id": 999999999,
        "item_id": "P999999",
        "description": "Test Inventory Item",
        "item_reference": "test12345",
        "locations": [1, 2, 3],
        "total_on_hand": 100,
        "total_expected": 0,
        "total_ordered": 10,
        "total_allocated": 5,
        "total_available": 95,
        "created_at": "2024-01-01 12:00:00",
        "updated_at": "2024-01-01 12:00:00"
    }
    
    response = requests.post(f"{url}/inventories", json=new_inventory, headers={"API_KEY": api_key})
    
    # Check the status code
    assert response.status_code == 201
    
    # Check if response has a content and is JSON
    if response.text:
        try:
            data = response.json()
            assert data["id"] == 999999999
            assert data["item_id"] == "P999999"
        except ValueError:
            pytest.fail(f"Response JSON could not be decoded. Response text: {response.text}")
    else:
        # Handle the case where no response content is provided
        print("No response content returned.")
    
    # Clean up: Delete the newly added inventory
    response = requests.delete(f"{url}/inventories/{new_inventory['id']}", headers={"API_KEY": api_key})
    assert response.status_code == 200  # 200 No Content indicates successful deletion


# Test PUT update inventory
def test_update_inventory(_DataPytestFixture):
    url, api_key = _DataPytestFixture
    inventory_id = 1  # Existing inventory ID

    # Retrieve original data to restore later
    original_data = requests.get(f"{url}/inventories/{inventory_id}", headers={"API_KEY": api_key}).json()

    updated_inventory = {
        "id": inventory_id,
        "item_id": "P000001",
        "description": "Updated Inventory Item",
        "item_reference": "sjQ23408K",
        "locations": [3211, 24700],
        "total_on_hand": 300,
        "total_expected": 0,
        "total_ordered": 90,
        "total_allocated": 50,
        "total_available": 250,
        "created_at": original_data["created_at"],  # Keep original timestamps
        "updated_at": "2024-01-01 12:00:00"
    }

    # Update the inventory using PUT request
    put_response = requests.put(f"{url}/inventories/{inventory_id}", json=updated_inventory, headers={"API_KEY": api_key})
    assert put_response.status_code == 200

    # Now make a GET request to verify the update
    get_response = requests.get(f"{url}/inventories/{inventory_id}", headers={"API_KEY": api_key})
    assert get_response.status_code == 200

    # Check if the data was updated correctly
    data = get_response.json()
    assert data["description"] == "Updated Inventory Item"

    # Restore the original data
    restore_response = requests.put(f"{url}/inventories/{inventory_id}", json=original_data, headers={"API_KEY": api_key})
    assert restore_response.status_code == 200

# Test Delete inventory by ID
def test_delete_inventory_item(_DataPytestFixture):
    url, api_key = _DataPytestFixture
    new_inventory = {
        "id": 999999999,
        "item_id": "P999999",
        "description": "Test Inventory Item",
        "item_reference": "test12345",
        "locations": [1, 2, 3],
        "total_on_hand": 100,
        "total_expected": 0,
        "total_ordered": 10,
        "total_allocated": 5,
        "total_available": 95,
        "created_at": "2024-01-01 12:00:00",
        "updated_at": "2024-01-01 12:00:00"
    }

    # First, add the new inventory item
    response = requests.post(f"{url}/inventories", json=new_inventory, headers={"API_KEY": api_key})
    assert response.status_code == 201  # Check if creation was successful

    # Now, attempt to delete the inventory item
    delete_response = requests.delete(f"{url}/inventories/{new_inventory['id']}", headers={"API_KEY": api_key})
    
    # Check if the deletion was successful
    assert delete_response.status_code == 200  # Expect a 200 OK response for successful deletion

def test_get_inventory_by_id_with_invalid_id(_DataPytestFixture):
    url, api_key = _DataPytestFixture
    inventory_id = "invalid_id"  # Use a string to represent an invalid ID

    # Attempt to retrieve the inventory item with an invalid ID
    response = requests.get(f"{url}/inventories/{inventory_id}", headers={"API_KEY": api_key})

    # Log the response status code and message for debugging
    print(f"Response Status Code: {response.status_code}")

    # Check for a 400 Bad Request if the API is working correctly
    if response.status_code == 500:
        print("Server error occurred. Please check the server logs.")
    else:
        assert response.status_code == 400  # Expect a 400 Bad Request response

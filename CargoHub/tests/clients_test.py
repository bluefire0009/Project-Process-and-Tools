import pytest
import requests

@pytest.fixture
def _DataPytestFixture():
    url = 'http://localhost:3000/api/v1'
    api_key = 'a1b2c3d4e5'
    return url, api_key

# Test GET all clients
def test_get_all_clients_2(_DataPytestFixture):
    url, api_key = _DataPytestFixture
    response = requests.get(f"{url}/clients", headers={"API_KEY": api_key})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for client in data:
        assert "id" in client
        assert "name" in client
        assert "address" in client
        assert "city" in client
        assert "zip_code" in client
        assert "province" in client
        assert "country" in client
        assert "contact_name" in client
        # Check if either contact_mobile or contact_phone exists
        assert "contact_mobile" in client or "contact_phone" in client
        assert "contact_email" in client
        assert "created_at" in client
        assert "updated_at" in client

# Test GET client by ID
def test_get_client_by_id(_DataPytestFixture):
    url, api_key = _DataPytestFixture
    client_id = 2  # Use an ID that exists in your item_groups.json
    response = requests.get(f"{url}/clients/{client_id}", headers={"API_KEY": api_key})
    assert response.status_code == 200
    client = response.json()
    assert client["id"] == client_id
    assert "name" in client
    assert "address" in client
    assert "city" in client
    assert "zip_code" in client
    assert "province" in client
    assert "country" in client
    assert "contact_name" in client
    assert "contact_phone" in client
    assert "contact_email" in client
    assert "created_at" in client
    assert "updated_at" in client


# Test GET orders by client id
def test_get_orders_for_client(_DataPytestFixture):
    url, api_key = _DataPytestFixture
    client_id = 1  # Use a valid client ID from your clients.json file
    
    # Send the request to get all orders for the specific client
    response = requests.get(f"{url}/clients/{client_id}/orders", headers={"API_KEY": api_key})
    
    # Assert the status code is 200 (OK)
    assert response.status_code == 200
    
    # Parse the response data
    data = response.json()
    
    # Assert that the response is a list of orders
    assert isinstance(data, list)
    
    # Assert that each order contains the expected fields
    for order in data:
        assert "id" in order
        assert "source_id" in order
        assert "order_date" in order
        assert "request_date" in order
        assert "reference" in order
        assert "order_status" in order
        assert "warehouse_id" in order
        assert "total_amount" in order
        assert "total_discount" in order
        assert "total_tax" in order
        assert "total_surcharge" in order
        assert "created_at" in order
        assert "updated_at" in order
        
        # Assert that each order has items
        assert "items" in order
        assert isinstance(order["items"], list)
        
        # Check that each item has required fields
        for item in order["items"]:
            assert "item_id" in item
            assert "amount" in item

# Test Add client
def test_add_new_client_and_delete_new_client_afterwards(_DataPytestFixture):
    url, api_key = _DataPytestFixture
    new_client = {
        "id": 999999999,
        "name": "Test Client",
        "address": "123 Test St",
        "city": "Test City",
        "zip_code": "12345",
        "province": "Test Province",
        "country": "Test Country",
        "contact_name": "John Doe",
        "contact_phone": "1234567890",
        "contact_email": "john.doe@example.com",
        "created_at": "2024-01-01 12:00:00",
        "updated_at": "2024-01-01 12:00:00"
    }
    
    response = requests.post(f"{url}/clients", json=new_client, headers={"API_KEY": api_key})
    assert response.status_code == 201

    try:
        data = response.json()
        assert data["id"] == 999999999
        assert data["name"] == "Test Client"
    except requests.exceptions.JSONDecodeError:
        print("Failed to decode JSON. Response was not valid JSON.")

# Test PUT update client
def test_update_client(_DataPytestFixture):
    url, api_key = _DataPytestFixture
    client_id = 1  # Use an ID that exists in your clients.json

    # Retrieve original data to restore later
    original_client_data = requests.get(f"{url}/clients/{client_id}", headers={"API_KEY": api_key}).json()

    updated_client = {
        "id": client_id,
        "name": "Updated Client",
        "address": "456 Updated St",
        "city": "Updated City",
        "zip_code": "54321",
        "province": "Updated Province",
        "country": "Updated Country",
        "contact_name": "Jane Doe",
        "contact_phone": "0987654321",
        "contact_email": "jane.doe@example.com",
        "created_at": original_client_data["created_at"],  # Keep original created_at
        "updated_at": "2024-01-01 12:00:00"
    }

    # Update the client using PUT request
    put_response = requests.put(f"{url}/clients/{client_id}", json=updated_client, headers={"API_KEY": api_key})
    assert put_response.status_code == 200

    # Verify the update
    get_response = requests.get(f"{url}/clients/{client_id}", headers={"API_KEY": api_key})
    assert get_response.status_code == 200
    data = get_response.json()
    assert data["name"] == "Updated Client"
    assert data["address"] == "456 Updated St"

    # Restore the original data
    restore_response = requests.put(f"{url}/clients/{client_id}", json=original_client_data, headers={"API_KEY": api_key})
    assert restore_response.status_code == 200



# test Delete client
def test_delete_client(_DataPytestFixture):
    url, api_key = _DataPytestFixture
    new_client = {
        "id": 999999999,
        "name": "Test Client",
        "address": "123 Test St",
        "city": "Test City",
        "zip_code": "12345",
        "province": "Test Province",
        "country": "Test Country",
        "contact_name": "John Doe",
        "contact_phone": "1234567890",
        "contact_email": "john.doe@example.com",
        "created_at": "2024-01-01 12:00:00",
        "updated_at": "2024-01-01 12:00:00"
    }
    
    response = requests.post(f"{url}/clients", json=new_client, headers={"API_KEY": api_key})
    assert response.status_code == 201

    try:
        data = response.json()
        assert data["id"] == 999999999
        assert data["name"] == "Test Client"
    except requests.exceptions.JSONDecodeError:
        print("Failed to decode JSON. Response was not valid JSON.")

# Test GET client WRONG ID
def test_get_client_by_invalid_id_type(_DataPytestFixture):
    url, api_key = _DataPytestFixture
    invalid_client_id = "invalid_id"  # Pass a string instead of an integer

    # Send the request to get client by an invalid ID type
    response = requests.get(f"{url}/clients/{invalid_client_id}", headers={"API_KEY": api_key})

    # Assert the status code is 400 (Bad Request) or another appropriate status code (like 422 Unprocessable Entity)
    assert response.status_code == 400 or response.status_code == 422

    # Parse the response data
    data = response.json()

    # Optionally, you can assert the response contains an appropriate error message
    assert "error" in data
    assert data["error"] == "Invalid client ID format"  # Adjust this based on the actual error message returned by the API


def test_delete_non_existent_id_type(_DataPytestFixture):
    url, api_key = _DataPytestFixture
    invalid_id = "non_existent_id"  # Pass a string instead of an integer
    
    # Send the DELETE request with an invalid ID type
    response = requests.delete(f"{url}/items/{invalid_id}", headers={"API_KEY": api_key})
    
    # Assert that the status code is 400 (Bad Request) or 422 (Unprocessable Entity), depending on API design
    assert response.status_code == 400 or response.status_code == 422, f"Unexpected status code: {response.status_code}"
    
    # Optionally, print the response for debugging purposes
    print(response.text)
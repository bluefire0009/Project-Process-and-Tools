import time
import pytest
import requests
import http.client
import json

BASE_URL = "http://localhost:3000/api/v1"

ITEMS_PATH = 'CargoHub/data/items.json'

@pytest.fixture
def setup_teardown():
    # Setup code
    # Save the warehouses.json content
    with open(ITEMS_PATH, 'r') as itemsFile:
        global itemsBefore 
        itemsBefore = itemsFile.read()
        itemsFile.close()
    
    # Overwrite the content of warehouses.json with empty file   
    with open(ITEMS_PATH, 'w') as itemsFile:
        itemsFile.write("")
        itemsFile.close()

    yield
    # Teardown code
    # Restore the content of warehouses.json
    with open(ITEMS_PATH, 'w') as itemsFile:
        itemsFile.write(itemsBefore)
        itemsFile.close()

def test_get_all_items():
    connection = http.client.HTTPConnection('localhost', 3000)
    connection.request('GET', "/api/v1/items", headers={"API_KEY":"a1b2c3d4e5"})
    response = connection.getresponse()
    data = response.read()
    result = json.loads(data)
    assert response.status == 200
    assert len(result) > 1000
    assert result[0] == {
        "uid": "P000001",
        "code": "sjQ23408K",
        "description": "Face-to-face clear-thinking complexity",
        "short_description": "must",
        "upc_code": "6523540947122",
        "model_number": "63-OFFTq0T",
        "commodity_code": "oTo304",
        "item_line": 11,
        "item_group": 73,
        "item_type": 14,
        "unit_purchase_quantity": 47,
        "unit_order_quantity": 13,
        "pack_order_quantity": 11,
        "supplier_id": 34,
        "supplier_code": "SUP423",
        "supplier_part_number": "E-86805-uTM",
        "created_at": "2015-02-19 16:08:24",
        "updated_at": "2015-09-26 06:37:56"
    }

def test_get_item_by_id():
    connection = http.client.HTTPConnection('localhost', 3000)
    connection.request('GET', "/api/v1/items/P000002", headers={"API_KEY":"a1b2c3d4e5"})
    response = connection.getresponse()
    data = response.read()
    result = json.loads(data)
    
    assert response.status == 200
    assert result == {
        "uid": "P000002",
        "code": "nyg48736S",
        "description": "Focused transitional alliance",
        "short_description": "may",
        "upc_code": "9733132830047",
        "model_number": "ck-109684-VFb",
        "commodity_code": "y-20588-owy",
        "item_line": 69,
        "item_group": 85,
        "item_type": 39,
        "unit_purchase_quantity": 10,
        "unit_order_quantity": 15,
        "pack_order_quantity": 23,
        "supplier_id": 57,
        "supplier_code": "SUP312",
        "supplier_part_number": "j-10730-ESk",
        "created_at": "2020-05-31 16:00:08",
        "updated_at": "2020-11-08 12:49:21"
    }

def test_get_item_inventory():
    connection = http.client.HTTPConnection('localhost', 3000)
    connection.request('GET', "/api/v1/items/P000002/inventory", headers={"API_KEY":"a1b2c3d4e5"})
    response = connection.getresponse()
    data = response.read()
    result = json.loads(data)

    assert response.status == 200
    assert len(result) == 1
    assert result[0] == {
    "id": 2,
    "item_id": "P000002",
    "description": "Focused transitional alliance",
    "item_reference": "nyg48736S",
    "locations": [
      19800,
      23653,
      3068,
      3334,
      20477,
      20524,
      17579,
      2271,
      2293,
      22717
    ],
    "total_on_hand": 194,
    "total_expected": 0,
    "total_ordered": 139,
    "total_allocated": 0,
    "total_available": 55,
    "created_at": "2020-05-31 16:00:08",
    "updated_at": "2020-11-08 12:49:21"
  }

def test_get_item_inventory_totals():
    connection = http.client.HTTPConnection('localhost', 3000)
    connection.request('GET', "/api/v1/items/P000002/inventory/totals", headers={"API_KEY":"a1b2c3d4e5"})
    response = connection.getresponse()
    data = response.read()
    result = json.loads(data)

    assert response.status == 200
    assert result == {
    "total_expected": 0,
    "total_ordered": 139,
    "total_allocated": 0,
    "total_available": 55
    }

def test_post_item():
    connection = http.client.HTTPConnection('localhost', 3000)
    jsonData = json.dumps({
        "uid": "P999999",
        "code": "mYt79640E",
        "description": "Down-sized system-worthy productivity",
        "short_description": "pass",
        "upc_code": "2541112620796",
        "model_number": "ZK-417773-PXy",
        "commodity_code": "z-761-L5A",
        "item_line": 81,
        "item_group": 83,
        "item_type": 74,
        "unit_purchase_quantity": 3,
        "unit_order_quantity": 18,
        "pack_order_quantity": 13,
        "supplier_id": 10,
        "supplier_code": "SUP468",
        "supplier_part_number": "ZH-103509-MLv",
        "created_at": "2024-10-06 02:30:31",
        "updated_at": "2024-10-06 02:30:31"
    })
    connection.request('POST', "/api/v1/items", headers={"API_KEY":"a1b2c3d4e5", "Content-Type": "application/json"}, body=jsonData)
    time.sleep(1)
    response = connection.getresponse()

    assert response.status == 201

def test_put_item():
    jsonData = json.dumps({
        "uid": "P999999",
        "code": "mYt79640E",
        "description": "test123",
        "short_description": "pass",
        "upc_code": "2541112620796",
        "model_number": "ZK-417773-PXy",
        "commodity_code": "z-761-L5A",
        "item_line": 81,
        "item_group": 83,
        "item_type": 74,
        "unit_purchase_quantity": 3,
        "unit_order_quantity": 18,
        "pack_order_quantity": 13,
        "supplier_id": 10,
        "supplier_code": "SUP468",
        "supplier_part_number": "ZH-103509-MLv",
        "created_at": "2024-10-06 02:30:31",
        "updated_at": "2024-10-06 02:30:31"
    })
    
    connection = http.client.HTTPConnection('localhost', 3000)
    connection.request('PUT', "/api/v1/items/P999999", headers={"API_KEY":"a1b2c3d4e5", "Content-Type": "application/json"}, body=jsonData)
    time.sleep(2)
    response = connection.getresponse()

    assert response.code == 200

    connection.request('GET', "/api/v1/items/P999999", headers={"API_KEY":"a1b2c3d4e5"})
    response = connection.getresponse()
    data = response.read()
    result = json.loads(data)

    assert result['description'] == "test123"

def test_delete_item():
    connection = http.client.HTTPConnection('localhost', 3000)
    connection.request('DELETE', "/api/v1/items/P999999", headers={"API_KEY":"a1b2c3d4e5"})
    response = connection.getresponse()

    assert response.code == 200
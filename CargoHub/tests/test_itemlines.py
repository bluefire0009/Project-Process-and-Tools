import time
import pytest
import http.client
import json

BASE_URL = "http://localhost:3000/api/v1"

ITEMS_PATH = 'CargoHub/data/item_lines.json'


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


def test_get_all_item_lines():
    connection = http.client.HTTPConnection('localhost', 3000)
    connection.request('GET', "/api/v1/item_lines", headers={"API_KEY": "a1b2c3d4e5"})
    response = connection.getresponse()
    data = response.read()
    result = json.loads(data)
    assert response.status == 200
    assert len(result) > 80
    assert result[0] == {
        "id": 0,
        "name": "Tech Gadgets",
        "description": "",
        "created_at": "2022-08-18 07:05:25",
        "updated_at": "2023-05-15 15:44:28"
    }


def test_get_item_line_by_id():
    connection = http.client.HTTPConnection('localhost', 3000)
    connection.request('GET', "/api/v1/item_lines/1", headers={"API_KEY": "a1b2c3d4e5"})
    response = connection.getresponse()
    data = response.read()
    result = json.loads(data)

    assert response.status == 200
    assert result == {
        "id": 1,
        "name": "Home Appliances",
        "description": "",
        "created_at": "1979-01-16 07:07:50",
        "updated_at": "2024-01-05 23:53:25"
    }


def test_get_item_line_items():
    connection = http.client.HTTPConnection('localhost', 3000)
    connection.request('GET', "/api/v1/item_lines/1/items", headers={"API_KEY": "a1b2c3d4e5"})
    response = connection.getresponse()
    data = response.read()
    result = json.loads(data)

    assert response.status == 200
    assert len(result) == 109
    assert result[0] == {
        "uid": "P000104",
        "code": "RnV03385d",
        "description": "Enterprise-wide solution-oriented focus group",
        "short_description": "affect",
        "upc_code": "1111948769009",
        "model_number": "NHW191",
        "commodity_code": "S-83981-mJD",
        "item_line": 1,
        "item_group": 28,
        "item_type": 90,
        "unit_purchase_quantity": 44,
        "unit_order_quantity": 24,
        "pack_order_quantity": 5,
        "supplier_id": 36,
        "supplier_code": "SUP785",
        "supplier_part_number": "PAg021",
        "created_at": "2021-07-20 18:34:59",
        "updated_at": "2022-08-18 04:40:30"
    }


def test_put_item_line():
    jsonData = json.dumps({
        "id": 1,
        "name": "testing",
        "description": "test123",
        "created_at": "1979-01-16 07:07:50",
        "updated_at": "2024-01-05 23:53:25"
    })

    connection = http.client.HTTPConnection('localhost', 3000)
    connection.request(
        'PUT',
        "/api/v1/item_lines/1",
        headers={
            "API_KEY": "a1b2c3d4e5",
            "Content-Type": "application/json"},
        body=jsonData)
    time.sleep(2)
    response = connection.getresponse()

    assert response.code == 200

    connection.request('GET', "/api/v1/item_lines/1", headers={"API_KEY": "a1b2c3d4e5"})
    response = connection.getresponse()
    data = response.read()
    result = json.loads(data)

    assert result['description'] == "test123"


def test_delete_item():
    connection = http.client.HTTPConnection('localhost', 3000)
    connection.request('DELETE', "/api/v1/item_lines/1", headers={"API_KEY": "a1b2c3d4e5"})
    response = connection.getresponse()

    assert response.code == 200

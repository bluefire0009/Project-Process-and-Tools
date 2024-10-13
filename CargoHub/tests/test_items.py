import time
import pytest
import http.client
import json


@pytest.fixture
def _data():
    return "/api/v1", "a1b2c3d4e5"


def test_get_all_items(_data):
    url, key = _data
    connection = http.client.HTTPConnection('localhost', 3000)
    connection.request('GET', f"{url}/items", headers={"API_KEY": key})
    response = connection.getresponse()
    data = response.read()
    result = json.loads(data)
    assert response.status == 200
    assert isinstance(result, list)


def test_get_item_by_id(_data):
    url, key = _data
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
    connection.request(
        "POST",
        f"{url}/items",
        headers={
            "API_KEY": key,
            "Content-Type": "application/json"},
        body=jsonData)
    connection.getresponse()
    time.sleep(5)

    connection.request('GET', f"{url}/items/P999999", headers={"API_KEY": key})
    response = connection.getresponse()
    data = response.read()
    result = json.loads(data)

    connection.request('DELETE', f"{url}/items/P999999", headers={"API_KEY": key})

    assert response.status == 200
    assert result["uid"] == "P999999"
    assert result["code"] == "mYt79640E"
    assert result["description"] == "Down-sized system-worthy productivity"
    assert result["short_description"] == "pass"
    assert result["upc_code"] == "2541112620796"
    assert result["model_number"] == "ZK-417773-PXy"
    assert result["commodity_code"] == "z-761-L5A"
    assert result["item_line"] == 81
    assert result["item_group"] == 83
    assert result["item_type"] == 74
    assert result["unit_purchase_quantity"] == 3
    assert result["unit_order_quantity"] == 18
    assert result["pack_order_quantity"] == 13
    assert result["supplier_id"] == 10
    assert result["supplier_code"] == "SUP468"
    assert result["supplier_part_number"] == "ZH-103509-MLv"


def test_get_item_inventory(_data):
    url, key = _data
    connection = http.client.HTTPConnection('localhost', 3000)
    connection.request('GET', f"{url}/items/P000002/inventory", headers={"API_KEY": key})
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


def test_get_item_inventory_totals(_data):
    url, key = _data
    connection = http.client.HTTPConnection('localhost', 3000)
    connection.request('GET', f"{url}/items/P000002/inventory/totals", headers={"API_KEY": key})
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


def test_post_item(_data):
    url, key = _data
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
    connection.request(
        'POST',
        f"{url}/items",
        headers={
            "API_KEY": key,
            "Content-Type": "application/json"},
        body=jsonData)
    time.sleep(1)
    response = connection.getresponse()

    connection.request('DELETE', f"{url}/items/P999999", headers={"API_KEY": key})

    assert response.status == 201


def test_put_item(_data):
    url, key = _data
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
    connection.request(
        'POST',
        f"{url}/items",
        headers={
            "API_KEY": key,
            "Content-Type": "application/json"},
        body=jsonData)

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
    connection.request(
        'PUT',
        f"{url}/items/P999999",
        headers={
            "API_KEY": key,
            "Content-Type": "application/json"},
        body=jsonData)
    time.sleep(2)
    response = connection.getresponse()

    assert response.code == 200

    connection.request('GET', f"{url}/items/P999999", headers={"API_KEY": key})
    response = connection.getresponse()
    data = response.read()
    result = json.loads(data)

    connection.request('DELETE', f"{url}/items/P999999", headers={"API_KEY": key})
    assert result['description'] == "test123"


def test_delete_item(_data):
    url, key = _data
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
    connection.request(
        'POST',
        f"{url}/items",
        headers={
            "API_KEY": key,
            "Content-Type": "application/json"},
        body=jsonData)
    response = connection.getresponse()
    assert response.code == 201, "insertion failed"

    connection.request('DELETE', f"{url}/items/P999999", headers={"API_KEY": key})
    response = connection.getresponse()

    assert response.code == 200

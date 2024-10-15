import time
import pytest
import http.client
import json


@pytest.fixture
def _data():
    return http.client.HTTPConnection('localhost', 3000), "/api/v1", "a1b2c3d4e5"


def test_get_all_items(_data):
    connection, url, key = _data
    connection.request('GET', f"{url}/items", headers={"API_KEY": key})
    response = connection.getresponse()
    data = response.read()
    result = json.loads(data)
    assert response.status == 200
    assert isinstance(result, list)


def test_get_item_by_id(_data):
    connection, url, key = _data
    connection.request('GET', f"{url}/items/P000005", headers={"API_KEY": key})
    response = connection.getresponse()
    data = response.read()
    result = json.loads(data)

    assert response.status == 200
    assert result == {
        "uid": "P000005",
        "code": "mHo61152n",
        "description": "Stand-alone 24hour emulation",
        "short_description": "there",
        "upc_code": "0943113854446",
        "model_number": "j-587-L3H",
        "commodity_code": "67-vxkaB7P",
        "item_line": 16,
        "item_group": 50,
        "item_type": 28,
        "unit_purchase_quantity": 44,
        "unit_order_quantity": 2,
        "pack_order_quantity": 20,
        "supplier_id": 35,
        "supplier_code": "SUP347",
        "supplier_part_number": "NzG-36a1",
        "created_at": "2016-03-28 10:35:32",
        "updated_at": "2024-05-20 22:42:05"
    }


def test_get_item_inventory(_data):
    connection, url, key = _data
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
    connection, url, key = _data
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
    connection, url, key = _data
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

    assert response.status == 201


def test_put_item(_data):
    connection, url, key = _data

    jsonData = json.dumps({
        "uid": "P000005",
        "code": "mHo61152n",
        "description": "test123",
        "short_description": "there",
        "upc_code": "0943113854446",
        "model_number": "j-587-L3H",
        "commodity_code": "67-vxkaB7P",
        "item_line": 16,
        "item_group": 50,
        "item_type": 28,
        "unit_purchase_quantity": 44,
        "unit_order_quantity": 2,
        "pack_order_quantity": 20,
        "supplier_id": 35,
        "supplier_code": "SUP347",
        "supplier_part_number": "NzG-36a1",
        "created_at": "2016-03-28 10:35:32",
        "updated_at": "2024-05-20 22:42:05"
    })

    connection = http.client.HTTPConnection('localhost', 3000)
    connection.request(
        'PUT',
        f"{url}/items/P000005",
        headers={
            "API_KEY": key,
            "Content-Type": "application/json"},
        body=jsonData)
    time.sleep(2)
    response = connection.getresponse()

    assert response.code == 200

    connection.request('GET', f"{url}/items/P000005", headers={"API_KEY": key})
    response = connection.getresponse()
    data = response.read()
    result = json.loads(data)

    jsonData = json.dumps({
        "uid": "P000005",
        "code": "mHo61152n",
        "description": "Stand-alone 24hour emulation",
        "short_description": "there",
        "upc_code": "0943113854446",
        "model_number": "j-587-L3H",
        "commodity_code": "67-vxkaB7P",
        "item_line": 16,
        "item_group": 50,
        "item_type": 28,
        "unit_purchase_quantity": 44,
        "unit_order_quantity": 2,
        "pack_order_quantity": 20,
        "supplier_id": 35,
        "supplier_code": "SUP347",
        "supplier_part_number": "NzG-36a1",
        "created_at": "2016-03-28 10:35:32",
        "updated_at": "2024-05-20 22:42:05"
    })
    connection.request(
        'PUT',
        f"{url}/items/P000005",
        headers={
            "API_KEY": key,
            "Content-Type": "application/json"},
        body=jsonData)
    time.sleep(2)
    response = connection.getresponse()
    assert result['description'] == "test123"


def test_delete_item(_data):
    connection, url, key = _data
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


def test_get_item_invalid_id(_data):
    connection, url, key = _data
    connection.request('GET', f"{url}/items/invalidIdentification", headers={"API_KEY": key})
    response = connection.getresponse()

    assert response.status == 500


def test_post_invalid_object(_data):
    connection, url, key = _data
    jsonData = json.dumps({
        "uid": "P9999999",
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

    assert response.status == 201

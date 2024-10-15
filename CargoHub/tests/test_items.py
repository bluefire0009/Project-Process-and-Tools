import time
import pytest
import http.client
import json


@pytest.fixture
def _data():
    return http.client.HTTPConnection('localhost', 3000), "/api/v1", "a1b2c3d4e5"


def test_get_all_items(_data):
    connection, url, key = _data

    test_data = {
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
    }
    jsonData = json.dumps(test_data)
    connection.request(
        'POST',
        f"{url}/items",
        headers={
            "API_KEY": key,
            "Content-Type": "application/json"},
        body=jsonData)
    post_response = connection.getresponse()
    assert post_response.code == 201, "insertion failed"

    connection.request('GET', f"{url}/items", headers={"API_KEY": key})
    response = connection.getresponse()
    data = response.read()
    result = json.loads(data)

    connection.request('DELETE', f"{url}/items/P999999", headers={"API_KEY": key})
    delete_response = connection.getresponse()
    assert delete_response.status == 200, "delete failed"

    resultIds = [w["uid"] for w in result]

    assert response.status == 200
    assert isinstance(result, list)
    assert len(result) > 0
    assert test_data["uid"] in resultIds


def test_get_item_by_id(_data):
    connection, url, key = _data
    
    test_data = {
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
    }
    jsonData = json.dumps(test_data)
    connection.request(
        'POST',
        f"{url}/items",
        headers={
            "API_KEY": key,
            "Content-Type": "application/json"},
        body=jsonData)
    post_response = connection.getresponse()
    assert post_response.code == 201, "insertion failed"

    connection.request('GET', f"{url}/items/P999999", headers={"API_KEY": key})
    response = connection.getresponse()
    data = response.read()
    result = json.loads(data)

    connection.request('DELETE', f"{url}/items/P999999", headers={"API_KEY": key})
    delete_response = connection.getresponse()
    assert delete_response.status == 200, "delete failed"

    assert response.status == 200
    assert result["uid"] == test_data["uid"] 
    assert result["code"] == test_data["code"] 
    assert result["description"] == test_data["description"] 
    assert result["short_description"] == test_data["short_description"] 
    assert result["upc_code"] == test_data["upc_code"] 
    assert result["model_number"] == test_data["model_number"] 
    assert result["commodity_code"] == test_data["commodity_code"] 
    assert result["item_line"] == test_data["item_line"] 
    assert result["item_group"] == test_data["item_group"] 
    assert result["item_type"] == test_data["item_type"] 
    assert result["unit_purchase_quantity"] == test_data["unit_purchase_quantity"] 
    assert result["unit_order_quantity"] == test_data["unit_order_quantity"] 
    assert result["pack_order_quantity"] == test_data["pack_order_quantity"] 
    assert result["supplier_id"] == test_data["supplier_id"] 
    assert result["supplier_code"] == test_data["supplier_code"] 
    assert result["supplier_part_number"] == test_data["supplier_part_number"] 


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
    test_data = {
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
    }
    jsonData = json.dumps(test_data)
    connection.request(
        'POST',
        f"{url}/items",
        headers={
            "API_KEY": key,
            "Content-Type": "application/json"},
        body=jsonData)
    time.sleep(1)
    response = connection.getresponse()

    
    connection.request('GET', f"{url}/items/P999999", headers={"API_KEY": key})
    get_response = connection.getresponse()
    get_data = get_response.read()
    get_result = json.loads(get_data)

    
    connection.request('DELETE', f"{url}/items/P999999", headers={"API_KEY": key})
    delete_response = connection.getresponse()
    assert delete_response.status == 200, "delete failed"

    assert response.status == 201
    assert get_result["uid"] == test_data["uid"] 
    assert get_result["code"] == test_data["code"] 
    assert get_result["description"] == test_data["description"] 
    assert get_result["short_description"] == test_data["short_description"] 
    assert get_result["upc_code"] == test_data["upc_code"] 
    assert get_result["model_number"] == test_data["model_number"] 
    assert get_result["commodity_code"] == test_data["commodity_code"] 
    assert get_result["item_line"] == test_data["item_line"] 
    assert get_result["item_group"] == test_data["item_group"] 
    assert get_result["item_type"] == test_data["item_type"] 
    assert get_result["unit_purchase_quantity"] == test_data["unit_purchase_quantity"] 
    assert get_result["unit_order_quantity"] == test_data["unit_order_quantity"] 
    assert get_result["pack_order_quantity"] == test_data["pack_order_quantity"] 
    assert get_result["supplier_id"] == test_data["supplier_id"] 
    assert get_result["supplier_code"] == test_data["supplier_code"] 
    assert get_result["supplier_part_number"] == test_data["supplier_part_number"] 


def test_put_item(_data):
    connection, url, key = _data

    test_data = {
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
    }
    jsonData = json.dumps(test_data)
    connection.request(
        'POST',
        f"{url}/items",
        headers={
            "API_KEY": key,
            "Content-Type": "application/json"},
        body=jsonData)
    connection.getresponse()

    test_updated_data = {
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
    }

    jsonData = json.dumps(test_updated_data)
    
    connection.request(
        'PUT',
        f"{url}/items/P999999",
        headers={
            "API_KEY": key,
            "Content-Type": "application/json"},
        body=jsonData)
    response = connection.getresponse()

    assert response.code == 200

    connection.request('GET', f"{url}/items/P999999", headers={"API_KEY": key})
    get_response = connection.getresponse()
    get_data = get_response.read()
    get_result = json.loads(get_data)

    connection.request('DELETE', f"{url}/items/P999999", headers={"API_KEY": key})
    delete_response = connection.getresponse()
    assert delete_response.status == 200, "delete failed"

    assert response.status == 200
    assert get_result["uid"] == test_updated_data["uid"] 
    assert get_result["code"] == test_updated_data["code"] 
    assert get_result["description"] == test_updated_data["description"] 
    assert get_result["short_description"] == test_updated_data["short_description"] 
    assert get_result["upc_code"] == test_updated_data["upc_code"] 
    assert get_result["model_number"] == test_updated_data["model_number"] 
    assert get_result["commodity_code"] == test_updated_data["commodity_code"] 
    assert get_result["item_line"] == test_updated_data["item_line"] 
    assert get_result["item_group"] == test_updated_data["item_group"] 
    assert get_result["item_type"] == test_updated_data["item_type"] 
    assert get_result["unit_purchase_quantity"] == test_updated_data["unit_purchase_quantity"] 
    assert get_result["unit_order_quantity"] == test_updated_data["unit_order_quantity"] 
    assert get_result["pack_order_quantity"] == test_updated_data["pack_order_quantity"] 
    assert get_result["supplier_id"] == test_updated_data["supplier_id"] 
    assert get_result["supplier_code"] == test_updated_data["supplier_code"] 
    assert get_result["supplier_part_number"] == test_updated_data["supplier_part_number"] 


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

    assert response.status == 400


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

    assert response.status == 400

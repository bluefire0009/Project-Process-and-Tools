import time
import pytest
import http.client
import json

BASE_URL = "http://localhost:3000/api/v1"


def test_get_all_item_types():
    connection = http.client.HTTPConnection('localhost', 3000)
    connection.request('GET', "/api/v1/item_types", headers={"API_KEY": "a1b2c3d4e5"})
    response = connection.getresponse()
    data = response.read()
    result = json.loads(data)
    assert response.status == 200
    assert result[0] == {
        "id": 0,
        "name": "Laptop",
        "description": "",
        "created_at": "2001-11-02 23:02:40",
        "updated_at": "2008-07-01 04:09:17"
    }


def test_get_item_types_by_id():
    connection = http.client.HTTPConnection('localhost', 3000)
    connection.request('GET', "/api/v1/item_types/1", headers={"API_KEY": "a1b2c3d4e5"})
    response = connection.getresponse()
    data = response.read()
    result = json.loads(data)

    assert response.status == 200
    assert result == {
        "id": 1,
        "name": "Desktop",
        "description": "",
        "created_at": "1993-07-28 13:43:32",
        "updated_at": "2022-05-12 08:54:35"
    }


def test_get_item_types_items():
    connection = http.client.HTTPConnection('localhost', 3000)
    connection.request('GET', "/api/v1/item_types/1/items", headers={"API_KEY": "a1b2c3d4e5"})
    response = connection.getresponse()
    data = response.read()
    result = json.loads(data)

    assert response.status == 200
    assert len(result) > 100
    assert result[0] == {
        "uid": "P000123",
        "code": "CRD57317J",
        "description": "Organic asymmetric data-warehouse",
        "short_description": "particularly",
        "upc_code": "9538419150098",
        "model_number": "Ws-6191",
        "commodity_code": "x-300-Y2v",
        "item_line": 33,
        "item_group": 2,
        "item_type": 1,
        "unit_purchase_quantity": 49,
        "unit_order_quantity": 4,
        "pack_order_quantity": 16,
        "supplier_id": 28,
        "supplier_code": "SUP467",
        "supplier_part_number": "I-776-D8c",
        "created_at": "2003-10-03 12:11:00",
        "updated_at": "2024-08-07 10:58:47"
    }


def test_put_item_types():
    jsonData = json.dumps({
        "id": 1,
        "name": "Desktop",
        "description": "test123",
        "created_at": "1993-07-28 13:43:32",
        "updated_at": "2022-05-12 08:54:35"
    })

    connection = http.client.HTTPConnection('localhost', 3000)
    connection.request(
        'PUT',
        "/api/v1/item_types/1",
        headers={
            "API_KEY": "a1b2c3d4e5",
            "Content-Type": "application/json"},
        body=jsonData)
    time.sleep(2)
    response = connection.getresponse()

    assert response.code == 200

    connection.request('GET', "/api/v1/item_types/1", headers={"API_KEY": "a1b2c3d4e5"})
    time.sleep(1)
    response = connection.getresponse()
    data = response.read()
    result = json.loads(data)

    assert result['description'] == "test123"


def test_delete_item_type():
    connection = http.client.HTTPConnection('localhost', 3000)
    connection.request('DELETE', "/api/v1/item_types/2", headers={"API_KEY": "a1b2c3d4e5"})
    response = connection.getresponse()

    assert response.code == 200

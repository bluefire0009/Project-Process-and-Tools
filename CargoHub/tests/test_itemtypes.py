import time
import pytest
import http.client
import json


@pytest.fixture
def _data():
    return http.client.HTTPConnection('localhost', 3000), "/api/v1", "a1b2c3d4e5"


def test_get_all_item_lines(_data):
    connection, url, key = _data
    connection.request('GET', f"{url}/item_types", headers={"API_KEY": key})
    response = connection.getresponse()
    data = response.read()
    result = json.loads(data)
    assert response.status == 200
    assert isinstance(result, list)


def test_get_item_types_by_id(_data):
    connection, url, key = _data

    connection.request(
        'GET', f"{url}/item_types/5", headers={"API_KEY": key})
    response = connection.getresponse()
    data = response.read()
    result = json.loads(data)

    assert response.status == 200
    assert result == {
        "id": 5,
        "name": "Headphones",
        "description": "",
        "created_at": "1995-07-05 08:05:05",
        "updated_at": "2010-02-04 10:11:54"
    }


def test_get_item_type_items(_data):
    connection, url, key = _data
    connection.request(
        'GET', f"{url}/item_types/1/items", headers={"API_KEY": key})
    response = connection.getresponse()
    data = response.read()
    result = json.loads(data)

    assert response.status == 200
    assert len(result) == 121
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


def test_post_item_type(_data):
    connection, url, key = _data
    jsonData = json.dumps({
        "id": 999999,
        "name": "Desktop",
        "description": "test123",
        "created_at": "1993-07-28 13:43:32",
        "updated_at": "2022-05-12 08:54:35"
    })
    connection.request(
        'POST',
        f"{url}/item_types",
        headers={
            "API_KEY": key,
            "Content-Type": "application/json"},
        body=jsonData)
    time.sleep(1)
    response = connection.getresponse()

    assert response.status == 201


def test_put_item_types(_data):
    connection, url, key = _data

    jsonData = json.dumps({
        "id": 5,
        "name": "Headphones",
        "description": "test123",
        "created_at": "1995-07-05 08:05:05",
        "updated_at": "2010-02-04 10:11:54"
    })

    connection.request(
        'PUT',
        f"{url}/item_types/5",
        headers={
            "API_KEY": key,
            "Content-Type": "application/json"},
        body=jsonData)
    time.sleep(2)
    response = connection.getresponse()

    assert response.code == 200

    connection.request(
        'GET', f"{url}/item_types/5", headers={"API_KEY": key})
    response = connection.getresponse()
    data = response.read()
    result = json.loads(data)

    assert result['description'] == "test123"


def test_delete_item_type(_data):
    connection, url, key = _data

    connection.request(
        'DELETE', f"{url}/item_types/999999", headers={"API_KEY": key})
    response = connection.getresponse()

    assert response.code == 200


def test_get_item_type_invalid_id(_data):
    connection, url, key = _data
    connection.request('GET', f"{url}/item_types/invalidIdentification", headers={"API_KEY": key})
    response = connection.getresponse()

    assert response.status == 500


def test_post_invalid_object(_data):
    connection, url, key = _data
    jsonData = json.dumps({
        "id": "99999999",
    })
    connection.request(
        'POST',
        f"{url}/item_types",
        headers={
            "API_KEY": key,
            "Content-Type": "application/json"},
        body=jsonData)
    time.sleep(1)
    response = connection.getresponse()

    assert response.status == 500

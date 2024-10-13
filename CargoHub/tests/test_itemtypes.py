import time
import pytest
import http.client
import json


@pytest.fixture
def _data():
    return "/api/v1", "a1b2c3d4e5"

def test_get_all_item_lines(_data):
    url, key = _data
    connection = http.client.HTTPConnection('localhost', 3000)
    connection.request('GET', f"{url}/item_types", headers={"API_KEY": key})
    response = connection.getresponse()
    data = response.read()
    result = json.loads(data)
    assert response.status == 200
    assert isinstance(result, list)


def test_get_item_types_by_id(_data):
    url, key = _data
    connection = http.client.HTTPConnection('localhost', 3000)

    jsonData = json.dumps({
        "id": 999999,
        "name": "test Desktop",
        "description": "test 123",
        "created_at": "1993-07-28 13:43:32",
        "updated_at": "2022-05-12 08:54:35"
    })
    connection.request(
        "POST",
        f"{url}/item_types",
        headers={
            "API_KEY": key,
            "Content-Type": "application/json"},
        body=jsonData)
    connection.getresponse()
    time.sleep(5)

    connection.request(
        'GET', f"{url}/item_types/999999", headers={"API_KEY": key})
    response = connection.getresponse()
    data = response.read()
    result = json.loads(data)

    connection.request(
        'DELETE', f"{url}/item_types/999999", headers={"API_KEY": key})

    assert response.status == 200
    assert result["id"] == "999999"
    assert result["name"] == "test Desktop"
    assert result["description"] == "test 123"


def test_get_item_type_items(_data):
    url, key = _data
    connection = http.client.HTTPConnection('localhost', 3000)
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
    url, key = _data
    connection = http.client.HTTPConnection('localhost', 3000)
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

    connection.request(
        'DELETE', f"{url}/item_types/999999", headers={"API_KEY": key})

    assert response.status == 201


def test_put_item_types(_data):
    url, key = _data
    connection = http.client.HTTPConnection('localhost', 3000)
    jsonData = json.dumps({
        "id": 999999,
        "name": "Test Appliances",
        "description": "test 123",
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

    jsonData = json.dumps({
        "id": 999999,
        "name": "Test Appliances",
        "description": "test 12345",
        "created_at": "1979-01-16 07:07:50",
        "updated_at": "2024-01-05 23:53:25"
    })

    connection = http.client.HTTPConnection('localhost', 3000)
    connection.request(
        'PUT',
        f"{url}/item_types/999999",
        headers={
            "API_KEY": key,
            "Content-Type": "application/json"},
        body=jsonData)
    time.sleep(2)
    response = connection.getresponse()

    assert response.code == 200

    connection.request(
        'GET', f"{url}/item_types/999999", headers={"API_KEY": key})
    response = connection.getresponse()
    data = response.read()
    result = json.loads(data)

    connection.request(
        'DELETE', f"{url}/item_types/999999", headers={"API_KEY": key})

    assert result['description'] == "test 12345"



def test_delete_item_type(_data):
    url, key = _data
    connection = http.client.HTTPConnection('localhost', 3000)
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
    response = connection.getresponse()
    assert response.code == 201, "insertion failed"

    connection.request(
        'DELETE', f"{url}/item_types/999999", headers={"API_KEY": key})
    response = connection.getresponse()

    assert response.code == 200

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
    connection.request('GET', f"{url}/item_lines", headers={"API_KEY": key})
    response = connection.getresponse()
    data = response.read()
    result = json.loads(data)
    assert response.status == 200
    assert isinstance(result, list)


def test_get_item_line_by_id(_data):
    url, key = _data
    connection = http.client.HTTPConnection('localhost', 3000)

    jsonData = json.dumps({
        "id": 999999,
        "name": "Test Appliances",
        "description": "test 123",
        "created_at": "1979-01-16 07:07:50",
        "updated_at": "2024-01-05 23:53:25"
    })
    connection.request(
        "POST",
        f"{url}/item_lines",
        headers={
            "API_KEY": key,
            "Content-Type": "application/json"},
        body=jsonData)
    connection.getresponse()
    time.sleep(5)

    connection.request(
        'GET', f"{url}/item_lines/999999", headers={"API_KEY": key})
    response = connection.getresponse()
    data = response.read()
    result = json.loads(data)

    connection.request(
        'DELETE', f"{url}/item_lines/999999", headers={"API_KEY": key})

    assert response.status == 200
    assert result["id"] == "999999"
    assert result["name"] == "Test Appliances"
    assert result["description"] == "test 123"


def test_get_item_line_items(_data):
    url, key = _data
    connection = http.client.HTTPConnection('localhost', 3000)
    connection.request(
        'GET', f"{url}/item_lines/1/items", headers={"API_KEY": key})
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


def test_post_item_line(_data):
    url, key = _data
    connection = http.client.HTTPConnection('localhost', 3000)
    jsonData = json.dumps({
        "id": 999999,
        "name": "Test Appliances",
        "description": "test 123",
        "created_at": "1979-01-16 07:07:50",
        "updated_at": "2024-01-05 23:53:25"
    })
    connection.request(
        'POST',
        f"{url}/item_lines",
        headers={
            "API_KEY": key,
            "Content-Type": "application/json"},
        body=jsonData)
    time.sleep(1)
    response = connection.getresponse()

    connection.request(
        'DELETE', f"{url}/item_lines/999999", headers={"API_KEY": key})

    assert response.status == 201


def test_put_item_line(_data):
    url, key = _data
    connection = http.client.HTTPConnection('localhost', 3000)
    jsonData = json.dumps({
        "id": 999999,
        "name": "Test Appliances",
        "description": "test 123",
        "created_at": "1979-01-16 07:07:50",
        "updated_at": "2024-01-05 23:53:25"
    })
    connection.request(
        'POST',
        f"{url}/item_lines",
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
        f"{url}/item_lines/999999",
        headers={
            "API_KEY": key,
            "Content-Type": "application/json"},
        body=jsonData)
    time.sleep(2)
    response = connection.getresponse()

    assert response.code == 200

    connection.request(
        'GET', f"{url}/item_lines/999999", headers={"API_KEY": key})
    response = connection.getresponse()
    data = response.read()
    result = json.loads(data)

    connection.request(
        'DELETE', f"{url}/item_lines/999999", headers={"API_KEY": key})

    assert result['description'] == "test12345"


def test_delete_item_line(_data):
    url, key = _data
    connection = http.client.HTTPConnection('localhost', 3000)
    jsonData = json.dumps({
        "id": 999999,
        "name": "Test Appliances",
        "description": "test 123",
        "created_at": "1979-01-16 07:07:50",
        "updated_at": "2024-01-05 23:53:25"
    })
    connection.request(
        'POST',
        f"{url}/item_lines",
        headers={
            "API_KEY": key,
            "Content-Type": "application/json"},
        body=jsonData)
    response = connection.getresponse()
    assert response.code == 201, "insertion failed"

    connection.request(
        'DELETE', f"{url}/item_lines/999999", headers={"API_KEY": key})
    response = connection.getresponse()

    assert response.code == 200
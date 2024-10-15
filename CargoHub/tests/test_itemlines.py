import time
import pytest
import http.client
import json


@pytest.fixture
def _data():
    return http.client.HTTPConnection('localhost', 3000), "/api/v1", "a1b2c3d4e5"


def test_get_all_item_lines(_data):
    connection, url, key = _data

    test_data = {
        "id": 999999,
        "name": "Test Appliances",
        "description": "test 123",
        "created_at": "1979-01-16 07:07:50",
        "updated_at": "2024-01-05 23:53:25"
    }
    jsonData = json.dumps(test_data)
    connection.request(
        'POST',
        f"{url}/item_lines",
        headers={
            "API_KEY": key,
            "Content-Type": "application/json"},
        body=jsonData)
    post_response = connection.getresponse()
    assert post_response.code == 201, "insertion failed"

    connection.request('GET', f"{url}/item_lines", headers={"API_KEY": key})
    response = connection.getresponse()
    data = response.read()
    result = json.loads(data)
    resultIds = [w["id"] for w in result]

    connection.request('DELETE', f"{url}/item_lines/999999", headers={"API_KEY": key})
    delete_response = connection.getresponse()
    assert delete_response.status == 200

    assert response.status == 200
    assert isinstance(result, list)
    assert test_data["id"] in resultIds


def test_get_item_line_by_id(_data):
    connection, url, key = _data

    test_data = {
        "id": 999999,
        "name": "Test Appliances",
        "description": "test 123",
        "created_at": "1979-01-16 07:07:50",
        "updated_at": "2024-01-05 23:53:25"
    }
    jsonData = json.dumps(test_data)
    connection.request(
        'POST',
        f"{url}/item_lines",
        headers={
            "API_KEY": key,
            "Content-Type": "application/json"},
        body=jsonData)
    post_response = connection.getresponse()
    assert post_response.code == 201, "insertion failed"

    connection.request(
        'GET', f"{url}/item_lines/999999", headers={"API_KEY": key})
    response = connection.getresponse()
    data = response.read()
    result = json.loads(data)

    connection.request('DELETE', f"{url}/item_lines/999999", headers={"API_KEY": key})
    delete_response = connection.getresponse()
    assert delete_response.status == 200

    assert response.status == 200
    assert result["id"] == test_data["id"]
    assert result["name"] == test_data["name"]
    assert result["description"] == test_data["description"]


def test_get_item_line_items(_data):
    connection, url, key = _data
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
    connection, url, key = _data

    test_data = {
        "id": 999999,
        "name": "Test Appliances",
        "description": "test 123",
        "created_at": "1979-01-16 07:07:50",
        "updated_at": "2024-01-05 23:53:25"
    }
    jsonData = json.dumps(test_data)
    connection.request(
        'POST',
        f"{url}/item_lines",
        headers={
            "API_KEY": key,
            "Content-Type": "application/json"},
        body=jsonData)
    time.sleep(1)
    post_response = connection.getresponse()

    connection.request(
        'GET', f"{url}/item_lines/999999", headers={"API_KEY": key})
    get_response = connection.getresponse()
    get_data = get_response.read()
    get_result = json.loads(get_data)

    connection.request('GET', f"{url}/item_lines", headers={"API_KEY": key})
    get_all_response = connection.getresponse()
    get_all_data = get_all_response.read()
    get_all_result = json.loads(get_all_data)
    get_all_resultIds = [w["id"] for w in get_all_result]

    connection.request(
        'DELETE', f"{url}/item_lines/999999", headers={"API_KEY": key})

    assert post_response.status == 201
    assert test_data["id"] in get_all_resultIds
    assert get_result["id"] == test_data["id"]
    assert get_result["name"] == test_data["name"]
    assert get_result["description"] == test_data["description"]


def test_put_item_line(_data):
    connection, url, key = _data

    test_data = {
        "id": 999999,
        "name": "Test Appliances",
        "description": "test 123",
        "created_at": "1979-01-16 07:07:50",
        "updated_at": "2024-01-05 23:53:25"
    }
    jsonData = json.dumps(test_data)
    connection.request(
        'POST',
        f"{url}/item_lines",
        headers={
            "API_KEY": key,
            "Content-Type": "application/json"},
        body=jsonData)
    
    test_updated_data = {
        "id": 999999,
        "name": "Test Appliances",
        "description": "test 12345",
        "created_at": "1979-01-16 07:07:50",
        "updated_at": "2024-01-05 23:53:25"
    }
    jsonData = json.dumps(test_updated_data)

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

    assert result["id"] == test_updated_data["id"]
    assert result["name"] == test_updated_data["name"]
    assert result["description"] == test_updated_data["description"]


def test_delete_item_line(_data):
    connection, url, key = _data
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

    connection.request('DELETE', f"{url}/item_lines/999999", headers={"API_KEY": key})
    response = connection.getresponse()

    connection.request(
        'GET', f"{url}/item_lines/999999", headers={"API_KEY": key})
    get_response = connection.getresponse()
    get_data = get_response.read()
    get_result = json.loads(get_data)


    assert response.code == 200
    assert get_result == None


def test_get_item_line_invalid_id(_data):
    connection, url, key = _data
    connection.request('GET', f"{url}/item_lines/invalidIdentification", headers={"API_KEY": key})
    response = connection.getresponse()

    assert response.status == 400


def test_post_invalid_object(_data):
    connection, url, key = _data
    jsonData = json.dumps({
        "id": "99999999",
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

    assert response.status == 400

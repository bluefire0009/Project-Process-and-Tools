import time
import pytest
import http.client
import json


@pytest.fixture
def _data():
    return http.client.HTTPConnection('localhost', 3000), "/api/v1", "a1b2c3d4e5"


def test_get_all_item_types(_data):
    connection, url, key = _data
    
    test_data = {
        "id": 999999,
        "name": "Headphones",
        "description": "",
        "created_at": "1995-07-05 08:05:05",
        "updated_at": "2010-02-04 10:11:54"
    }
    jsonData = json.dumps(test_data)
    connection.request(
        'POST',
        f"{url}/item_types",
        headers={
            "API_KEY": key,
            "Content-Type": "application/json"},
        body=jsonData)
    post_response = connection.getresponse()
    assert post_response.code == 201, "insertion failed"
    
    connection.request('GET', f"{url}/item_types", headers={"API_KEY": key})
    response = connection.getresponse()
    data = response.read()
    result = json.loads(data)
    resultIds = [w["id"] for w in result]

    connection.request('DELETE', f"{url}/item_types/999999", headers={"API_KEY": key})
    delete_response = connection.getresponse()
    assert delete_response.status == 200

    assert response.status == 200
    assert isinstance(result, list)
    assert test_data["id"] in resultIds


def test_get_item_types_by_id(_data):
    connection, url, key = _data

    test_data = {
        "id": 999999,
        "name": "Headphones",
        "description": "",
        "created_at": "1995-07-05 08:05:05",
        "updated_at": "2010-02-04 10:11:54"
    }
    jsonData = json.dumps(test_data)
    connection.request(
        'POST',
        f"{url}/item_types",
        headers={
            "API_KEY": key,
            "Content-Type": "application/json"},
        body=jsonData)
    post_response = connection.getresponse()
    assert post_response.code == 201, "insertion failed"

    connection.request(
        'GET', f"{url}/item_types/5", headers={"API_KEY": key})
    response = connection.getresponse()
    data = response.read()
    result = json.loads(data)

    connection.request('DELETE', f"{url}/item_types/999999", headers={"API_KEY": key})
    delete_response = connection.getresponse()
    assert delete_response.status == 200

    assert response.status == 200
    assert result["id"] == test_data["id"]
    assert result["name"] == test_data["name"]
    assert result["description"] == test_data["description"]


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
    test_data = {
        "id": 999999,
        "name": "Desktop",
        "description": "test123",
        "created_at": "1993-07-28 13:43:32",
        "updated_at": "2022-05-12 08:54:35"
    }
    jsonData = json.dumps(test_data)
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
        'GET', f"{url}/item_types/999999", headers={"API_KEY": key})
    get_response = connection.getresponse()
    get_data = get_response.read()
    get_result = json.loads(get_data)

    connection.request('GET', f"{url}/item_types", headers={"API_KEY": key})
    get_all_response = connection.getresponse()
    get_all_data = get_all_response.read()
    get_all_result = json.loads(get_all_data)
    get_all_resultIds = [w["id"] for w in get_all_result]

    connection.request('DELETE', f"{url}/item_types/999999", headers={"API_KEY": key})
    delete_response = connection.getresponse()
    assert delete_response.status == 200

    assert response.status == 201
    assert test_data["id"] in get_all_resultIds
    assert get_result["id"] == test_data["id"]
    assert get_result["name"] == test_data["name"]
    assert get_result["description"] == test_data["description"]


def test_put_item_types(_data):
    connection, url, key = _data

    test_data = {
        "id": 999999,
        "name": "Headphones",
        "description": "",
        "created_at": "1995-07-05 08:05:05",
        "updated_at": "2010-02-04 10:11:54"
    }
    jsonData = json.dumps(test_data)
    connection.request(
        'POST',
        f"{url}/item_types",
        headers={
            "API_KEY": key,
            "Content-Type": "application/json"},
        body=jsonData)
    post_response = connection.getresponse()
    assert post_response.code == 201, "insertion failed"

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

    connection.request('DELETE', f"{url}/item_types/999999", headers={"API_KEY": key})
    delete_response = connection.getresponse()
    assert delete_response.status == 200

    assert result["id"] == test_updated_data["id"]
    assert result["name"] == test_updated_data["name"]
    assert result["description"] == test_updated_data["description"]


def test_delete_item_type(_data):
    connection, url, key = _data

    test_data = {
        "id": 999999,
        "name": "Headphones",
        "description": "",
        "created_at": "1995-07-05 08:05:05",
        "updated_at": "2010-02-04 10:11:54"
    }
    jsonData = json.dumps(test_data)
    connection.request(
        'POST',
        f"{url}/item_types",
        headers={
            "API_KEY": key,
            "Content-Type": "application/json"},
        body=jsonData)
    post_response = connection.getresponse()
    assert post_response.code == 201, "insertion failed"

    connection.request('DELETE', f"{url}/item_types/999999", headers={"API_KEY": key})
    delete_response = connection.getresponse()
    assert delete_response.status == 200

    assert delete_response.code == 200

    connection.request(
        'GET', f"{url}/item_types/999999", headers={"API_KEY": key})
    get_response = connection.getresponse()
    get_data = get_response.read()
    get_result = json.loads(get_data)


    assert get_response.code == 200
    assert get_result == None


def test_get_item_type_invalid_id(_data):
    connection, url, key = _data
    connection.request('GET', f"{url}/item_types/invalidIdentification", headers={"API_KEY": key})
    response = connection.getresponse()

    assert response.status == 400


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

    assert response.status == 400

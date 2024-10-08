import http.client
import json
import pytest


headers = {'API_KEY': 'a1b2c3d4e5', 'Content-Type': 'application/json'}

# not a test


def delete_test_location(connection: http.client.HTTPConnection):
    # delete location with "id": 99999
    connection.request("DELETE", "/api/v1/locations/99999", headers=headers)
    response = connection.getresponse()
    assert response.status == 200
    connection.close()


# not a test
def post_location(connection: http.client.HTTPConnection):
    body = {
        "id": 99999,
        "warehouse_id": 99999,
        "code": "test_code",
        "name": "test_name",
        "created_at": "",
        "updated_at": ""
    }
    json_body = json.dumps(body).encode('utf-8')

    # post location
    connection.request("POST", "/api/v1/locations/", headers=headers, body=json_body)
    # get response
    response = connection.getresponse()
    # assert that it has created
    assert response.status == 201
    # close connection
    response.close()

    return body


def test_get_all_locations():
    connection = http.client.HTTPConnection('localhost', 3000)
    connection.request("GET", "/api/v1/locations", headers=headers)

    response = connection.getresponse()
    assert response.status == 200
    data = json.loads(response.read())
    assert isinstance(data, list)
    connection.close()


def test_post_get_location():
    connection = http.client.HTTPConnection('localhost', 3000)
    body = post_location(connection)

    # get the body just posted
    connection.request("GET", f"/api/v1/locations/{body["id"]}", headers=headers)

    response = connection.getresponse()
    assert response.status == 200

    data = response.read()
    connection.close()

    location_dict = json.loads(data)
    assert len(location_dict) == 6
    assert location_dict["id"] == body["id"]
    assert location_dict["warehouse_id"] == body["warehouse_id"]
    assert location_dict["code"] == body["code"]
    assert location_dict["name"] == body["name"]

    delete_test_location(connection)


def test_put_location():
    connection = http.client.HTTPConnection('localhost', 3000)
    body = post_location(connection)

    # adjust locaton and PUT it
    body["code"] = "changed_code"
    json_body = json.dumps(body).encode('utf-8')
    connection.request("PUT", f"/api/v1/locations/{body["id"]}", headers=headers, body=json_body)
    connection.close()

    # GET adjusted location
    # get the body just posted
    connection.request("GET", f"/api/v1/locations/{body["id"]}", headers=headers)

    response = connection.getresponse()
    assert response.status == 200

    data = response.read()
    connection.close()

    location_dict = json.loads(data)
    assert len(location_dict) == 6
    assert location_dict["id"] == body["id"]
    assert location_dict["warehouse_id"] == body["warehouse_id"]
    assert location_dict["code"] == body["code"]
    assert location_dict["name"] == body["name"]

    delete_test_location(connection)

def test_delete_location():
    connection = http.client.HTTPConnection('localhost', 3000)
    # post location
    body = post_location(connection)
    # delte location
    delete_test_location(connection)



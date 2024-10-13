import http.client
import json
import pytest
from datetime import datetime
import time


@pytest.fixture()
def connection() -> http.client.HTTPConnection:
    return http.client.HTTPConnection('localhost', 3000)


@pytest.fixture()
def headers():
    return {'API_KEY': 'a1b2c3d4e5', 'Content-Type': 'application/json'}


def delete_test_location(connection: http.client.HTTPConnection, headers):
    # this test doesnt run standalone but is part of multiple tests
    # delete location with 'id': 99999
    connection.request('DELETE', '/api/v1/locations/99999', headers=headers)
    response = connection.getresponse()
    assert response.status == 200
    connection.close()


def get_posted_location(connection: http.client.HTTPConnection, headers, id: int):
    # this test doesnt run standalone but is part of multiple tests
    connection.request('GET', f"/api/v1/locations/{id}", headers=headers)

    response = connection.getresponse()
    assert response.status == 200

    data = response.read()
    connection.close()
    return json.loads(data)


def post_location(connection: http.client.HTTPConnection, headers):
    # this test doesnt run standalone but is part of multiple tests
    body = {
        'id': 99999,
        'warehouse_id': 99999,
        'code': 'test_code',
        'name': 'test_name',
        'created_at': '',
        'updated_at': ''
    }
    json_body = json.dumps(body).encode('utf-8')

    # post location
    connection.request('POST', '/api/v1/locations/', headers=headers, body=json_body)
    # get response
    response = connection.getresponse()
    # assert that it has created
    assert response.status == 201
    # close connection
    response.close()

    return body


def test_get_all_locations(connection: http.client.HTTPConnection, headers):
    connection.request('GET', '/api/v1/locations', headers=headers)

    response = connection.getresponse()
    assert response.status == 200
    data = json.loads(response.read())
    assert isinstance(data, list)
    connection.close()


def test_post_get_location(connection: http.client.HTTPConnection, headers):
    body = post_location(connection, headers)

    # get the body just posted
    connection.request('GET', f"/api/v1/locations/{body['id']}", headers=headers)

    response = connection.getresponse()
    assert response.status == 200

    data = response.read()
    connection.close()

    location_dict = json.loads(data)
    assert len(location_dict) == 6
    assert location_dict['id'] == body['id']
    assert location_dict['warehouse_id'] == body['warehouse_id']
    assert location_dict['code'] == body['code']
    assert location_dict['name'] == body['name']

    delete_test_location(connection, headers)


def test_put_location(connection: http.client.HTTPConnection, headers):
    body = post_location(connection, headers)

    # adjust locaton and PUT it
    body['code'] = 'changed_code'
    json_body = json.dumps(body).encode('utf-8')
    connection.request('PUT', f"/api/v1/locations/{body['id']}", headers=headers, body=json_body)
    connection.close()

    # GET adjusted location
    # get the body just posted
    connection.request('GET', f"/api/v1/locations/{body['id']}", headers=headers)

    response = connection.getresponse()
    assert response.status == 200

    data = response.read()
    connection.close()

    location_dict = json.loads(data)
    assert len(location_dict) == 6
    assert location_dict['id'] == body['id']
    assert location_dict['warehouse_id'] == body['warehouse_id']
    assert location_dict['code'] == body['code']
    assert location_dict['name'] == body['name']

    delete_test_location(connection, headers)


def test_delete_location(connection: http.client.HTTPConnection, headers):
    # post location
    body = post_location(connection, headers)
    # delte location
    delete_test_location(connection, headers)


def assert_time_string_format(connection, headers, date_string):
    # this test will fail: the datimestring being written is in the wrong format
    try:
        # Attempt to parse with the expected format
        datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
    except ValueError as e:
        # if it breaks clean up the file
        delete_test_location(connection, headers)
        raise AssertionError(f"Error: {str(e)}")


def test_created_at(connection: http.client.HTTPConnection, headers):
    # created at is empty in the body that gets posted
    body = post_location(connection, headers)
    location_dict = get_posted_location(connection, headers, body['id'])

    assert location_dict["created_at"] != ""

    # assert that the created at is in the right format
    assert_time_string_format(connection, headers, location_dict["created_at"])

    # turn string into datetime obj
    read_date_obj = datetime.strptime(location_dict["created_at"], "%Y-%m-%d %H:%M:%S")
    current_time_obj = datetime.now()

    assert read_date_obj.year == current_time_obj.year
    assert read_date_obj.month == current_time_obj.month
    assert read_date_obj.day == current_time_obj.day
    assert read_date_obj.hour == current_time_obj.hour
    assert read_date_obj.minute == current_time_obj.minute

    delete_test_location(connection, headers)


def test_updated_at(connection: http.client.HTTPConnection, headers):
    # created at is empty in the body that gets posted
    body = post_location(connection, headers)

    # wait one seconds so the created object will not be the same as the updated
    time.sleep(2)
    # update te location
    body['code'] = 'changed_code'
    json_body = json.dumps(body).encode('utf-8')
    connection.request('PUT', f"/api/v1/locations/{body['id']}", headers=headers, body=json_body)
    connection.close()

    # get the location ad check if updated_at is empty
    location_dict = get_posted_location(connection, headers, body['id'])
    assert location_dict["updated_at"] != ""

    # assert that the created at is in the right format
    assert_time_string_format(connection, headers, location_dict["updated_at"])

    # turn string into datetime obj
    read_date_obj = datetime.strptime(location_dict["updated_at"], "%Y-%m-%d %H:%M:%S")
    current_time_obj = datetime.now()

    assert read_date_obj.year == current_time_obj.year
    assert read_date_obj.month == current_time_obj.month
    assert read_date_obj.day == current_time_obj.day
    assert read_date_obj.hour == current_time_obj.hour
    assert read_date_obj.minute == current_time_obj.minute

    # make sure the created_at and updated_at are not the same
    assert location_dict["updated_at"] != location_dict["created_at"]

    delete_test_location(connection, headers)
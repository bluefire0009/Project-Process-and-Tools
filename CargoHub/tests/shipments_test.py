import http.client
import threading
import json
import pytest
import os

shipmentsPath = './data/shipments.json'
headers = {'API_KEY': 'a1b2c3d4e5', 'Content-Type': 'application/json'}

# def run_api():
#     relative_path = "start-system.bat"
#     os.system('cd ..')
#     os.system(relative_path)


@pytest.fixture(scope='function')
def setup_teardown():
    # Setup: Save the original content of the file
    with open(shipmentsPath, 'r') as shipmentsFile:
        original_content = shipmentsFile.read()

    # Clear the file for the test
    with open(shipmentsPath, 'w') as shipmentsFile:
        shipmentsFile.write("[]")

    # Provide this setup to the test and then ensure cleanup runs afterward
    yield

    # Teardown: Restore the file to its original content
    with open(shipmentsPath, 'w') as shipmentsFile:
        shipmentsFile.write(original_content)


def post_test_shipment(connection: http.client.HTTPConnection):
    body = {
        "id": 999999999,
        "order_id": 999999999,
        "source_id": 33,
        "order_date": "test_order_date",
        "request_date": "test_request_date",
        "shipment_date": "test_shipment_date",
        "shipment_type": "Test_I",
        "shipment_status": "",
        "notes": "test_notes",
        "carrier_code": "DPD",
        "carrier_description": "Dynamic Parcel Distribution",
        "service_code": "Fastest",
        "payment_type": "Manual",
        "transfer_mode": "Ground",
        "total_package_count": 31,
        "total_package_weight": 594.42,
        "created_at": "",
        "updated_at": "",
        "items": [
            {"item_id": "P007435", "amount": 23},
            {"item_id": "P009557", "amount": 1}
        ]
    }
    json_body = json.dumps(body).encode('utf-8')

    # post shipment
    connection.request('POST', '/api/v1/shipments', headers=headers, body=json_body)
    # get response
    post_response = connection.getresponse()
    # assert that it has created
    assert post_response.status == 201
    # close connection
    post_response.close()

    return body


def test_setup_teardown(setup_teardown):
    with open(shipmentsPath, 'r') as shipmentsFile:
        content = shipmentsFile.read()

    assert content == "[]"  # File should be empty because of setup


def test_post_get_shipment(setup_teardown):
    connection = http.client.HTTPConnection('localhost', 3000)
    post_test_shipment(connection)

    # Get shipment
    connection.request("GET", "/api/v1/shipments/999999999", headers=headers)

    response = connection.getresponse()
    data = response.read()
    connection.close()

    shipmentDict = json.loads(data)
    # check if response json has all 19 fields
    assert len(shipmentDict) == 19
    assert shipmentDict["notes"] == "test_notes"


def test_put_shipment(setup_teardown):
    connection = http.client.HTTPConnection('localhost', 3000)
    body = post_test_shipment(connection)

    # change the shipment json object before PUT request
    body["source_id"] = 9999
    json_body = json.dumps(body).encode('utf-8')
    connection.request('PUT', '/api/v1/shipments/999999999', headers=headers, body=json_body)

    post_response = connection.getresponse()
    assert post_response.status == 200
    post_response.close()

    # Get shipment
    connection.request("GET", "/api/v1/shipments/999999999", headers=headers)

    response = connection.getresponse()
    data = response.read()
    connection.close()

    shipmentDict = json.loads(data)
    # check if response json has all 19 fields
    assert len(shipmentDict) == 19
    assert shipmentDict["source_id"] == 9999


def test_delete_shipment(setup_teardown):
    connection = http.client.HTTPConnection('localhost', 3000)
    body = post_test_shipment(connection)

    # delete shipment with "id": 999999999
    connection.request("DELETE", "/api/v1/shipments/999999999", headers=headers)
    response = connection.getresponse()
    assert response.status == 200
    connection.close()

    # have to delete shipments twice. For some reason the api (sometimes????) posts the shipment twice
    connection.request("DELETE", "/api/v1/shipments/999999999", headers=headers)
    response = connection.getresponse()
    assert response.status == 200
    connection.close()

    # Get shipment
    connection.request("GET", "/api/v1/shipments/999999999", headers=headers)

    response = connection.getresponse()
    assert response.status == 200
    data = response.read()
    connection.close()

    assert data == b'null'

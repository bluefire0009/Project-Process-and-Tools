import http.client
import threading
import json
import pytest
import os

shipmentsPath = './data/warehouses.json'
headers = {'API_KEY': 'a1b2c3d4e5', 'Content-Type': 'application/json'}

# def run_api():
#     relative_path = "start-system.bat"
#     os.system('cd ..')
#     os.system(relative_path)


@pytest.fixture
def setup_teardown():
    # Setup: Save the original content of the file
    with open(shipmentsPath, 'r') as shipmentsFile:
        original_content = shipmentsFile.read()

    # Clear the file for the test
    with open(shipmentsPath, 'w') as shipmentsFile:
        shipmentsFile.write("")

    # Provide this setup to the test and then ensure cleanup runs afterward
    yield

    # Teardown: Restore the file to its original content
    with open(shipmentsPath, 'w') as shipmentsFile:
        shipmentsFile.write(original_content)


def test_setup_teardown(setup_teardown):
    with open(shipmentsPath, 'r') as shipmentsFile:
        content = shipmentsFile.read()

    assert content == ""  # File should be empty because of setup


def test_post_get_shipment(setup_teardown):
    body = {
        "id": 1,
        "order_id": 1,
        "source_id": 33,
        "order_date": "2000-03-09",
        "request_date": "2000-03-11",
        "shipment_date": "2000-03-13",
        "shipment_type": "I",
        "shipment_status": "",
        "notes": "Zee vertrouwen klas rots heet lachen oneven begrijpen.",
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

    # make connection
    connection = http.client.HTTPConnection('localhost', 3000)

    # post shipment
    connection.request('POST', '/api/v1/shipments', headers=headers, body=json_body)
    # get response
    post_response = connection.getresponse()
    # assert that it has created
    assert post_response.status == 201
    # close connection
    post_response.close()

    # Get shipment
    connection.request("GET", "/api/v1/shipments/1", headers={'API_KEY': 'a1b2c3d4e5'})

    response = connection.getresponse()
    data = response.read()
    connection.close()

    shipmentDict = json.loads(data)
    assert shipmentDict["notes"] == body["notes"]

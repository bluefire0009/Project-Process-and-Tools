import http.client
import json
import pytest


headers = {'API_KEY': 'a1b2c3d4e5', 'Content-Type': 'application/json'}

# not a test


def delete_test_order(connection: http.client.HTTPConnection):
    # delete location with "id": 99999
    connection.request("DELETE", "/api/v1/orders/99999", headers=headers)
    response = connection.getresponse()
    assert response.status == 200
    connection.close()


# not a test
def post_order(connection: http.client.HTTPConnection):
    body = {
        "id": 99999,
        "source_id": 33,
        "order_date": "2019-04-03T11:33:15Z",
        "request_date": "2019-04-07T11:33:15Z",
        "reference": "ORD00001",
        "reference_extra": "Bedreven arm straffen bureau.",
        "order_status": "Delivered",
        "notes": "test_notes",
        "shipping_notes": "AAAAAAAAAAAAAAa",
        "picking_notes": "Ademen fijn volgorde scherp aardappel op leren.",
        "warehouse_id": 18,
        "ship_to": None,
        "bill_to": None,
        "shipment_id": 1,
        "total_amount": 9905.13,
        "total_discount": 150.77,
        "total_tax": 372.72,
        "total_surcharge": 77.6,
        "created_at": "2019-04-03T11:33:15Z",
        "updated_at": "2019-04-05T07:33:15Z",
        "items": [
            {
                "item_id": "P007435",
                "amount": 23
            },
            {
                "item_id": "P009557",
                "amount": 1
            }
        ]
    }
    json_body = json.dumps(body).encode('utf-8')

    # post location
    connection.request("POST", "/api/v1/orders/", headers=headers, body=json_body)
    # get response
    response = connection.getresponse()
    # assert that it has created
    assert response.status == 201
    # close connection
    response.close()

    return body


def test_get_all_locations():
    connection = http.client.HTTPConnection('localhost', 3000)
    connection.request("GET", "/api/v1/orders", headers=headers)

    response = connection.getresponse()
    assert response.status == 200
    data = json.loads(response.read())
    assert isinstance(data, list)
    connection.close()


def test_post_get_orders():
    connection = http.client.HTTPConnection('localhost', 3000)
    body = post_order(connection)

    # get the body just posted
    connection.request("GET", f"/api/v1/orders/{body["id"]}", headers=headers)

    response = connection.getresponse()
    assert response.status == 200

    data = response.read()
    connection.close()

    order_dict = json.loads(data)
    assert len(order_dict) == 6
    assert order_dict["notes"] == body["notes"]
    assert order_dict["shipping_notes"] == body["shipping_notes"]


    delete_test_order(connection)

import http.client
import json
import pytest


headers = {'API_KEY': 'a1b2c3d4e5', 'Content-Type': 'application/json'}

# not a test


def delete_test_order(connection: http.client.HTTPConnection):
    # delete location with "id": 99999
    connection.request("DELETE", "/api/v1/locations/99999", headers=headers)
    response = connection.getresponse()
    assert response.status == 200
    connection.close()


# not a test
def post_order(connection: http.client.HTTPConnection):
    body = {
        "id": 1,
        "source_id": 33,
        "order_date": "2019-04-03T11:33:15Z",
        "request_date": "2019-04-07T11:33:15Z",
        "reference": "ORD00001",
        "reference_extra": "Bedreven arm straffen bureau.",
        "order_status": "Delivered",
        "notes": "Voedsel vijf vork heel.",
        "shipping_notes": "Buurman betalen plaats bewolkt.",
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
            },
            {
                "item_id": "P009553",
                "amount": 50
            },
            {
                "item_id": "P010015",
                "amount": 16
            },
            {
                "item_id": "P002084",
                "amount": 33
            },
            {
                "item_id": "P009663",
                "amount": 18
            },
            {
                "item_id": "P010125",
                "amount": 18
            },
            {
                "item_id": "P005768",
                "amount": 26
            },
            {
                "item_id": "P004051",
                "amount": 1
            },
            {
                "item_id": "P005026",
                "amount": 29
            },
            {
                "item_id": "P000726",
                "amount": 22
            },
            {
                "item_id": "P008107",
                "amount": 47
            },
            {
                "item_id": "P001598",
                "amount": 32
            },
            {
                "item_id": "P002855",
                "amount": 20
            },
            {
                "item_id": "P010404",
                "amount": 30
            },
            {
                "item_id": "P010446",
                "amount": 6
            },
            {
                "item_id": "P001517",
                "amount": 9
            },
            {
                "item_id": "P009265",
                "amount": 2
            },
            {
                "item_id": "P001108",
                "amount": 20
            },
            {
                "item_id": "P009110",
                "amount": 18
            },
            {
                "item_id": "P009686",
                "amount": 13
            }
        ]
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

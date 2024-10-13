import http.client
import json
import pytest


@pytest.fixture()
def connection() -> http.client.HTTPConnection:
    return http.client.HTTPConnection('localhost', 3000)


@pytest.fixture()
def headers():
    return {'API_KEY': 'a1b2c3d4e5', 'Content-Type': 'application/json'}



def delete_test_order(connection: http.client.HTTPConnection, headers):
    # delete location with 'id': 99999
    connection.request('DELETE', '/api/v1/orders/99999', headers=headers)
    response = connection.getresponse()
    assert response.status == 200
    connection.close()


def post_order(connection: http.client.HTTPConnection, headers):
    body = {
        'id': 99999,
        'source_id': 33,
        'order_date': '2019-04-03T11:33:15Z',
        'request_date': '2019-04-07T11:33:15Z',
        'reference': 'ORD00001',
        'reference_extra': 'Bedreven arm straffen bureau.',
        'order_status': 'Delivered',
        'notes': 'test_notes',
        'shipping_notes': 'AAAAAAAAAAAAAAa',
        'picking_notes': 'Ademen fijn volgorde scherp aardappel op leren.',
        'warehouse_id': 18,
        'ship_to': None,
        'bill_to': None,
        'shipment_id': 1,
        'total_amount': 9905.13,
        'total_discount': 150.77,
        'total_tax': 372.72,
        'total_surcharge': 77.6,
        'created_at': '2019-04-03T11:33:15Z',
        'updated_at': '2019-04-05T07:33:15Z',
        'items': [
            {
                'item_id': 'P007435',
                'amount': 23
            },
            {
                'item_id': 'P009557',
                'amount': 1
            }
        ]
    }
    json_body = json.dumps(body).encode('utf-8')

    # post location
    connection.request('POST', '/api/v1/orders/', headers=headers, body=json_body)
    # get response
    response = connection.getresponse()
    # assert that it has created
    assert response.status == 201
    # close connection
    response.close()

    return body


def test_get_all_orders(connection: http.client.HTTPConnection, headers):
    connection.request('GET', '/api/v1/orders', headers=headers)

    response = connection.getresponse()
    assert response.status == 200
    data = json.loads(response.read())
    assert isinstance(data, list)
    connection.close()


def test_post_get_orders(connection: http.client.HTTPConnection, headers):
    body = post_order(connection, headers)

    # get the body just posted
    connection.request('GET', f"/api/v1/orders/{body['id']}", headers=headers)

    response = connection.getresponse()
    assert response.status == 200

    data = response.read()
    connection.close()

    order_dict = json.loads(data)
    assert len(order_dict) == len(body)
    assert order_dict['notes'] == body['notes']
    assert order_dict['shipping_notes'] == body['shipping_notes']

    delete_test_order(connection, headers)


def test_put_order(connection: http.client.HTTPConnection, headers):
    body = post_order(connection, headers)

    # adjust order and PUT it
    body['notes'] = 'changed_notes'
    json_body = json.dumps(body).encode('utf-8')
    connection.request('PUT', f"/api/v1/orders/{body['id']}", headers=headers, body=json_body)
    connection.close()

    # GET adjusted order
    connection.request('GET', f"/api/v1/orders/{body['id']}", headers=headers)

    response = connection.getresponse()
    assert response.status == 200

    data = response.read()
    connection.close()

    location_dict = json.loads(data)
    assert len(location_dict) == len(body)
    # loop trough response and original to check if they are the same
    for response_item, original in zip(location_dict, body):
        # skip time created and updated since this is variable
        if body["created_at"] == original or body["updated_at"] == original:
            continue
        assert response_item == original

    delete_test_order(connection, headers)


def test_get_order_items(connection: http.client.HTTPConnection, headers):
    body = post_order(connection, headers)

    connection.request('GET', f"/api/v1/orders/{body['id']}/items", headers=headers)
    response = connection.getresponse()
    assert response.status == 200

    data = response.read()
    connection.close()
    order_dict = json.loads(data)

    # assert if items are the same
    for original_item, response_item in zip(body['items'], order_dict):
        assert original_item == response_item

    delete_test_order(connection, headers)


def test_delete_location(connection: http.client.HTTPConnection, headers):
    # post location
    post_order(connection, headers)
    # delte location
    delete_test_order(connection, headers)

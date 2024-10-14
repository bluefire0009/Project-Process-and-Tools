import http.client
import json
import pytest

@pytest.fixture
def _DataPytestFixture():
    _connection = http.client.HTTPConnection('localhost', 3000)
    _url = "/api/v1/transfers"
    _testTransfers = [{"id": 100000001, "reference": "TR00001", "transfer_from": 9284, "transfer_to": 9229, "transfer_status": "Scheduled", "created_at": "2000-03-11T13:11:14Z", "updated_at": "2000-03-12T16:11:14Z", "items": [{"item_id": "P007435", "amount": 23}]}, 
                      {"id": 100000002, "reference": "TR00002", "transfer_from": 9229, "transfer_to": 9284, "transfer_status": "Scheduled", "created_at": "2017-09-19T00:33:14Z", "updated_at": "2017-09-20T01:33:14Z", "items": [{"item_id": "P007435", "amount": 23}]}]
    _headers = {
        'API_KEY': 'a1b2c3d4e5', 
        'Content-Type': 'application/json'}   
    return _connection, _url, _testTransfers, _headers

def test_post_transfer(_DataPytestFixture):
    # Arrange
    _connection, _url, _testTransfers, _headers = _DataPytestFixture

    # Act
    # Add the two test transfers to the database
    postStatuss = []
    for transfer in _testTransfers:
        json_data = json.dumps(transfer).encode('utf-8')
        _connection.request('POST',_url, body=json_data, headers=_headers)
        response = _connection.getresponse()
        postStatuss.append(response.status)
        response.close()

    # Send a GET request to the GET_ALL endpoint
    _connection.request('GET', _url, headers=_headers)
    response = _connection.getresponse()
    data = response.read()
    transfers = json.loads(data)
    # list comprehension to get a list of all transfer id's
    transferIds = [s["id"] for s in transfers]
    
    # Assert
    assert len(transfers) >= 2
    for transfer in _testTransfers:
        assert transfer["id"] in transferIds
    
    for status in postStatuss:
        assert status == 201

    # Clean up
    for transfer in _testTransfers:
        json_data = json.dumps(transfer).encode('utf-8')
        _connection.request('DELETE',f'{_url}/{transfer["id"]}', headers=_headers)
        _connection.getresponse().close()

def test_get_all(_DataPytestFixture):
    # Arrange
    _connection, _url, _testTransfers, _headers = _DataPytestFixture
    # Add the two test transfers to the database
    for transfer in _testTransfers:
        json_data = json.dumps(transfer).encode('utf-8')
        _connection.request('POST',_url, body=json_data, headers=_headers)
        _connection.getresponse().close()

    # Act
    # Send a GET request to the GET_ALL endpoint
    _connection.request('GET', _url, headers=_headers)
    response = _connection.getresponse()
    data = response.read()
    transfers = json.loads(data)
    # list comprehension to get a list of all transfer id's
    transferIds = [s["id"] for s in transfers]
    
    # Assert
    assert str(response.status) == '200'
    assert len(transfers) >= 2
    for transfer in _testTransfers:
        assert transfer["id"] in transferIds

    # Clean up
    for transfer in _testTransfers:
        json_data = json.dumps(transfer).encode('utf-8')
        _connection.request('DELETE',f'{_url}/{transfer["id"]}', headers=_headers)
        _connection.getresponse().close()

        
def test_get_one(_DataPytestFixture):
    # Arrange
    _connection, _url, _testTransfers, _headers = _DataPytestFixture
    # Add the two test transfers to the database
    for transfer in _testTransfers:
        json_data = json.dumps(transfer).encode('utf-8')
        _connection.request('POST',_url, body=json_data, headers=_headers)
        _connection.getresponse().close()    

    # Act   
    # Send a GET request to the GET_SPECIFIC_TRANSFER endpoint
    _connection.request('GET', f'{_url}/{_testTransfers[0]["id"]}', headers=_headers)
    response = _connection.getresponse()
    data = response.read()
    transferAfter = json.loads(data)

    # Assert
    assert str(response.status) == '200'
    assert type(transferAfter) == dict
    assert transferAfter["id"] == _testTransfers[0]["id"]
    assert transferAfter["reference"] == _testTransfers[0]["reference"]
    assert transferAfter["transfer_from"] == _testTransfers[0]["transfer_from"]
    assert transferAfter["transfer_to"] == _testTransfers[0]["transfer_to"]
    assert transferAfter["transfer_status"] == _testTransfers[0]["transfer_status"]
    assert transferAfter["items"] == _testTransfers[0]["items"]
    
    # Clean up
    for transfer in _testTransfers:
        json_data = json.dumps(transfer).encode('utf-8')
        _connection.request('DELETE',f'{_url}/{transfer["id"]}', headers=_headers)
        _connection.getresponse().close()

def test_get_one_items(_DataPytestFixture):
    # Arrange
    _connection, _url, _testTransfers, _headers = _DataPytestFixture
    # Add the two test transfers to the database
    for transfer in _testTransfers:
        json_data = json.dumps(transfer).encode('utf-8')
        _connection.request('POST', f'{_url}/', body=json_data, headers=_headers)
        _connection.getresponse().close()

    # Act
    # Send a GET request to the GET_SPECIFIC_TRANSFER endpoint
    _connection.request('GET', f'{_url}/{_testTransfers[0]["id"]}/items', headers=_headers)
    response = _connection.getresponse()
    data = response.read()
    itemsAfter = json.loads(data)

    # Assert
    assert _testTransfers[0]['items'] == itemsAfter
        
    # Clean up
    for transfer in _testTransfers:
        json_data = json.dumps(transfer).encode('utf-8')
        _connection.request('DELETE',f'{_url}/{transfer["id"]}', headers=_headers)
        _connection.getresponse().close()

def test_put_transfer(_DataPytestFixture):
    # Arrange
    _connection, _url, _testTransfers, _headers = _DataPytestFixture
    extraTransfer = {"id": 100000003, "reference": "TR00001", "transfer_from": None, "transfer_to": 9229, "transfer_status": "Scheduled", "created_at": "2000-03-11T13:11:14Z", "updated_at": "2000-03-12T16:11:14Z", "items": [{"item_id": "P007666", "amount": 69}]}
    # Add the two test transfers to the database
    for transfer in _testTransfers:
        json_data = json.dumps(transfer).encode('utf-8')
        _connection.request('POST', f'{_url}', body=json_data, headers=_headers)
        _connection.getresponse().close()

    # Act
    # Update the first test transfer with the extraTransfer
    json_data = json.dumps(extraTransfer).encode('utf-8')
    _connection.request('PUT',f'{_url}/{_testTransfers[0]["id"]}', body=json_data, headers=_headers)
    response = _connection.getresponse()
    putStatusCode = response.status
    response.close()

    # Send a GET request to the GET_SPECIFIC_TRANSFER endpoint
    _connection.request('GET', f'{_url}/{extraTransfer["id"]}', headers=_headers)
    response = _connection.getresponse()
    data = response.read()
    transferAfter = json.loads(data)
    
    # Assert
    assert str(putStatusCode) == '200'
    assert type(transferAfter) == dict
    assert transferAfter["id"] == extraTransfer["id"]
    assert transferAfter["reference"] == extraTransfer["reference"]
    assert transferAfter["transfer_from"] == extraTransfer["transfer_from"]
    assert transferAfter["transfer_to"] == extraTransfer["transfer_to"]
    assert transferAfter["transfer_status"] == extraTransfer["transfer_status"]
    assert transferAfter["items"] == extraTransfer["items"]

    # Clean up
    _connection.request('DELETE',f'{_url}/{extraTransfer["id"]}', headers=_headers)
    _connection.getresponse().close()
    for transfer in _testTransfers:
        json_data = json.dumps(transfer).encode('utf-8')
        _connection.request('DELETE',f'{_url}/{transfer["id"]}', headers=_headers)
        _connection.getresponse().close()

# DOESN'T WORK BECAUSE THERE IS NO FIELD "location_id"
def test_put_transfer_commit(_DataPytestFixture):
    # Arrange
    _connection, _url, _testTransfers, _headers = _DataPytestFixture
    # Add the two test transfers to the database
    for transfer in _testTransfers:
        json_data = json.dumps(transfer).encode('utf-8')
        _connection.request('POST',_url, body=json_data, headers=_headers)
        _connection.getresponse().close()

    # Add the test location to the database
    testLocation = {'id': 99999,'warehouse_id': 99999,'code': 'test_code','name': 'test_name','created_at': '','updated_at': ''}
    json_body = json.dumps(testLocation).encode('utf-8')
    _connection.request('POST', '/api/v1/locations/', headers=_headers, body=json_body)
    _connection.getresponse().close()

    # Act
    # Update the first test transfer to "Processed"
    _connection.request('PUT',f'{_url}/{_testTransfers[0]["id"]}/commit', headers=_headers)
    update_status = _connection.getresponse()

    # Assert

    # Clean up
    _connection.request('DELETE',f'/api/v1/locations/{testLocation["id"]}', headers=_headers)
    _connection.getresponse().close()
    for transfer in _testTransfers:
        json_data = json.dumps(transfer).encode('utf-8')
        _connection.request('DELETE',f'{_url}/{transfer["id"]}', headers=_headers)
        _connection.getresponse().close()

def test_delete_transfer(_DataPytestFixture):
    # Arrange  
    _connection, _url, _testTransfers, _headers = _DataPytestFixture
    # Add the two test transfers to the database
    for transfer in _testTransfers:
        json_data = json.dumps(transfer).encode('utf-8')
        _connection.request('POST', f'{_url}', body=json_data, headers=_headers)
        _connection.getresponse().close()

    # Act  
    # Delete the first transfer
    _connection.request('DELETE',f'{_url}/{_testTransfers[0]["id"]}', headers=_headers)
    response = _connection.getresponse()
    deleteStatusCode = response.status
    response.close()

    # Try getting the deleted transfer
    _connection.request('GET', f'{_url}/{_testTransfers[0]["id"]}', headers=_headers)
    response = _connection.getresponse()
    transferAfter = response.read()
    
    # Assert
    # "b'null'" Means that no transfer was found
    assert str(transferAfter) == "b'null'"
    assert deleteStatusCode == 200

    # Clean up
    for transfer in _testTransfers:
        json_data = json.dumps(transfer).encode('utf-8')
        _connection.request('DELETE',f'{_url}/{transfer["id"]}', headers=_headers)
        _connection.getresponse().close()

def test_add_transfer_wrong_format(_DataPytestFixture):
    # Arrange  
    _connection, _url, _testTransfers, _headers = _DataPytestFixture
    
    extraWrongTransfer = {"id": 100000003, "refference": "TR00001", "tlansfer_from": None, "tlansfer_to": 9229, "tlansfer_status": "Scheduled", "created_at": "2000-03-11T13:11:14Z", "updated_at": "2000-03-12T16:11:14Z", "idems": [{"idem_id": "P007666", "amound": 69}]}    
    
    # Act
    # Try adding the transfer with the wrong format
    json_data = json.dumps(extraWrongTransfer).encode('utf-8')
    _connection.request('POST',_url, body=json_data, headers=_headers)
    response = _connection.getresponse()
    postStatus = response.status
    response.close()

    # Send a GET request to the GET_ALL endpoint
    _connection.request('GET', _url, headers=_headers)
    response = _connection.getresponse()
    data = response.read()
    transfers = json.loads(data)
    # list comprehension to get a list of all transfer id's
    transfersIds = [t["id"] for t in transfers]

    # Clean up
    _connection.request('DELETE',f'{_url}/{extraWrongTransfer["id"]}', headers=_headers)
    _connection.getresponse().close()

    # Assert
    assert postStatus == 400
    assert extraWrongTransfer["id"] not in transfersIds

def test_put_transfer_wrong_format(_DataPytestFixture):
    # Arrange
    _connection, _url, _testTransfers, _headers = _DataPytestFixture
    extraWrongTransfer = {"id": 100000003, "refference": "TR00001", "tlansfer_from": None, "tlansfer_to": 9229, "tlansfer_status": "Scheduled", "created_at": "2000-03-11T13:11:14Z", "updated_at": "2000-03-12T16:11:14Z", "idems": [{"idem_id": "P007666", "amound": 69}]}
    # Add the two test transfer to the database
    for transfer in _testTransfers:
        json_data = json.dumps(transfer).encode('utf-8')
        _connection.request('POST', f'{_url}', body=json_data, headers=_headers)
        _connection.getresponse().close()

    # Act
    # Update the first test transfer with the extraWrongTransfer
    json_data = json.dumps(extraWrongTransfer).encode('utf-8')
    _connection.request('PUT',f'{_url}/{_testTransfers[0]["id"]}', body=json_data, headers=_headers)
    response = _connection.getresponse()
    putStatusCode = response.status
    response.close()

    # Send a GET request to the GET_ALL endpoint
    _connection.request('GET', _url, headers=_headers)
    response = _connection.getresponse()
    data = response.read()
    transfers = json.loads(data)
    # list comprehension to get a list of all transfer id's
    transfersIds = [w["id"] for w in transfers]
    
    # Clean up
    _connection.request('DELETE',f'{_url}/{extraWrongTransfer["id"]}', headers=_headers)
    _connection.getresponse().close()
    for transfer in _testTransfers:
        json_data = json.dumps(transfer).encode('utf-8')
        _connection.request('DELETE',f'{_url}/{transfer["id"]}', headers=_headers)
        _connection.getresponse().close()

    # Assert
    assert putStatusCode == 400
    assert extraWrongTransfer["id"] not in transfersIds
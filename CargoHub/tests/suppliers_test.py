import http.client
import json
import pytest

@pytest.fixture
def _DataPytestFixture():
    _connection = http.client.HTTPConnection('localhost', 3000)
    _url = "/api/v1/suppliers"
    _testSuppliers = [{"id": 1000001,"code": "SUP0001","name": "Lee, Parks and Johnson","address": "5989 Sullivan Drives","address_extra": "Apt. 996","city": "Port Anitaburgh","zip_code": "91688","province": "Illinois","country": "Czech Republic","contact_name": "Toni Barnett","phonenumber": "363.541.7282x36825","reference": "LPaJ-SUP0001","created_at": "1971-10-20 18:06:17","updated_at": "1985-06-08 00:13:46"},
        {"id": 1000002,"code": "SUP0002","name": "Holden-Quinn","address": "576 Christopher Roads","address_extra": "Suite 072","city": "Amberbury","zip_code": "16105","province": "Illinois","country": "Saint Martin","contact_name": "Kathleen Vincent","phonenumber": "001-733-291-8848x3542","reference": "H-SUP0002","created_at": "1995-12-18 03:05:46","updated_at": "2019-11-10 22:11:12"}]
    _headers = {
        'API_KEY': 'a1b2c3d4e5', 
        'Content-Type': 'application/json'}   
    return _connection, _url, _testSuppliers, _headers

def test_post_supplier(_DataPytestFixture):
    # Arrange
    _connection, _url, _testSuppliers, _headers = _DataPytestFixture

    # Act
    # Add the two test suppliers to the database
    postStatuss = []
    for supplier in _testSuppliers:
        json_data = json.dumps(supplier).encode('utf-8')
        _connection.request('POST',_url, body=json_data, headers=_headers)
        response = _connection.getresponse()
        postStatuss.append(response.status)
        response.close()

    # Send a GET request to the GET_ALL endpoint
    _connection.request('GET', _url, headers=_headers)
    response = _connection.getresponse()
    data = response.read()
    suppliers = json.loads(data)
    
    # list comprehension to get a list of all supplier id's
    supplierIds = [s["id"] for s in suppliers]
    
    # Clean up
    for supplier in _testSuppliers:
        json_data = json.dumps(supplier).encode('utf-8')
        _connection.request('DELETE',f'{_url}/{supplier["id"]}', headers=_headers)
        _connection.getresponse().close()

    # Assert
    assert len(suppliers) >= 2
    for supplier in _testSuppliers:
        assert supplier["id"] in supplierIds

    for status in postStatuss:
        assert status == 201

def test_get_all(_DataPytestFixture):
    # Arrange
    _connection, _url, _testSuppliers, _headers = _DataPytestFixture
    # Add the two test suppliers to the database
    for supplier in _testSuppliers:
        json_data = json.dumps(supplier).encode('utf-8')
        _connection.request('POST',_url, body=json_data, headers=_headers)
        _connection.getresponse().close()

    # Act
    # Send a GET request to the GET_ALL endpoint
    _connection.request('GET', _url, headers=_headers)

    # Get the response
    response = _connection.getresponse()
    data = response.read()
    suppliers = json.loads(data)
    # list comprehension to get a list of all supplier id's
    supplierIds = [s["id"] for s in suppliers]
    
    # Clean up
    for supplier in _testSuppliers:
        json_data = json.dumps(supplier).encode('utf-8')
        _connection.request('DELETE',f'{_url}/{supplier["id"]}', headers=_headers)
        _connection.getresponse().close()

    # Assert
    assert str(response.status) == '200'
    assert len(suppliers) >= 2
    for supplier in _testSuppliers:
        assert supplier["id"] in supplierIds

        
def test_get_one(_DataPytestFixture):
    # Arrange
    _connection, _url, _testSuppliers, _headers = _DataPytestFixture
    # Add the two test suppliers to the database
    for supplier in _testSuppliers:
        json_data = json.dumps(supplier).encode('utf-8')
        _connection.request('POST',_url, body=json_data, headers=_headers)
        _connection.getresponse().close()

    # Act   
    # Send a GET request to the GET_SPECIFIC_SUPPLIER endpoint
    _connection.request('GET', f'{_url}/{_testSuppliers[0]["id"]}', headers=_headers)

    # Get the response
    response = _connection.getresponse()
    data = response.read()
    supplierAfter = json.loads(data)

    # Clean up
    for supplier in _testSuppliers:
        json_data = json.dumps(supplier).encode('utf-8')
        _connection.request('DELETE',f'{_url}/{supplier["id"]}', headers=_headers)
        _connection.getresponse().close()

    # Assert
    assert str(response.status) == '200'
    assert type(supplierAfter) == dict
    assert supplierAfter["id"] == _testSuppliers[0]["id"]
    assert supplierAfter["code"] == _testSuppliers[0]["code"]
    assert supplierAfter["name"] == _testSuppliers[0]["name"]
    assert supplierAfter["address"] == _testSuppliers[0]["address"]
    assert supplierAfter["address_extra"] == _testSuppliers[0]["address_extra"]
    assert supplierAfter["city"] == _testSuppliers[0]["city"]
    assert supplierAfter["zip_code"] == _testSuppliers[0]["zip_code"]
    assert supplierAfter["province"] == _testSuppliers[0]["province"]
    assert supplierAfter["country"] == _testSuppliers[0]["country"]
    assert supplierAfter["contact_name"] == _testSuppliers[0]["contact_name"]
    assert supplierAfter["phonenumber"] == _testSuppliers[0]["phonenumber"]
    assert supplierAfter["reference"] == _testSuppliers[0]["reference"]

def test_get_one_items(_DataPytestFixture):
    # Arrange
    _connection, _url, _testSuppliers, _headers = _DataPytestFixture
    # Add the two test suppliers to the database
    for supplier in _testSuppliers:
        json_data = json.dumps(supplier).encode('utf-8')
        _connection.request('POST', f'{_url}/', body=json_data, headers=_headers)
        _connection.getresponse().close()

    # Add the test item with the first test supplier information
    test_item = {"uid": "P999999","code": "mYt79640E","description": "Down-sized system-worthy productivity","short_description": "pass","upc_code": "2541112620796","model_number": "ZK-417773-PXy","commodity_code": "z-761-L5A","item_line": 81,"item_group": 83,"item_type": 74,"unit_purchase_quantity": 3,"unit_order_quantity": 18,"pack_order_quantity": 13,"supplier_id": _testSuppliers[0]['id'],"supplier_code": _testSuppliers[0]['code'],"supplier_part_number": "ZB-103509-MLv","created_at": "2024-10-06 02:30:31","updated_at": "2024-10-06 02:30:31"}
    json_data = json.dumps(test_item).encode('utf-8')
    _connection.request('POST',  '/api/v1/items', body=json_data, headers=_headers)
    _connection.getresponse().close()

    # Act
    # Send a GET request to the GET_SPECIFIC_SUPPLIER endpoint
    _connection.request('GET', f'{_url}/{_testSuppliers[0]["id"]}/items', headers=_headers)

    # Get the response
    response = _connection.getresponse()
    data = response.read()
    itemAfter = json.loads(data)

    # Clean up
    _connection.request('DELETE', f'/api/v1/items/{test_item["uid"]}', headers=_headers)
    _connection.getresponse().close()
    for supplier in _testSuppliers:
        json_data = json.dumps(supplier).encode('utf-8')
        _connection.request('DELETE',f'{_url}/{supplier["id"]}', headers=_headers)
        _connection.getresponse().close()

    # Assert
    assert test_item['uid'] == itemAfter[0]['uid']
    assert test_item['code'] == itemAfter[0]['code']
    assert test_item['description'] == itemAfter[0]['description']
    assert test_item['short_description'] == itemAfter[0]['short_description']
    assert test_item['upc_code'] == itemAfter[0]['upc_code']
    assert test_item['model_number'] == itemAfter[0]['model_number']
    assert test_item['commodity_code'] == itemAfter[0]['commodity_code']
    assert test_item['item_line'] == itemAfter[0]['item_line']
    assert test_item['item_group'] == itemAfter[0]['item_group']
    assert test_item['item_type'] == itemAfter[0]['item_type']
    assert test_item['unit_purchase_quantity'] == itemAfter[0]['unit_purchase_quantity']
    assert test_item['unit_order_quantity'] == itemAfter[0]['unit_order_quantity']
    assert test_item['pack_order_quantity'] == itemAfter[0]['pack_order_quantity']
    assert test_item['supplier_id'] == itemAfter[0]['supplier_id']
    assert test_item['supplier_code'] == itemAfter[0]['supplier_code']
    assert test_item['supplier_part_number'] == itemAfter[0]['supplier_part_number']

    assert itemAfter[0]['supplier_id'] == _testSuppliers[0]['id']
    assert itemAfter[0]['supplier_code'] == _testSuppliers[0]['code']

def test_put_supplier(_DataPytestFixture):
    # Arrange
    _connection, _url, _testSuppliers, _headers = _DataPytestFixture
    extraSupplier = {"id": 1000003,"code": "PUS0002","name": "Holden-Nuts","address": "666 Christopher Roads","address_extra": "Suite 069","city": "Amberbusy","zip_code": "16905","province": "Illinose","country": "Devil Martin","contact_name": "Caitlynn Vincent","phonenumber": "666-733-291-8848x3542","reference": "H-PUS0002","created_at": "1995-12-18 03:05:46","updated_at": "2019-11-10 22:11:12"}
    # Add the two test suppliers to the database
    for supplier in _testSuppliers:
        json_data = json.dumps(supplier).encode('utf-8')
        _connection.request('POST', f'{_url}', body=json_data, headers=_headers)
        _connection.getresponse().close()

    # Act
    # Update the first test supplier with the extraSupplier
    json_data = json.dumps(extraSupplier).encode('utf-8')
    _connection.request('PUT',f'{_url}/{_testSuppliers[0]["id"]}', body=json_data, headers=_headers)
    response = _connection.getresponse()
    putStatusCode = response.status
    response.close()

    # Send a GET request to the GET_SPECIFIC_SUPPLIER endpoint
    _connection.request('GET', f'{_url}/{extraSupplier["id"]}', headers=_headers)

    # Get the response
    response = _connection.getresponse()
    data = response.read()
    supplierAfter = json.loads(data)
    
    # Clean up
    _connection.request('DELETE',f'{_url}/{extraSupplier["id"]}', headers=_headers)
    _connection.getresponse().close()
    for supplier in _testSuppliers:
        json_data = json.dumps(supplier).encode('utf-8')
        _connection.request('DELETE',f'{_url}/{supplier["id"]}', headers=_headers)
        _connection.getresponse().close()

    # Assert
    assert putStatusCode == 200
    assert supplierAfter["id"] == extraSupplier["id"]
    assert supplierAfter["code"] == extraSupplier["code"]
    assert supplierAfter["name"] == extraSupplier["name"]
    assert supplierAfter["address"] == extraSupplier["address"]
    assert supplierAfter["address_extra"] == extraSupplier["address_extra"]
    assert supplierAfter["city"] == extraSupplier["city"]
    assert supplierAfter["zip_code"] == extraSupplier["zip_code"]
    assert supplierAfter["province"] == extraSupplier["province"]
    assert supplierAfter["country"] == extraSupplier["country"]
    assert supplierAfter["contact_name"] == extraSupplier["contact_name"]
    assert supplierAfter["phonenumber"] == extraSupplier["phonenumber"]
    assert supplierAfter["reference"] == extraSupplier["reference"]

def test_delete_supplier(_DataPytestFixture):
    # Arrange  
    _connection, _url, _testSuppliers, _headers = _DataPytestFixture
    # Add the two test suppliers to the database
    for supplier in _testSuppliers:
        json_data = json.dumps(supplier).encode('utf-8')
        _connection.request('POST', f'{_url}', body=json_data, headers=_headers)
        _connection.getresponse().close()

    # Act  
    # Delete the first supplier
    _connection.request('DELETE',f'{_url}/{_testSuppliers[0]["id"]}', headers=_headers)
    response = _connection.getresponse()
    deleteStatusCode = response.status
    response.close()

    # Try getting the deleted supplier
    _connection.request('GET', f'{_url}/{_testSuppliers[0]["id"]}', headers=_headers)

    # Get the response
    response = _connection.getresponse()
    supplierAfter = response.read()
    
    # Clean up
    for supplier in _testSuppliers:
        json_data = json.dumps(supplier).encode('utf-8')
        _connection.request('DELETE',f'{_url}/{supplier["id"]}', headers=_headers)
        _connection.getresponse().close()
        
    # Assert
    # "b'null'" Means that no supplier was found
    assert str(supplierAfter) == "b'null'"
    assert deleteStatusCode == 200

def test_add_supplier_wrong_format(_DataPytestFixture):
    # Arrange  
    _connection, _url, _testSuppliers, _headers = _DataPytestFixture
    
    extraWrongSupplier = {"id": 1000003,"cude": "PUS0002","Sname": "Holden-Nuts","adress": "666 Christopher Roads","adress_extra": "Suite 069","citty": "Amberbusy","sip_code": "16905","brovince": "Illinose","cuntry": "Devil Martin","contact_Sname": "Caitlynn Vincent","bhonenumber": "666-733-291-8848x3542","breference": "H-PUS0002","created_at": "1995-12-18 03:05:46","updated_at": "2019-11-10 22:11:12"}    
    
    # Act
    # Try adding the supplier with the wrong format
    json_data = json.dumps(extraWrongSupplier).encode('utf-8')
    _connection.request('POST',_url, body=json_data, headers=_headers)
    response = _connection.getresponse()
    postStatus = response.status
    response.close()

    # Send a GET request to the GET_ALL endpoint
    _connection.request('GET', _url, headers=_headers)
    response = _connection.getresponse()
    data = response.read()
    suppliers = json.loads(data)
    # list comprehension to get a list of all supplier id's
    suppliersIds = [w["id"] for w in suppliers]

    # Clean up
    _connection.request('DELETE',f'{_url}/{extraWrongSupplier["id"]}', headers=_headers)
    _connection.getresponse().close()

    # Assert
    assert postStatus == 400
    assert extraWrongSupplier["id"] not in suppliersIds

def test_put_supplier_wrong_format(_DataPytestFixture):
    # Arrange
    _connection, _url, _testSuppliers, _headers = _DataPytestFixture
    extraWrongSupplier = {"id": 1000003,"cude": "PUS0002","Sname": "Holden-Nuts","adress": "666 Christopher Roads","adress_extra": "Suite 069","citty": "Amberbusy","sip_code": "16905","brovince": "Illinose","cuntry": "Devil Martin","contact_Sname": "Caitlynn Vincent","bhonenumber": "666-733-291-8848x3542","breference": "H-PUS0002","created_at": "1995-12-18 03:05:46","updated_at": "2019-11-10 22:11:12"}
    # Add the two test suppliers to the database
    for supplier in _testSuppliers:
        json_data = json.dumps(supplier).encode('utf-8')
        _connection.request('POST', f'{_url}', body=json_data, headers=_headers)
        _connection.getresponse().close()

    # Act
    # Update the first test supplier with the extraWrongSupplier
    json_data = json.dumps(extraWrongSupplier).encode('utf-8')
    _connection.request('PUT',f'{_url}/{_testSuppliers[0]["id"]}', body=json_data, headers=_headers)
    response = _connection.getresponse()
    putStatusCode = response.status
    response.close()

    # Send a GET request to the GET_ALL endpoint
    _connection.request('GET', _url, headers=_headers)
    response = _connection.getresponse()
    data = response.read()
    suppliers = json.loads(data)
    # list comprehension to get a list of all suppliers id's
    supplierssIds = [w["id"] for w in suppliers]
    
    # Clean up
    _connection.request('DELETE',f'{_url}/{extraWrongSupplier["id"]}', headers=_headers)
    _connection.getresponse().close()
    for supplier in _testSuppliers:
        json_data = json.dumps(supplier).encode('utf-8')
        _connection.request('DELETE',f'{_url}/{supplier["id"]}', headers=_headers)
        _connection.getresponse().close()

    # Assert
    assert putStatusCode == 400
    assert extraWrongSupplier["id"] not in supplierssIds
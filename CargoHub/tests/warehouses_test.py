import http.client
import json

warehousesPath = './data/warehouses.json'

def test_get_all():
    # Arrange
    headers = {
        'API_KEY': 'a1b2c3d4e5', 
        'Content-Type': 'application/json'
    }        
    testWarehouses = [{"id": 1000001, "code": "YQZZNL56", "name": "Heemskerk cargo hub", "address": "Karlijndreef 281", "zip": "4002 AS", "city": "Heemskerk", "province": "Friesland", "country": "NL", "contact": {"name": "Fem Keijzer", "phone": "(078) 0013363", "email": "blamore@example.net"}, "created_at": "1983-04-13 04:59:55", "updated_at": "2007-02-08 20:11:00"}, 
                      {"id": 1000002, "code": "GIOMNL90", "name": "Petten longterm hub", "address": "Owenweg 731", "zip": "4615 RB", "city": "Petten", "province": "Noord-Holland", "country": "NL", "contact": {"name": "Maud Adryaens", "phone": "+31836 752702", "email": "nickteunissen@example.com"}, "created_at": "2008-02-22 19:55:39", "updated_at": "2009-08-28 23:15:50"}]
    
    # Create a connection to localhost on port 3000
    connection = http.client.HTTPConnection('localhost', 3000)

    # Add the two test warehouses to the database
    for warehouse in testWarehouses:
        json_data = json.dumps(warehouse).encode('utf-8')
        connection.request('POST','/api/v1/warehouses', body=json_data, headers=headers)
        connection.getresponse().close()

    # Act
    # Send a GET request to the GET_ALL endpoint
    connection.request('GET', '/api/v1/warehouses', headers=headers)

    # Get the response
    response = connection.getresponse()
    data = response.read()
    warehouses = json.loads(data)
    # list comprehension to get a list of all warehouse id's
    warehousesIds = [w["id"] for w in warehouses]
    
    # Assert
    assert str(response.status) == '200'
    assert len(warehouses) >= 2
    for warehouse in testWarehouses:
        assert warehouse["id"] in warehousesIds

    # Clean up
    for warehouse in testWarehouses:
        json_data = json.dumps(warehouse).encode('utf-8')
        connection.request('DELETE',f'/api/v1/warehouses/{warehouse["id"]}', headers=headers)
        connection.getresponse().close()

        
def test_get_one():
    # Arrange
    headers = {
        'API_KEY': 'a1b2c3d4e5', 
        'Content-Type': 'application/json'
    }        
    testWarehouses = [{"id": 1000001, "code": "YQZZNL56", "name": "Heemskerk cargo hub", "address": "Karlijndreef 281", "zip": "4002 AS", "city": "Heemskerk", "province": "Friesland", "country": "NL", "contact": {"name": "Fem Keijzer", "phone": "(078) 0013363", "email": "blamore@example.net"}, "created_at": "1983-04-13 04:59:55", "updated_at": "2007-02-08 20:11:00"}, 
                      {"id": 1000002, "code": "GIOMNL90", "name": "Petten longterm hub", "address": "Owenweg 731", "zip": "4615 RB", "city": "Petten", "province": "Noord-Holland", "country": "NL", "contact": {"name": "Maud Adryaens", "phone": "+31836 752702", "email": "nickteunissen@example.com"}, "created_at": "2008-02-22 19:55:39", "updated_at": "2009-08-28 23:15:50"}]
    
    # Create a connection to localhost on port 3000
    connection = http.client.HTTPConnection('localhost', 3000)

    # Add the two test warehouses to the database
    for warehouse in testWarehouses:
        json_data = json.dumps(warehouse).encode('utf-8')
        connection.request('POST','/api/v1/warehouses', body=json_data, headers=headers)
        connection.getresponse().close()
    # Act   
    # Send a GET request to the GET_SPECIFIC_WAREHOUSE endpoint
    connection.request('GET', f'/api/v1/warehouses/{testWarehouses[0]["id"]}', headers=headers)

    # Get the response
    response = connection.getresponse()
    data = response.read()
    warehouseAfter = json.loads(data)

    # Assert
    assert str(response.status) == '200'
    assert type(warehouseAfter) == dict
    assert warehouseAfter["code"] == testWarehouses[0]["code"]
    assert warehouseAfter["name"] == testWarehouses[0]["name"]
    assert warehouseAfter["address"] == testWarehouses[0]["address"]
    assert warehouseAfter["zip"] == testWarehouses[0]["zip"]
    assert warehouseAfter["city"] == testWarehouses[0]["city"]
    assert warehouseAfter["province"] == testWarehouses[0]["province"]
    assert warehouseAfter["country"] == testWarehouses[0]["country"]
    assert warehouseAfter["contact"] == testWarehouses[0]["contact"]
    # Clean up
    for warehouse in testWarehouses:
        json_data = json.dumps(warehouse).encode('utf-8')
        connection.request('DELETE',f'/api/v1/warehouses/{warehouse["id"]}', headers=headers)
        connection.getresponse().close()

def test_put_warehouse():
    # Arrange
    headers = {
        'API_KEY': 'a1b2c3d4e5', 
        'Content-Type': 'application/json'
    }        
    testWarehouses = [{"id": 1, "code": "YQZZNL56", "name": "Heemskerk cargo hub", "address": "Karlijndreef 281", "zip": "4002 AS", "city": "Heemskerk", "province": "Friesland", "country": "NL", "contact": {"name": "Fem Keijzer", "phone": "(078) 0013363", "email": "blamore@example.net"}, "created_at": "1983-04-13 04:59:55", "updated_at": "2007-02-08 20:11:00"}, 
                      {"id": 2, "code": "GIOMNL90", "name": "Petten longterm hub", "address": "Owenweg 731", "zip": "4615 RB", "city": "Petten", "province": "Noord-Holland", "country": "NL", "contact": {"name": "Maud Adryaens", "phone": "+31836 752702", "email": "nickteunissen@example.com"}, "created_at": "2008-02-22 19:55:39", "updated_at": "2009-08-28 23:15:50"}]
    
    extraWarehouse = {"id": 3, "code": "LIGMAL90", "name": "Petten shortterm hub", "address": "Owenweg 666", "zip": "6420 RB", "city": "Patten", "province": "Zuid-Holland", "country": "DE", "contact": {"name": "Maud Adryaens", "phone": "+31836 752702", "email": "nickteunissen@gmail.com"}, "created_at": "2021-02-22 19:55:39", "updated_at": "2009-08-28 23:15:50"}

    
    
    # Act
    # Create a connection to localhost on port 3000
    connection = http.client.HTTPConnection('localhost', 3000)

    # Add the two test warehouses to the database
    for warehouse in testWarehouses:
        json_data = json.dumps(warehouse).encode('utf-8')
        connection.request('POST','/api/v1/warehouses', body=json_data, headers=headers)
        connection.getresponse().close()
    
    # Update the first test warehouse with the extraWarehouse
    json_data = json.dumps(extraWarehouse).encode('utf-8')
    connection.request('PUT',f'/api/v1/warehouses/{testWarehouses[0]["id"]}', body=json_data, headers=headers)
    response = connection.getresponse()
    putStatusCode = response.status
    response.close()

    # Send a GET request to the GET_SPECIFIC_WAREHOUSE endpoint
    connection.request('GET', f'/api/v1/warehouses/{extraWarehouse["id"]}', headers=headers)

    # Get the response
    response = connection.getresponse()
    data = response.read()
    warehouseAfter = json.loads(data)
    
    
    # Assert
    assert putStatusCode == 200
    assert warehouseAfter["code"] == extraWarehouse["code"]
    assert warehouseAfter["name"] == extraWarehouse["name"]
    assert warehouseAfter["address"] == extraWarehouse["address"]
    assert warehouseAfter["zip"] == extraWarehouse["zip"]
    assert warehouseAfter["city"] == extraWarehouse["city"]
    assert warehouseAfter["province"] == extraWarehouse["province"]
    assert warehouseAfter["country"] == extraWarehouse["country"]
    assert warehouseAfter["contact"] == extraWarehouse["contact"]

def test_delete_warehouse():
    # Arrange
    headers = {
        'API_KEY': 'a1b2c3d4e5', 
        'Content-Type': 'application/json'
    }        
    testWarehouses = [{"id": 1, "code": "YQZZNL56", "name": "Heemskerk cargo hub", "address": "Karlijndreef 281", "zip": "4002 AS", "city": "Heemskerk", "province": "Friesland", "country": "NL", "contact": {"name": "Fem Keijzer", "phone": "(078) 0013363", "email": "blamore@example.net"}, "created_at": "1983-04-13 04:59:55", "updated_at": "2007-02-08 20:11:00"}, 
                      {"id": 2, "code": "GIOMNL90", "name": "Petten longterm hub", "address": "Owenweg 731", "zip": "4615 RB", "city": "Petten", "province": "Noord-Holland", "country": "NL", "contact": {"name": "Maud Adryaens", "phone": "+31836 752702", "email": "nickteunissen@example.com"}, "created_at": "2008-02-22 19:55:39", "updated_at": "2009-08-28 23:15:50"}]
    
    
    
    # Act
    # Create a connection to localhost on port 3000
    connection = http.client.HTTPConnection('localhost', 3000)

    # Add the two test warehouses to the database
    for warehouse in testWarehouses:
        json_data = json.dumps(warehouse).encode('utf-8')
        connection.request('POST','/api/v1/warehouses', body=json_data, headers=headers)
        connection.getresponse().close()
    
    # Delete the first warehouse
    connection.request('DELETE',f'/api/v1/warehouses/{testWarehouses[0]["id"]}', headers=headers)
    response = connection.getresponse()
    deleteStatusCode = response.status
    response.close()

    # Send a GET request to the GET_ALL endpoint
    connection.request('GET', '/api/v1/warehouses', headers=headers)
    response = connection.getresponse()
    data = response.read()
    warehousesDict = json.loads(data)

    # Try getting the deleted warehouse
    connection.request('GET', f'/api/v1/warehouses/{testWarehouses[0]["id"]}', headers=headers)

    # Get the response
    response = connection.getresponse()
    warehouseAfter = response.read()
    
    # Assert
    # "b'null'" Means that no warehouse was found
    assert str(warehouseAfter) == "b'null'"
    assert deleteStatusCode == 200
    assert len(warehousesDict) == 1
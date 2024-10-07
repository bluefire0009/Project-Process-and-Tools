import http.client
import signal
import threading
import json
import pytest
import os

warehousesPath = './data/warehouses.json'

def run_api():
     relative_path = 'start-system.bat'
     os.system('cd ..')
     os.system(relative_path)

def kill_api():
    output = os.popen('tasklist | findstr python').read()
    for line in output.splitlines():
        if 'python3.12.exe' in line:
            pid = int(line.split()[1])
            os.kill(pid, signal.SIGTERM)

@pytest.fixture
def setup_teardown():
    # Setup code
    # Save the warehouses.json content
    with open(warehousesPath, 'r') as warehouseFile:
        global warehousesBefore 
        warehousesBefore = warehouseFile.read()
        warehouseFile.close()
    
    # Overwrite the content of warehouses.json with empty file   
    with open(warehousesPath, 'w') as warehouseFile:
        warehouseFile.write("[]")
        warehouseFile.close()

    yield
    # Teardown code
    # Restore the content of warehouses.json
    with open(warehousesPath, 'w') as warehouseFile:
        warehouseFile.write(warehousesBefore)
        warehouseFile.close()

def test_get_all(setup_teardown):
    # Arrange
    headers = {
        'API_KEY': 'a1b2c3d4e5', 
        'Content-Type': 'application/json'
    }        
    testWarehouses = [{"id": 1, "code": "YQZZNL56", "name": "Heemskerk cargo hub", "address": "Karlijndreef 281", "zip": "4002 AS", "city": "Heemskerk", "province": "Friesland", "country": "NL", "contact": {"name": "Fem Keijzer", "phone": "(078) 0013363", "email": "blamore@example.net"}, "created_at": "1983-04-13 04:59:55", "updated_at": "2007-02-08 20:11:00"}, 
                      {"id": 2, "code": "GIOMNL90", "name": "Petten longterm hub", "address": "Owenweg 731", "zip": "4615 RB", "city": "Petten", "province": "Noord-Holland", "country": "NL", "contact": {"name": "Maud Adryaens", "phone": "+31836 752702", "email": "nickteunissen@example.com"}, "created_at": "2008-02-22 19:55:39", "updated_at": "2009-08-28 23:15:50"}]
    
    threading.Thread(target=run_api).start()
    
    # Act
    # Create a connection to localhost on port 3000
    connection = http.client.HTTPConnection('localhost', 3000)

    # Send two POST requests to the ADD_ONE endpoint
    for warehouse in testWarehouses:
        json_data = json.dumps(warehouse).encode('utf-8')
        warehouseRequest = connection.request('POST','/api/v1/warehouses', body=json_data, headers=headers)
        connection.getresponse().close()
    
    # Send a GET request to the GET_ALL endpoint
    connection.request('GET', '/api/v1/warehouses', headers=headers)

    # Get the response
    response = connection.getresponse()
    data = response.read()
    warehousesDict = json.loads(data)
    
    kill_api()
    # Assert
    assert str(response.status) == '200'
    assert len(warehousesDict) == 2
        
def test_get_one(setup_teardown):
    # Arrange
    headers = {
        'API_KEY': 'a1b2c3d4e5', 
        'Content-Type': 'application/json'
    }        
    testWarehouses = [{"id": 1, "code": "YQZZNL56", "name": "Heemskerk cargo hub", "address": "Karlijndreef 281", "zip": "4002 AS", "city": "Heemskerk", "province": "Friesland", "country": "NL", "contact": {"name": "Fem Keijzer", "phone": "(078) 0013363", "email": "blamore@example.net"}, "created_at": "1983-04-13 04:59:55", "updated_at": "2007-02-08 20:11:00"}, 
                      {"id": 2, "code": "GIOMNL90", "name": "Petten longterm hub", "address": "Owenweg 731", "zip": "4615 RB", "city": "Petten", "province": "Noord-Holland", "country": "NL", "contact": {"name": "Maud Adryaens", "phone": "+31836 752702", "email": "nickteunissen@example.com"}, "created_at": "2008-02-22 19:55:39", "updated_at": "2009-08-28 23:15:50"}]
    
    threading.Thread(target=run_api).start()
    
    # Act
    # Create a connection to localhost on port 3000
    connection = http.client.HTTPConnection('localhost', 3000)

    # Send two POST requests to the ADD_ONE endpoint
    for warehouse in testWarehouses:
        json_data = json.dumps(warehouse).encode('utf-8')
        warehouseRequest = connection.request('POST','/api/v1/warehouses', body=json_data, headers=headers)
        connection.getresponse().close()
    
    # Send a GET request to the GET_SPECIFIC_WAREHOUSE endpoint
    connection.request('GET', f'/api/v1/warehouses/{testWarehouses[0]["id"]}', headers=headers)

    # Get the response
    response = connection.getresponse()
    data = response.read()
    warehouseAfter = json.loads(data)
    
    kill_api()
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
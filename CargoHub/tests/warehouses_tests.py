import http.client
import threading
import json
import pytest
import os

warehousesPath = './data/warehouses.json'

def run_api():
     relative_path = 'start-system.bat'
     os.system('cd ..')
     os.system(relative_path)

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
        warehouseFile.write("")
        warehouseFile.close()

    yield
    # Teardown code
    # Restore the content of warehouses.json
    with open(warehousesPath, 'w') as warehouseFile:
        warehouseFile.write(warehousesBefore)
        warehouseFile.close()

def test_get_all(setup_teardown):
        # Arrange
        headers = {'API_KEY': 'a1b2c3d4e5'}        
        testWarehouses = '[{"id": 1, "code": "YQZZNL56", "name": "Heemskerk cargo hub", "address": "Karlijndreef 281", "zip": "4002 AS", "city": "Heemskerk", "province": "Friesland", "country": "NL", "contact": {"name": "Fem Keijzer", "phone": "(078) 0013363", "email": "blamore@example.net"}, "created_at": "1983-04-13 04:59:55", "updated_at": "2007-02-08 20:11:00"}, {"id": 2, "code": "GIOMNL90", "name": "Petten longterm hub", "address": "Owenweg 731", "zip": "4615 RB", "city": "Petten", "province": "Noord-Holland", "country": "NL", "contact": {"name": "Maud Adryaens", "phone": "+31836 752702", "email": "nickteunissen@example.com"}, "created_at": "2008-02-22 19:55:39", "updated_at": "2009-08-28 23:15:50"}]'
        # Add two warehouses to data file to test
        with open(warehousesPath, 'w') as warehouseFile:
                warehouseFile.write(testWarehouses)
                warehouseFile.close()

        threading.Thread(target=run_api).start()
       
        # Act
        # Create a connection to localhost on port 3000
        connection = http.client.HTTPConnection('localhost', 3000)

        # Send a GET request to the specific endpoint
        connection.request('GET', '/api/v1/warehouses', headers=headers)

        # Get the response
        response = connection.getresponse()
        data = response.read()
        warehousesDict = json.loads(data)
        
        # Assert
        assert str(response.status) == '200'
        assert len(warehousesDict) == 2
        

    


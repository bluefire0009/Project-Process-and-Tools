import http.client
import threading
import json
import pytest
import os

shipmentsPath = './data/shipments.json'


def run_api():
    relative_path = 'start-system.bat'
    os.system('cd ..')
    os.system(relative_path)


# Path to the shipments.json file
shipmentsPath = './data/shipments.json'


@pytest.fixture(scope='function')
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


def post_get_test(setup_teardown):
    with open(shipmentsPath, 'r') as shipmentsFile:
        content = shipmentsFile.read()
    assert content == ""  # File should be empty because of setup

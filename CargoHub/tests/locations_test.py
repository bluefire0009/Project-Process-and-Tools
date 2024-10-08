import http.client
import threading
import json
import pytest
import os
import signal

shipmentsPath = './data/locations.json'
headers = {'API_KEY': 'a1b2c3d4e5', 'Content-Type': 'application/json'}


def run_api():
    relative_path = "start-system.bat"
    os.system('cd ..')
    os.system(relative_path)


def kill_api():
    output = os.popen('tasklist | findstr python').read()
    for line in output.splitlines():
        if 'python3.12.exe' in line:
            pid = int(line.split()[1])
            os.kill(pid, signal.SIGTERM)


@pytest.fixture(scope='session')
def run_kill_api():
    threading.Thread(target=run_api).start()

    yield

    kill_api()


@pytest.fixture()
def setup_teardown():
    # Setup: Save the original content of the file
    with open(shipmentsPath, 'r') as shipmentsFile:
        original_content = shipmentsFile.read()

    # Clear the file for the test
    with open(shipmentsPath, 'w') as shipmentsFile:
        shipmentsFile.write("[]")

    # Provide this setup to the test and then ensure cleanup runs afterward
    yield

    # Teardown: Restore the file to its original content
    with open(shipmentsPath, 'w') as shipmentsFile:
        shipmentsFile.write(original_content)

def 
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


# @pytest.fixture
def setup_file():
    
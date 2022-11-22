import requests
from config import config
import time

macro_number = 0 

def test_runMacro_two():
    macro_number = 201 
    r = requests.post(f'{config.API_URL}/macros/{macro_number}/run')
    assert r.status_code == 200
    time.sleep(10)

def test_runMacro_two():
    macro_number = 2 
    r = requests.post(f'{config.API_URL}/macros/{macro_number}/run')
    assert r.status_code == 200
    time.sleep(15)

def test_runMacro_three():
    macro_number = 3 
    r = requests.post(f'{config.API_URL}/macros/{macro_number}/run')
    assert r.status_code == 200
    time.sleep(15)


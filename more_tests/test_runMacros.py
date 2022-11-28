import requests
from config import config

macro_number = 0 

def test_runMacro_two():
    macro_number = 2 
    r = requests.post(f'{config.API_URL}/macros/{macro_number}/run')
    assert r.status_code == 200

def test_runMacro_three():
    macro_number = 3 
    r = requests.post(f'{config.API_URL}/macros/{macro_number}/run')
    assert r.status_code == 200


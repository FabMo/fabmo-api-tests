import requests
from config import config

macro_number = 0 

def test_runMacro_two_hundred_one():
    macro_number = 201 
    r = requests.post(f'{config.API_URL}/macros/{macro_number}/run')
    assert r.status_code == 200
import requests
from config import config

def test_getConfig():
    r = requests.get(f'{config.API_URL}/config')
    assert r.status_code == 200


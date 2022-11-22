import requests
from config import config

def test_getStatus():
    r = requests.get(f'{config.API_URL}/status/')
    assert r.status_code == 200


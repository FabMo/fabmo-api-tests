import requests
from config import config

def test_getVersion():
    r = requests.get(f'{config.API_URL}/version/')
    assert r.status_code == 200


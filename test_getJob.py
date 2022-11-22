import requests
from config import config

def test_getJobQueue():
    r = requests.get(f'{config.API_URL}/job')
    assert r.status_code == 200


import requests
from config import config

def test_runNextJob():
    r = requests.post(f'{config.API_URL}/jobs/queue/run')
    assert r.status_code == 200


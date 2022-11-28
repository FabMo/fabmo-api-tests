import requests
from config import config

def test_clearJobQueue():
    r = requests.delete(f'{config.API_URL}/jobs/queue')
    assert r.status_code == 200


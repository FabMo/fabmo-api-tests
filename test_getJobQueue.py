import requests
from config import config

def test_getJobQueue():
    r = requests.get(f'{config.API_URL}/jobs/queue')
    assert r.status_code == 200


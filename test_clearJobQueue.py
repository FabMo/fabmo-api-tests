import requests
from config import config

def test_clearJobQueue():
    print("Test clear job queue, not fully implemented")
    r = requests.delete(f'{config.API_URL}/jobs/queue')
    assert r.status_code == 200


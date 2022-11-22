import requests
from config import config
import time

def test_runNextJob():
    r = requests.post(f'{config.API_URL}/jobs/queue/run')
    assert r.status_code == 200
    time.sleep(10)


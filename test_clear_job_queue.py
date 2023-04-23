import requests
from config import config

def test_clear_job_queue():
    print("Test clear job queue, not fully implemented")
    r = requests.delete(f'{config.API_URL}/jobs/queue', timeout = config.TIMEOUT)
    assert r.status_code == 200

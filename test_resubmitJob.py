import requests
from config import config

job_to_submit = 3

def test_resubmitJob():
    r = requests.post(f'{config.API_URL}/job/{job_to_submit}')
    assert r.status_code == 200


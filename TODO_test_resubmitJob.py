# TODO not fully implementented and can cause issues with pytest
# when an unexpected job is resubmitted
# Should submit a job, retrieve the id, clear the queue and then
# resubmit the known job and clear the queue at the end

import requests
from config import config

job_to_submit = 3

def test_resubmitJob():
    print("Test resubmit job, not fully implemented")
    r = requests.post(f'{config.API_URL}/job/{job_to_submit}', timeout=config.TIMEOUT)
    assert r.status_code == 200

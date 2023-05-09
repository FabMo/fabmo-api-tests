import time
import urllib3
import requests
from config import config
from message_monitor import MessageMonitor

mm = MessageMonitor()

class Job:
    def __init__(self):
        self.initialized = 1
    #public method
    #Takes three optional arguments
    #The most important is the filename, which must exist in the local jobs directory
    #If no arguments are provided, the sample_shopbot_logo file will be submitted
    def submit(self, filename = "sample_shopbot_logo.sbp", name = "test_name", description="test_description"):
        # Setup for requests
        with open('jobs/' + filename, 'r', encoding="utf8") as file:
            codes = file.read()

        metadata = {
            'files' : [
                {
                    'filename' : filename,
                    'name' : name,
                    'description' : description
                }
            ],
            'meta' : {}
        }

        # First request
        r = requests.post(f'{config.API_URL}/job', json=metadata, timeout=config.TIMEOUT)

        # Setup for second request
        # Extract key from first response json
        json_data = r.json()
        response_key = json_data['data']['key']
        fields = {
            'key': response_key,
            'index': 0,
            'file': (filename, codes),
        }

        body, content_type = urllib3.encode_multipart_formdata(fields)
        headers = {"Content-type": content_type, "Accept":"text/plain"}

        # Second request
        r = requests.post(f'{config.API_URL}/job', data=body, headers=headers, timeout=config.TIMEOUT)

    def submit_by_id(self, job_id):
        r = requests.post(f'{config.API_URL}/job/{job_id}', timeout=config.TIMEOUT)

    def clear_queue(self):
        r = requests.delete(f'{config.API_URL}/jobs/queue', timeout=config.TIMEOUT)

    def delete(self, job_id):
        r = requests.delete(f'{config.API_URL}/job/{job_id}', timeout=config.TIMEOUT)
        print(r.text)

    def run_next_job_in_queue(self):
        r = requests.post(f'{config.API_URL}/jobs/queue/run', timeout=config.TIMEOUT)

    def resume(self):
        r = requests.post(f'{config.API_URL}/resume', timeout=config.TIMEOUT)

    def pause(self):
        r = requests.post(f'{config.API_URL}/pause', timeout=config.TIMEOUT)

    def quit(self):
        r = requests.post(f'{config.API_URL}/quit', timeout=config.TIMEOUT)

    def get_by_id(self, job_id):
        r = requests.get(f'{config.API_URL}/job/{job_id}', timeout=config.TIMEOUT)
        assert r.status_code == 200
        return r.json()

    def get_queue(self):
        r = requests.get(f'{config.API_URL}/jobs/queue', timeout=config.TIMEOUT)
        assert r.status_code == 200
        return r.json()

    def check_if_queue_is_empty(self):
        r = requests.get(f'{config.API_URL}/jobs/queue', timeout=config.TIMEOUT)
        assert r.status_code == 200
        queue = r.json()
        jobs_pending = queue['data']['jobs']['pending']
        if jobs_pending == []:
            return True
        else:
            return False

    def check_if_queue_is_not_empty(self):
        r = requests.get(f'{config.API_URL}/jobs/queue', timeout=config.TIMEOUT)
        assert r.status_code == 200
        queue = r.json()
        jobs_pending = queue['data']['jobs']['pending']
        if jobs_pending != []:
            return True
        else:
            return False

    # queue_index argument is its position in the job queue, i.e the first job is 0, second is 1, etc
    # desired_key argument is the key that you wish to retrieve the corresponding value from
    def get_value_from_queue(self, queue_index, desired_key):
        r = requests.get(f'{config.API_URL}/jobs/queue', timeout=config.TIMEOUT)
        assert r.status_code == 200
        queue = r.json()
        # I tried using file_id instead of _id here but it did not seem to work correctly
        id_value = queue['data']['jobs']['pending'][queue_index][desired_key]
        if id_value is not None:
            return id_value
        return False

    def get_job_history(self, start, count):
        r = requests.get(f'{config.API_URL}/jobs/history?start={start}&count={count}', timeout=config.TIMEOUT)
        return r.json()

    # TODO def update_order()

    # timeout is how long to wait for the expected state before giving up
    # interval is how long to sleep between pause and resume
    # repetitions dictates how many times a pause and resume will occur
    def pause_resume(self, timeout, interval, repetitions):
        for x in range(repetitions):
            print(f"pausing {x}")
            self.pause()
            print("waiting for paused")
            success = mm.wait_for_state("paused", timeout)
            if success:
                print("now paused")
            else:
                print("Timed out waiting for pause")
                return False
            time.sleep(interval)

            print(f"resuming {x}")
            self.resume()
            print("waiting for resume")
            success = mm.wait_for_state("running", timeout)
            if success:
                print("now running")
            else:
                print("Timed out waiting for resume")
                return False
            time.sleep(interval)
        return True

if __name__ == "__main__":
    job = Job()

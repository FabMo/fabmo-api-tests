import time
import uuid
import io
import codecs
import mimetypes
import sys
import json
import requests
from config import config
from message_monitor import MessageMonitor

mm = MessageMonitor()

# MultipartFormdataEncoder is a legacy class that is necessary for
# submitting a new job to fabmo, I would love to see this class go away.
# The requests library probably has the means to achieve this
class MultipartFormdataEncoder:
    def __init__(self):
        self.boundary = uuid.uuid4().hex
        self.content_type = f"multipart/form-data; boundary={self.boundary}"

    @classmethod
    def u(cls, s):
        if sys.hexversion < 0x03000000 and isinstance(s, str):
            s = s.decode('utf-8')
        if sys.hexversion >= 0x03000000 and isinstance(s, bytes):
            s = s.decode('utf-8')
        return s

    def iter(self, fields, files):
        """
        fields is a sequence of (name, value) elements for regular form fields.
        files is a sequence of (name, filename, file-type) elements for data to be uploaded as files
        Yield body's chunk as bytes
        """
        encoder = codecs.getencoder('utf-8')
        for (key, value) in fields:
            key = self.u(key)
            yield encoder(f"--{self.boundary}\r\n")
            yield encoder(self.u('Content-Disposition: form-data; name="{}"\r\n').format(key))
            yield encoder('\r\n')
            if isinstance(value, int) or isinstance(value, float):
                value = str(value)
            yield encoder(self.u(value))
            yield encoder('\r\n')
        for (key, filename, fd) in files:
            key = self.u(key)
            filename = self.u(filename)
            yield encoder(f"--{self.boundary}\r\n")
            yield encoder(self.u(f"Content-Disposition: form-data; name=\"{key}\"; filename=\"{filename}\"\r\n"))
            yield encoder(f"Content-Type: {mimetypes.guess_type(filename)[0] or 'application/octet-stream'}\r\n")
            yield encoder('\r\n')
            with fd:
                buff = fd.read()
                yield (buff, len(buff))
            yield encoder('\r\n')
        yield encoder(f"--{self.boundary}--\r\n")

    def encode(self, fields, files):
        body = io.BytesIO()
        for chunk, chunk_len in self.iter(fields, files):
            body.write(chunk)
        return self.content_type, body.getvalue()


class Job:
    def __init__(self):
        self.initialized = 1
    #public method
    #Takes three optional arguments
    #The most important is the filename, which must exist in the local jobs directory
    #If no arguments are provided, the sample_shopbot_logo file will be submitted
    def submit(self, filename = "sample_shopbot_logo.sbp", name = "test_name", description="test_description"):
        # Setup for requests
        key = ''
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
        if json_data and 'data' in json_data:
            if 'key' in json_data['data']:
                for k in json_data['data']['key']:
                    key += k

        content_type, body = MultipartFormdataEncoder().encode([('key', key), ('index',0)], [('file', filename, io.BytesIO(codes.encode('utf-8')))])
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
        if queue and 'data' in queue:
            if 'jobs' in queue['data']:
                if 'pending' in queue['data']['jobs']:
                    if queue['data']['jobs']['pending'] == []:
                        return True
                    else:
                        return False
        else:
            print("Check if queue is empty failed")
            return False

    def check_if_queue_is_not_empty(self):
        r = requests.get(f'{config.API_URL}/jobs/queue', timeout=config.TIMEOUT)
        assert r.status_code == 200
        queue = r.json()
        if queue and 'data' in queue:
            if 'jobs' in queue['data']:
                if 'pending' in queue['data']['jobs']:
                    if queue['data']['jobs']['pending'] != []:
                        return True
                    else:
                        return False
        else:
            print("Check if queue is NOT empty failed")
            return False

    # queue_index argument is its position in the job queue, i.e the first job is 0, second is 1, etc
    # desired_key argument is the key that you wish to retrieve the corresponding value from
    def get_value_from_queue(self, queue_index, desired_key):
        r = requests.get(f'{config.API_URL}/jobs/queue', timeout=config.TIMEOUT)
        assert r.status_code == 200
        data = r.text
        queue = json.loads(data)
        # I tried using file_id instead of _id here but it did not seem to work correctly
        id_value = queue['data']['jobs']['pending'][queue_index][desired_key]
        if id_value is not None:
            return id_value
        return False


    # TODO def get_job_history(start, count)

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

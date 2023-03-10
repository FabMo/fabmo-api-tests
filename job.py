import requests
import time
from config import config
import io, codecs, mimetypes, sys, uuid

# MultipartFormdataEncoder is a legacy class that is necessary for 
# submitting a new job to fabmo, I would love to see this class go away.
# The requests library probably has the means to achieve this
class MultipartFormdataEncoder(object):
    def __init__(self):
        self.boundary = uuid.uuid4().hex
        self.content_type = 'multipart/form-data; boundary={}'.format(self.boundary)

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
            yield encoder('--{}\r\n'.format(self.boundary))
            yield encoder(self.u('Content-Disposition: form-data; name="{}"\r\n').format(key))
            yield encoder('\r\n')
            if isinstance(value, int) or isinstance(value, float):
                value = str(value)
            yield encoder(self.u(value))
            yield encoder('\r\n')
        for (key, filename, fd) in files:
            key = self.u(key)
            filename = self.u(filename)
            yield encoder('--{}\r\n'.format(self.boundary))
            yield encoder(self.u('Content-Disposition: form-data; name="{}"; filename="{}"\r\n').format(key, filename))
            yield encoder('Content-Type: {}\r\n'.format(mimetypes.guess_type(filename)[0] or 'application/octet-stream'))
            yield encoder('\r\n')
            with fd:
                buff = fd.read()
                yield (buff, len(buff))
            yield encoder('\r\n')
        yield encoder('--{}--\r\n'.format(self.boundary))

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
        with open('jobs/' + filename, 'r') as file:
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
        r = requests.post(f'{config.API_URL}/job', json=metadata)

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
        r = requests.post(f'{config.API_URL}/job', data=body, headers=headers)

    def clear_job_queue(self):
        r = requests.delete(f'{config.API_URL}/jobs/queue')

    def run_next_job_in_queue(self):
        r = requests.post(f'{config.API_URL}/jobs/queue/run')

    def resume_job(self):
        r = requests.post(f'{config.API_URL}/resume')

    def pause_job(self):
        r = requests.post(f'{config.API_URL}/pause')

    def quit_job(self):
        r = requests.post(f'{config.API_URL}/quit')

    def get_job_by_id(self, id):
        r = requests.get(f'{config.API_URL}/job/{id}')
        assert r.status_code == 200
        return r.json()

    def get_job_queue(self):
        r = requests.get(f'{config.API_URL}/jobs/queue')
        assert r.status_code == 200
        return r.json()

if __name__ == "__main__":
    job = Job()


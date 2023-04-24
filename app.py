import uuid
import io
import codecs
import mimetypes
import sys
import requests
from config import config

# MultipartFormdataEncoder is a legacy class that is necessary for
# submitting a new job to fabmo, I would love to see this class go away.
# The requests library probably has the means to achieve this
class MultipartFormdataEncoder():
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


class App:
    def __init__(self):
        self.initialized = 1
    #public method
    def submit(self, app_to_submit):
        # Setup for requests
        key = ''
        with open('apps/' + app_to_submit, 'rb') as file:
            codes = file.read()

        metadata = {
            'files' : [
                {
                    'app' : app_to_submit,
                }
            ],
            'meta' : {}
        }

        # First request
        r = requests.post(f'{config.API_URL}/apps', json=metadata, timeout=config.TIMEOUT)
        print(r.text)

        # Setup for second request
        # Extract key from first response json
        json_data = r.json()
        if json_data and 'data' in json_data:
            if 'key' in json_data['data']:
                for k in json_data['data']['key']:
                    key += k

        content_type, body = MultipartFormdataEncoder().encode([('key', key), ('index',0)], [('file', app_to_submit, io.BytesIO(codes))])
        headers = {"Content-type": content_type, "Accept":"text/plain"}

        # Second request
        r = requests.post(f'{config.API_URL}/apps', data=body, headers=headers, timeout=config.TIMEOUT)
        print(r.text)

    def delete(self, app_to_delete):
        r = requests.delete(f'{config.API_URL}/apps/{app_to_delete}', timeout=config.TIMEOUT)
        print(r.text)

    def getApps(self):
        r = requests.get(f'{config.API_URL}/apps', timeout = config.TIMEOUT)
        assert r.status_code == 200
        return r.json()

    def getAppConfig(self, app_id):
        r = requests.get(f'{config.API_URL}/apps/{app_id}/config', timeout = config.TIMEOUT)
        assert r.status_code == 200
        return r.json()

    # TODO def setAppConfig(self, app_id):

if __name__ == "__main__":
    app = App()

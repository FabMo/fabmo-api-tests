import requests
import time
import threading
from config import config
from message_monitor import MessageMonitor
import io, codecs, mimetypes, sys, uuid
s=requests.Session()
global mm 
mm = MessageMonitor()
mm.clear_all_state()

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

# Utility functions
def submitJob(results):
    # Setup for requests
    filename = "job.sbp"
    name = "test_name"
    description = "test_description"
    key = ''

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
    print(r.text)
    if r.status_code != 200:
        results["code"] = False
        results["msg"] = "bad http code"
        return

    # Extract key from response json
    json_data = r.json()
    if json_data and 'data' in json_data:
        if 'key' in json_data['data']:
            for k in json_data['data']['key']:
                key += k
    print(key)
    print(type(key))
    codes = "mx, 10\nmx, 0"
    content_type, body = MultipartFormdataEncoder().encode([('key', key), ('index',0)], [('file', filename, io.BytesIO(codes.encode('utf-8')))])
    headers = {"Content-type": content_type, "Accept":"text/plain"}
    print("body")
    print(body)
    print(type(body))
    print("headers")
    print(headers)
    print(type(headers))
    # Second request
    r = requests.post(f'{config.API_URL}/job', data=body, headers=headers)
    print("r.text")
    print(r.text)
    if r.status_code != 200:
        results["code"] = False
        results["msg"] = "bad http code"
        return

    # Did test pass?
    results["code"] = True
    results["msg"] = "success"
    return 

def thread_for_mm(args):
    mm.run()

# test function

def test_submitJob():
    # setting things up so test can run
    messageMonitorThread = threading.Thread(target=thread_for_mm, args=(1,), daemon=True)
    results = {"code":False, "msg":""}
    testThread = threading.Thread(target=submitJob, args=(results,))

    # test sequence 
    messageMonitorThread.start() 
    time.sleep(1) # time for the MessageMonitor to get up and running
    testThread.start()
    testThread.join() #waiting for the test to return

    #reporting results
    # debug (i'm sure there is pytest way to turn this on and off)
    #print(results)
    assert(results["code"] == True)
 
if __name__ == "__main__":
    print("NEW SCRIPT")
    print(config.API_URL)
    test_submitJob()


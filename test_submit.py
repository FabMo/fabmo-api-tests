import json
import http.client
import io, codecs, mimetypes, sys, uuid

TIMEOUT = 3
conn = http.client.HTTPConnection('10.24.1.71', 80, timeout=TIMEOUT)

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

def submitJob():
    
    filename = "job.sbp"
    name = "test_name"
    description = "test_description"

    # First request
    headers = {"Content-type":"application/json", "Accept":"text/plain"}
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
    json_payload = json.dumps(metadata)
    conn.request("POST", "/job", json_payload, headers)
    response = conn.getresponse()
    response_text = response.read().decode('utf-8')
    print(response_text)
    response_data = json.loads(response_text)['data']
    # Second request
    codes = "mx, 10\nmx, 0"
    print(response_data['key'])
    print(type(response_data['key']))
    content_type, body = MultipartFormdataEncoder().encode([('key', response_data['key']), ('index',0)], [('file', filename, io.BytesIO(codes.encode('utf-8')))])
    headers = {"Content-type":content_type, "Accept":"text/plain"}
    conn.request("POST", "/job", body, headers)
    print("body")
    print(body)
    print(type(body))
    print("headers")
    print(headers)
    print(type(headers))
    response = conn.getresponse()
    response_text = response.read().decode('utf-8')
    response_data = json.loads(response_text)
    print("response_text")
    print(response_text)
    print("response_data")
    print(response_data)
    conn.close()

if __name__ == "__main__":
    print("OLD SCRIPT")
    submitJob()


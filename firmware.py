import urllib3
import requests
from config import config

class Firmware:
    def __init__(self):
        self.initialized = 1
    #public method
    def submit(self, firmware_to_submit):
        # Setup for requests
        with open('firmware/' + firmware_to_submit, 'rb') as file:
            codes = file.read()

        metadata = {
            'files' : [
                {
                    'firmware' : firmware_to_submit,
                }
            ],
            'meta' : {}
        }

        # First request
        r = requests.post(f'{config.API_URL}/firmware/update', json=metadata, timeout=config.TIMEOUT)
        print(r.text)

        # Setup for second request
        # Extract key from first response json
        json_data = r.json()
        response_key = json_data['data']['key']
        fields = {
            'key': response_key,
            'index': 0,
            'file': (firmware_to_submit, codes),
        }

        body, content_type = urllib3.encode_multipart_formdata(fields)
        headers = {"Content-type": content_type, "Accept":"text/plain"}
        # Second request
        r = requests.post(f'{config.API_URL}/firmware/update', data=body, headers=headers, timeout=config.TIMEOUT)
        print(r.text)

if __name__ == "__main__":
    firmware = Firmware()
    
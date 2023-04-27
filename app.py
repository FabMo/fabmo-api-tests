import urllib3
import requests
from config import config

class App:
    def __init__(self):
        self.initialized = 1
    #public method
    def submit(self, app_to_submit):
        # Setup for requests
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
        response_key = json_data['data']['key']

        fields = {
            'key': response_key,
            'index': 0,
            'file': (app_to_submit, codes),
        }

        body, content_type = urllib3.encode_multipart_formdata(fields)
        headers = {"Content-type": content_type, "Accept":"text/plain"}

        # Second request
        r = requests.post(f'{config.API_URL}/apps', data=body, headers=headers, timeout=config.TIMEOUT)
        print(r.text)

    def delete(self, app_to_delete):
        r = requests.delete(f'{config.API_URL}/apps/{app_to_delete}', timeout=config.TIMEOUT)
        print(r.text)

    def get_apps(self):
        r = requests.get(f'{config.API_URL}/apps', timeout = config.TIMEOUT)
        assert r.status_code == 200
        return r.json()

    def check_for_app(self, id_of_app):
        r = requests.get(f'{config.API_URL}/apps', timeout = config.TIMEOUT)
        assert r.status_code == 200
        app_list = r.json()
        for i in app_list['data']['apps']:
            if i['id'] == id_of_app:
                return True
        return False

    def get_app_config(self, app_id):
        r = requests.get(f'{config.API_URL}/apps/{app_id}/config', timeout = config.TIMEOUT)
        assert r.status_code == 200
        return r.json()

    # TODO def setAppConfig(self, app_id):

if __name__ == "__main__":
    app = App()

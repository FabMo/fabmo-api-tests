import requests
from config import config

class Get_Requests:
    def __init__(self):
        self.initialized = 1

    def get_config(self):
        r = requests.get(f'{config.API_URL}/config', timeout = config.TIMEOUT)
        assert r.status_code == 200
        return r.json()

    def get_status(self):
        r = requests.get(f'{config.API_URL}/status/', timeout = config.TIMEOUT)
        assert r.status_code == 200
        return r.json()

    def get_version(self):
        r = requests.get(f'{config.API_URL}/version/', timeout = config.TIMEOUT)
        assert r.status_code == 200
        return r.json()

    def get_info(self):
        r = requests.get(f'{config.API_URL}/info/', timeout = config.TIMEOUT)
        assert r.status_code == 200
        return r.json()

if __name__ == '__main__':
    get_requests = Get_Requests()

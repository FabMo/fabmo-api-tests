import requests
from config import config

class Updater:
    def __init__(self):
        self.initialized = 1

    def get_config(self):
        r = requests.get(f'{config.API_URL}/updater/config', timeout = config.TIMEOUT)
        assert r.status_code == 200
        return r.json()

    def set_config(self, config_data):
        r = requests.get(f'{config.API_URL}/updater/config', data = config_data, timeout = config.TIMEOUT)
        assert r.status_code == 200
        return r.json()

if __name__ == "__main__":
    updater = Updater()

import requests
from config import config

class Getters:
    def __init__(self):
        self.initialized = 1

    @staticmethod
    def getConfig():
        r = requests.get(f'{config.API_URL}/config')
        assert r.status_code == 200
        json_obj = r.json()
        return json_obj

    @staticmethod
    def getJob():
        r = requests.get(f'{config.API_URL}/job')
        assert r.status_code == 200
        json_obj = r.json()
        return json_obj

    @staticmethod
    def getJobQueue():
        r = requests.get(f'{config.API_URL}/job')
        assert r.status_code == 200
        return r.json()

    @staticmethod
    def getStatus():
        r = requests.get(f'{config.API_URL}/status/')
        assert r.status_code == 200
        return r.json()

    @staticmethod
    def getVersion():
        r = requests.get(f'{config.API_URL}/version/')
        assert r.status_code == 200
        return r.json()

if __name__ == '__main__':
    getters = Getters()
import requests
from config import config

class Get_Requests:
    def __init__(self):
        self.initialized = 1

    def getConfig(self):
        r = requests.get(f'{config.API_URL}/config')
        assert r.status_code == 200
        return r.json()

    def getJob(self, id):
        r = requests.get(f'{config.API_URL}/job/{id}')
        assert r.status_code == 200
        return r.json()

    def getJobQueue(self):
        r = requests.get(f'{config.API_URL}/jobs/queue')
        assert r.status_code == 200
        return r.json()

    def getStatus(self):
        r = requests.get(f'{config.API_URL}/status/')
        assert r.status_code == 200
        return r.json()

    def getVersion(self):
        r = requests.get(f'{config.API_URL}/version/')
        assert r.status_code == 200
        return r.json()

if __name__ == '__main__':
    get_requests = Get_Requests()
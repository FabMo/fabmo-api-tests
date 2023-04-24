import requests
from config import config

class User:
    def __init__(self):
        self.initialized = 1

    def get_current_user(self):
        r = requests.get(f'{config.API_URL}/authentication/user', timeout = config.TIMEOUT)
        assert r.status_code == 200
        return r.json()

    # TODO def add_user(self):
        #r = requests.post(f'{config.API_URL}/authentication/user', user_info=, timeout = config.TIMEOUT)

    # TODO def modify_user(self):
        #r = requests.post(f'{config.API_URL}/authentication/user', user_info=, timeout = config.TIMEOUT)

    def delete_user(self, user_id):
        r = requests.post(f'{config.API_URL}/authentication/user/{user_id}', timeout = config.TIMEOUT)

if __name__ == "__main__":
    user = User()

import requests
from config import config

class User:
    def __init__(self):
        self.initialized = 1

    def get_current_user(self):
        r = requests.get(f'{config.API_URL}/authentication/user', timeout = config.TIMEOUT)
        assert r.status_code == 200
        return r.json()

    def get_users(self):
        r = requests.get(f'{config.API_URL}/authentication/users', timeout = config.TIMEOUT)
        assert r.status_code == 200
        return r.json()

    # def add_user(self, new_user):
    #     r = requests.post(f'{config.API_URL}/authentication/user', data=new_user, timeout = config.TIMEOUT)
    #     print(r.text)

    # def modify_user(self, username, user_info):
    #    r = requests.post(f'{config.API_URL}/authentication/user/{username}', data=user_info, auth=('admin', 'test444'), timeout = config.TIMEOUT)
    #    print(r.text)

    def delete_user(self, user_id):
        r = requests.post(f'{config.API_URL}/authentication/user/{user_id}', timeout = config.TIMEOUT)

if __name__ == "__main__":
    user = User()

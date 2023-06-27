import requests
from config import config

# Create a session to persist the authentication cookies
session = requests.Session()

class User:
    def __init__(self):
        self.initialized = 1

    def authenticate(self):
        # Define the authentication credentials
        username = "admin"
        password = "go2fabmo"

        # Perform the authentication request
        auth_response = session.post(f"{config.API_URL}/authentication/login", data={"username": username, "password": password})
        
        assert auth_response.status_code == 200

    def get_current_user(self):
        self.authenticate()
        r = session.get(f'{config.API_URL}/authentication/user', timeout = config.TIMEOUT)
        assert r.status_code == 200
        print(r.json())
        return r.json()

    def get_users(self):
        self.authenticate()
        r = session.get(f'{config.API_URL}/authentication/users', timeout = config.TIMEOUT)
        assert r.status_code == 200
        print(r.json())
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

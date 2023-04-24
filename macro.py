import requests
from config import config

class Macro:
    def __init__(self):
        self.initialized = 1

    # TODO def update_macro

    def delete(self, macro_id):
        r = requests.delete(f'{config.API_URL}/macros/{macro_id}', timeout=config.TIMEOUT)
        print(r.text)

    def run_macro(self, macro_id):
        r = requests.post(f'{config.API_URL}/macros/{macro_id}', timeout=config.TIMEOUT)

    def get_macros(self):
        r = requests.get(f'{config.API_URL}/macros', timeout=config.TIMEOUT)
        assert r.status_code == 200
        return r.json()

if __name__ == "__main__":
    macro = Macro()

#import requests
#from config import config

class Firmware:
    def __init__(self):
        self.initialized = 1

    # def submit_update(self):
    #    r = requests.post(f'{config.API_URL}/firmware/update', file= , timeout = config.TIMEOUT)

if __name__ == "__main__":
    firmware = Firmware()

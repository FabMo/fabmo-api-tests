import requests
from config import config

class Network:
    def __init__(self):
        self.initialized = 1

    def connect_to_wifi(self, ssid, password):
        data = { 'ssid': ssid, 'password': password }
        r = requests.post(f'{config.API_URL}/network/wifi/connect', data, timeout = config.TIMEOUT)
        assert r.status_code == 200

    def disconnect_from_wifi(self):
        r = requests.post(f'{config.API_URL}/network/wifi/disconnect', timeout = config.TIMEOUT)
        assert r.status_code == 200

    def forget_wifi(self):
        r = requests.post(f'{config.API_URL}/network/wifi/forget', timeout = config.TIMEOUT)
        assert r.status_code == 200

    def enable_wifi(self):
        data = {'enabled': True}
        r = requests.post(f'{config.API_URL}/network/wifi/state', data, timeout = config.TIMEOUT)
        assert r.status_code == 200

    def disable_wifi(self):
        data = {'enabled': False}
        r = requests.post(f'{config.API_URL}/network/wifi/state', data, timeout = config.TIMEOUT)
        assert r.status_code == 200

    def enable_hotspot(self):
        data = {'enabled': True}
        r = requests.post(f'{config.API_URL}/network/hotspot/state', data, timeout = config.TIMEOUT)
        assert r.status_code == 200

    def disable_hotspot(self):
        data = {'enabled': False}
        r = requests.post(f'{config.API_URL}/network/hotspot/state', data, timeout = config.TIMEOUT)
        assert r.status_code == 200

    def get_network_identity(self):
        r = requests.get(f'{config.API_URL}/network/identity', timeout = config.TIMEOUT)
        assert r.status_code == 200
        return r.json()

    def set_network_identity(self, identity):
        r = requests.post(f'{config.API_URL}/network/identity', json = identity, timeout = config.TIMEOUT)
        assert r.status_code == 200
        print(r.json())

    def get_is_online(self):
        r = requests.get(f'{config.API_URL}/network/online', timeout = config.TIMEOUT)
        assert r.status_code == 200
        return r.json()

    def get_wifi_networks(self):
        r = requests.get(f'{config.API_URL}/network/wifi/scan', timeout = config.TIMEOUT)
        assert r.status_code == 200
        return r.json()

    def get_wifi_network_history(self):
        r = requests.get(f'{config.API_URL}/network/wifi/history', timeout = config.TIMEOUT)
        assert r.status_code == 200
        return r.json()

if __name__ == "__main__":
    network = Network()

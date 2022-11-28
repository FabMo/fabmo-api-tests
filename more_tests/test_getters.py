import requests
from config import config

def test_getConfig():
    r = requests.get(f'{config.API_URL}/config')
    assert r.status_code == 200

def test_getJob():
    r = requests.get(f'{config.API_URL}/job')
    assert r.status_code == 200

def test_getJobQueue():
    r = requests.get(f'{config.API_URL}/job')
    assert r.status_code == 200

def test_getStatus():
    r = requests.get(f'{config.API_URL}/status/')
    assert r.status_code == 200

def test_getVersion():
    r = requests.get(f'{config.API_URL}/version/')
    assert r.status_code == 200

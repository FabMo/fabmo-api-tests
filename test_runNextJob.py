import requests
from config import config
from message_monitor import MessageMonitor

def test_runNextJob():
    r = requests.post(f'{config.API_URL}/jobs/queue/run')
    assert r.status_code == 200

if  __name__ == "__main__": 
    print(config.API_URL) 
    test_runNextJob()
    mm = MessageMonitor()
    mm.run()
    

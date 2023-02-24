import requests
import time
import threading
from config import config
from message_monitor import MessageMonitor
from submit_job import SubmitJob
import io, codecs, mimetypes, sys, uuid

global mm 
mm = MessageMonitor()
mm.clear_all_state()

# Utility functions
def submitJob(results):
    # Setup for requests
    filename = "job.sbp"
    name = "test_name"
    description = "test_description"
    key = ''
    with open('jobs/sample_shopbot_logo.sbp', 'r') as file:
        codes = file.read()

    metadata = {
        'files' : [
            {
                'filename' : filename,
                'name' : name,
                'description' : description
            }
        ],
        'meta' : {}
    }

    # First request
    r = requests.post(f'{config.API_URL}/job', json=metadata)
    if r.status_code != 200:
        results["code"] = False
        results["msg"] = "bad http code"
        return

    # Setup for second request
    # Extract key from first response json
    json_data = r.json()
    if json_data and 'data' in json_data:
        if 'key' in json_data['data']:
            for k in json_data['data']['key']:
                key += k

    content_type, body = MultipartFormdataEncoder().encode([('key', key), ('index',0)], [('file', filename, io.BytesIO(codes.encode('utf-8')))])
    headers = {"Content-type": content_type, "Accept":"text/plain"}

    # Second request
    r = requests.post(f'{config.API_URL}/job', data=body, headers=headers)
    if r.status_code != 200:
        results["code"] = False
        results["msg"] = "bad http code"
        return

    # Did test pass?
    results["code"] = True
    results["msg"] = "success"
    return 

def thread_for_mm(args):
    mm.run()

# test function

def test_submitJob():
    # setting things up so test can run
    messageMonitorThread = threading.Thread(target=thread_for_mm, args=(1,), daemon=True)
    results = {"code":False, "msg":""}
    testThread = threading.Thread(target=submitJob, args=(results,))

    # test sequence 
    messageMonitorThread.start() 
    time.sleep(1) # time for the MessageMonitor to get up and running
    testThread.start()
    testThread.join() #waiting for the test to return

    #reporting results
    # debug (i'm sure there is pytest way to turn this on and off)
    #print(results)
    assert(results["code"] == True)
 
if __name__ == "__main__":
    print(config.API_URL)
    test_submitJob()


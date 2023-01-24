import requests
import time
import threading
from config import config
from message_monitor import MessageMonitor

global mm 
mm = MessageMonitor()
mm.clear_all_state()

# Utility functions
# TODO, job id is hard coded, needs to be flexible
def submitJob(results):

    payload = {"meta": {"metadata"}, "files":[{"file": "Mx, 10", "filename": "test", "name": "test", "description": "test"}]}
    r = requests.post(f'{config.API_URL}/job/', data=payload)
    print(r.text)
    if r.status_code != 200:
        results["code"] = False
        results["msg"] = "bad http code"
        return

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
    testThread.join() #waitig for the test to return

    #reporting results
    # debug (i'm sure there is pytest way to turn this on and off)
    #print(results)
    assert(results["code"] == True)
 
if __name__ == "__main__":
    print(config.API_URL)
    test_submitJob()


import requests
import time
import threading
from config import config
from message_monitor import MessageMonitor

global mm 
mm = MessageMonitor()
mm.clear_all_state()
macro_number = 0

def runMacro_two_hundred_one(results):
    macro_number = 201 
    r = requests.post(f'{config.API_URL}/macros/{macro_number}/run')
    if r.status_code != 200:
        results["code"] = False
        results["msg"] = "bad http code"
        return

    # Wait for running state
    print("waiting for running")
    time.sleep(0.5)
    success = mm.wait_for_state("running", 0.5)
    if success:
        print("macro 201 is running")
    else:
        results["code"] = False
        results["msg"] = "timed out while waiting for running"
        return

    # Wait for idle at end of file, signaling that the file completed
    print("waiting for idle, end of macro 201")
    time.sleep(5)
    success = mm.wait_for_state("idle", 10) 
    if success:
        print("macro 201 completed successfully")
    else:
        results["code"] = False
        results["msg"] = "timed out while waiting for idle"
        return

    results["code"] = True
    results["msg"] = "success"
    return 

def thread_for_mm(args):
    mm.run()

# test function
def test_runMacro_two_hundred_one():
    # setting things up so test can run
    messageMonitorThread = threading.Thread(target=thread_for_mm, args=(1,), daemon=True)
    results = {"code":False, "msg":""}
    testThread = threading.Thread(target=runMacro_two_hundred_one, args=(results,))

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
    test_runMacro_two_hundred_one()
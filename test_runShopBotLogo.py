import requests
import time
import threading
from config import config
from message_monitor import MessageMonitor

global mm 
mm = MessageMonitor()
mm.clear_all_state()

# Utility funcitons
def runShopBotLogo(results):
    r = requests.post(f'{config.API_URL}/jobs/{"job": "/fabmo-test/jobs/sample_shopbot_logo.sbp"}')
    if r.status_code != 200:
        results["code"] = False
        results["msg"] = "bad http code"
        return

    print("waiting for running")
    success = mm.wait_for_state("running", 10)
    if success:
        print("now running")
    else:
        results["code"] = False
        results["msg"] = "timed out while waiting for running"
        return 

    #print("waiting for idle")
    #success = mm.wait_for_state("idle", 600) 
    #if success:
    #    print("now idle")
    #else:
    #    results["code"] = False
    #    results["msg"] = "timed out while waiting for idle"
    #    return 

    results["code"] = True
    results["msg"] = "success"
    return 

def thread_for_mm(args):
    mm.run() 

# test function
def test_runShopBotLogo():
    # setting things up so test can run
    messageMonitorThread = threading.Thread(target=thread_for_mm, args=(1,), daemon=True)
    results = {"code":False, "msg":""}
    testThread = threading.Thread(target=runShopBotLogo, args=(results,))

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
    test_runShopBotLogo()
   
    

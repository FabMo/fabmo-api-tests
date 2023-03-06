import requests
import time
import threading
from config import config
from message_monitor import MessageMonitor

global mm 
mm = MessageMonitor()
mm.clear_all_state()

def thread_for_mm(args):
    mm.run() 


def main(results):
    print("pausing 1")
    r = requests.post(f'{config.API_URL}/pause')
    if r.status_code != 200:
            print("error")
            results["code"] = False
            results["msg"] = "bad http code"
            return
    print("waiting for paused")
    success = mm.wait_for_state("paused", 10)
    if success:
        print("now paused")
    else:
        results["code"] = False
        results["msg"] = "timed out while waiting for paused"
        return 

    time.sleep(3) 
    print("resuming 1")
    r = requests.post(f'{config.API_URL}/resume')
    if r.status_code != 200:
            results["code"] = False
            results["msg"] = "bad http code"
            return
    print(r.text)
    time.sleep(2)
    print("pausing 2")
    r = requests.post(f'{config.API_URL}/pause')
    if r.status_code != 200:
            results["code"] = False
            results["msg"] = "bad http code"
            return
    print(r.text)
    time.sleep(2)
    print("resuming 2")
    r = requests.post(f'{config.API_URL}/resume')
    if r.status_code != 200:
            results["code"] = False
            results["msg"] = "bad http code"
            return
    print(r.text)
    time.sleep(2)

    results["code"] = True
    results["msg"] = "success"
    return

# test function
def test_main():
    # setting things up so test can run
    messageMonitorThread = threading.Thread(target=thread_for_mm, args=(1,), daemon=True)
    results = {"code":False, "msg":""}
    testThread = threading.Thread(target=main, args=(results,))

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
    test_main()

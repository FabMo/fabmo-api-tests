# Test is not currently Passing!!

import time
import threading
import requests
from config import config
from message_monitor import MessageMonitor
from job import Job

mm = MessageMonitor()
mm.clear_all_state()
job = Job()

def quit_successfully(results):
    print("Test quit successfully")
    macro_number = 211
    r = requests.post(f'{config.API_URL}/macros/{macro_number}/run', timeout = config.TIMEOUT)
    if r.status_code != 200:
        results["code"] = False
        results["msg"] = "bad http code"
        return

    # Wait for running state
    print("waiting for running")
    time.sleep(1)
    success = mm.wait_for_state("running", 10)
    if success:
        print("macro 211 is running")
    else:
        results["code"] = False
        results["msg"] = "timed out while waiting for running"
        return

    # Wait for a short time, error usually occurs when quitting shortly
    # after starting the file
    time.sleep(3)

    job.pause_job()
    time.sleep(2)
    job.quit_job()

    # Wait for running after sending quit. Job should not run at all.
    print("waiting for running signaling a failed quit")
    time.sleep(1)
    failure = mm.wait_for_state("running", 10)
    if failure:
        results["code"] = False
        results["msg"] = "Job did not quit successfully"
        return
    else:
        print("Quit job successfully")

    results["code"] = True
    results["msg"] = "success"
    return

def thread_for_mm(args):
    mm.run()

# test function
def test_quit_successfully():
    # setting things up so test can run
    messageMonitorThread = threading.Thread(target=thread_for_mm, args=(1,), daemon=True)
    results = {"code":False, "msg":""}
    testThread = threading.Thread(target=quit_successfully, args=(results,))

    # test sequence
    messageMonitorThread.start()
    time.sleep(1) # time for the MessageMonitor to get up and running
    testThread.start()
    testThread.join() #waiting for the test to return

    #reporting results
    # debug (i'm sure there is pytest way to turn this on and off)
    #print(results)
    assert results["code"] is True

if __name__ == "__main__":
    print(config.API_URL)
    test_quit_successfully()

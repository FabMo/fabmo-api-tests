import requests
import time
import threading
from config import config
from message_monitor import MessageMonitor
from job import Job

global mm 
mm = MessageMonitor()
mm.clear_all_state()
job = Job()
job.clear_job_queue()

# Runs the job that is currently in the job manager queue
# Currently, It is hard coded to handle a file with a pause at the end
# Will improve later
def runNextJob(results):
    r = requests.post(f'{config.API_URL}/jobs/queue/run')
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

    print("wait for message at the end of the file, indicating completion")
    success = mm.wait_for_message("DONE with ShopBot Logo ... any key to continue", 600)
    if success:
        print("DONE with ShopBot Logo")
    else:
        results["code"] = False
        results["msg"] = "timed out while waiting for ShopBot Logo to complete"
        return 

    job.resume_job()

    print("waiting for idle")
    success = mm.wait_for_state("idle", 10)
    if success:
        print("now idle")
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
def test_runNextJob():
    # setting things up so test can run
    messageMonitorThread = threading.Thread(target=thread_for_mm, args=(1,), daemon=True)
    results = {"code":False, "msg":""}
    testThread = threading.Thread(target=runNextJob, args=(results,))

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
    test_runNextJob()

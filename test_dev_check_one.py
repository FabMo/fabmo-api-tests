import time
import threading
from config import config
from message_monitor import MessageMonitor
from job import Job
from get_requests import Get_Requests

get = Get_Requests()
global mm 
mm = MessageMonitor()
mm.clear_all_state()

def dev_check_one(results):
    job = Job()
    filename = "sample_shopbot_logo.sbp"
    name = "testing dev check one"
    description = "test_description"

    # Submit the job
    job.submit(filename, name, description)

    # Run the Job
    job.run_next_job_in_queue()

    print("waiting for running")
    success = mm.wait_for_state("running", 10)
    if success:
        print("now running")
    else:
        results["code"] = False
        results["msg"] = "timed out while waiting for running"
        return 

    print("waiting for pause at end of file")
    success = mm.wait_for_state("paused", 600)
    if success:
        print("now paused")
    else:
        results["code"] = False
        results["msg"] = "timed out while waiting for paused"
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

    # Did test pass?
    results["code"] = True
    results["msg"] = "success"
    return 

def thread_for_mm(args):
    mm.run()

# test function

def test_dev_check_one():
    # setting things up so test can run
    messageMonitorThread = threading.Thread(target=thread_for_mm, args=(1,), daemon=True)
    results = {"code":False, "msg":""}
    testThread = threading.Thread(target=dev_check_one, args=(results,))

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
    print("Testing dev_check_one")
    test_dev_check_one()

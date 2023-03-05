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

def submitJob(results):
    job = Job()
    jobs_in_queue = False
    filename = "test.sbp"
    name = "testing submitJob"
    description = "test_description"
    queue = get.getJobQueue()
    print(queue)
    ##Can check if the job queue is empty
    if queue and 'data' in queue:
            if 'jobs' in queue['data']:
                if 'pending' in queue['data']['jobs']:
                    if queue['data']['jobs']['pending'] == []:
                        print("Empty")
                    else:
                        print("Not empty")
    job.submit(filename, name, description)

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


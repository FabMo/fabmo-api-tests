import time
import threading
from config import config
from message_monitor import MessageMonitor
from job import Job

global mm
mm = MessageMonitor()
mm.clear_all_state()
job = Job()

def dev_check_two(results):
    filename = "syntax_error_reporting_with_undef.sbp"
    name = "testing dev check two"
    description = "test_description"

    # Submit the job
    job.submit(filename, name, description)

    # Run the Job
    job.run_next_job_in_queue()

    # First pause at the very start of file
    print("waiting for paused")
    success = mm.wait_for_state("paused", 10)
    if success:
        print("now paused")
    else:
        results["code"] = False
        results["msg"] = "timed out while waiting for running"
        return

    job.resume_job()

    print("wait for idle after error message")
    success = mm.wait_for_state("idle", 10)
    if success:
        print("Error message displayed")
    else:
        results["code"] = False
        results["msg"] = "timed out while waiting expected error message"
        return 

    # Did test pass?
    results["code"] = True
    results["msg"] = "success"
    return

def thread_for_mm(args):
    mm.run()

# test function

def test_dev_check_two():
    # setting things up so test can run
    messageMonitorThread = threading.Thread(target=thread_for_mm, args=(1,), daemon=True)
    results = {"code":False, "msg":""}
    testThread = threading.Thread(target=dev_check_two, args=(results,))

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
    print("Testing dev_check_two")
    test_dev_check_two()


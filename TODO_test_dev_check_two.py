#Test is not currently working!!
#The error message cannot be resolved by posting
#A resume, or a quit. Not sure how to proceed.

import time
import threading
from config import config
from message_monitor import MessageMonitor
from job import Job

mm = MessageMonitor()
mm.clear_all_state()
job = Job()
job.clear_queue()

def dev_check_two(results):
    print("Testing dev_check_two error reporting")

    filename = "dev_check_two_error_reporting.sbp"
    name = "testing dev check two"
    description = "testing dev check two"

    # Submit the job
    job.submit(filename, name, description)

    # Run the Job
    job.run_next_job_in_queue()

    print("wait for first message")
    time.sleep(3)

    job.resume()

    print("wait for error message")
    success = mm.wait_for_state("idle", 5)
    if success:
        print("Error message reached")
    else:
        results["code"] = False
        results["msg"] = "timed out while waiting for error message"
        return

    # print("waiting for idle")
    # success = mm.wait_for_state("idle", 10)
    # if success:
    #     print("now idle")
    # else:
    #     results["code"] = False
    #     results["msg"] = "timed out while waiting for idle"
    #     return

    # Did tests pass?
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
    print(results)
    assert results["code"] is True

if __name__ == "__main__":
    print(config.API_URL)
    print("Testing dev_check_two")
    test_dev_check_two()

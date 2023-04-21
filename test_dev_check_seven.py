import time
import threading
from config import config
from message_monitor import MessageMonitor
from job import Job

mm = MessageMonitor()
mm.clear_all_state()
job = Job()
job.clear_job_queue()

def dev_check_seven(results):
    print("Testing dev_check_seven file with macro 9")

    filename = "dev_check_seven_file_with_macro_9.sbp"
    name = "testing dev check seven"
    description = "testing dev check seven file with macro 9 post"

    # Submit the job
    job.submit(filename, name, description)

    # Run the Job
    job.run_next_job_in_queue()

    print("waiting for running")
    success = mm.wait_for_state("running", 10)
    if success:
        print("now running")
    else:
        print("timed out while waiting for running")
        results["code"] = False
        results["msg"] = "timed out while waiting for running"
        return

    print("waiting for idle")
    success = mm.wait_for_state("idle", 600)
    if success:
        print("now idle")
    else:
        print("timed out while waiting for idle")
        results["code"] = False
        results["msg"] = "timed out while waiting for idle"
        return

    # Did tests pass?
    results["code"] = True
    results["msg"] = "success"
    return

def thread_for_mm(args):
    mm.run()

# test function

def test_dev_check_seven():
    # setting things up so test can run
    messageMonitorThread = threading.Thread(target=thread_for_mm, args=(1,), daemon=True)
    results = {"code":False, "msg":""}
    testThread = threading.Thread(target=dev_check_seven, args=(results,))

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
    print("Testing dev_check_seven")
    test_dev_check_seven()

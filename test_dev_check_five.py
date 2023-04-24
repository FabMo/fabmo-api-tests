import time
import threading
from config import config
from message_monitor import MessageMonitor
from job import Job

mm = MessageMonitor()
mm.clear_all_state()

job = Job()
job.clear_job_queue()

def dev_check_five(results):
    print("Testing dev_check_five subs and loops")

    filename = "dev_check_five_subs_loops.sbp"
    name = "testing dev check five"
    description = "testing dev check five subs and loops"

    # Submit the job
    job.submit(filename, name, description)

    # Run the Job
    job.run_next_job_in_queue()

    # Wait for 5 minutes, then quit
    # TODO should add various pause and resumes test cases
    time.sleep(300)
    job.pause_job()
    time.sleep(2)
    job.quit_job()

    # Make sure we are in an expected state
    # If something went wrong, we will probably not be idle
    print("waiting for idle")
    success = mm.wait_for_state("idle", 10)
    if success:
        print("now idle")
    else:
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

def test_dev_check_five():
    # setting things up so test can run
    messageMonitorThread = threading.Thread(target=thread_for_mm, args=(1,), daemon=True)
    results = {"code":False, "msg":""}
    testThread = threading.Thread(target=dev_check_five, args=(results,))

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
    print("Testing dev_check_five")
    test_dev_check_five()
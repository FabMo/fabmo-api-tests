import time
import threading
from config import config
from message_monitor import MessageMonitor
from job import Job
from util import Util

mm = MessageMonitor()
mm.clear_all_state()

job = Job()
util = Util()

def dev_check_five(results):
    print("Testing dev_check_five subs and loops")

    filename = "dev_check_five_subs_loops.sbp"
    name = "testing dev check five"
    description = "testing dev check five subs and loops"

    # Submit the job
    job.submit(filename, name, description)

    # Run the Job
    job.run_next_job_in_queue()

    print("waiting for running")
    check = util.test_check(mm.wait_for_state("running", 10), "now running", "timed out while waiting for running")
    if check is False:
        return

    # Wait for a bit, then quit
    # TODO should add various pause and resumes test cases
    time.sleep(10)
    job.pause()
    time.sleep(2)
    job.quit()

    # Make sure we are in an expected state
    # If something went wrong, we will probably not be idle
    print("waiting for idle")
    check = util.test_check(mm.wait_for_state("idle", 10), "now idle", "timed out while waiting for idle")
    if check is False:
        return

    # Did tests pass?
    results["code"] = True
    return

def thread_for_mm(args):
    mm.run()

# test function

def test_dev_check_five():
    # setting things up so test can run
    messageMonitorThread = threading.Thread(target=thread_for_mm, args=(1,), daemon=True)
    results = {"code":False}
    testThread = threading.Thread(target=dev_check_five, args=(results,))

    # test sequence
    messageMonitorThread.start()
    time.sleep(1) # time for the MessageMonitor to get up and running
    testThread.start()
    testThread.join() #waiting for the test to return

    #reporting result
    assert results["code"] is True

if __name__ == "__main__":
    print(config.API_URL)
    print("Testing dev_check_five")
    test_dev_check_five()

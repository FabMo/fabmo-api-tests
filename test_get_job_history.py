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

def get_job_history(results):
    print("Testing get_job_history")
    print("First capture the current job count in history")
    history = job.get_job_history(0, 0)
    job_count_one = history['data']['jobs']['total_count']
    print(f"Job_count_one: {job_count_one}")

    print("Run two jobs then compare the job count, should be that much higher.")
    filename = "test.sbp"
    name = "testing submitJob"
    description = "test submit job"

    # Submit the job
    job.submit(filename, name, description)
    job.run_next_job_in_queue()
    check = util.test_check(mm.wait_for_state('running', 10), "Job 1 is running", "Job 1 failed to run")
    if check is False:
        return
    check = util.test_check(mm.wait_for_state('idle', 300), "Job 1 is idle", "Job 1 did not end idle.")
    if check is False:
        return

    filename = "test.sbp"
    name = "testing submitJob"
    description = "test submit job"

    # Submit the job
    job.submit(filename, name, description)
    job.run_next_job_in_queue()
    check = util.test_check(mm.wait_for_state('running', 10), "Job 2 is running", "Job 2 failed to run")
    if check is False:
        return
    check = util.test_check(mm.wait_for_state('idle', 300), "Job 1 is idle", "Job 1 did not end idle.")
    if check is False:
        return

    print("Compare the original count to the current count")
    history = job.get_job_history(0, 0)
    job_count_two = history['data']['jobs']['total_count']
    print(f"Job_count_two: {job_count_two}")

    check = util.test_check((job_count_one + 2) == job_count_two, "The difference is appropriate", "Job history not updating correctly")
    if check is False:
        return

    # Did tests pass?
    results["code"] = True
    return

def thread_for_mm(args):
    mm.run()

# test function

def test_get_job_history():
    # setting things up so test can run
    messageMonitorThread = threading.Thread(target=thread_for_mm, args=(1,), daemon=True)
    results = {"code":False}
    testThread = threading.Thread(target=get_job_history, args=(results,))

    # test sequence
    messageMonitorThread.start()
    time.sleep(1) # time for the MessageMonitor to get up and running
    testThread.start()
    testThread.join() #waiting for the test to return

    #reporting results
    assert results["code"] is True

if __name__ == "__main__":
    print(config.API_URL)
    print("Testing get_job_history")
    test_get_job_history()
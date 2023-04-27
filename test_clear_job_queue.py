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

def clear_job_queue(results):
    print("testing clear_job_queue")
    job.clear_queue()

    print("Check that the queue is cleared")
    check = util.test_check(job.check_if_queue_is_empty(), "Job queue is clear", "Job queue is NOT clear")
    if check is False:
        return

    json_object = job.get_queue()
    print(json_object)

    print("submit a job to the queue so that it can be cleared")
    # Submit the job
    job.submit()

    print("Check that the submitted job is in the queue")
    check = util.test_check(job.check_if_queue_is_not_empty(), "There are jobs in the queue", "Job queue clear and it should not be")
    if check is False:
        return

    json_object = job.get_queue()
    print(json_object)

    # Clean up for future tests by clearing the queue once more
    job.clear_queue()
    print("Check that the queue is cleared")
    check = util.test_check(job.check_if_queue_is_empty(), "Job queue is clear", "Job queue is NOT clear")
    if check is False:
        return

    json_object = job.get_queue()
    print(json_object)

    # Did test pass?
    results["code"] = True
    return

def thread_for_mm(args):
    mm.run()

# test function

def test_clear_job_queue():
    # setting things up so test can run
    messageMonitorThread = threading.Thread(target=thread_for_mm, args=(1,), daemon=True)
    results = {"code":False}
    testThread = threading.Thread(target=clear_job_queue, args=(results,))

    # test sequence
    messageMonitorThread.start()
    time.sleep(1) # time for the MessageMonitor to get up and running
    testThread.start()
    testThread.join() #waiting for the test to return

    #reporting results
    assert results["code"] is True

if __name__ == "__main__":
    print(config.API_URL)
    test_clear_job_queue()
    
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

def submit_job_by_id(results):
    print("testing submit_job_by_id")

    #job queue should be empty, but check just in case
    check = util.test_check(job.check_if_queue_is_empty(), "queue is empty", "Clearing job queue")
    if check is False:
        job.clear_queue()

    print("submitting job so that we have a known id to work with")
    job.submit()

    print("Retrieve _id from queue.")
    print("Check that it was retrieved.")
    _id = job.get_value_from_queue(0, '_id')
    check = util.test_check(_id is not None, "_id retrieved", "Something went wrong while retrieving _id")
    if check is False:
        return

    print("Retrieve job_id from queue for comparison later.")
    job_id = job.get_value_from_queue(0, 'file_id')
    check = util.test_check(job_id is not None, "file_id retrieved", "Something went wrong while retrieving file_id")
    if check is False:
        return

    print("submit new job using the obtained id")
    job.submit_by_id(_id)

    print("Retrieve job_id from new job and compare with the original")
    submitted_with_job_id = job.get_value_from_queue(0, 'file_id')
    check = util.test_check(submitted_with_job_id is not None, "Job submitted with a specific id retrieved", "Something went wrong while retrieving job with id")
    if check is False:
        return

    # Final cleanup
    job.clear_queue()
    check = util.test_check(job_id == submitted_with_job_id, "file_id that was retrieved from original, and job submitted with id are the same", "File_ids do not match, something went wrong")
    if check is False:
        return

    # Did test pass?
    results["code"] = True
    return

def thread_for_mm(args):
    mm.run()

# test function

def test_submit_job_by_id():
    # setting things up so test can run
    messageMonitorThread = threading.Thread(target=thread_for_mm, args=(1,), daemon=True)
    results = {"code":False}
    testThread = threading.Thread(target=submit_job_by_id, args=(results,))

    # test sequence
    messageMonitorThread.start()
    time.sleep(1) # time for the MessageMonitor to get up and running
    testThread.start()
    testThread.join() #waiting for the test to return

    #reporting results
    assert results["code"] is True

if __name__ == "__main__":
    print(config.API_URL)
    test_submit_job_by_id()

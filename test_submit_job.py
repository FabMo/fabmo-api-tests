import time
import threading
from config import config
from message_monitor import MessageMonitor
from job import Job

mm = MessageMonitor()
mm.clear_all_state()
job = Job()

def submit_job(results):
    print("testing submit_job")

    # Clear the job queue, test that it is cleared successfully
    # TODO use check if queue is clear function in job class
    job.clear_queue()
    queue = job.get_queue()
    if queue and 'data' in queue:
        if 'jobs' in queue['data']:
            if 'pending' in queue['data']['jobs']:
                if queue['data']['jobs']['pending'] == []:
                    print("Job queue is clear")
                else:
                    results["code"] = False
                    return

    filename = "test.sbp"
    name = "testing submitJob"
    description = "test submit job"

    # Submit the job
    job.submit(filename, name, description)

    # Check that the submitted job is in the queue
    queue = job.get_queue()
    if queue and 'data' in queue:
        if 'jobs' in queue['data']:
            if 'pending' in queue['data']['jobs']:
                if queue['data']['jobs']['pending'] == []:
                    results["code"] = False
                    return
                else:
                    print("Job submitted successfully")

    job.clear_queue()

    # Did test pass?
    results["code"] = True
    return

def thread_for_mm(args):
    mm.run()

# test function

def test_submit_job():
    # setting things up so test can run
    messageMonitorThread = threading.Thread(target=thread_for_mm, args=(1,), daemon=True)
    results = {"code":False}
    testThread = threading.Thread(target=submit_job, args=(results,))

    # test sequence
    messageMonitorThread.start()
    time.sleep(1) # time for the MessageMonitor to get up and running
    testThread.start()
    testThread.join() #waiting for the test to return

    #reporting results
    assert results["code"] is True

if __name__ == "__main__":
    print(config.API_URL)
    test_submit_job()

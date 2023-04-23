import time
import threading
from config import config
from message_monitor import MessageMonitor
from job import Job

mm = MessageMonitor()
mm.clear_all_state()
job = Job()
job.clear_job_queue()

def submit_job(results):
    print("testing submit_job")
    filename = "test.sbp"
    name = "testing submitJob"
    description = "test submit job"

    # Clear the job queue, test that it is cleared successfully
    job.clear_job_queue()
    queue = job.get_job_queue()
    if queue and 'data' in queue:
        if 'jobs' in queue['data']:
            if 'pending' in queue['data']['jobs']:
                if queue['data']['jobs']['pending'] == []:
                    print("Job queue is clear")
                else:
                    results["code"] = False
                    results["msg"] = "Job queue is NOT clear"
                    return

    # Submit the job
    job.submit(filename, name, description)

    # Check that the submitted job is in the queue
    queue = job.get_job_queue()
    if queue and 'data' in queue:
        if 'jobs' in queue['data']:
            if 'pending' in queue['data']['jobs']:
                if queue['data']['jobs']['pending'] == []:
                    results["code"] = False
                    results["msg"] = "Job not submmited successfully"
                    return
                else:
                    print("Job submitted successfully")

    job.clear_job_queue()

    # Did test pass?
    results["code"] = True
    results["msg"] = "success"
    return

def thread_for_mm(args):
    mm.run()

# test function

def test_submit_job():
    # setting things up so test can run
    messageMonitorThread = threading.Thread(target=thread_for_mm, args=(1,), daemon=True)
    results = {"code":False, "msg":""}
    testThread = threading.Thread(target=submit_job, args=(results,))

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
    test_submit_job()

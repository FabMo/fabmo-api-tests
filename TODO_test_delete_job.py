import time
import threading
from config import config
from message_monitor import MessageMonitor
from job import Job

mm = MessageMonitor()
mm.clear_all_state()
job = Job()

def delete_job(results):
    print("testing delete_job")
    job_to_delete = 154

    # Submit the job
    job.delete(job_to_delete)

    # Did test pass?
    results["code"] = True
    return

def thread_for_mm(args):
    mm.run()

# test function

def test_delete_job():
    # setting things up so test can run
    messageMonitorThread = threading.Thread(target=thread_for_mm, args=(1,), daemon=True)
    results = {"code":False}
    testThread = threading.Thread(target=delete_job, args=(results,))

    # test sequence
    messageMonitorThread.start()
    time.sleep(1) # time for the MessageMonitor to get up and running
    testThread.start()
    testThread.join() #waiting for the test to return

    #reporting results
    assert results["code"] is True

if __name__ == "__main__":
    print(config.API_URL)
    test_delete_job()

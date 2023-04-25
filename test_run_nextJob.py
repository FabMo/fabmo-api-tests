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

# Runs the job that is currently in the job manager queue
def run_next_job(results):
    filename = "sample_shopbot_logo.sbp"
    name = "testing dev check one"
    description = "test_description"
    job.submit(filename, name, description)

    print("Test run next job currently in queue")
    job.run_next_job_in_queue()

    print("waiting for running")
    check = util.test_dialog(mm.wait_for_state("running", 10), "now running", "timed out while waiting for running")
    if check is False:
        return

    print("wait for message at the end of the file, indicating completion")
    check = util.test_dialog(mm.wait_for_message("DONE with ShopBot Logo ... any key to continue", 600), "DONE with ShopBot Logo", "timed out while waiting for ShopBot Logo to complete")
    if check is False:
        return

    job.resume()

    print("waiting for idle")
    check = util.test_dialog(mm.wait_for_state("idle", 10), "now idle", "timed out while waiting for idle")
    if check is False:
        return

    results["code"] = True
    return

def thread_for_mm(args):
    mm.run()

# test function
def test_run_next_job():
    # setting things up so test can run
    messageMonitorThread = threading.Thread(target=thread_for_mm, args=(1,), daemon=True)
    results = {"code":False}
    testThread = threading.Thread(target=run_next_job, args=(results,))

    # test sequence
    messageMonitorThread.start()
    time.sleep(1) # time for the MessageMonitor to get up and running
    testThread.start()
    testThread.join() #waiting for the test to return

    #reporting results
    assert results["code"] is True

if __name__ == "__main__":
    print(config.API_URL)
    test_run_next_job()

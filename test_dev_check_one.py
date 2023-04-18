import time
import threading
from config import config
from message_monitor import MessageMonitor
from job import Job

global mm
mm = MessageMonitor()
mm.clear_all_state()
job = Job()
job.clear_job_queue()

# timeout is how long to wait for the expected state before giving up
# interval is how long to sleep between pause and resume
# repetitions dictates how many times a pause and resume will occur
def pause_resume(timeout, interval, repetitions):
    for x in range(repetitions):
        print(f"pausing {x}")
        job.pause_job()
        print("waiting for paused")
        success = mm.wait_for_state("paused", timeout)
        if success:
            print("now paused")
        else:
            results["code"] = False
            results["msg"] = "timed out while waiting for paused"
            return 
        time.sleep(interval)
    
        print(f"resuming {x}")
        job.resume_job()
        print("waiting for resume")
        success = mm.wait_for_state("running", timeout)
        if success:
            print("now running")
        else:
            results["code"] = False
            results["msg"] = "timed out while waiting for running"
            return
        time.sleep(interval)


def dev_check_one(results):
    ###########################################################################
    #Run file to the end without pausing or quitting
    ###########################################################################
    filename = "sample_shopbot_logo.sbp"
    name = "testing dev check one"
    description = "test_description"

    # Submit the job
    job.submit(filename, name, description)

    # Run the Job
    job.run_next_job_in_queue()

    print("waiting for running")
    success = mm.wait_for_state("running", 10)
    if success:
        print("now running")
    else:
        results["code"] = False
        results["msg"] = "timed out while waiting for running"
        return 

    print("wait for message at the end of the file, indicating completion")
    success = mm.wait_for_message("DONE with ShopBot Logo ... any key to continue", 600)
    if success:
        print("DONE with ShopBot Logo")
    else:
        results["code"] = False
        results["msg"] = "timed out while waiting for ShopBot Logo to complete"
        return 

    job.resume_job()

    print("waiting for idle")
    success = mm.wait_for_state("idle", 10)
    if success:
        print("now idle")
    else:
        results["code"] = False
        results["msg"] = "timed out while waiting for idle"
        return 
    ###########################################################################

    ###########################################################################
    #Run file, pause and quit after a few seconds
    ###########################################################################
    filename = "sample_shopbot_logo.sbp"
    name = "testing dev check one"
    description = "test_description"

    # Submit the job
    job.submit(filename, name, description)

    # Run the Job
    job.run_next_job_in_queue()

    print("waiting for running")
    success = mm.wait_for_state("running", 10)
    if success:
        print("now running")
    else:
        results["code"] = False
        results["msg"] = "timed out while waiting for running"
        return 

    job.pause_job()
    time.sleep(2)
    job.quit_job()

    print("wait for idle, indicating a successful quit")
    success = mm.wait_for_state("idle", 10)
    if success:
        print("Quit job successfully")
    else:
        results["code"] = False
        results["msg"] = "timed out while waiting for ShopBot Logo to quit"
        return 
    ###########################################################################

    ###########################################################################
    #Run file, pausing and resuming every three seconds
    ###########################################################################
    filename = "sample_shopbot_logo.sbp"
    name = "testing dev check one"
    description = "test_description"

    # Submit the job
    job.submit(filename, name, description)

    # Run the Job
    job.run_next_job_in_queue()

    print("waiting for running")
    success = mm.wait_for_state("running", 10)
    if success:
        print("now running")
    else:
        results["code"] = False
        results["msg"] = "timed out while waiting for running"
        return 

    pause_resume(10, 3, 5)

    print("wait for message at the end of the file, indicating completion")
    success = mm.wait_for_message("DONE with ShopBot Logo ... any key to continue", 600)
    if success:
        print("DONE with ShopBot Logo")
    else:
        results["code"] = False
        results["msg"] = "timed out while waiting for ShopBot Logo to complete"
        return 

    job.resume_job()

    print("waiting for idle")
    success = mm.wait_for_state("idle", 10)
    if success:
        print("now idle")
    else:
        results["code"] = False
        results["msg"] = "timed out while waiting for idle"
        return 
    ###########################################################################

    # Did tests pass?
    results["code"] = True
    results["msg"] = "success"
    return 

def thread_for_mm(args):
    mm.run()

# test function

def test_dev_check_one():
    # setting things up so test can run
    messageMonitorThread = threading.Thread(target=thread_for_mm, args=(1,), daemon=True)
    results = {"code":False, "msg":""}
    testThread = threading.Thread(target=dev_check_one, args=(results,))

    # test sequence 
    messageMonitorThread.start() 
    time.sleep(1) # time for the MessageMonitor to get up and running
    testThread.start()
    testThread.join() #waiting for the test to return

    #reporting results
    # debug (i'm sure there is pytest way to turn this on and off)
    #print(results)
    assert(results["code"] == True)
 
if __name__ == "__main__":
    print(config.API_URL)
    print("Testing dev_check_one")
    test_dev_check_one()


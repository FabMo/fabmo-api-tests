# Test is not currently Passing!!
# Fabmo-engine issue 970
# https://github.com/FabMo/FabMo-Engine/issues/970

import time
import threading
from config import config
from message_monitor import MessageMonitor
from job import Job
from macro import Macro
from util import Util

mm = MessageMonitor()
mm.clear_all_state()
job = Job()
macro = Macro()
util = Util()

def quit_successfully(results):
    print("Test quit successfully")
    macro_number = 211
    macro.run_macro(macro_number)

    # Wait for running state
    print("waiting for running")
    check = util.test_check(mm.wait_for_state("running", 10), "now running", "timed out while waiting for running")
    if check is False:
        return

    # Wait for a short time, error usually occurs when quitting shortly
    # after starting the file
    time.sleep(3)

    job.pause()
    time.sleep(2)
    job.quit()

    # Wait for running after sending quit. Job should not run at all.
    # If the check evaluates to true, that means that the job was running after
    # sending a quit. Hence the test should fail.
    print("waiting for running signaling a failed quit")
    check = util.test_check(mm.wait_for_state("running", 10), "now running", "timed out while waiting for running")
    if check is True:
        return

    results["code"] = True
    return

def thread_for_mm(args):
    mm.run()

# test function
def test_quit_successfully():
    # setting things up so test can run
    messageMonitorThread = threading.Thread(target=thread_for_mm, args=(1,), daemon=True)
    results = {"code":False}
    testThread = threading.Thread(target=quit_successfully, args=(results,))

    # test sequence
    messageMonitorThread.start()
    time.sleep(1) # time for the MessageMonitor to get up and running
    testThread.start()
    testThread.join() #waiting for the test to return

    #reporting results
    assert results["code"] is True

if __name__ == "__main__":
    print(config.API_URL)
    test_quit_successfully()

#TODO, this test runs to fast to test it by observing the fabmo state
# A better way to test it may be to edit one of the config system
# variables that macro 201 sets, then run 201, then observe that the change took place

import time
import threading
from config import config
from message_monitor import MessageMonitor
from macro import Macro
from util import Util

mm = MessageMonitor()
mm.clear_all_state()

macro = Macro()
util = Util()

def run_macro_two_hundred_one(results):
    print("Test macro 201")
    macro_number = 201
    macro.run_macro(macro_number)

    # Wait for running state
    check = util.test_dialog(mm.wait_for_state("running", 10), "now running", "timed out while waiting for running")
    if check is False:
        return

    # Wait for idle at end of file, signaling that the file completed
    check = util.test_dialog(mm.wait_for_state("idle", 10), "now idle", "timed out while waiting for idle")
    if check is False:
        return

    results["code"] = True
    return

def thread_for_mm(args):
    mm.run()

# test function
def test_run_macro_two_hundred_one():
    # setting things up so test can run
    messageMonitorThread = threading.Thread(target=thread_for_mm, args=(1,), daemon=True)
    results = {"code":False}
    testThread = threading.Thread(target=run_macro_two_hundred_one, args=(results,))

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
    test_run_macro_two_hundred_one()

import time
import threading
from config import config
from message_monitor import MessageMonitor
from macro import Macro

mm = MessageMonitor()
mm.clear_all_state()

macro = Macro()

def run_macro_two_hundred_one(results):
    print("Test macro 201")
    macro_number = 201
    macro.run_macro(macro_number)

    # Wait for running state
    print("waiting for running")
    success = mm.wait_for_state("running", 5)
    if success:
        print("macro 201 is running")
    else:
        results["code"] = False
        results["msg"] = "timed out while waiting for running"
        return

    # Wait for idle at end of file, signaling that the file completed
    print("waiting for idle, end of macro 201")
    success = mm.wait_for_state("idle", 10)
    if success:
        print("macro 201 completed successfully")
    else:
        results["code"] = False
        results["msg"] = "timed out while waiting for idle"
        return

    results["code"] = True
    results["msg"] = "success"
    return

def thread_for_mm(args):
    mm.run()

# test function
def test_run_macro_two_hundred_one():
    # setting things up so test can run
    messageMonitorThread = threading.Thread(target=thread_for_mm, args=(1,), daemon=True)
    results = {"code":False, "msg":""}
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

import time
import threading
from config import config
from message_monitor import MessageMonitor
from macro import Macro

mm = MessageMonitor()
mm.clear_all_state()

macro = Macro()

def run_macro_five(results):
    print("Test macro 5")
    macro_number = 5
    # Make request to run macro 5
    macro.run_macro(macro_number)

    print("Waiting for output 1, spindle on")
    time.sleep(1)
    success = mm.wait_for_output(1, 4)
    if success:
        print("output 1 is on")
    else:
        results["code"] = False
        results["msg"] = "timed out while waiting for output"
        return

    # Wait for idle at end of file, signaling that the file completed
    print("waiting for idle, end of macro 5")
    time.sleep(1)
    success = mm.wait_for_state("idle", 150)
    if success:
        print("macro 5 completed successfully")
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
def test_run_macro_five():
    # setting things up so test can run
    messageMonitorThread = threading.Thread(target=thread_for_mm, args=(1,), daemon=True)
    results = {"code":False, "msg":""}
    testThread = threading.Thread(target=run_macro_five, args=(results,))

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
    test_run_macro_five()

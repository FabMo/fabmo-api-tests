import time
import threading
from config import config
from message_monitor import MessageMonitor
from job import Job
from macro import Macro
from util import Util
from get_requests import Get_Requests

job = Job()
mm = MessageMonitor()
mm.clear_all_state()
macro = Macro()
util = Util()
get = Get_Requests()

# This job runs too quickly to observe state changes
def run_macro_two_hundred_one(results):
    print("Test macro 201")
    print("First run a modified macro 201 and check that it changes a variable ($sb_homeOff_X to 1)")
    filename = "macro_201_modified.sbp"
    job.submit(filename)
    job.run_next_job_in_queue()

    time.sleep(2)

    print("Check the config to see that the value has changed to 1")
    check_config = get.config()
    check = util.test_check(check_config['data']['config']['opensbp']['variables']['SB_HOMEOFF_X'] == 1, "The config has been changed", "The config appears unchanged")
    if check is False:
        print(f"Value is not correct {check_config['data']['config']['opensbp']['variables']['SB_HOMEOFF_X']}")
        return
    print(f"changed to {check_config['data']['config']['opensbp']['variables']['SB_HOMEOFF_X']}")

    time.sleep(2)

    print("Now run the original macro 201 which will change the value back to its proper value, 0.5")
    macro_number = 201
    macro.run_macro(macro_number)

    time.sleep(2)

    check_config = get.config()
    check = util.test_check(check_config['data']['config']['opensbp']['variables']['SB_HOMEOFF_X'] == 0.5, "The config has been changed back", "The config has not been changed back")
    if check is False:
        print(f"Value is not correct {check_config['data']['config']['opensbp']['variables']['SB_HOMEOFF_X']}")
        return
    print(f"changed to {check_config['data']['config']['opensbp']['variables']['SB_HOMEOFF_X']}")

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
    assert results["code"] is True

if __name__ == "__main__":
    print(config.API_URL)
    test_run_macro_two_hundred_one()

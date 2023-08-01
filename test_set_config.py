import time
import threading
from config import config
from message_monitor import MessageMonitor
from fabmo_info import Fabmo_Info
from util import Util

mm = MessageMonitor()
mm.clear_all_state()

info = Fabmo_Info()
util = Util()

def set_config(results):
    print("Testing set fabmo config using test temp variable")
    print("Clear test variable if it already exists, if not it will be initialized to 0")
    test_var = {
                "opensbp": {
                    "tempVariables": {"TEST": 0}
                }
            }
    info.set_config(test_var)

    print("Get the config and check that test variable is 0")
    fabmo_config = info.get_config()
    check = util.test_check(fabmo_config['data']['config']['opensbp']['tempVariables'].get("TEST") == 0, "Test var is 0","Test var is not 0")
    if check is False:
        print(f"The test var returned {fabmo_config['data']['config']['opensbp']['tempVariables'].get('TEST')}")
        return

    print("Set test variable to 1")
    test_var = {
                "opensbp": {
                    "tempVariables": {"TEST": 1}
                }
            }
    info.set_config(test_var)

    print("Parse the config for the test variable, this time it should be 1")
    fabmo_config = info.get_config()
    check = util.test_check(fabmo_config['data']['config']['opensbp']['tempVariables'].get("TEST") == 1, "Test var is 1","Test var is not 1")
    if check is False:
        return

    print("Cleanup")
    test_var = {
                "opensbp": {
                    "tempVariables": {"TEST": 0}
                }
            }
    info.set_config(test_var)

    print("Get the config and check that test var is 0")
    fabmo_config = info.get_config()
    check = util.test_check(fabmo_config['data']['config']['opensbp']['tempVariables'].get("TEST") == 0, "Test var is 0","Test var is not 0")
    if check is False:
        return

    # Did tests pass?
    results["code"] = True
    return

def thread_for_mm(args):
    mm.run()

# test function

def test_set_config():
    # setting things up so test can run
    messageMonitorThread = threading.Thread(target=thread_for_mm, args=(1,), daemon=True)
    results = {"code":False}
    testThread = threading.Thread(target=set_config, args=(results,))

    # test sequence
    messageMonitorThread.start()
    time.sleep(1) # time for the MessageMonitor to get up and running
    testThread.start()
    testThread.join() #waiting for the test to return

    #reporting results
    assert results["code"] is True

if __name__ == "__main__":
    print(config.API_URL)
    print("Testing set_config")
    test_set_config()

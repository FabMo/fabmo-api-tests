# TODO Is online returns false even when we are on a network. Why is this?
import time
import threading
from config import config
from message_monitor import MessageMonitor
from network import Network
from util import Util

mm = MessageMonitor()
mm.clear_all_state()

network = Network()
util = Util()

def get_is_online(results):
    is_online = network.get_is_online()
    print(is_online['data']['online'])
    check = util.test_check(is_online['data']['online'] is False, "is_online is true", "is_online is false.")
    if check is False:
        return

    # Did tests pass?
    results["code"] = True
    return

def thread_for_mm(args):
    mm.run()

# test function

def test_get_is_online():
    # setting things up so test can run
    messageMonitorThread = threading.Thread(target=thread_for_mm, args=(1,), daemon=True)
    results = {"code":False}
    testThread = threading.Thread(target=get_is_online, args=(results,))

    # test sequence
    messageMonitorThread.start()
    time.sleep(1) # time for the MessageMonitor to get up and running
    testThread.start()
    testThread.join() #waiting for the test to return

    #reporting results
    assert results["code"] is True

if __name__ == "__main__":
    print(config.API_URL)
    print("Testing get_is_online")
    test_get_is_online()

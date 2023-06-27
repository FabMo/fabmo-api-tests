import time
import threading
from config import config
from message_monitor import MessageMonitor
from user import User
from util import Util

mm = MessageMonitor()
mm.clear_all_state()

user = User()
util = Util()

def get_users(results):
    print("Test get users, if the request does not return none, the test passes")
    check = util.test_check(user.get_users() is not None, "All users were retrieved", "Unable to get users")
    if check is False:
        return

    # Did tests pass?
    results["code"] = True
    return

def thread_for_mm(args):
    mm.run()

# test function

def test_get_users():
    # setting things up so test can run
    messageMonitorThread = threading.Thread(target=thread_for_mm, args=(1,), daemon=True)
    results = {"code":False}
    testThread = threading.Thread(target=get_users, args=(results,))

    # test sequence
    messageMonitorThread.start()
    time.sleep(1) # time for the MessageMonitor to get up and running
    testThread.start()
    testThread.join() #waiting for the test to return

    #reporting results
    assert results["code"] is True

if __name__ == "__main__":
    print(config.API_URL)
    print("Testing get_users")
    test_get_users()

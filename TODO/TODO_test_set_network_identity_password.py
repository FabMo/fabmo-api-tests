# Not working correctly yet
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

def set_network_identity_password(results):

    print("Set the password to something new.")
    set_identity = {'password' : "test12345"}
    network.set_network_identity(set_identity)

    # Did tests pass?
    results["code"] = True
    return

def thread_for_mm(args):
    mm.run()

# test function

def test_set_network_identity_password():
    # setting things up so test can run
    messageMonitorThread = threading.Thread(target=thread_for_mm, args=(1,), daemon=True)
    results = {"code":False}
    testThread = threading.Thread(target=set_network_identity_password, args=(results,))

    # test sequence
    messageMonitorThread.start()
    time.sleep(1) # time for the MessageMonitor to get up and running
    testThread.start()
    testThread.join() #waiting for the test to return

    #reporting results
    assert results["code"] is True

if __name__ == "__main__":
    print(config.API_URL)
    print("Testing set_network_identity_password")
    test_set_network_identity_password()

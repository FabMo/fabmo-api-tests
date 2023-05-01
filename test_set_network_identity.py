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

def set_network_identity(results):
    original_network_id = network.get_network_identity()
    print(f"First retrieve the original network id: {original_network_id}")
    check = util.test_check(original_network_id['data']['name'] is not None, "Retrieved network id", "Unable to retrieve network id")
    if check is False:
        return
    print(f"Original network id: {original_network_id['data']['name']}")

    print("Now set the id to something new.")
    set_identity = {'name' : "test_network_id"}
    network.set_network_identity(set_identity)

    print("Check id again to make sure the change took.")
    new_network_id = network.get_network_identity()
    print(new_network_id)
    check = util.test_check(new_network_id['data']['name'] == "test_network_id", "Set network id successfully", "Unable to set network id")
    if check is False:
        return

    # Did tests pass?
    results["code"] = True
    return

def thread_for_mm(args):
    mm.run()

# test function

def test_set_network_identity():
    # setting things up so test can run
    messageMonitorThread = threading.Thread(target=thread_for_mm, args=(1,), daemon=True)
    results = {"code":False}
    testThread = threading.Thread(target=set_network_identity, args=(results,))

    # test sequence
    messageMonitorThread.start()
    time.sleep(1) # time for the MessageMonitor to get up and running
    testThread.start()
    testThread.join() #waiting for the test to return

    #reporting results
    assert results["code"] is True

if __name__ == "__main__":
    print(config.API_URL)
    print("Testing set_network_identity")
    test_set_network_identity()

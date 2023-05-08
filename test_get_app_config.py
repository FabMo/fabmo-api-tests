import time
import threading
from config import config
from message_monitor import MessageMonitor
from app import App
from util import Util

mm = MessageMonitor()
mm.clear_all_state()

app = App()
util = Util()

def get_app_config(results):
    app_config_to_get = 'editor'
    print("Test get app config, get from editor since it is a built in app")
    check = util.test_check(app.get_app_config(app_config_to_get) is not None, "Got the app config", "Unable to get app config")
    if check is False:
        return

    # Did tests pass?
    results["code"] = True
    return

def thread_for_mm(args):
    mm.run()

# test function

def test_get_app_config():
    # setting things up so test can run
    messageMonitorThread = threading.Thread(target=thread_for_mm, args=(1,), daemon=True)
    results = {"code":False}
    testThread = threading.Thread(target=get_app_config, args=(results,))

    # test sequence
    messageMonitorThread.start()
    time.sleep(1) # time for the MessageMonitor to get up and running
    testThread.start()
    testThread.join() #waiting for the test to return

    #reporting results
    assert results["code"] is True

if __name__ == "__main__":
    print(config.API_URL)
    print("Testing get_app_config")
    test_get_app_config()

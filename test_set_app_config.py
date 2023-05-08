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

def set_app_config(results):
    print("Test set app config")
    test_app = 'fabmo-sb4'
    test_app_filename = 'fabmo-sb4.fma'
    print("First check if the app already exists, if it does delete it, then resubmit it to ensure a clean config")
    check = util.test_check(app.check_for_app(test_app), "App already exists deleting it", "App does not exist, free to submit")
    if check is True:
        app.delete(test_app)
    app.submit(test_app_filename)

    time.sleep(2)

    print("Now check if app config is clean")
    app_config = app.get_app_config('fabmo-sb4')
    print(app_config)
    check = util.test_check(app_config['data']['config'] == {}, "App config is clean", "App config is not clean and it should be")
    if check is False:
        return

    print("Submit a change to the config for testing")
    config_change = {
        "config":
            {
                "test": "testing"
            }
    }
    app.set_app_config(test_app, config_change)
    app_config = app.get_app_config(test_app)
    print(app_config)
    check = util.test_check(app_config['data']['config']['test'] == 'testing', "Got the app config change", "Unable to get app config change")
    if check is False:
        return

    print("Cleanup the config")
    config_change = {"config":{}}
    app.set_app_config(test_app, config_change)
    app_config = app.get_app_config(test_app)
    print(app_config)
    check = util.test_check(app_config['data']['config'] == {}, "Cleaned up app config", "App config not cleaned up")
    if check is False:
        return

    # Did tests pass?
    results["code"] = True
    return

def thread_for_mm(args):
    mm.run()

# test function

def test_set_app_config():
    # setting things up so test can run
    messageMonitorThread = threading.Thread(target=thread_for_mm, args=(1,), daemon=True)
    results = {"code":False}
    testThread = threading.Thread(target=set_app_config, args=(results,))

    # test sequence
    messageMonitorThread.start()
    time.sleep(1) # time for the MessageMonitor to get up and running
    testThread.start()
    testThread.join() #waiting for the test to return

    #reporting results
    assert results["code"] is True

if __name__ == "__main__":
    print(config.API_URL)
    print("Testing set_app_config")
    test_set_app_config()

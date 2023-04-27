# This test is identical to test_delete_app, keeping both for coverage
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

def submit_app(results):
    print("testing submit_app")
    app_to_submit = "fabmo-dev-tests-app.fma"
    # If this check is false we will move on with submitting the app, if it returns true we will delete the app, then move on
    check = util.test_dialog(app.check_for_app('fabmo-dev-tests-app'), "The app exists in the list", "The app does not exist in the list")
    if check is True:
        print("App is already in the list, delete it")
        app.delete('fabmo-dev-tests-app')
        time.sleep(3)

    print("App is not in the list, submit it")
    app.submit(app_to_submit)
    time.sleep(3)
    check = util.test_dialog(app.check_for_app('fabmo-dev-tests-app'), "The app exists in the list", "The app does not exist in the list")
    if check is False:
        return

    print("Delete the app for cleanup purposes")
    app.delete('fabmo-dev-tests-app')
    time.sleep(3)
    check = util.test_dialog(app.check_for_app('fabmo-dev-tests-app'), "The app exists in the list", "The app has been cleared for cleanup")
    if check is True:
        print("App still in the list after deleting it")
        return

    # Did test pass?
    results["code"] = True
    return

def thread_for_mm(args):
    mm.run()

# test function

def test_submit_app():
    # setting things up so test can run
    messageMonitorThread = threading.Thread(target=thread_for_mm, args=(1,), daemon=True)
    results = {"code":False}
    testThread = threading.Thread(target=submit_app, args=(results,))

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
    test_submit_app()

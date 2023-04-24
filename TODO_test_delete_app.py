import time
import threading
from config import config
from message_monitor import MessageMonitor
from app import App

mm = MessageMonitor()
mm.clear_all_state()
app = App()

def delete_app(results):
    print("testing delete_app")
    app_to_delete = "fabmo-dev-tests-app"

    # Submit the app
    app.delete(app_to_delete)

    # Did test pass?
    results["code"] = True
    results["msg"] = "success"
    return

def thread_for_mm(args):
    mm.run()

# test function

def test_delete_app():
    # setting things up so test can run
    messageMonitorThread = threading.Thread(target=thread_for_mm, args=(1,), daemon=True)
    results = {"code":False, "msg":""}
    testThread = threading.Thread(target=delete_app, args=(results,))

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
    test_delete_app()

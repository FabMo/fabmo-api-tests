import time
import threading
from config import config
from message_monitor import MessageMonitor
from util import Util
from firmware import Firmware
from get_requests import Get_Requests

mm = MessageMonitor()
mm.clear_all_state()
util = Util()
firmware = Firmware()
get = Get_Requests()

def submit_firmware(results):
    print("testing submit_firmware")
    firmware_to_submit = "g2core_101_57_44.bin"

    # Submit the firmware
    firmware.submit(firmware_to_submit)
    time.sleep(120)
    get_firmware_version = get.info()
    check = util.test_check(get_firmware_version['data']['info']['firmware']['version'] == '101.57.44', "Firmware version matches what was submitted", "Firmware version is incorrect")
    if check is False:
        return

    print("Repeat the test with the most recent firmware.")
    firmware_to_submit = "g2core_101_57_45.bin"

    # Submit the firmware
    firmware.submit(firmware_to_submit)
    time.sleep(120)
    get_firmware_version = get.info()
    check = util.test_check(get_firmware_version['data']['info']['firmware']['version'] == '101.57.45-dirty', "Firmware version matches what was submitted", "Firmware version is incorrect")
    if check is False:
        return

    # Did test pass?
    results["code"] = True
    return

def thread_for_mm(args):
    mm.run()

# test function

def test_submit_firmware():
    # setting things up so test can run
    messageMonitorThread = threading.Thread(target=thread_for_mm, args=(1,), daemon=True)
    results = {"code":False}
    testThread = threading.Thread(target=submit_firmware, args=(results,))

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
    test_submit_firmware()

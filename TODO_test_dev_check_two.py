# Error message dialog can be resolved with selenium
# I am having trouble deciding where and how to run selenium
# Having trouble making it cross platform
# Google chrome is not a good fit for the raspberry pi but it
# is the only browser I have been successful with

import time
import threading
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from config import config
from message_monitor import MessageMonitor
from job import Job

mm = MessageMonitor()
mm.clear_all_state()
job = Job()

def dev_check_two(results):
    print("Testing dev_check_two error reporting")

    DRIVER_LOCATION = "/usr/bin/chromedriver"
    BINARY_LOCATION = "/usr/bin/google-chrome"

    # start selenium
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.binary_location = BINARY_LOCATION
    service = Service(executable_path = DRIVER_LOCATION)
    driver = webdriver.Chrome(service=service)
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(config.API_URL)
    username_box = driver.find_element(By.NAME, "username")
    username_box.send_keys("admin")
    password_box = driver.find_element(By.NAME, "password")
    password_box.send_keys("go2fabmo")
    time.sleep(3)
    login_button = driver.find_element(By.CLASS_NAME, "button")
    login_button.click()
    time.sleep(3)

    filename = "dev_check_two_error_reporting.sbp"
    name = "testing dev check two"
    description = "testing dev check two"

    # Submit the job
    job.submit(filename, name, description)

    # Run the Job
    job.run_next_job_in_queue()

    print("wait for first message")
    time.sleep(3)

    job.resume()

    print("wait for error message")
    success = mm.wait_for_state("idle", 5)
    if success:
        print("Error message reached")
    else:
        results["code"] = False
        return

    button = driver.find_element(By.CLASS_NAME, "modalCancel")
    button.click()

    time.sleep(2)

    # Did tests pass?
    results["code"] = True
    # # close browser and quit driver
    driver.close()
    driver.quit()
    return

def thread_for_mm(args):
    mm.run()

# test function

def test_dev_check_two():
    # setting things up so test can run
    messageMonitorThread = threading.Thread(target=thread_for_mm, args=(1,), daemon=True)
    results = {"code":False}
    testThread = threading.Thread(target=dev_check_two, args=(results,))

    # test sequence
    messageMonitorThread.start()
    time.sleep(1) # time for the MessageMonitor to get up and running
    testThread.start()
    testThread.join() #waiting for the test to return

    #reporting results
    assert results["code"] is True

if __name__ == "__main__":
    print(config.API_URL)
    print("Testing dev_check_two")
    test_dev_check_two()

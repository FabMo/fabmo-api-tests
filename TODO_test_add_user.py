# Adding a user by posting to the api endpoint does not seem
# to function the same as adding a user in the UI
# In short, adding a user in the UI works, requesting through a post does not
# import time
# import threading
# from config import config
# from message_monitor import MessageMonitor
# from user import User

# mm = MessageMonitor()
# mm.clear_all_state()
# user = User()

# def add_user(results):
#     print("testing add_user")
#     new_user = {
#                 "username":"testingg",
#                 "password":"test123"
#                 }

#     # Submit the app
#     user.add_user(new_user)

#     # Did test pass?
#     results["code"] = True
#     results["msg"] = "success"
#     return

# def thread_for_mm(args):
#     mm.run()

# # test function

# def test_add_user():
#     # setting things up so test can run
#     messageMonitorThread = threading.Thread(target=thread_for_mm, args=(1,), daemon=True)
#     results = {"code":False, "msg":""}
#     testThread = threading.Thread(target=add_user, args=(results,))

#     # test sequence
#     messageMonitorThread.start()
#     time.sleep(1) # time for the MessageMonitor to get up and running
#     testThread.start()
#     testThread.join() #waiting for the test to return

#     #reporting results
#     # debug (i'm sure there is pytest way to turn this on and off)
#     print(results)
#     assert results["code"] is True

# if __name__ == "__main__":
#     print(config.API_URL)
#     test_add_user()
    
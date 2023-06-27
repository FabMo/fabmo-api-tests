# Waiting for authentication PR to be pulled in
# import time
# import threading
# from config import config
# from message_monitor import MessageMonitor
# from user import User
# from util import Util

# mm = MessageMonitor()
# mm.clear_all_state()

# user = User()
# util = Util()

# def modify_user(results):
#     username = "admin"
#     user_info = {
#         b"username": username.encode(),
#         b"password": b"test222",
#     }
#     user.modify_user(username, user_info)


#     # Did tests pass?
#     results["code"] = True
#     return

# def thread_for_mm(args):
#     mm.run()

# # test function

# def test_modify_user():
#     # setting things up so test can run
#     messageMonitorThread = threading.Thread(target=thread_for_mm, args=(1,), daemon=True)
#     results = {"code":False}
#     testThread = threading.Thread(target=modify_user, args=(results,))

#     # test sequence
#     messageMonitorThread.start()
#     time.sleep(1) # time for the MessageMonitor to get up and running
#     testThread.start()
#     testThread.join() #waiting for the test to return

#     #reporting results
#     assert results["code"] is True

# if __name__ == "__main__":
#     print(config.API_URL)
#     print("Testing modify_user")
#     test_modify_user()

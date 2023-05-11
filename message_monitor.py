import asyncio
import time
import threading
import socketio
from config import config
from msg_fabmo_status import FabmoStatus

lock = threading.Lock()

class MessageMonitor:
    def __init__(self):
        self.initialized = 1

    #private data
    eventsReceived = {
        "change" : "notYet",
        "state" : "notYet",
        "out1" : "notYet",
        "message" : "notYet"
    }

    @staticmethod
    def setState(state):
        with lock:
            MessageMonitor.eventsReceived["state"] = state

    @staticmethod
    def getState():
        with lock:
            rc = MessageMonitor.eventsReceived["state"]
        return rc

    @staticmethod
    def setChange(change):
        with lock:
            MessageMonitor.eventsReceived["change"] = change

    @staticmethod
    def getChange():
        with lock:
            rc = MessageMonitor.eventsReceived["change"]
        return rc

    @staticmethod
    def setOut1(output):
        with lock:
            MessageMonitor.eventsReceived["out1"] = output

    @staticmethod
    def getOut1():
        with lock:
            rc = MessageMonitor.eventsReceived["out1"]
        return rc

    @staticmethod
    def setMsg(msg):
        with lock:
            MessageMonitor.eventsReceived["message"] = msg

    @staticmethod
    def getMsg():
        with lock:
            rc = MessageMonitor.eventsReceived["message"]
        return rc


    #######################################################
    # Public API for use by tests

    # async wait_for_state(state2wait4, timeout):
    #
    # This function will block until # the socketio status
    # first shows the state indicated in state2wait4 parameter
    #   if the message has already arrived, then
    #     the function will return a true value immediately
    #   if the message arrives before the time out, then
    #     the function returns a true value once the msg
    #     has been parsed
    #   if the time out is reached it will return false value
    #     after the timeout
    # Return values: false means "timed out"
    #
    # Usage:
    # call this function with a string representing the specific status
    # that you want to know has happened E.g. You have commanded over API
    # that a job start, and want to know that it has started, so call:
    #       wait_for_status("running")
    # then maybe call
    #       wait_for_status("idle")
    #
    # Note: you may want to call clear_all_state() before starting a test
    #    case to make sure that you start with no "holdever" messages from
    #    prior test cases.
    #######################################################
    #public method
    def wait_for_state(self, state2wait4, timeout):
#       print(f"{state2wait4}, {timeout}");
        end_time = time.time() + timeout
        while time.time() < end_time:
            currentState = MessageMonitor.getState()
            if state2wait4 == currentState:
                return True
            time.sleep(1)
        return False

    def wait_for_output(self, output2wait4, timeout):
        end_time = time.time() + timeout
        while time.time() < end_time:
            output = MessageMonitor.getOut1()
            if output2wait4 == output:
                return True
            time.sleep(1)
        return False

    def wait_for_message(self, message2wait4, timeout):
        end_time = time.time() + timeout
        while time.time() < end_time:
            message = MessageMonitor.getMsg()
            if message2wait4 == message:
                return True
            time.sleep(1)
        return False

    #public method
#    def wait_for_change(self, change2wait4, timeout):
##        print(f"{change2wait4}, {timeout}")

    #public method
    def clear_all_state(self):
        MessageMonitor.setState("notYet")
        MessageMonitor.setChange("notChange")
        MessageMonitor.setOut1("notOutput")
        MessageMonitor.setMsg("notMessage")

    # public method
    def run(self):
        asyncio.run(main())

#################################################################
# everything from here on down is meant to be private
# and is a mess - need to figure out how to hide this in the
# class above or make a module that can be a member of the class above
#
# Internal socketio server
#  to make API work:

# Using the global keyword below for connected
# This is to prevent socketio from attempting to reconnect
# If it is already connected

sio = socketio.AsyncClient()
connected = False

# implemented from server to client
@sio.on('status')
async def onStatus(status):
    msg = FabmoStatus(status)
    #DEBUG
    # msg.printMe()
    # print("\n\n\n\n")
    #DEBUG
    state = msg.get_key("state")
    out1 = msg.get_key("out1")
    #TODO, there is a bug were retrieving sub keys sometimes causes
    # issues, I think it happens when there is no sub key to retrieve
    #Specifically it happens when trying to retrieve an error message
    message = msg.get_sub_key("info", "message")
    MessageMonitor.setState(state)
    MessageMonitor.setOut1(out1)
    MessageMonitor.setMsg(message)

# implemented from server to client
@sio.on('change')
async def onChange(change):
    MessageMonitor.setChange(change)
    #print(f"MessageMonitor.change: {change}\n")

@sio.on('job_start')
async def onStart(start_info):
    print(f"Job start: {start_info}\n")

@sio.on('job_end')
async def onEnd(end_info):
    print(f"Job end: {end_info}\n")

@sio.on('connect')
async def onConnect():
    global connected
    connected = True
    print("Websocket connected\n")

@sio.on('disconnect')
async def onDisconnect():
    global connected
    connected = False
    print("Websocket disconnected\n")

@sio.event
async def disconnect():
    print('disconnected from server\n')

async def main():
    global connected
    if not connected:
        await sio.connect(f'{config.API_URL}')
        await sio.wait()


if __name__ == '__main__':
    monitor = MessageMonitor()
    monitor.run()

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
        "out1" : "notYet"
    }

    @staticmethod
    def setState(state):
        lock.acquire()
        MessageMonitor.eventsReceived["state"] = state
        lock.release()

    @staticmethod
    def getState():
        lock.acquire()
        rc = MessageMonitor.eventsReceived["state"] 
        lock.release()
        return rc

    @staticmethod
    def setChange(change):
        lock.acquire()
        MessageMonitor.eventsReceived["change"] = change
        lock.release()

    @staticmethod
    def getChange():
        lock.acquire()
        rc = MessageMonitor.eventsReceived["change"] 
        lock.release()
        return rc

    @staticmethod
    def setOut1(output):
        lock.acquire()
        MessageMonitor.eventsReceived["out1"] = output
        lock.release()

    @staticmethod
    def getOut1():
        lock.acquire()
        rc = MessageMonitor.eventsReceived["out1"]
        lock.release()
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
#       print(f"{state2wait4}, {timeout}");
        end_time = time.time() + timeout
        while time.time() < end_time:
            output = MessageMonitor.getOut1()
            if output2wait4 == output:
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

sio = socketio.AsyncClient()
 

# implemented from server to client
@sio.on('status')
async def onStatus(status):
    msg = FabmoStatus(status)
    state = msg.get("state")
    out1 = msg.get("out1")
    MessageMonitor.setState(state)
    MessageMonitor.setOut1(out1)

# implemented from server to client
@sio.on('change')
async def onChange(change):
    MessageMonitor.setChange(change)
    print(f"MessageMonitor.change: {change}\n")

@sio.on('job_start')
async def onStart(start_info):
    print(f"Job start: {start_info}\n")

@sio.on('job_end')
async def onEnd(end_info):
    print(f"Job end: {end_info}\n")

@sio.on('connect')
async def onConnect():
    print("Websocket connected\n")

@sio.on('disconnect')
async def onDisconnect():
    print("Websocket disconnected\n")

@sio.event
async def disconnect():
    print('disconnected from server\n')

async def main():
    await sio.connect(f'{config.API_URL}')
    await sio.wait()


if __name__ == '__main__':
    monitor = MessageMonitor()
    monitor.run()

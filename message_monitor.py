import asyncio
import socketio
from config import config
from msg_fabmo_status import FabmoStatus

class MessageMonitor:
    def __init__(self):
        self.run();        

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
    async def wait_for_state(self, state2wait4, timeout):
        print("hello")


    #public method
    #async def wait_for_change(self, change2wait4):


    #public method
    def clear_all_state(self):
        eventsReceived["state"] = "notYet"
        eventsReceived["change"] = "state"

    # public method
    def run(self):
        asyncio.run(main())

#################################################################
# everything from here on down is meant to be private
# Internal socketio server 
#  to make API work:

sio = socketio.AsyncClient()
 
#private data
eventsReceived = {
    "change" : "notYet",
    "state" : "notYet"
}


# implemented from server to client
@sio.on('status')
async def onStatus(status):
    msg = FabmoStatus(status)
    state = msg.get("state")
    eventsReceived["state"] = state
#    print(f"state: {state}\n")
    print(f"events: {eventsReceived}\n")

# implemented from server to client
@sio.on('change')
async def onChange(change):
    eventsReceived["change"] = change
    print(f"change: {change}\n")

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

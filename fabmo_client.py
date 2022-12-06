import asyncio
import socketio
from config import config
from msg_fabmo_status import FabmoStatus

eventsReceived = {
    "change" : "notYet",
    "status" : "notYet"
}

sio = socketio.AsyncClient()

# implemented from server to client
@sio.on('status')
async def onStatus(status):
    msg = FabmoStatus(status)
    state = msg.get("state")
    eventsReceived["status"] = state
    print(f"state: {state}\n")
    print(f"events: {eventsReceived}\n")

# implemented from server to client
@sio.on('change')
async def onChange(change):
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
    asyncio.run(main())

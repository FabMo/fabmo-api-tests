import asyncio
import socketio
from config import config

sio = socketio.AsyncClient()

@sio.event
async def connect():
    print('connection established\n')

@sio.on('status')
async def onStatus(status):
    print(f"status: {status}\n")

@sio.on('change')
async def onChange(change):
    print(f"change: {change}\n")

@sio.on('connect')
async def onConnect():
    print("Websocket connected\n")

@sio.on('message')
async def onMessage(message):
    print(f"message: {message}\n")

@sio.on('disconnect')
async def onDisconnect():
    print("Websocket disconnected\n")

@sio.on('authentication_failed')
async def onAuthFail(message):
    print(f"authentication failed message: {message}\n")

@sio.on('connect_error')
async def onConnectError():
    print(f"Websocket disconnected (connection error)\n")

@sio.on('user_change')
async def onUserChange(user):
    print(f"user change: {user}\n")

@sio.on('*')
async def catch_all(event, data):
    print(f"Event: {event}")
    print(f"Data: {data}\n")

@sio.event
async def disconnect():
    print('disconnected from server\n')

async def main():
    await sio.connect(f'{config.API_URL}')
    await sio.wait()

if __name__ == '__main__':
    asyncio.run(main())

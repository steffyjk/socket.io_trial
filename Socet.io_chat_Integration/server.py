import asyncio
from aiohttp import web
import socketio

# Create a Socket.IO server
sio = socketio.AsyncServer(cors_allowed_origins='*')  # Allow all origins for testing
app = web.Application()
sio.attach(app)

# Event handler for client connections
@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")

# Event handler for Chat 1 messages (sends to Chat 2)
@sio.event
async def chat_message_1(sid, data):
    print(f"Chat 1 to Chat 2 message from {sid}: {data}")
    await sio.emit('chat_message_2', data)  # Send to Chat 2

# Event handler for Chat 2 messages (sends to Chat 1)
@sio.event
async def chat_message_2(sid, data):
    print(f"Chat 2 to Chat 1 message from {sid}: {data}")
    await sio.emit('chat_message_1', data)  # Send to Chat 1

# Event handler for client disconnections
@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")

# Start the server
async def start_server():
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 3000)
    await site.start()
    print("Server running on http://localhost:3000")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server())
    loop.run_forever()
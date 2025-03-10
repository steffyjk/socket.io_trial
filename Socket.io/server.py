import asyncio
from aiohttp import web
import socketio

# Create a Socket.IO server with explicit transport support
sio = socketio.AsyncServer(cors_allowed_origins='*')  # Allow all origins for testing
app = web.Application()
sio.attach(app)

# Event handlers
@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")

@sio.event
async def chat_message(sid, data):
    print(f"Message from {sid}: {data}")
    await sio.emit('chat_message', data)

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
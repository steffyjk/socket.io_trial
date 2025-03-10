import socketio

# Create a Socket.IO client
sio = socketio.Client()

@sio.event
def connect():
    print('Connected to server')
    sio.emit('chat_message', 'Hello from Python client!')

@sio.event
def chat_message(data):
    print(f"Received message: {data}")

@sio.event
def disconnect():
    print('Disconnected from server')

# Connect to the server
sio.connect('http://localhost:3000')
sio.wait()
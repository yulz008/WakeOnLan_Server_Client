# client.py

import socketio
from wol_script import send_magic_packet  # 👈 Import function

sio = socketio.Client()

@sio.event
def connect():
    print("Connected to WebSocket server")

@sio.event
def disconnect():
    print("Disconnected from server")

@sio.on('command')
def on_command(data):
    print("Received command:", data)
    if data.get('cmd') == 'ON':
        print("ON command received")
        # Send the magic packet here
        send_magic_packet(mac_address="FF-FF-FF-FF-FF-FF", ip_address="192.168.1.2")

try:
    sio.connect('http://localhost:5000')  # Or your server IP
    sio.wait()
except Exception as e:
    print("Connection error:", e)

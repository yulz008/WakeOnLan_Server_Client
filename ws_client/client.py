# client.py

import socketio
import subprocess
import time
from wol_script import send_magic_packet  # Import function

sio = socketio.Client()

def ping_host(ip_address, timeout=1, count=4):
    """
    Ping the target host to check if it's alive
    Returns True if at least one ping was successful, False otherwise
    """
    try:
        # Platform-independent ping command
        if subprocess.os.name == 'nt':  # Windows
            command = ['ping', '-n', str(count), '-w', str(timeout*1000), ip_address]
        else:  # Linux/Mac
            command = ['ping', '-c', str(count), '-W', str(timeout), ip_address]
        
        # Run ping command
        result = subprocess.run(command, capture_output=True, text=True)
        
        # Check if ping was successful
        return result.returncode == 0
    except Exception as e:
        print(f"Ping error: {e}")
        return False

def ping_host_continuously(ip_address, max_attempts=30, interval=5):
    """
    Continuously ping the host until it responds or max attempts reached
    Returns True if host responded, False otherwise
    """
    print(f"Waiting for {ip_address} to wake up...")
    
    for attempt in range(1, max_attempts + 1):
        print(f"Ping attempt {attempt}/{max_attempts}")
        
        if ping_host(ip_address):
            print(f"Host {ip_address} is alive!")
            return True
        
        if attempt < max_attempts:
            time.sleep(interval)
    
    print(f"Host {ip_address} did not respond after {max_attempts} attempts")
    return False

@sio.event
def connect():
    print("Connected to WebSocket server")
    sio.emit('client_connected', {'type': 'wol_client', 'status': 'ready'})

@sio.event
def disconnect():
    print("Disconnected from server")

@sio.on('command')
def on_command(data):
    print("Received command:", data)
    if data.get('cmd') == 'ON':
        print("ON command received")
        
        # Send the magic packet
        mac_address = "FF-FF-FF-FF-FF-FF"  # Replace with actual MAC
        ip_address = "192.168.1.2"         # Replace with actual IP
        
        try:
            send_magic_packet(mac_address=mac_address, ip_address=ip_address)
            print(f"Magic packet sent to {mac_address}")
            
            # Notify server that magic packet was sent
            sio.emit('wol_status', {
                'status': 'magic_packet_sent',
                'mac_address': mac_address,
                'ip_address': ip_address
            })
            
            # Ping the target to verify it woke up
            is_alive = ping_host_continuously(ip_address)
            
            # Notify server of the wake result
            if is_alive:
                print("Target device is awake and responsive!")
                sio.emit('wol_status', {
                    'status': 'device_awake',
                    'ip_address': ip_address,
                    'message': 'Device is responding to ping'
                })
            else:
                print("Target device did not respond to ping")
                sio.emit('wol_status', {
                    'status': 'device_not_responding',
                    'ip_address': ip_address,
                    'message': 'Device did not respond to ping after multiple attempts'
                })
                
        except Exception as e:
            print(f"Error sending magic packet: {e}")
            sio.emit('wol_status', {
                'status': 'error',
                'message': str(e)
            })

if __name__ == "__main__":
    try:
        sio.connect('http://localhost:5000')  # Or your server IP
        sio.wait()
    except Exception as e:
        print("Connection error:", e)
import socket

def send_magic_packet(mac_address, ip_address="255.255.255.255", port=9):
    # Normalize MAC: remove any separators and convert to bytes
    mac_bytes = bytes.fromhex(mac_address.replace("-", "").replace(":", ""))
    if len(mac_bytes) != 6:
        raise ValueError("Invalid MAC address format")

    # Build magic packet: 6 x 0xFF + 16 x MAC
    magic_packet = b"\xFF" * 6 + mac_bytes * 16

    # Send packet using UDP broadcast
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(magic_packet, (ip_address, port))
        print(f"Magic packet sent to {mac_address} via {ip_address}:{port}")

# Your configuration
# Sample Mac Address
mac = "FF-FF-FF-FF-FF-FF"
ip = "192.168.68.118"  # You can use "255.255.255.255" for global broadcast

send_magic_packet(mac, ip_address=ip)

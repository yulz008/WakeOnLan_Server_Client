# Wake-on-LAN WebSocket Server and Client

This project enables **remote Wake-on-LAN (WOL)** functionality via a **Flask-SocketIO server** and **Python WebSocket client**. The server acts as a central controller, broadcasting a command to wake up a target machine using a Magic Packet. The client listens for the command and triggers the actual WOL.

---

## 📁 Project Structure

```
WOL_Server_Client-main/
│
├── ws_server/               # Flask WebSocket server
│   ├── server.py
│   └── templates/
│       └── index.html
│
├── ws_client/               # Python WebSocket client
│   ├── client.py
│   ├── index.html           # (Optional) Static file
│   └── wol_script.py        # Sends magic packet
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Requirements

Install dependencies via:

```bash
pip install -r requirements.txt
```

Alternatively, split requirements for each:

### Server
```txt
flask
flask-socketio
eventlet
```

### Client (optional)
```txt
requests
websocket-client
```

---

## 🖥️ Deployment Context

- **Server**: A Google Cloud Platform (GCP) virtual machine instance running the Flask-SocketIO server.
- **Client**: A Raspberry Pi connected to the same network as your personal PC, responsible for listening to the WOL command and sending a magic packet.
- **Target**: Your personal PC that receives the magic packet and powers on remotely.

---

## 🖥️ Running the Server

### Linux / macOS

```bash
cd ws_server
python3 -m venv venv
source venv/bin/activate
pip install -r ../requirements.txt
python server.py
```

### Windows

```cmd
cd ws_server
python -m venv venv
venv\Scripts\activate
pip install -r ..\requirements.txt
python server.py
```

Once running, the server listens on `http://0.0.0.0:5000/` and broadcasts the `ON` command to WebSocket clients upon a `/wake` POST.

---

## 💻 Running the Client

```bash
cd ws_client
python client.py
```

This starts the Python WebSocket client that listens for the `ON` command and sends a Wake-on-LAN magic packet to the configured MAC address.

Make sure to edit `wol_script.py` to include your **target MAC address** and **broadcast IP**, e.g.:

```python
send_magic_packet(mac_address="FF-FF-FF-FF-FF-FF", ip_address="192.168.69.255")
```

---

## 🌐 Trigger WOL via API

Send a POST request to:

```
http://<server-ip>:5000/wake
```

### Example with curl:

```bash
curl -X POST http://localhost:5000/wake
```

### Example with Frontend Components access via external ip address of the web server

![image](https://github.com/user-attachments/assets/3efb0850-0c74-425c-acf1-3e7904da6672)


---

## 🧪 Testing Tips

- Ensure that your network allows broadcast packets.
- The target machine must support WOL and be configured correctly in BIOS/UEFI and OS.
- Test locally before deploying across networks.

---

## 🔒 Security Note

This is a **simple demo project**. Do not expose the WOL endpoint to the public internet without securing it (authentication, encryption, etc.).

---

## 📜 License

MIT (or specify if otherwise).

---

## 🙌 Credits

Developed by [Your Name]. Powered by Flask, Flask-SocketIO, and Python.

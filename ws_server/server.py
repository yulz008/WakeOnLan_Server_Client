from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/wake', methods=['POST'])
def wake():
    print("Wake command received. Broadcasting 'ON' to clients...")
    socketio.emit('command', {'cmd': 'ON'})
    return jsonify({'status': 'sent'})

@socketio.on('connect')
def connect():
    print("Client connected")

@socketio.on('disconnect')
def disconnect():
    print("Client disconnected")

if __name__ == '__main__':
    print("Flask-SocketIO server is running at http://localhost:5000")
    socketio.run(app, host='0.0.0.0', port=5000)

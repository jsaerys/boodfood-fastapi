import os
import sys

# Asegurar directorio de trabajo al nivel del repo
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from socket_events import socketio

app = create_app('production')

if __name__ == '__main__':
    # Ejecutar SocketIO (soporta WebSockets/eventlet)
    socketio.run(app, host='0.0.0.0', port=8000)

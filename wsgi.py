"""
Punto de entrada principal para la aplicación BoodFood
"""
import sys
import os

# Añadir src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from app.app import create_app
from app.socket_events import socketio

if __name__ == '__main__':
    app = create_app('development')
    socketio.run(app, host='127.0.0.1', port=5000, debug=True)

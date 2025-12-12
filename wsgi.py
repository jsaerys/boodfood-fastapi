"""
Punto de entrada principal para la aplicación BoodFood (Flask)
"""
import sys
import os

# Configurar path para importes
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(current_dir, 'src'))
sys.path.insert(0, current_dir)

from app.app import create_app
from app.socket_events import socketio

if __name__ == '__main__':
    app = create_app('development')
    print("="*70)
    print("🚀 BoodFood - Flask Application")
    print("="*70)
    print("📍 Frontend:   http://0.0.0.0:5000")
    print("📍 WebSocket:  Habilitado en puerto 5000")
    print("="*70)
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)

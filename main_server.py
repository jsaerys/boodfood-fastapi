"""
Servidor principal que integra Flask y FastAPI
Ejecuta ambas aplicaciones en paralelo
"""
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi_app import create_fastapi_app
from app import create_app, socketio
import threading


def run_flask():
    """Ejecutar servidor Flask con SocketIO"""
    flask_app = create_app('development')
    socketio.run(flask_app, host='0.0.0.0', port=5000, debug=False, use_reloader=False)


def run_fastapi():
    """Ejecutar servidor FastAPI"""
    uvicorn.run(
        "main_server:fastapi_app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )


if __name__ == '__main__':
    print("="*70)
    print("🚀 Iniciando BoodFood - Sistema Completo")
    print("="*70)
    print("📍 Flask (Web + SocketIO): http://localhost:5000")
    print("📍 FastAPI (REST API):      http://localhost:8000/api")
    print("📍 API Docs (Swagger):      http://localhost:8000/api/docs")
    print("📍 API Docs (ReDoc):        http://localhost:8000/api/redoc")
    print("="*70)
    
    # Crear aplicación FastAPI
    fastapi_app = create_fastapi_app()
    
    # Opción 1: Ejecutar solo FastAPI (recomendado para desarrollo)
    # uvicorn.run(fastapi_app, host="0.0.0.0", port=8000, reload=True)
    
    # Opción 2: Ejecutar Flask y FastAPI en hilos separados
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # FastAPI se ejecuta en el hilo principal
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8000, reload=False)

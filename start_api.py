#!/usr/bin/env python
"""
Script para iniciar FastAPI
"""
import subprocess
import webbrowser
import time
from threading import Thread
import sys

def open_browser():
    """Abre el navegador después de un pequeño delay"""
    time.sleep(3)  # Esperar a que el servidor inicie
    try:
        webbrowser.open('http://localhost:8000/api')
        print("\n🌐 Navegador abierto en http://localhost:8000/api")
    except Exception as e:
        print(f"⚠️ No se pudo abrir el navegador: {e}")

if __name__ == '__main__':
    # Iniciar apertura del navegador en un hilo separado
    browser_thread = Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    # Iniciar el servidor FastAPI
    print("="*70)
    print("🚀 Iniciando BoodFood API")
    print("="*70)
    print("📍 API:              http://localhost:3311/api")
    print("📚 Docs (Swagger):   http://localhost:3311/api/docs")
    print("📘 ReDoc:            http://localhost:3311/api/redoc")
    print("="*70 + "\n")
    
    # Ejecutar uvicorn via subprocess
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "fastapi_app.asgi:app",
            "--host", "127.0.0.1",
            "--port", "3311",
            "--reload"
        ], check=False)
    except KeyboardInterrupt:
        print("\n\n👋 Servidor detenido")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error al iniciar servidor: {e}")
        sys.exit(1)

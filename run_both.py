"""
Ejecutar ambos servidores (Flask + FastAPI) en paralelo
"""
import subprocess
import sys
import time
from multiprocessing import Process


def run_flask():
    """Ejecutar Flask en proceso separado"""
    print("🔵 Iniciando Flask...")
    subprocess.run([sys.executable, "app.py"])


def run_fastapi():
    """Ejecutar FastAPI en proceso separado"""
    print("🟢 Iniciando FastAPI...")
    subprocess.run([sys.executable, "run_fastapi.py"])


if __name__ == '__main__':
    print("="*70)
    print("🚀 BoodFood - Sistema Completo (Flask + FastAPI)")
    print("="*70)
    print("📍 Flask (Web + Templates + SocketIO): http://localhost:5000")
    print("📍 FastAPI (REST API):                  http://localhost:8000/api")
    print("📍 Swagger Docs:                        http://localhost:8000/api/docs")
    print("="*70)
    print("\n⚠️  Presiona Ctrl+C para detener ambos servidores\n")
    
    # Crear procesos
    flask_process = Process(target=run_flask)
    fastapi_process = Process(target=run_fastapi)
    
    try:
        # Iniciar ambos servidores
        flask_process.start()
        time.sleep(2)  # Esperar a que Flask inicie
        fastapi_process.start()
        
        # Esperar a que ambos terminen
        flask_process.join()
        fastapi_process.join()
        
    except KeyboardInterrupt:
        print("\n\n👋 Deteniendo servidores...")
        flask_process.terminate()
        fastapi_process.terminate()
        flask_process.join()
        fastapi_process.join()
        print("✅ Servidores detenidos")

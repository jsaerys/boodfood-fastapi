"""
Ejecutar solo el servidor FastAPI con contexto de Flask
"""
import sys
import os

# Asegurar que estamos en el directorio correcto
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import uvicorn
from app import create_app as create_flask_app
from fastapi_app import create_fastapi_app

if __name__ == '__main__':
    print("="*70)
    print("🚀 Iniciando FastAPI - BoodFood API REST")
    print("="*70)
    print("📍 API Base:          http://localhost:8000/api")
    print("📍 Swagger Docs:      http://localhost:8000/api/docs")
    print("📍 ReDoc:             http://localhost:8000/api/redoc")
    print("📍 OpenAPI JSON:      http://localhost:8000/api/openapi.json")
    print("="*70)
    print()
    
    # IMPORTANTE: Crear contexto de Flask ANTES de FastAPI
    flask_app = create_flask_app('development')
    print("✅ Contexto de Flask creado")
    
    app = create_fastapi_app()
    print("✅ FastAPI creado")
    
    print("\n🎯 Servidor listo en http://localhost:8000\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False,  # Desactivado para evitar warning
        log_level="info"
    )

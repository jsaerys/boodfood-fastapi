"""
Punto de entrada para FastAPI (ASGI)
"""
import sys
import os

# Configurar path para importes
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(current_dir, 'src'))
sys.path.insert(0, current_dir)

print("🚀 Initializing FastAPI application...")
from fastapi_app import create_fastapi_app

app = create_fastapi_app()
print("✅ FastAPI application ready")

"""
Punto de entrada para FastAPI
"""
import sys
import os

# Añadir src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from fastapi_app import create_fastapi_app

app = create_fastapi_app()

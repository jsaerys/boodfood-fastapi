"""
Script para probar directamente la API de menú
"""
import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from app import create_app
import json

app = create_app('development')

with app.test_client() as client:
    # Simular login (necesitamos estar autenticados)
    with app.test_request_context():
        from models import Usuario
        from flask import session
        from flask_login import login_user
        
        # Usar el cliente de prueba
        print("\n=== PRUEBA DE API DE MENÚ ===\n")
        
        print("1️⃣ Probando GET /admin/api/menu/items")
        response = client.get('/admin/api/menu/items')
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.get_json()
            print(f"   ✅ Items devueltos: {len(data)}")
            if data:
                print(f"   📋 Primer item: {json.dumps(data[0], indent=2)}")
        else:
            print(f"   ❌ Error: {response.data.decode()}")
        
        print("\n2️⃣ Probando GET /admin/api/categorias/lista")
        response = client.get('/admin/api/categorias/lista')
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.get_json()
            print(f"   ✅ Categorías devueltas: {len(data)}")
            for cat in data:
                print(f"      - {cat['nombre']}")
        else:
            print(f"   ❌ Error: {response.data.decode()}")
        
        print("\n=== FIN DE LA PRUEBA ===\n")

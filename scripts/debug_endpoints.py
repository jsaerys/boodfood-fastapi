#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Debug rápido para ver los errores específicos de pedidos y reservas"""
import sys
import os

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from fastapi_app import create_fastapi_app
from app import create_app as create_flask_app

flask_app = create_flask_app('development')

with flask_app.app_context():
    app = create_fastapi_app()
    client = TestClient(app)

    # Verificar mesas disponibles
    print("--- MESAS DISPONIBLES ---")
    mesas_res = client.get("/api/v1/mesas")
    mesas = mesas_res.json()
    available_mesas = [m for m in mesas if m.get('disponible')]
    print(f"Total: {len(mesas)}, Disponibles: {len(available_mesas)}")
    if available_mesas:
        print(f"IDs disponibles: {[m['id'] for m in available_mesas[:5]]}")
    
    # Verificar items de menú
    print("\n--- ITEMS DE MENU ---")
    menu_res = client.get("/api/v1/menu")
    items = menu_res.json()
    print(f"Total items: {len(items)}")
    if items:
        print(f"Primeros IDs: {[it['id'] for it in items[:5]]}")
        print(f"Primeros nombres: {[it['nombre'] for it in items[:3]]}")

    # Registrar y login
    print("\n--- REGISTRO Y LOGIN ---")
    reg = client.post("/api/v1/auth/register", json={
        "nombre": "Debug", "apellido": "Test", "email": f"debug{os.urandom(2).hex()}@test.com",
        "password": "Pass123!", "telefono": "3105551234", "direccion": "Test"
    })
    print(f"Register: {reg.status_code}")
    
    email = reg.json().get("message", "debug@test.com")
    login = client.post("/api/v1/auth/login", json={
        "email": reg.json().get("email", "debug@test.com") if "email" in reg.json() else f"debug{os.urandom(2).hex()}@test.com",
        "password": "Pass123!"
    })
    
    # Usar la del formulario de registro
    emails_sent = client.get("/api/v1/mesas").json()  # para resetear
    new_email = f"debug_working_{os.urandom(3).hex()}@test.com"
    reg2 = client.post("/api/v1/auth/register", json={
        "nombre": "DebugUser", "apellido": "Test2", "email": new_email,
        "password": "TestPass123!", "telefono": "3105551234", "direccion": "Calle Test"
    })
    
    login2 = client.post("/api/v1/auth/login", json={
        "email": new_email, "password": "TestPass123!"
    })
    print(f"Login 2: {login2.status_code}")
    if login2.status_code == 200:
        token = login2.json()["access_token"]
        
        # Test Pedido con primer item válido
        if items:
            first_item_id = items[0]["id"]
            print(f"\n--- PEDIDO (usando item ID {first_item_id}) ---")
            pedido_res = client.post("/api/v1/pedidos", 
                json={"tipo_servicio": "domicilio", "mesa_id": None, 
                      "items": [{"menu_item_id": first_item_id, "cantidad": 1, "precio_unitario": 25.0}],
                      "metodo_pago": "efectivo"},
                headers={"Authorization": f"Bearer {token}"})
            print(f"Status: {pedido_res.status_code}")
            if pedido_res.status_code != 201:
                print(f"Response: {pedido_res.text[:300]}")
            else:
                print(f"Pedido creado exitosamente!")
        
        # Test Reserva
        print(f"\n--- RESERVA (usando fecha 2025-12-15 19:00) ---")
        reserva_res = client.post("/api/v1/reservas",
            json={"fecha_reserva": "2025-12-15 19:00", 
                  "numero_personas": 4, "notas": "Test"},
            headers={"Authorization": f"Bearer {token}"})
        print(f"Status: {reserva_res.status_code}")
        if reserva_res.status_code != 201:
            print(f"Response: {reserva_res.text[:300]}")
        else:
            print(f"Reserva creada exitosamente!")


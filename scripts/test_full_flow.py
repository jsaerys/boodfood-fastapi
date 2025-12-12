"""
Script para probar login y creación de mesa con requests
Esto nos muestra exactamente qué está pasando
"""
import requests
import json
import time

BASE_URL = "http://127.0.0.1:8002"

print("=" * 70)
print("TEST COMPLETO: LOGIN + CREAR MESA")
print("=" * 70)

# Step 1: Login
print("\n[1/3] Haciendo POST /api/v1/auth/login...")
login_response = requests.post(
    f"{BASE_URL}/api/v1/auth/login",
    json={
        "email": "admin1@gmail.com",
        "password": "3144210095"
    }
)

print(f"Status: {login_response.status_code}")
print(f"Headers: {dict(login_response.headers)}")
print(f"Body: {login_response.text}")

if login_response.status_code != 200:
    print("ERROR en login!")
    exit(1)

login_data = login_response.json()
token = login_data.get("access_token")

if not token:
    print("ERROR: No se obtuvo token en la respuesta")
    exit(1)

print(f"\nToken obtenido exitosamente:")
print(f"  Primeros 50 chars: {token[:50]}")
print(f"  Últimos 50 chars: {token[-50:]}")
print(f"  Longitud total: {len(token)}")

# Step 2: Crear mesa con el token
print("\n[2/3] POST /api/v1/mesas con Authorization Bearer token...")

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

mesa_data = {
    "numero": 99,
    "capacidad": 4,
    "tipo": "interior",
    "descripcion": "Mesa de prueba con script"
}

print(f"Headers:")
for k, v in headers.items():
    if k == "Authorization":
        print(f"  {k}: Bearer {v.split('Bearer ')[1][:50]}...")
    else:
        print(f"  {k}: {v}")

print(f"Body: {json.dumps(mesa_data, indent=2)}")

mesa_response = requests.post(
    f"{BASE_URL}/api/v1/mesas",
    json=mesa_data,
    headers=headers
)

print(f"\nStatus: {mesa_response.status_code}")
print(f"Headers: {dict(mesa_response.headers)}")
print(f"Body: {mesa_response.text}")

if mesa_response.status_code == 201:
    print("\n✓ Mesa creada exitosamente!")
    mesa = mesa_response.json()
    print(f"  ID: {mesa.get('id')}")
    print(f"  Número: {mesa.get('numero')}")
else:
    print(f"\n✗ Error al crear mesa: {mesa_response.status_code}")
    print(f"Response: {mesa_response.text}")

print("\n" + "=" * 70)

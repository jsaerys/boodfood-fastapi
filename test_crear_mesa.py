"""
Script de prueba para crear una mesa con autenticación correcta
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8002/api/v1"

# 1. Login para obtener el token
print("=" * 60)
print("1. HACIENDO LOGIN...")
print("=" * 60)

login_payload = {
    "email": "admin1@gmail.com",
    "password": "3144210095"
}

response = requests.post(f"{BASE_URL}/auth/login", json=login_payload)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")

if response.status_code == 200:
    data = response.json()
    token = data.get("access_token")
    print(f"Token obtenido: {token[:50]}...")
    
    # 2. Crear una mesa con el token
    print("\n" + "=" * 60)
    print("2. CREANDO MESA CON TOKEN...")
    print("=" * 60)
    
    mesa_payload = {
        "numero": 5,
        "capacidad": 4,
        "tipo": "interior",
        "descripcion": "Mesa de prueba"
    }
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    print(f"Payload: {json.dumps(mesa_payload, indent=2)}")
    print(f"Headers: Authorization: Bearer {token[:50]}...")
    
    response = requests.post(f"{BASE_URL}/mesas", json=mesa_payload, headers=headers)
    print(f"\nStatus: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 201:
        print("\n✓ Mesa creada exitosamente!")
    else:
        print(f"\n✗ Error al crear mesa: {response.status_code}")
else:
    print(f"\n✗ Error en login: {response.status_code}")

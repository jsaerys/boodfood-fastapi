"""
Script de debug para probar login y creación de mesa
"""
import sys
import json

# Simular la llamada a login y token
print("=" * 70)
print("TEST DE AUTENTICACIÓN Y CREACIÓN DE MESA")
print("=" * 70)

# Credenciales
email = "admin1@gmail.com"
password = "3144210095"

print(f"\n1. Intentando login con:")
print(f"   Email: {email}")
print(f"   Password: {password}")

# Aquí deberías obtener el token manualmente desde Swagger y pegarlo
# Para este test, voy a mostrar cómo deberías estructurar el header

token = input("\nPega aquí el token JWT que obtuviste del login (sin 'Bearer '): ").strip()

if not token:
    print("No ingresaste un token. Abortando.")
    sys.exit(1)

print(f"\n2. Token ingresado: {token[:50]}...")

print(f"\n3. Header que debes usar en POST /api/v1/mesas:")
print(f"   Authorization: Bearer {token}")

print(f"\n4. Body para crear mesa:")
mesa_payload = {
    "numero": 5,
    "capacidad": 4,
    "tipo": "interior",
    "descripcion": "Mesa de prueba"
}
print(json.dumps(mesa_payload, indent=2, ensure_ascii=False))

print("\n" + "=" * 70)
print("Ahora en Swagger:")
print("1. Click en 'Authorize' (arriba a la derecha)")
print(f"2. Pega: Bearer {token}")
print("3. Click en 'Authorize'")
print("4. Luego POST /api/v1/mesas con el body anterior")
print("=" * 70)

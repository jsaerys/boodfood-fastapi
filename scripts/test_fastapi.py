"""
Script de prueba para la API de FastAPI
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def print_response(response, title):
    """Imprimir respuesta formateada"""
    print(f"\n{'='*70}")
    print(f"📍 {title}")
    print(f"{'='*70}")
    print(f"Status: {response.status_code}")
    try:
        print(f"Response:\n{json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"Response: {response.text}")


def test_api():
    """Probar endpoints de la API"""
    
    print("🚀 Iniciando pruebas de FastAPI - BoodFood")
    
    # 1. Verificar que la API está corriendo
    try:
        response = requests.get("http://localhost:8000/api")
        print_response(response, "GET /api - Verificación de API")
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: No se pudo conectar a FastAPI")
        print("   Asegúrate de que el servidor esté corriendo:")
        print("   python run_fastapi.py")
        return
    
    # 2. Login (obtener token)
    print("\n\n" + "="*70)
    print("🔐 AUTENTICACIÓN")
    print("="*70)
    
    login_data = {
        "email": "admin@boodfood.com",
        "password": "admin123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print_response(response, "POST /auth/login - Iniciar sesión")
    
    if response.status_code != 200:
        print("\n⚠️  Login falló. Intenta con estas credenciales de prueba:")
        print("   Email: admin@boodfood.com")
        print("   Password: admin123")
        print("\n   Si no existen, créalas primero en el sistema Flask.")
        token = None
    else:
        token = response.json()["access_token"]
        print(f"\n✅ Token obtenido: {token[:50]}...")
    
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    
    # 3. Probar endpoints públicos
    print("\n\n" + "="*70)
    print("📋 ENDPOINTS PÚBLICOS")
    print("="*70)
    
    # Mesas
    response = requests.get(f"{BASE_URL}/mesas")
    print_response(response, "GET /mesas - Listar todas las mesas")
    
    # Menú
    response = requests.get(f"{BASE_URL}/menu?disponible=true")
    print_response(response, "GET /menu - Listar items disponibles")
    
    # Categorías
    response = requests.get(f"{BASE_URL}/categorias")
    print_response(response, "GET /categorias - Listar categorías")
    
    # 4. Probar endpoints protegidos
    if token:
        print("\n\n" + "="*70)
        print("🔒 ENDPOINTS PROTEGIDOS")
        print("="*70)
        
        # Mi perfil
        response = requests.get(f"{BASE_URL}/usuarios/me", headers=headers)
        print_response(response, "GET /usuarios/me - Mi perfil")
        
        # Mis pedidos
        response = requests.get(f"{BASE_URL}/pedidos", headers=headers)
        print_response(response, "GET /pedidos - Mis pedidos")
        
        # Mis reservas
        response = requests.get(f"{BASE_URL}/reservas", headers=headers)
        print_response(response, "GET /reservas - Mis reservas")
    
    # 5. Resumen
    print("\n\n" + "="*70)
    print("✅ PRUEBAS COMPLETADAS")
    print("="*70)
    print("\n📚 Para documentación interactiva, visita:")
    print("   🔹 Swagger UI: http://localhost:8000/api/docs")
    print("   🔹 ReDoc:      http://localhost:8000/api/redoc")
    print("\n💡 Endpoints disponibles:")
    print("   - Autenticación: /api/v1/auth/*")
    print("   - Mesas:        /api/v1/mesas/*")
    print("   - Menú:         /api/v1/menu/*")
    print("   - Pedidos:      /api/v1/pedidos/*")
    print("   - Reservas:     /api/v1/reservas/*")
    print("   - Usuarios:     /api/v1/usuarios/*")
    print()


if __name__ == '__main__':
    test_api()

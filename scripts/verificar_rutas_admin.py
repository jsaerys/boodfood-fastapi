# Script de Verificación de Rutas API - Admin Panel
# Verifica que todas las rutas existan y respondan correctamente

import sys
import requests
from getpass import getpass

BASE_URL = "http://localhost:5000"

def login(email, password):
    """Login y obtener cookies de sesión"""
    session = requests.Session()
    
    # Primero obtener el CSRF token si existe
    response = session.get(f"{BASE_URL}/auth/login")
    
    # Hacer login
    login_data = {
        'email': email,
        'password': password
    }
    
    response = session.post(f"{BASE_URL}/auth/login", data=login_data, allow_redirects=True)
    
    if response.status_code == 200:
        print("✅ Login exitoso")
        return session
    else:
        print(f"❌ Login fallido: {response.status_code}")
        print(response.text)
        return None

def test_route(session, method, route, data=None, descripcion=""):
    """Prueba una ruta específica"""
    url = f"{BASE_URL}{route}"
    
    try:
        if method == "GET":
            response = session.get(url)
        elif method == "POST":
            response = session.post(url, json=data)
        elif method == "PUT":
            response = session.put(url, json=data)
        elif method == "DELETE":
            response = session.delete(url)
        
        if response.status_code in [200, 201]:
            print(f"  ✅ {method} {route} - {descripcion}")
            return True
        elif response.status_code == 404:
            print(f"  ❌ {method} {route} - NOT FOUND - {descripcion}")
            return False
        else:
            print(f"  ⚠️ {method} {route} - Status {response.status_code} - {descripcion}")
            return False
    except Exception as e:
        print(f"  ❌ {method} {route} - ERROR: {str(e)}")
        return False

def main():
    print("🔍 Verificación de Rutas API - Admin Panel\n")
    print("=" * 60)
    
    # Solicitar credenciales
    print("\n📝 Ingresa tus credenciales de ADMIN:")
    email = input("Email: ").strip()
    password = getpass("Password: ")
    
    # Login
    print("\n🔐 Iniciando sesión...")
    session = login(email, password)
    
    if not session:
        print("\n❌ No se pudo iniciar sesión. Verifica tus credenciales.")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("📊 PRUEBAS DE RUTAS")
    print("=" * 60)
    
    total = 0
    exitosas = 0
    
    # PEDIDOS
    print("\n📦 PEDIDOS:")
    routes = [
        ("GET", "/api/pedidos", None, "Listar pedidos"),
    ]
    for method, route, data, desc in routes:
        if test_route(session, method, route, data, desc):
            exitosas += 1
        total += 1
    
    # RESERVAS
    print("\n📅 RESERVAS:")
    routes = [
        ("GET", "/api/reservas", None, "Listar reservas"),
    ]
    for method, route, data, desc in routes:
        if test_route(session, method, route, data, desc):
            exitosas += 1
        total += 1
    
    # USUARIOS
    print("\n👥 USUARIOS:")
    routes = [
        ("GET", "/api/usuarios", None, "Listar usuarios"),
        ("GET", "/api/usuarios/lista", None, "Listar usuarios (alternativa)"),
    ]
    for method, route, data, desc in routes:
        if test_route(session, method, route, data, desc):
            exitosas += 1
        total += 1
    
    # MESAS
    print("\n🪑 MESAS:")
    routes = [
        ("GET", "/api/mesas", None, "Listar mesas"),
    ]
    for method, route, data, desc in routes:
        if test_route(session, method, route, data, desc):
            exitosas += 1
        total += 1
    
    # INVENTARIO (referencia que funciona)
    print("\n📦 INVENTARIO (Referencia):")
    routes = [
        ("GET", "/admin/api/inventario", None, "Listar inventario"),
    ]
    for method, route, data, desc in routes:
        if test_route(session, method, route, data, desc):
            exitosas += 1
        total += 1
    
    # Resumen
    print("\n" + "=" * 60)
    print(f"📊 RESUMEN: {exitosas}/{total} rutas funcionando correctamente")
    print("=" * 60)
    
    if exitosas == total:
        print("\n✅ ¡TODAS LAS RUTAS FUNCIONAN CORRECTAMENTE!")
    else:
        print(f"\n⚠️ {total - exitosas} rutas con problemas")
    
    print("\n💡 SIGUIENTE PASO:")
    print("1. Abre el navegador en: http://localhost:5000/admin")
    print("2. Navega a cada sección: Pedidos, Reservas, Usuarios, Mesas")
    print("3. Haz clic en los botones Ver/Editar/Eliminar")
    print("4. Verifica que los modales se abran correctamente")
    print("\n✨ Si los modales se abren, ¡TODO FUNCIONA! ✨\n")

if __name__ == "__main__":
    main()

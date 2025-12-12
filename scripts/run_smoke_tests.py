#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script completo de smoke-tests para FastAPI
Ejecuta dentro del contexto de Flask para que Flask-SQLAlchemy funcione correctamente
"""
import sys
import os

# Configurar encoding UTF-8
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

from datetime import datetime

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from fastapi_app import create_fastapi_app
from app import create_app as create_flask_app


class TestRunner:
    def __init__(self):
        self.results = []
        self.token = None
        self.user_id = None
        self.current_email = f"test_{datetime.now().timestamp()}@example.com"

    def log(self, test_name, passed, message="", response_data=None):
        """Registra el resultado de una prueba"""
        status = "✅ PASS" if passed else "❌ FAIL"
        result = {
            "test": test_name,
            "passed": passed,
            "message": message,
            "response": response_data
        }
        self.results.append(result)
        print(f"{status} | {test_name}")
        if message:
            print(f"   └─ {message}")
        return passed

    def test_register(self, client):
        """Test: Registrar usuario"""
        print("\n--- AUTENTICACIÓN ---")
        payload = {
            "nombre": "Test",
            "apellido": "User",
            "email": self.current_email,
            "password": "TestPass123!",
            "telefono": "3105551234",
            "direccion": "Test St 123"
        }
        try:
            r = client.post("/api/v1/auth/register", json=payload)
            success = r.status_code in [200, 201]
            self.log(
                "POST /auth/register",
                success,
                f"Status: {r.status_code}",
                r.json() if r.text else None
            )
            return success
        except Exception as e:
            self.log("POST /auth/register", False, str(e))
            return False

    def test_login(self, client):
        """Test: Login y obtener token"""
        payload = {
            "email": self.current_email,
            "password": "TestPass123!"
        }
        try:
            r = client.post("/api/v1/auth/login", json=payload)
            success = r.status_code == 200
            if success:
                data = r.json()
                if "access_token" in data:
                    self.token = data["access_token"]
                    if "user" in data:
                        self.user_id = data["user"].get("id")
                    self.log(
                        "POST /auth/login",
                        True,
                        f"Token obtenido. User: {data['user']['nombre'] if 'user' in data else 'N/A'}",
                        data
                    )
                else:
                    self.log("POST /auth/login", False, "No token en respuesta", data)
                    return False
            else:
                self.log("POST /auth/login", False, f"Status: {r.status_code}", r.json())
                return False
            return True
        except Exception as e:
            self.log("POST /auth/login", False, str(e))
            return False

    def test_get_profile(self, client):
        """Test: Obtener perfil del usuario autenticado"""
        print("\n--- USUARIOS ---")
        if not self.token:
            self.log("GET /usuarios/me", False, "No token disponible")
            return False
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            r = client.get("/api/v1/usuarios/me", headers=headers)
            success = r.status_code == 200
            self.log(
                "GET /usuarios/me",
                success,
                f"Status: {r.status_code}",
                r.json() if r.text else None
            )
            return success
        except Exception as e:
            self.log("GET /usuarios/me", False, str(e))
            return False

    def test_get_mesas(self, client):
        """Test: Listar mesas"""
        print("\n--- MESAS ---")
        try:
            r = client.get("/api/v1/mesas")
            success = r.status_code == 200
            data = r.json() if r.text else []
            count = len(data) if isinstance(data, list) else 0
            self.log(
                "GET /mesas",
                success,
                f"Status: {r.status_code}, Mesas encontradas: {count}",
                {"count": count, "sample": data[:1] if data else []}
            )
            return success
        except Exception as e:
            self.log("GET /mesas", False, str(e))
            return False

    def test_get_menu(self, client):
        """Test: Obtener menú"""
        print("\n--- MENÚ ---")
        try:
            r = client.get("/api/v1/menu")
            success = r.status_code == 200
            data = r.json() if r.text else []
            count = len(data) if isinstance(data, list) else 0
            self.log(
                "GET /menu",
                success,
                f"Status: {r.status_code}, Items: {count}",
                {"count": count, "sample": data[:1] if data else []}
            )
            return success
        except Exception as e:
            self.log("GET /menu", False, str(e))
            return False

    def test_create_pedido(self, client):
        """Test: Crear pedido con item válido"""
        print("\n--- PEDIDOS ---")
        if not self.token:
            self.log("POST /pedidos", False, "No token disponible")
            return False
        
        # Primero, obtener un item válido del menú
        try:
            menu_res = client.get("/api/v1/menu")
            menu_items = menu_res.json() if menu_res.text else []
            if not menu_items:
                self.log("POST /pedidos", False, "No hay items en el menú")
                return False
            menu_item_id = menu_items[0]["id"]
        except Exception as e:
            self.log("POST /pedidos", False, f"Error al obtener menú: {str(e)}")
            return False
        
        payload = {
            "tipo_servicio": "domicilio",
            "mesa_id": None,
            "items": [
                {"menu_item_id": menu_item_id, "cantidad": 2, "precio_unitario": 25.0}
            ],
            "metodo_pago": "efectivo"
        }
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            r = client.post("/api/v1/pedidos", json=payload, headers=headers)
            success = r.status_code in [200, 201]
            if not success and r.text:
                try:
                    error_data = r.json()
                    self.log(
                        "POST /pedidos",
                        False,
                        f"Status: {r.status_code}, Error: {error_data}",
                        error_data
                    )
                except:
                    self.log("POST /pedidos", False, f"Status: {r.status_code}, Body: {r.text[:200]}")
            else:
                self.log(
                    "POST /pedidos",
                    success,
                    f"Status: {r.status_code}",
                    r.json() if r.text else None
                )
            return success
        except Exception as e:
            self.log("POST /pedidos", False, str(e))
            return False

    def test_create_reserva(self, client):
        """Test: Crear reserva"""
        print("\n--- RESERVAS ---")
        if not self.token:
            self.log("POST /reservas", False, "No token disponible")
            return False
        payload = {
            "fecha_reserva": "2025-12-10 19:00",
            "numero_personas": 4,
            "notas": "Prueba desde smoke-tests"
        }
        try:
            headers = {"Authorization": f"Bearer {self.token}"}
            r = client.post("/api/v1/reservas", json=payload, headers=headers)
            success = r.status_code in [200, 201]
            if not success and r.text:
                try:
                    error_data = r.json()
                    self.log(
                        "POST /reservas",
                        False,
                        f"Status: {r.status_code}, Error: {error_data}",
                        error_data
                    )
                except:
                    self.log("POST /reservas", False, f"Status: {r.status_code}, Body: {r.text[:200]}")
            else:
                self.log(
                    "POST /reservas",
                    success,
                    f"Status: {r.status_code}",
                    r.json() if r.text else None
                )
            return success
        except Exception as e:
            self.log("POST /reservas", False, str(e))
            return False

    def test_root_endpoint(self, client):
        """Test: Endpoint raíz"""
        print("\n--- API RAÍZ ---")
        try:
            r = client.get("/api")
            success = r.status_code == 200
            data = r.json() if r.text else {}
            self.log(
                "GET /api",
                success,
                f"Status: {r.status_code}, Message: {data.get('message', 'N/A')}",
                data
            )
            return success
        except Exception as e:
            self.log("GET /api", False, str(e))
            return False

    def print_summary(self):
        """Imprime resumen de resultados"""
        total = len(self.results)
        passed = sum(1 for r in self.results if r["passed"])
        failed = total - passed
        
        print("\n" + "="*60)
        print("📊 RESUMEN DE PRUEBAS")
        print("="*60)
        print(f"Total: {total} | ✅ Exitosas: {passed} | ❌ Fallidas: {failed}")
        print(f"Porcentaje de éxito: {(passed/total*100):.1f}%" if total > 0 else "N/A")
        
        if failed > 0:
            print("\n❌ PRUEBAS FALLIDAS:")
            for r in self.results:
                if not r["passed"]:
                    print(f"  - {r['test']}: {r['message']}")
        
        print("\n" + "="*60)
        return passed == total

    def run_all_tests(self, client):
        """Ejecuta todas las pruebas en orden"""
        print("\n🚀 INICIANDO SMOKE-TESTS DE FASTAPI")
        print("="*60)
        
        # Pruebas sin autenticación
        self.test_root_endpoint(client)
        self.test_get_mesas(client)
        self.test_get_menu(client)
        
        # Autenticación
        if self.test_register(client):
            if self.test_login(client):
                # Pruebas autenticadas
                self.test_get_profile(client)
                self.test_create_pedido(client)
                self.test_create_reserva(client)
        
        # Resumen
        success = self.print_summary()
        return success


def main():
    """Punto de entrada principal"""
    print("⏳ Inicializando entorno...")
    
    # Crear contexto de Flask
    flask_app = create_flask_app('development')
    
    with flask_app.app_context():
        print("✅ Contexto Flask creado")
        
        # Crear instancia de FastAPI
        fastapi_app = create_fastapi_app()
        client = TestClient(fastapi_app)
        
        print("✅ Cliente TestClient creado")
        print()
        
        # Ejecutar pruebas
        runner = TestRunner()
        success = runner.run_all_tests(client)
        
        # Retornar código de salida
        sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()

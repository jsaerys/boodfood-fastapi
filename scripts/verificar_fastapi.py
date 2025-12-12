"""
Verificación rápida de FastAPI
"""
import requests
import sys

def verificar_fastapi():
    """Verificar que FastAPI está funcionando"""
    
    print("="*70)
    print("🔍 VERIFICACIÓN DE FASTAPI")
    print("="*70)
    
    try:
        # Verificar endpoint raíz
        print("\n1️⃣ Verificando API...")
        response = requests.get("http://localhost:8000/api", timeout=5)
        
        if response.status_code == 200:
            print("   ✅ API respondiendo correctamente")
            data = response.json()
            print(f"   📌 Versión: {data.get('message', 'N/A')}")
        else:
            print(f"   ❌ API respondió con código {response.status_code}")
            return False
        
        # Verificar documentación
        print("\n2️⃣ Verificando Swagger UI...")
        response = requests.get("http://localhost:8000/api/docs", timeout=5)
        if response.status_code == 200:
            print("   ✅ Swagger UI disponible")
        else:
            print("   ⚠️  Swagger UI no disponible")
        
        # Verificar OpenAPI
        print("\n3️⃣ Verificando OpenAPI...")
        response = requests.get("http://localhost:8000/api/openapi.json", timeout=5)
        if response.status_code == 200:
            print("   ✅ OpenAPI JSON disponible")
            openapi = response.json()
            print(f"   📌 Endpoints: {len(openapi.get('paths', {}))}")
        else:
            print("   ⚠️  OpenAPI no disponible")
        
        # Verificar endpoint de mesas (público)
        print("\n4️⃣ Probando endpoint público...")
        response = requests.get("http://localhost:8000/api/v1/mesas", timeout=5)
        if response.status_code == 200:
            mesas = response.json()
            print(f"   ✅ Endpoint /mesas funcionando")
            print(f"   📊 Mesas encontradas: {len(mesas)}")
        else:
            print(f"   ❌ Error en /mesas: {response.status_code}")
        
        # Resultado final
        print("\n" + "="*70)
        print("✅ FASTAPI FUNCIONANDO CORRECTAMENTE")
        print("="*70)
        print("\n📍 URLs disponibles:")
        print("   • API Base:    http://localhost:8000/api")
        print("   • Swagger UI:  http://localhost:8000/api/docs")
        print("   • ReDoc:       http://localhost:8000/api/redoc")
        print("   • OpenAPI:     http://localhost:8000/api/openapi.json")
        print("\n💡 Abre Swagger UI en tu navegador para probar la API")
        print()
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: No se pudo conectar a FastAPI")
        print("\n🔧 Solución:")
        print("   1. Asegúrate de que FastAPI esté corriendo:")
        print("      C:/Users/LENOVO/Desktop/Proyec11/.venv/Scripts/python.exe run_fastapi.py")
        print("\n   2. Espera unos segundos para que inicie")
        print("   3. Vuelve a ejecutar este script")
        print()
        return False
    
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return False


if __name__ == '__main__':
    success = verificar_fastapi()
    sys.exit(0 if success else 1)

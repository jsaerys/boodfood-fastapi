"""
Script para probar directamente las rutas de menú
"""
import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from app import create_app
from models import Usuario, MenuItem, Categoria

app = create_app('development')

print("\n" + "="*70)
print("PROBANDO RUTAS DE MENÚ DIRECTAMENTE")
print("="*70 + "\n")

with app.test_client() as client:
    with app.app_context():
        # Obtener usuario admin
        admin = Usuario.query.filter_by(rol='admin').first()
        
        if not admin:
            print("❌ No se encontró un usuario admin en la base de datos")
            sys.exit(1)
        
        print(f"✅ Usuario admin encontrado: {admin.email}")
        
        # Hacer login
        print("\n1️⃣ Haciendo login...")
        login_response = client.post('/login', data={
            'email': admin.email,
            'password': 'admin123'  # Ajusta la contraseña si es diferente
        }, follow_redirects=False)
        
        print(f"   Status: {login_response.status_code}")
        
        # Probar ruta de categorías
        print("\n2️⃣ Probando GET /admin/api/categorias/lista")
        cat_response = client.get('/admin/api/categorias/lista')
        print(f"   Status: {cat_response.status_code}")
        
        if cat_response.status_code == 200:
            categorias = cat_response.get_json()
            print(f"   ✅ {len(categorias)} categorías encontradas")
            for cat in categorias:
                print(f"      • {cat['nombre']}")
        else:
            print(f"   ❌ Error: {cat_response.data.decode()[:200]}")
        
        # Probar ruta de items
        print("\n3️⃣ Probando GET /admin/api/menu/items")
        items_response = client.get('/admin/api/menu/items')
        print(f"   Status: {items_response.status_code}")
        
        if items_response.status_code == 200:
            items = items_response.get_json()
            print(f"   ✅ {len(items)} items encontrados")
            for item in items[:5]:
                print(f"      • {item['nombre']} - ${item['precio']:,.0f}")
        else:
            print(f"   ❌ Error: {items_response.data.decode()[:200]}")
        
        # Verificar datos directamente de la BD
        print("\n4️⃣ Verificando datos directamente de la BD")
        categorias_bd = Categoria.query.all()
        items_bd = MenuItem.query.all()
        print(f"   ✅ Categorías en BD: {len(categorias_bd)}")
        print(f"   ✅ Items en BD: {len(items_bd)}")
        
        print("\n" + "="*70)
        print("RESUMEN")
        print("="*70)
        
        if cat_response.status_code == 200 and items_response.status_code == 200:
            print("✅ Todas las rutas funcionan correctamente")
            print("✅ El problema está en el frontend (JavaScript)")
            print("\nRecomendaciones:")
            print("1. Abre la consola del navegador (F12)")
            print("2. Ve a la pestaña 'Network' (Red)")
            print("3. Recarga la sección Menú")
            print("4. Busca las peticiones a /admin/api/categorias/lista y /admin/api/menu/items")
            print("5. Revisa qué código de estado devuelven (200, 401, 403, 500, etc.)")
        else:
            print("❌ Las rutas NO están funcionando correctamente")
            print("El problema está en el backend")
        
        print("="*70 + "\n")

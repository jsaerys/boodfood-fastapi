"""
Script para probar la conexión al nuevo dominio mysql.enlinea.sbs
"""
import sys
sys.path.append('.')

from app import create_app
from models import db, Mesa, MenuItem, Usuario

app = create_app()

with app.app_context():
    print("="*70)
    print("PRUEBA DE CONEXIÓN A mysql.enlinea.sbs")
    print("="*70)
    
    try:
        # Probar conexión básica
        print("\n1️⃣ Probando conexión básica...")
        db.session.execute(db.text('SELECT 1'))
        print("   ✅ Conexión exitosa")
        
        # Probar consulta de mesas
        print("\n2️⃣ Consultando mesas...")
        total_mesas = Mesa.query.count()
        print(f"   ✅ {total_mesas} mesas encontradas")
        
        # Probar consulta de menú
        print("\n3️⃣ Consultando items del menú...")
        total_items = MenuItem.query.count()
        print(f"   ✅ {total_items} items encontrados")
        
        # Probar consulta de usuarios
        print("\n4️⃣ Consultando usuarios...")
        total_usuarios = Usuario.query.count()
        print(f"   ✅ {total_usuarios} usuarios encontrados")
        
        print("\n" + "="*70)
        print("🎉 TODAS LAS PRUEBAS PASARON EXITOSAMENTE")
        print("="*70)
        print(f"\n✅ Dominio actualizado: mysql.enlinea.sbs:3311")
        print(f"✅ Base de datos: f58_brandon")
        print(f"✅ Usuario: brandon")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\n⚠️ Verifica:")
        print("   1. Que el dominio mysql.enlinea.sbs sea accesible")
        print("   2. Que el puerto 3311 esté abierto")
        print("   3. Que las credenciales sean correctas")
        print("   4. Que tengas conexión a internet")
        print("\n")
        sys.exit(1)

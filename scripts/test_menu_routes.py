"""
Script para probar las rutas de menú y ver qué está devolviendo
"""
import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from app import create_app
from models import MenuItem, Categoria

app = create_app('development')

with app.app_context():
    print("\n=== PRUEBA DE RUTAS DE MENÚ ===\n")
    
    # Verificar items del menú
    items = MenuItem.query.all()
    print(f"✅ Items en la base de datos: {len(items)}")
    
    if items:
        print("\n📋 Items encontrados:")
        for item in items[:5]:  # Mostrar solo los primeros 5
            print(f"  - ID: {item.id}, Nombre: {item.nombre}, Precio: {item.precio}, Disponible: {item.disponible}")
        
        print("\n🔍 Probando to_dict() del primer item:")
        try:
            dict_item = items[0].to_dict()
            print(f"  ✅ to_dict() funciona correctamente:")
            for key, value in dict_item.items():
                print(f"    {key}: {value}")
        except Exception as e:
            print(f"  ❌ Error en to_dict(): {e}")
    else:
        print("⚠️ No hay items en el menú")
    
    # Verificar categorías
    categorias = Categoria.query.all()
    print(f"\n✅ Categorías en la base de datos: {len(categorias)}")
    if categorias:
        for cat in categorias:
            print(f"  - ID: {cat.id}, Nombre: {cat.nombre}")
    
    print("\n=== FIN DE LA PRUEBA ===\n")

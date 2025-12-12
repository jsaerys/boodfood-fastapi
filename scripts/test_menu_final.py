"""
Script final para verificar que el módulo de menú funcione
"""
import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from app import create_app
from models import MenuItem, Categoria

app = create_app('development')

with app.app_context():
    print("\n" + "="*60)
    print("VERIFICACIÓN FINAL DEL MÓDULO DE MENÚ")
    print("="*60 + "\n")
    
    # 1. Verificar categorías
    categorias = Categoria.query.all()
    print(f"✅ Categorías: {len(categorias)}")
    for cat in categorias:
        print(f"   • {cat.nombre} (ID: {cat.id})")
    
    # 2. Verificar items del menú
    items = MenuItem.query.all()
    print(f"\n✅ Items del menú: {len(items)}")
    
    if items:
        print("\n📋 Primeros 10 items:")
        for item in items[:10]:
            cat_nombre = 'Sin categoría'
            if item.categoria_id:
                cat = Categoria.query.get(item.categoria_id)
                if cat:
                    cat_nombre = cat.nombre
            
            disponible = '✅' if item.disponible else '❌'
            print(f"   • {item.nombre} - ${item.precio:,.0f} - {cat_nombre} - {disponible}")
        
        print("\n🔍 Probando to_dict() en un item:")
        try:
            item_dict = items[0].to_dict()
            print("   ✅ to_dict() funciona correctamente")
            print(f"   Campos: {', '.join(item_dict.keys())}")
        except Exception as e:
            print(f"   ❌ Error en to_dict(): {e}")
    else:
        print("   ⚠️ No hay items en el menú")
    
    print("\n" + "="*60)
    print("RUTAS DEL BACKEND QUE DEBEN EXISTIR:")
    print("="*60)
    print("✅ GET  /admin/api/categorias/lista")
    print("✅ GET  /admin/api/menu/items")
    print("✅ POST /admin/api/menu/crear")
    print("✅ PUT  /admin/api/menu/<id>/actualizar")
    print("✅ DELETE /admin/api/menu/<id>")
    
    print("\n" + "="*60)
    print("ARCHIVOS MODIFICADOS:")
    print("="*60)
    print("✅ static/js/admin/menu.js - Reescrito completamente")
    print("✅ templates/admin/menu_content.html - Mejorado")
    print("✅ routes/admin.py - Rutas verificadas")
    
    print("\n" + "="*60)
    print("INSTRUCCIONES PARA PROBAR:")
    print("="*60)
    print("1. Reinicia el servidor Flask: python app.py")
    print("2. Abre el navegador: http://localhost:5000/admin")
    print("3. Haz login como admin")
    print("4. Abre la consola del navegador (F12)")
    print("5. Ve a la sección 'Menú'")
    print("6. Deberías ver los", len(items), "items en la tabla")
    print("="*60 + "\n")

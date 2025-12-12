"""
Script para verificar y actualizar las imágenes de los items del menú
"""
import sys
sys.path.insert(0, 'c:/Users/LENOVO/Desktop/Proyec11')

from app import create_app

app = create_app()

with app.app_context():
    from models import db, MenuItem
    
    print("🔍 Verificando imágenes de items del menú...\n")
    
    items = MenuItem.query.all()
    
    print(f"📊 Total items: {len(items)}\n")
    
    items_sin_imagen = []
    items_con_imagen = []
    
    for item in items:
        if item.imagen_url:
            items_con_imagen.append(item)
            print(f"✅ {item.nombre}: {item.imagen_url[:60]}...")
        else:
            items_sin_imagen.append(item)
            print(f"❌ {item.nombre}: SIN IMAGEN")
    
    print(f"\n📈 Resumen:")
    print(f"   Con imagen: {len(items_con_imagen)}")
    print(f"   Sin imagen: {len(items_sin_imagen)}")
    
    if items_sin_imagen:
        print(f"\n⚠️  Items sin imagen que necesitan actualización:")
        for item in items_sin_imagen:
            print(f"   - {item.nombre} (ID: {item.id})")

"""
Script para verificar si falta algún item y corregir el ID 1
"""
import sys
sys.path.insert(0, 'c:/Users/LENOVO/Desktop/Proyec11')

from app import create_app

app = create_app()

with app.app_context():
    from models import db, MenuItem
    
    print("🔍 Verificando item ID 1...\n")
    
    item1 = db.session.get(MenuItem, 1)
    
    if item1:
        print(f"✅ Item ID 1 encontrado: {item1.nombre}")
        print(f"   Imagen actual: {item1.imagen_url or 'SIN IMAGEN'}")
        
        # Actualizar con imagen de alitas
        item1.imagen_url = 'https://images.unsplash.com/photo-1608039829572-78524f79c4c7?w=600&h=400&fit=crop'
        db.session.commit()
        print(f"\n✅ Imagen actualizada!")
        print(f"   Nueva URL: {item1.imagen_url}")
    else:
        print("❌ Item ID 1 no encontrado en la base de datos")
    
    print("\n📊 Verificando todos los items:")
    items = MenuItem.query.order_by(MenuItem.id).all()
    
    sin_imagen = []
    
    for item in items:
        if item.imagen_url and item.imagen_url.startswith('http'):
            print(f"✅ ID {item.id:2d} - {item.nombre:30s} → OK")
        else:
            print(f"❌ ID {item.id:2d} - {item.nombre:30s} → FALTA IMAGEN")
            sin_imagen.append(item)
    
    if sin_imagen:
        print(f"\n⚠️  {len(sin_imagen)} items necesitan actualización")
    else:
        print(f"\n🎉 ¡Perfecto! Todos los {len(items)} items tienen imágenes!")

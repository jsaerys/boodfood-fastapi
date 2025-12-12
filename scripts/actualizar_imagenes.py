"""
Script para actualizar las imágenes de los items del menú con URLs de Unsplash
"""
import sys
sys.path.insert(0, 'c:/Users/LENOVO/Desktop/Proyec11')

from app import create_app

app = create_app()

with app.app_context():
    from models import db, MenuItem
    
    print("🖼️  Actualizando imágenes de items del menú...\n")
    
    # Mapeo de items sin imagen a URLs de imágenes de Unsplash
    imagenes = {
        13: 'https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=600',  # Arroz chino
        14: 'https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=600',  # Papas Fritas
        15: 'https://images.unsplash.com/photo-1608039829572-78524f79c4c7?w=600',  # Alitas BBQ
        16: 'https://images.unsplash.com/photo-1582169296194-e4d644c48063?w=600',  # Nachos con Queso
        17: 'https://images.unsplash.com/photo-1523677011781-c91d1bbe2f4d?w=600',  # Limonada
        18: 'https://images.unsplash.com/photo-1600271886742-f049cd451bba?w=600',  # Jugo de Naranja
        19: 'https://images.unsplash.com/photo-1629203851122-3726ecdf080e?w=600',  # Gaseosa
        20: 'https://images.unsplash.com/photo-1548839140-29a749e1cf4d?w=600',  # Agua
        21: 'https://images.unsplash.com/photo-1612392061787-2d078b3e573f?w=600',  # Perro Caliente
        22: 'https://images.unsplash.com/photo-1639024471283-03518883512d?w=600',  # Salchipapas
        23: 'https://images.unsplash.com/photo-1535958636474-b021ee887b13?w=600',  # Cerveza Leona
        24: 'https://images.unsplash.com/photo-1608270586620-248524c67de9?w=600',  # Cerveza Dorada
        25: 'https://images.unsplash.com/photo-1608270586620-248524c67de9?w=600',  # Cerveza Bogotá
    }
    
    actualizados = 0
    
    for item_id, imagen_url in imagenes.items():
        item = MenuItem.query.get(item_id)
        if item:
            item.imagen_url = imagen_url
            print(f"✅ {item.nombre}: {imagen_url}")
            actualizados += 1
        else:
            print(f"❌ Item ID {item_id} no encontrado")
    
    db.session.commit()
    
    print(f"\n✅ {actualizados} imágenes actualizadas correctamente!")
    print(f"\n🎨 Ahora todos los items tienen imágenes en:")
    print(f"   - Página principal (index)")
    print(f"   - Página de menú")
    print(f"   - Página de domicilios")

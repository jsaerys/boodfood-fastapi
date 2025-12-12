"""
Script para agregar productos específicos para pedidos en la piscina
"""
from flask import Flask
from models import db, MenuItem
from config import config

def agregar_productos_piscina():
    """Agregar productos aptos para pedir en la piscina"""
    
    # Productos para piscina
    productos = [
        {
            'nombre': 'Papas Fritas Grandes',
            'descripcion': 'Porción grande de papas fritas crujientes',
            'precio': 8000,
            'categoria_nombre': 'Snacks',
            'subcategoria': 'Acompañamientos',
            'disponible': True,
            'tiempo_preparacion': 10
        },
        {
            'nombre': 'Alitas BBQ (6 unidades)',
            'descripcion': 'Alitas de pollo con salsa BBQ',
            'precio': 15000,
            'categoria_nombre': 'Snacks',
            'subcategoria': 'Alitas',
            'disponible': True,
            'tiempo_preparacion': 15
        },
        {
            'nombre': 'Nachos con Queso',
            'descripcion': 'Nachos crujientes con queso fundido',
            'precio': 12000,
            'categoria_nombre': 'Snacks',
            'subcategoria': 'Acompañamientos',
            'disponible': True,
            'tiempo_preparacion': 10
        },
        {
            'nombre': 'Limonada Natural Personal',
            'descripcion': 'Refrescante limonada natural',
            'precio': 5000,
            'categoria_nombre': 'Bebidas',
            'subcategoria': 'Bebidas Naturales',
            'disponible': True,
            'tiempo_preparacion': 5
        },
        {
            'nombre': 'Jugo de Naranja Natural',
            'descripcion': 'Jugo de naranja recién exprimido',
            'precio': 6000,
            'categoria_nombre': 'Bebidas',
            'subcategoria': 'Bebidas Naturales',
            'disponible': True,
            'tiempo_preparacion': 5
        },
        {
            'nombre': 'Gaseosa Personal',
            'descripcion': 'Gaseosa fría de 350ml',
            'precio': 3000,
            'categoria_nombre': 'Bebidas',
            'subcategoria': 'Gaseosas',
            'disponible': True,
            'tiempo_preparacion': 2
        },
        {
            'nombre': 'Agua Embotellada',
            'descripcion': 'Agua mineral embotellada 500ml',
            'precio': 2500,
            'categoria_nombre': 'Bebidas',
            'subcategoria': 'Agua',
            'disponible': True,
            'tiempo_preparacion': 1
        },
        {
            'nombre': 'Hamburguesa Clásica',
            'descripcion': 'Hamburguesa de carne con queso, lechuga y tomate',
            'precio': 18000,
            'categoria_nombre': 'Comidas',
            'subcategoria': 'Hamburguesas',
            'disponible': True,
            'tiempo_preparacion': 20
        },
        {
            'nombre': 'Perro Caliente Especial',
            'descripcion': 'Hot dog con papitas, queso y salsas',
            'precio': 10000,
            'categoria_nombre': 'Comidas',
            'subcategoria': 'Perros Calientes',
            'disponible': True,
            'tiempo_preparacion': 15
        },
        {
            'nombre': 'Salchipapas',
            'descripcion': 'Papas fritas con salchicha y salsas',
            'precio': 9000,
            'categoria_nombre': 'Snacks',
            'subcategoria': 'Acompañamientos',
            'disponible': True,
            'tiempo_preparacion': 12
        }
    ]
    
    print("Agregando productos para piscina...")
    agregados = 0
    existentes = 0
    
    for prod_data in productos:
        # Verificar si ya existe
        existe = MenuItem.query.filter_by(
            nombre=prod_data['nombre'],
            restaurante_id=1
        ).first()
        
        if existe:
            print(f"  ⚠️  '{prod_data['nombre']}' ya existe")
            existentes += 1
            continue
        
        # Crear nuevo producto
        nuevo = MenuItem(
            restaurante_id=1,
            nombre=prod_data['nombre'],
            descripcion=prod_data['descripcion'],
            precio=prod_data['precio'],
            categoria_nombre=prod_data['categoria_nombre'],
            subcategoria=prod_data['subcategoria'],
            disponible=prod_data['disponible'],
            tiempo_preparacion=prod_data['tiempo_preparacion']
        )
        
        db.session.add(nuevo)
        print(f"  ✅ Agregado: {prod_data['nombre']} - ${prod_data['precio']:,}")
        agregados += 1
    
    db.session.commit()
    
    print(f"\n✅ Proceso completado:")
    print(f"   - Productos agregados: {agregados}")
    print(f"   - Productos existentes: {existentes}")
    print(f"   - Total: {agregados + existentes}")

if __name__ == '__main__':
    app = Flask(__name__)
    app.config.from_object(config['development'])
    db.init_app(app)
    
    with app.app_context():
        agregar_productos_piscina()

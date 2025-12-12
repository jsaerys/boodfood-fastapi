"""
Script para inicializar la base de datos
"""
from app import create_app
from models import db, Usuario, Mesa, Categoria, Servicio, Mesero, MenuItem
from werkzeug.security import generate_password_hash

def init_database():
    """Inicializar la base de datos con datos de ejemplo"""
    app = create_app('development')
    
    with app.app_context():
        print("Creando tablas...")
        db.create_all()
        
        # Verificar si ya existen datos
        if Usuario.query.first():
            print("La base de datos ya tiene datos. Saltando inicialización.")
            return
        
        print("Insertando datos iniciales...")
        
        # Usuario administrador
        admin = Usuario(
            nombre='Admin',
            apellido='BoodFood',
            email='admin@boodfood.com',
            telefono='3001234567',
            rol='admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Categorías
        categorias_data = [
            {'nombre': 'Entradas', 'descripcion': 'Aperitivos y entradas', 'orden': 1},
            {'nombre': 'Platos Principales', 'descripcion': 'Platos fuertes', 'orden': 2},
            {'nombre': 'Bebidas', 'descripcion': 'Bebidas frías y calientes', 'orden': 3},
            {'nombre': 'Postres', 'descripcion': 'Dulces y postres', 'orden': 4},
            {'nombre': 'Cócteles', 'descripcion': 'Bebidas alcohólicas', 'orden': 5}
        ]
        
        categorias = []
        for cat_data in categorias_data:
            cat = Categoria(**cat_data)
            db.session.add(cat)
            categorias.append(cat)
        
        db.session.flush()
        
        # Mesas
        mesas_data = [
            {'numero': 1, 'capacidad': 4, 'ubicacion': 'Interior', 'tipo': 'interior'},
            {'numero': 2, 'capacidad': 4, 'ubicacion': 'Interior', 'tipo': 'interior'},
            {'numero': 3, 'capacidad': 2, 'ubicacion': 'Interior', 'tipo': 'interior'},
            {'numero': 4, 'capacidad': 6, 'ubicacion': 'Terraza', 'tipo': 'terraza'},
            {'numero': 5, 'capacidad': 8, 'ubicacion': 'Terraza', 'tipo': 'vip'},
            {'numero': 6, 'capacidad': 4, 'ubicacion': 'Terraza', 'tipo': 'terraza'}
        ]
        
        for mesa_data in mesas_data:
            mesa = Mesa(**mesa_data)
            db.session.add(mesa)
        
        # Servicios
        servicios_data = [
            {
                'nombre': 'Entrada Piscina',
                'descripcion': 'Acceso a la piscina por día',
                'precio': 15000.00,
                'tipo': 'piscina',
                'capacidad': 50
            },
            {
                'nombre': 'Mesa de Billar',
                'descripcion': 'Alquiler de mesa de billar por hora',
                'precio': 10000.00,
                'tipo': 'billar',
                'capacidad': 4
            },
            {
                'nombre': 'Salón de Eventos',
                'descripcion': 'Alquiler de salón para eventos privados',
                'precio': 500000.00,
                'tipo': 'evento',
                'capacidad': 100
            }
        ]
        
        for servicio_data in servicios_data:
            servicio = Servicio(**servicio_data)
            db.session.add(servicio)
        
        # Meseros
        meseros_data = [
            {
                'nombre': 'Juan Pérez',
                'especialidad': 'Servicio VIP',
                'foto': ''
            },
            {
                'nombre': 'María García',
                'especialidad': 'Eventos',
                'foto': ''
            },
            {
                'nombre': 'Carlos Rodríguez',
                'especialidad': 'Terraza',
                'foto': ''
            }
        ]
        
        for mesero_data in meseros_data:
            mesero = Mesero(**mesero_data)
            db.session.add(mesero)
        
        # Items del menú
        menu_items_data = [
            # Entradas
            {'nombre': 'Ensalada César', 'descripcion': 'Lechuga romana, crutones, parmesano', 'precio': 18000, 'categoria_id': categorias[0].id, 'tipo': 'entrada'},
            {'nombre': 'Alitas BBQ', 'descripcion': '10 alitas con salsa BBQ', 'precio': 25000, 'categoria_id': categorias[0].id, 'tipo': 'entrada'},
            
            # Platos Principales
            {'nombre': 'Hamburguesa Clásica', 'descripcion': 'Carne de res, queso, lechuga, tomate', 'precio': 28000, 'categoria_id': categorias[1].id, 'tipo': 'comida'},
            {'nombre': 'Lomo de Cerdo', 'descripcion': 'Con papas y ensalada', 'precio': 35000, 'categoria_id': categorias[1].id, 'tipo': 'comida'},
            {'nombre': 'Pasta Alfredo', 'descripcion': 'Fettuccine en salsa Alfredo con pollo', 'precio': 32000, 'categoria_id': categorias[1].id, 'tipo': 'comida'},
            
            # Bebidas
            {'nombre': 'Limonada Natural', 'descripcion': 'Limonada fresca', 'precio': 8000, 'categoria_id': categorias[2].id, 'tipo': 'bebida'},
            {'nombre': 'Jugo de Naranja', 'descripcion': 'Jugo natural de naranja', 'precio': 9000, 'categoria_id': categorias[2].id, 'tipo': 'bebida'},
            {'nombre': 'Gaseosa', 'descripcion': 'Coca Cola, Sprite, Fanta', 'precio': 5000, 'categoria_id': categorias[2].id, 'tipo': 'bebida'},
            
            # Postres
            {'nombre': 'Brownie con Helado', 'descripcion': 'Brownie caliente con helado de vainilla', 'precio': 15000, 'categoria_id': categorias[3].id, 'tipo': 'postre'},
            {'nombre': 'Cheesecake', 'descripcion': 'Tarta de queso con frutos rojos', 'precio': 18000, 'categoria_id': categorias[3].id, 'tipo': 'postre'},
            
            # Cócteles
            {'nombre': 'Mojito', 'descripcion': 'Ron, menta, limón, soda', 'precio': 22000, 'categoria_id': categorias[4].id, 'tipo': 'bebida'},
            {'nombre': 'Piña Colada', 'descripcion': 'Ron, piña, coco', 'precio': 24000, 'categoria_id': categorias[4].id, 'tipo': 'bebida'}
        ]
        
        for item_data in menu_items_data:
            item = MenuItem(**item_data)
            db.session.add(item)
        
        # Commit de todos los datos
        db.session.commit()
        
        print("✅ Base de datos inicializada exitosamente!")
        print("\nCredenciales de administrador:")
        print("Email: admin@boodfood.com")
        print("Password: admin123")


if __name__ == '__main__':
    init_database()

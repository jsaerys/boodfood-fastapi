"""
Script para limpiar todos los pedidos de la base de datos
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models import db, Pedido, PedidoItem

def limpiar_pedidos():
    app = create_app('development')
    with app.app_context():
        try:
            # Primero eliminar items de pedidos
            num_items = PedidoItem.query.delete()
            print(f'✅ {num_items} items de pedidos eliminados')
            
            # Luego eliminar pedidos
            num_pedidos = Pedido.query.delete()
            print(f'✅ {num_pedidos} pedidos eliminados')
            
            db.session.commit()
            print('✅ Base de datos limpiada exitosamente')
            
        except Exception as e:
            db.session.rollback()
            print(f'❌ Error: {e}')

if __name__ == '__main__':
    limpiar_pedidos()

import sys
sys.path.insert(0, 'c:/Users/LENOVO/Desktop/Proyec11')

from config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

class Mesa(db.Model):
    __tablename__ = 'mesas'
    id = db.Column(db.Integer, primary_key=True)
    numero_mesa = db.Column(db.Integer, nullable=False)
    capacidad = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.String(20), default='disponible')
    tipo_mesa = db.Column(db.String(50))
    ubicacion = db.Column(db.String(100))

with app.app_context():
    mesas = Mesa.query.all()
    print(f'\n📊 Total de mesas: {len(mesas)}\n')
    print('=' * 70)
    
    if len(mesas) == 0:
        print('⚠️  NO HAY MESAS EN LA BASE DE DATOS')
        print('\n💡 Necesitamos agregar mesas para que el cliente pueda reservar.\n')
    else:
        for m in mesas:
            estado_icon = '✅' if m.estado == 'disponible' else '❌'
            print(f'{estado_icon} Mesa #{m.numero_mesa:2d} | Capacidad: {m.capacidad} personas | Estado: {m.estado:15s} | Tipo: {m.tipo_mesa}')
    
    print('=' * 70)
    
    # Contar por estado
    disponibles = len([m for m in mesas if m.estado == 'disponible'])
    ocupadas = len([m for m in mesas if m.estado == 'ocupada'])
    reservadas = len([m for m in mesas if m.estado == 'reservada'])
    
    print(f'\n📈 Resumen:')
    print(f'   ✅ Disponibles: {disponibles}')
    print(f'   🔴 Ocupadas: {ocupadas}')
    print(f'   📅 Reservadas: {reservadas}')

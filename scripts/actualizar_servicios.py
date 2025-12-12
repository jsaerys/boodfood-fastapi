"""
Script para actualizar información de servicios
"""
from flask import Flask
from models import db, Servicio
from config import config

def actualizar_servicios():
    """Actualizar información de servicios"""
    
    # Obtener servicios
    piscina = Servicio.query.filter_by(tipo='piscina').first()
    billar = Servicio.query.filter_by(tipo='billar').first()
    evento = Servicio.query.filter_by(tipo='evento').first()
    
    if piscina:
        piscina.nombre = 'Entrada Piscina'
        piscina.descripcion = 'Disfruta de un día refrescante en nuestra piscina con área para niños y adultos. Precio por persona.'
        piscina.precio = 10000
        piscina.capacidad = 50
        piscina.disponible = True
        print(f'✅ Piscina actualizada: ${piscina.precio}/persona')
    
    if billar:
        billar.nombre = 'Mesa de Billar'
        billar.descripcion = 'Alquiler de mesa de billar por hora. Incluye tacos y bolas. Precio por hora.'
        billar.precio = 15000
        billar.capacidad = 8
        billar.disponible = True
        print(f'✅ Billar actualizado: ${billar.precio}/hora')
    
    if evento:
        evento.nombre = 'Salón de Eventos'
        evento.descripcion = 'Reserva nuestro salón para eventos especiales, cumpleaños, reuniones corporativas y más. Precio por persona.'
        evento.precio = 50000
        evento.capacidad = 200
        evento.disponible = True
        print(f'✅ Evento actualizado: ${evento.precio}/persona')
    
    db.session.commit()
    print('\n✅ Todos los servicios actualizados correctamente!')

if __name__ == '__main__':
    app = Flask(__name__)
    app.config.from_object(config['development'])
    db.init_app(app)
    
    with app.app_context():
        actualizar_servicios()

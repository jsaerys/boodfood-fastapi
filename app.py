"""
Aplicación principal BoodFood
Sistema de gestión para restaurante con reservas, pedidos y múltiples paneles
"""
from flask import Flask, render_template
from flask_login import LoginManager
from config import config
from models import db, Usuario

# Importar blueprints
from routes.auth import auth_bp
from routes.main import main_bp
from routes.reservas import reservas_bp
from routes.pedidos import pedidos_bp
from routes.cocina import cocina_bp
from routes.caja import caja_bp
from routes.admin import admin_bp


def create_app(config_name='default'):
    """Factory para crear la aplicación Flask"""
    app = Flask(__name__)
    
    # Cargar configuración
    app.config.from_object(config[config_name])
    
    # Inicializar extensiones
    db.init_app(app)
    
    # Configurar Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))
    
    # Registrar blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(reservas_bp)
    app.register_blueprint(pedidos_bp)
    app.register_blueprint(cocina_bp)
    app.register_blueprint(caja_bp)
    app.register_blueprint(admin_bp)
    
    # Manejador de errores
    @app.errorhandler(404)
    def not_found(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    # Crear tablas si no existen
    with app.app_context():
        db.create_all()
    
    return app


if __name__ == '__main__':
    app = create_app('development')
    app.run(host='0.0.0.0', port=5000, debug=True)

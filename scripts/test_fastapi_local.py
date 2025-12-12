"""
Script de verificación que usa TestClient para llamar a la app FastAPI
sin necesidad de ejecutar un servidor uvicorn separado.
"""
from fastapi.testclient import TestClient
from fastapi_app import create_fastapi_app
from app import create_app as create_flask_app


def main():
    # Crear contexto de Flask para que Flask-SQLAlchemy funcione dentro de dependencias
    flask_app = create_flask_app('development')
    with flask_app.app_context():
        app = create_fastapi_app()
        client = TestClient(app)

        print('GET /api')
        r = client.get('/api')
        print(r.status_code)
        print(r.json())

        print('\nGET /api/v1/mesas')
        r2 = client.get('/api/v1/mesas')
        print(r2.status_code)
        try:
            print(r2.json())
        except Exception as e:
            print('No JSON or error:', e)


if __name__ == '__main__':
    main()

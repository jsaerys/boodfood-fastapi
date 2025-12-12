"""
FastAPI App - Módulo principal
Sistema de API REST moderno para BoodFood
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from contextlib import asynccontextmanager
import importlib
import traceback

# Importar rutas desde los routers relativos
from . import routers
from .routers import mesas, menu, pedidos, reservas, usuarios, auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manejo del ciclo de vida de la aplicación"""
    # Startup
    print("🚀 FastAPI iniciando...")

    # Crear una instancia mínima de la aplicación Flask y almacenarla en el
    # state de FastAPI. No se hace push del contexto aquí porque los
    # manejadores de petición pueden ejecutarse en hilos/greenlets distintos;
    # en su lugar abriremos un `app_context` por petición en la dependencia.
    try:
        # Importar la factory de Flask en tiempo de ejecución para evitar
        # fallos si Flask no está instalado cuando se importa el paquete.
        try:
            flask_module = importlib.import_module('app.app')
            create_flask_app = getattr(flask_module, 'create_app', None)
        except Exception:
            create_flask_app = None

        if create_flask_app:
            flask_app = create_flask_app('development')
            # Guardar la app para que las dependencias la usen por petición
            app.state._flask_app = flask_app
            print("✅ Flask app instance stored on FastAPI state")
        else:
            print("⚠️ Flask factory `create_app` not available; skipping Flask integration")
    except Exception as e:
        print(f"⚠️ Could not create Flask app instance: {e}")
        traceback.print_exc()

    yield

    # Shutdown (limpiar la referencia a la app Flask si existe)
    try:
        if hasattr(app.state, '_flask_app'):
            delattr(app.state, '_flask_app')
            print("👋 Flask app reference removed from state")
    except Exception as e:
        print(f"⚠️ Error removing Flask app reference: {e}")

    print("👋 FastAPI cerrando...")


def create_fastapi_app():
    """Factory para crear la aplicación FastAPI"""
    
    app = FastAPI(
        title="BoodFood API",
        description="API REST moderna para sistema de gestión de restaurante",
        version="1.0.0",
        lifespan=lifespan,
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json"
    )
    
    # Configurar CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # En producción, especificar dominios
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Registrar rutas
    app.include_router(auth.router, prefix="/api/v1", tags=["Autenticación"])
    app.include_router(mesas.router, prefix="/api/v1", tags=["Mesas"])
    app.include_router(menu.router, prefix="/api/v1", tags=["Menú"])
    app.include_router(pedidos.router, prefix="/api/v1", tags=["Pedidos"])
    app.include_router(reservas.router, prefix="/api/v1", tags=["Reservas"])
    app.include_router(usuarios.router, prefix="/api/v1", tags=["Usuarios"])
    
    # Ruta raíz
    @app.get("/api")
    async def root():
        return {
            "message": "BoodFood API v1.0",
            "status": "online",
            "docs": "/api/docs",
            "endpoints": {
                "auth": "/api/v1/auth",
                "mesas": "/api/v1/mesas",
                "menu": "/api/v1/menu",
                "pedidos": "/api/v1/pedidos",
                "reservas": "/api/v1/reservas",
                "usuarios": "/api/v1/usuarios"
            }
        }

    # Redirecciones convenientes para usuarios que visiten las rutas por defecto
    @app.get("/", include_in_schema=False)
    async def root_redirect():
        return RedirectResponse(url="/api")

    @app.get("/docs", include_in_schema=False)
    async def docs_redirect():
        return RedirectResponse(url="/api/docs")

    @app.get("/openapi.json", include_in_schema=False)
    async def openapi_redirect():
        return RedirectResponse(url="/api/openapi.json")
    
    # Manejador de errores
    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        return JSONResponse(
            status_code=500,
            content={
                "error": "Error interno del servidor",
                "detail": str(exc)
            }
        )
    
    return app

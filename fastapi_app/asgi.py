"""
ASGI entrypoint for uvicorn: exposes `app` created by the factory.
This allows running `uvicorn fastapi_app.asgi:app`.
"""
from . import create_fastapi_app

app = create_fastapi_app()

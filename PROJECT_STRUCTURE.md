# 📁 Estructura del Proyecto - BoodFood

```
boodfood-fastapi/
├── src/                           # Código fuente principal
│   ├── app/                        # Aplicación Flask (Frontend)
│   │   ├── app.py                 # Factory de Flask
│   │   ├── models/                # Modelos de BD
│   │   ├── routes/                # Blueprints Flask
│   │   ├── templates/             # Templates HTML
│   │   ├── static/                # CSS, JS, imágenes
│   │   ├── utils/                 # Utilidades
│   │   ├── socket_events.py       # WebSocket con SocketIO
│   │   └── __init__.py
│   │
│   └── fastapi_app/               # Aplicación FastAPI (API REST)
│       ├── asgi.py                # Punto de entrada ASGI
│       ├── __init__.py
│       ├── routers/               # Rutas de la API
│       ├── services/              # Lógica de negocio
│       ├── repositories/          # Acceso a datos
│       ├── schemas/               # Modelos Pydantic
│       └── models/
│
├── config/                         # Configuración
│   ├── config.py                  # Configuración de BD y app
│   └── __init__.py
│
├── scripts/                        # Scripts y utilidades
│   ├── init_db.py                 # Inicializar BD
│   ├── run_*.py                   # Scripts de ejecución
│   ├── test_*.py                  # Tests
│   ├── *admin*.py                 # Scripts de admin
│   └── ...otros scripts
│
├── deployment/                     # Configuración de despliegue
│   ├── Dockerfile                 # Imagen Docker para API
│   ├── Dockerfile.frontend        # Imagen Docker para Frontend
│   ├── docker-compose.yml         # Orquestación contenedores
│   ├── docker-compose.split.yml   # Orquestación (separado)
│   ├── deploy.sh                  # Script despliegue Linux
│   └── deploy.bat                 # Script despliegue Windows
│
├── docs/                           # Documentación
│   ├── README_DEPLOYMENT.md       # Guía de despliegue
│   ├── DEPLOY_COOL_ENLINEA.md     # Instrucciones hosting
│   └── GITHUB_PUSH_STEPS.md       # Pasos para Git/GitHub
│
├── tests/                          # Pruebas unitarias
│   └── test_*.py
│
├── requirements.txt                # Dependencias Python
├── wsgi.py                        # Punto de entrada Flask
├── asgi.py                        # Punto de entrada FastAPI
├── README.md                      # Información del proyecto
│
├── .env                           # Variables de entorno (ignorado)
├── .env.example                   # Plantilla de .env
├── .gitignore                     # Git ignore
└── docker-ignore                  # Docker ignore
```

## 🚀 Puntos de Entrada

- **Frontend (Flask)**: `wsgi.py` → `python wsgi.py`
- **API (FastAPI)**: `asgi.py` → `python -m uvicorn asgi:app --port 3311`

## 📂 Cambios Principales

- ✅ Código fuente organizado en `/src`
- ✅ Configuración centralizada en `/config`
- ✅ Scripts y tests en `/scripts` y `/tests`
- ✅ Docker y deployment en `/deployment`
- ✅ Documentación en `/docs`
- ✅ Raíz limpia con solo puntos de entrada necesarios

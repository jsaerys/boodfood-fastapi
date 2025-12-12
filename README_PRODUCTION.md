# 🍽️ BoodFood - Sistema de Gestión de Restaurante

**Aplicación web full-stack para gestión de restaurantes con reservas, pedidos y múltiples paneles.**

---

## 📋 Requisitos

- **Python 3.8+**
- **MySQL 8.0+** (remota: mysql.enlinea.sbs:3311)
- **Git**

---

## 🚀 Instalación Rápida

### 1. Clonar repositorio
```bash
git clone https://github.com/jsaerys/boodfood-fastapi.git
cd boodfood-fastapi
```

### 2. Crear entorno virtual
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Ejecutar script de despliegue
```bash
chmod +x deploy.sh
./deploy.sh
```

---

## 🔧 Estructura del Proyecto

```
boodfood-fastapi/
├── src/
│   ├── app/                    # Flask Frontend
│   │   ├── routes/            # Blueprints (auth, pedidos, reservas, etc)
│   │   ├── templates/         # HTML Jinja2
│   │   ├── static/            # CSS, JS, uploads
│   │   ├── models/            # SQLAlchemy ORM
│   │   ├── utils/             # Funciones auxiliares
│   │   └── app.py             # Factory de Flask
│   │
│   └── fastapi_app/           # FastAPI REST API
│       ├── routers/           # Endpoints (auth, menu, pedidos, etc)
│       ├── services/          # Lógica de negocio
│       ├── repositories/      # Acceso a datos
│       ├── schemas/           # Validación Pydantic
│       ├── models/            # Modelos compartidos
│       ├── dependencies.py    # Inyección de dependencias
│       └── __init__.py        # Factory de FastAPI
│
├── config/
│   └── config.py              # Configuración centralizada
│
├── deployment/                # Scripts de despliegue
├── docs/                      # Documentación
├── wsgi.py                    # Punto entrada Flask (Gunicorn)
├── asgi.py                    # Punto entrada FastAPI (Uvicorn)
├── requirements.txt           # Dependencias Python
├── .env.example               # Plantilla de variables
└── DEPLOYMENT_GUIDE.md        # Guía completa de despliegue
```

---

## ▶️ Ejecutar en Desarrollo

### Terminal 1 - FastAPI (API REST)
```bash
python -m uvicorn asgi:app --host 0.0.0.0 --port 3311 --reload
```
📍 Acceso: http://localhost:3311/docs

### Terminal 2 - Flask (Frontend)
```bash
python wsgi.py
```
📍 Acceso: http://localhost:5001

---

## 📡 Endpoints Principales

### FastAPI (REST API)
```
GET    /docs                 # Swagger UI
GET    /redoc                # ReDoc
POST   /api/auth/login       # Login usuario
POST   /api/auth/register    # Registro
GET    /api/menu             # Listar menú
POST   /api/pedidos          # Crear pedido
GET    /api/pedidos/{id}     # Obtener pedido
POST   /api/reservas         # Crear reserva
GET    /api/mesas            # Listar mesas
```

### Flask (Web)
```
/                  # Dashboard
/menu              # Menú
/pedidos           # Gestión de pedidos
/reservas          # Gestión de reservas
/admin             # Panel administrativo
/login             # Login
/registro          # Registro de usuario
```

---

## 🗄️ Base de Datos

- **Servidor**: mysql.enlinea.sbs:3311
- **Base**: f58_brandon
- **Usuario**: brandon
- **Tablas**: usuarios, mesas, pedidos, reservas, menu_items, categorias, servicios, etc.

---

## 🔐 Variables de Entorno (.env)

```env
FLASK_ENV=production
DEBUG=False
SECRET_KEY=tu-clave-muy-segura-aqui
JWT_SECRET_KEY=tu-jwt-secret-aqui
DATABASE_URL=mysql+pymysql://brandon:brandonc@mysql.enlinea.sbs:3311/f58_brandon
```

---

## 📦 Despliegue en Producción

Ver [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) para:
- Despliegue con Gunicorn + Uvicorn
- Configuración de Supervisor
- Configuración de Nginx reverso proxy
- Certificados SSL
- Troubleshooting

---

## 🧪 Testing

```bash
# Verificar imports
python -c "from src.app.app import create_app; print('✅ Flask OK')"
python -c "from src.fastapi_app import create_fastapi_app; print('✅ FastAPI OK')"

# Verificar BD
python -c "from config.config import Config; print('✅ Config OK')"
```

---

## 📝 Logs

```bash
tail -f logs/flask.log      # Logs de Flask
tail -f logs/fastapi.log    # Logs de FastAPI
```

---

## 🤝 Contribuir

1. Fork el repositorio
2. Crea una rama (`git checkout -b feature/nueva-feature`)
3. Commit cambios (`git commit -am 'Add nueva feature'`)
4. Push a la rama (`git push origin feature/nueva-feature`)
5. Abre un Pull Request

---

## 📄 Licencia

MIT

---

## 💬 Soporte

Para problemas o preguntas:
- Revisar [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- Verificar logs en carpeta `logs/`
- Consultar documentación de FastAPI: http://localhost:3311/docs

---

**Última actualización**: Diciembre 12, 2025  
**Versión**: 1.0.0  
**Estado**: ✅ Listo para producción

# FastAPI - BoodFood API REST

API REST moderna y completamente documentada para el sistema de gestión de restaurante BoodFood.

## 🚀 Características

- ✅ **API REST completa** con FastAPI
- ✅ **Autenticación JWT** para endpoints protegidos
- ✅ **Validación automática** con Pydantic
- ✅ **Documentación interactiva** (Swagger UI y ReDoc)
- ✅ **Arquitectura modular** separada por recursos
- ✅ **Compatibilidad total** con el sistema Flask existente
- ✅ **Base de datos compartida** con SQLAlchemy

## 📁 Estructura del Proyecto

```
fastapi_app/
├── __init__.py              # Aplicación principal FastAPI
├── dependencies.py          # Dependencias comunes (auth, DB)
├── schemas/
│   └── __init__.py         # Esquemas Pydantic para validación
└── routes/
    ├── auth.py             # Autenticación y registro
    ├── mesas.py            # Gestión de mesas
    ├── menu.py             # Gestión del menú
    ├── pedidos.py          # Gestión de pedidos
    ├── reservas.py         # Gestión de reservas
    └── usuarios.py         # Gestión de usuarios
```

## 🔧 Instalación

### 1. Instalar dependencias

```powershell
pip install -r requirements.txt
```

### 2. Ejecutar solo FastAPI

```powershell
python run_fastapi.py
```

La API estará disponible en:
- **API Base**: http://localhost:8000/api
- **Swagger Docs**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

### 3. Ejecutar Flask + FastAPI (ambos servidores)

```powershell
python run_both.py
```

Esto ejecutará:
- **Flask** en http://localhost:5000 (Web + Templates + SocketIO)
- **FastAPI** en http://localhost:8000 (REST API)

## 📚 Documentación de la API

### Autenticación

#### POST `/api/v1/auth/login`
Iniciar sesión y obtener token JWT.

**Request:**
```json
{
  "email": "usuario@example.com",
  "password": "contraseña"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "nombre": "Brandon",
    "email": "usuario@example.com",
    "rol": "admin"
  }
}
```

#### POST `/api/v1/auth/register`
Registrar nuevo usuario.

**Request:**
```json
{
  "nombre": "Brandon",
  "apellido": "Perez",
  "email": "nuevo@example.com",
  "password": "contraseña123",
  "telefono": "3001234567"
}
```

### Headers para Endpoints Protegidos

Para acceder a endpoints protegidos, incluye el token JWT en el header:

```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

### Mesas

#### GET `/api/v1/mesas`
Obtener lista de mesas.

**Query Params:**
- `disponible` (bool): Filtrar por disponibilidad
- `tipo` (string): Filtrar por tipo (interior, terraza, vip)

**Response:**
```json
[
  {
    "id": 1,
    "numero": 1,
    "capacidad": 4,
    "ubicacion": "Interior",
    "tipo": "interior",
    "disponible": true,
    "ocupada": false
  }
]
```

#### POST `/api/v1/mesas` 🔒 Admin
Crear nueva mesa.

**Request:**
```json
{
  "numero": 10,
  "capacidad": 6,
  "ubicacion": "Terraza",
  "tipo": "terraza",
  "disponible": true
}
```

### Menú

#### GET `/api/v1/menu`
Obtener items del menú.

**Query Params:**
- `disponible` (bool): Solo items disponibles
- `categoria` (string): Filtrar por categoría
- `destacado` (bool): Solo items destacados

#### POST `/api/v1/menu` 🔒 Admin
Crear nuevo item del menú.

**Request:**
```json
{
  "nombre": "Hamburguesa Premium",
  "descripcion": "Con queso cheddar y bacon",
  "precio": 25000,
  "categoria_nombre": "Hamburguesas",
  "imagen_url": "https://example.com/imagen.jpg",
  "disponible": true,
  "destacado": false,
  "restaurante_id": 1
}
```

### Pedidos

#### GET `/api/v1/pedidos` 🔒
Obtener pedidos del usuario (o todos si es admin).

#### POST `/api/v1/pedidos` 🔒
Crear nuevo pedido.

**Request:**
```json
{
  "tipo_servicio": "mesa",
  "mesa_id": 5,
  "metodo_pago": "efectivo",
  "items": [
    {
      "menu_item_id": 2,
      "cantidad": 2,
      "precio_unitario": 25000
    },
    {
      "menu_item_id": 5,
      "cantidad": 1,
      "precio_unitario": 15000
    }
  ]
}
```

**Response:**
```json
{
  "id": 10,
  "codigo_pedido": "PED12AB34CD",
  "tipo_servicio": "mesa",
  "mesa_id": 5,
  "subtotal": 65000,
  "total": 65000,
  "estado": "pendiente",
  "metodo_pago": "efectivo",
  "fecha_pedido": "2025-11-27T10:30:00",
  "items": [...]
}
```

### Reservas

#### POST `/api/v1/reservas` 🔒
Crear nueva reserva.

**Request:**
```json
{
  "mesa_id": 3,
  "fecha_reserva": "2025-11-28T20:00:00",
  "num_personas": 4,
  "nombre_cliente": "Brandon Perez",
  "telefono_cliente": "3001234567",
  "email_cliente": "brandon@example.com",
  "ocasion_especial": "Cumpleaños",
  "notas": "Mesa cerca de la ventana"
}
```

### Usuarios

#### GET `/api/v1/usuarios/me` 🔒
Obtener perfil del usuario actual.

#### GET `/api/v1/usuarios` 🔒 Admin
Obtener lista de usuarios (solo admin).

## 🔐 Roles y Permisos

- **Cliente**: Acceso a sus propios pedidos y reservas
- **Admin**: Acceso completo a todos los recursos

Los endpoints marcados con 🔒 requieren autenticación.
Los endpoints marcados con 🔒 Admin requieren rol de administrador.

## 🧪 Testing con Swagger UI

1. Abre http://localhost:8000/api/docs
2. Haz clic en "Authorize" (candado verde)
3. Obtén un token haciendo POST a `/api/v1/auth/login`
4. Copia el `access_token` de la respuesta
5. Pégalo en el campo "Value" del diálogo de autorización
6. Ahora puedes probar todos los endpoints protegidos

## 🔄 Integración con Flask

FastAPI comparte la misma base de datos que Flask a través de SQLAlchemy:

- **Modelos**: Definidos en `models/__init__.py`
- **Base de datos**: MySQL remota en `mysql.enlinea.sbs:3311`
- **Configuración**: Compartida desde `config.py`

Ambos sistemas pueden coexistir y operar sobre los mismos datos.

## 📊 Ventajas de FastAPI sobre Flask

1. **Performance**: 2-3x más rápido que Flask
2. **Type Safety**: Validación automática con Pydantic
3. **Documentación**: Swagger UI y ReDoc automáticos
4. **Async**: Soporte nativo para operaciones asíncronas
5. **Modern Python**: Usa type hints y features de Python 3.10+

## 🚀 Endpoints Disponibles

| Método | Endpoint | Descripción | Auth |
|--------|----------|-------------|------|
| POST | `/api/v1/auth/login` | Iniciar sesión | ❌ |
| POST | `/api/v1/auth/register` | Registrar usuario | ❌ |
| GET | `/api/v1/mesas` | Listar mesas | ❌ |
| GET | `/api/v1/mesas/{id}` | Obtener mesa | ❌ |
| POST | `/api/v1/mesas` | Crear mesa | 🔒 Admin |
| PUT | `/api/v1/mesas/{id}` | Actualizar mesa | 🔒 Admin |
| DELETE | `/api/v1/mesas/{id}` | Eliminar mesa | 🔒 Admin |
| GET | `/api/v1/menu` | Listar items | ❌ |
| GET | `/api/v1/menu/{id}` | Obtener item | ❌ |
| POST | `/api/v1/menu` | Crear item | 🔒 Admin |
| PUT | `/api/v1/menu/{id}` | Actualizar item | 🔒 Admin |
| DELETE | `/api/v1/menu/{id}` | Eliminar item | 🔒 Admin |
| GET | `/api/v1/categorias` | Listar categorías | ❌ |
| GET | `/api/v1/pedidos` | Listar pedidos | 🔒 |
| GET | `/api/v1/pedidos/{id}` | Obtener pedido | 🔒 |
| POST | `/api/v1/pedidos` | Crear pedido | 🔒 |
| PUT | `/api/v1/pedidos/{id}` | Actualizar pedido | 🔒 |
| GET | `/api/v1/reservas` | Listar reservas | 🔒 |
| GET | `/api/v1/reservas/{id}` | Obtener reserva | 🔒 |
| POST | `/api/v1/reservas` | Crear reserva | 🔒 |
| PUT | `/api/v1/reservas/{id}` | Actualizar reserva | 🔒 |
| DELETE | `/api/v1/reservas/{id}` | Cancelar reserva | 🔒 |
| GET | `/api/v1/usuarios` | Listar usuarios | 🔒 Admin |
| GET | `/api/v1/usuarios/me` | Mi perfil | 🔒 |
| GET | `/api/v1/usuarios/{id}` | Obtener usuario | 🔒 |
| POST | `/api/v1/usuarios` | Crear usuario | 🔒 Admin |
| PUT | `/api/v1/usuarios/{id}` | Actualizar usuario | 🔒 |
| DELETE | `/api/v1/usuarios/{id}` | Eliminar usuario | 🔒 Admin |

## 💡 Notas

- Los tokens JWT expiran en 24 horas
- Los endpoints públicos no requieren autenticación
- Los endpoints protegidos requieren token JWT válido
- Solo los administradores pueden crear/editar/eliminar recursos

## 🐛 Debugging

Para ver logs detallados:

```powershell
# En run_fastapi.py, cambiar log_level
uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
```

## 📝 Licencia

Parte del sistema BoodFood - © 2025

# Ejemplos de Uso de la API - BoodFood FastAPI

## 🔐 Autenticación

### 1. Registrar nuevo usuario

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Juan",
    "apellido": "Pérez",
    "email": "juan@example.com",
    "password": "mipassword123",
    "telefono": "3001234567",
    "direccion": "Calle 123"
  }'
```

### 2. Iniciar sesión

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "juan@example.com",
    "password": "mipassword123"
  }'
```

**Respuesta:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": 5,
    "nombre": "Juan",
    "apellido": "Pérez",
    "email": "juan@example.com",
    "rol": "cliente"
  }
}
```

**Guardar el token para usarlo en las siguientes peticiones:**
```bash
export TOKEN="eyJ0eXAiOiJKV1QiLCJhbGc..."
```

---

## 🪑 Mesas

### 1. Listar todas las mesas

```bash
curl "http://localhost:8000/api/v1/mesas"
```

### 2. Filtrar mesas disponibles

```bash
curl "http://localhost:8000/api/v1/mesas?disponible=true"
```

### 3. Filtrar por tipo

```bash
curl "http://localhost:8000/api/v1/mesas?tipo=terraza"
```

### 4. Obtener mesa específica

```bash
curl "http://localhost:8000/api/v1/mesas/5"
```

### 5. Crear nueva mesa (Admin)

```bash
curl -X POST "http://localhost:8000/api/v1/mesas" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "numero": 50,
    "capacidad": 8,
    "ubicacion": "Terraza VIP",
    "tipo": "vip",
    "disponible": true
  }'
```

### 6. Actualizar mesa (Admin)

```bash
curl -X PUT "http://localhost:8000/api/v1/mesas/50" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "disponible": false
  }'
```

---

## 🍔 Menú

### 1. Listar todos los items

```bash
curl "http://localhost:8000/api/v1/menu"
```

### 2. Solo items disponibles

```bash
curl "http://localhost:8000/api/v1/menu?disponible=true"
```

### 3. Filtrar por categoría

```bash
curl "http://localhost:8000/api/v1/menu?categoria=Hamburguesas"
```

### 4. Solo items destacados

```bash
curl "http://localhost:8000/api/v1/menu?destacado=true"
```

### 5. Obtener item específico

```bash
curl "http://localhost:8000/api/v1/menu/2"
```

### 6. Listar categorías

```bash
curl "http://localhost:8000/api/v1/categorias"
```

### 7. Crear nuevo item (Admin)

```bash
curl -X POST "http://localhost:8000/api/v1/menu" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Pizza Hawaiana",
    "descripcion": "Pizza con piña y jamón",
    "precio": 35000,
    "categoria_nombre": "Pizzas",
    "imagen_url": "https://example.com/pizza.jpg",
    "disponible": true,
    "destacado": false,
    "restaurante_id": 1
  }'
```

### 8. Actualizar item (Admin)

```bash
curl -X PUT "http://localhost:8000/api/v1/menu/25" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "precio": 32000,
    "destacado": true
  }'
```

---

## 📦 Pedidos

### 1. Listar mis pedidos

```bash
curl "http://localhost:8000/api/v1/pedidos" \
  -H "Authorization: Bearer $TOKEN"
```

### 2. Filtrar por estado

```bash
curl "http://localhost:8000/api/v1/pedidos?estado=pendiente" \
  -H "Authorization: Bearer $TOKEN"
```

### 3. Crear pedido para mesa

```bash
curl -X POST "http://localhost:8000/api/v1/pedidos" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "tipo_servicio": "mesa",
    "mesa_id": 10,
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
  }'
```

### 4. Crear pedido para domicilio

```bash
curl -X POST "http://localhost:8000/api/v1/pedidos" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "tipo_servicio": "domicilio",
    "metodo_pago": "tarjeta",
    "direccion_entrega": "Calle 50 #10-20",
    "telefono_contacto": "3009876543",
    "instrucciones_entrega": "Timbre apartamento 302",
    "items": [
      {
        "menu_item_id": 3,
        "cantidad": 1,
        "precio_unitario": 45000
      }
    ]
  }'
```

### 5. Actualizar estado del pedido

```bash
curl -X PUT "http://localhost:8000/api/v1/pedidos/15" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "estado": "preparando"
  }'
```

### 6. Obtener pedido específico

```bash
curl "http://localhost:8000/api/v1/pedidos/15" \
  -H "Authorization: Bearer $TOKEN"
```

---

## 📅 Reservas

### 1. Listar mis reservas

```bash
curl "http://localhost:8000/api/v1/reservas" \
  -H "Authorization: Bearer $TOKEN"
```

### 2. Crear nueva reserva

```bash
curl -X POST "http://localhost:8000/api/v1/reservas" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "mesa_id": 12,
    "fecha_reserva": "2025-11-28T20:00:00",
    "num_personas": 4,
    "nombre_cliente": "Juan Pérez",
    "telefono_cliente": "3001234567",
    "email_cliente": "juan@example.com",
    "ocasion_especial": "Aniversario",
    "notas": "Mesa cerca de la ventana"
  }'
```

### 3. Actualizar reserva

```bash
curl -X PUT "http://localhost:8000/api/v1/reservas/8" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "num_personas": 6,
    "notas": "Necesitamos silla para bebé"
  }'
```

### 4. Cancelar reserva

```bash
curl -X DELETE "http://localhost:8000/api/v1/reservas/8" \
  -H "Authorization: Bearer $TOKEN"
```

---

## 👥 Usuarios

### 1. Obtener mi perfil

```bash
curl "http://localhost:8000/api/v1/usuarios/me" \
  -H "Authorization: Bearer $TOKEN"
```

### 2. Actualizar mi perfil

```bash
curl -X PUT "http://localhost:8000/api/v1/usuarios/5" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "telefono": "3009999999",
    "direccion": "Nueva Calle 456"
  }'
```

### 3. Listar todos los usuarios (Admin)

```bash
curl "http://localhost:8000/api/v1/usuarios" \
  -H "Authorization: Bearer $TOKEN"
```

### 4. Crear usuario (Admin)

```bash
curl -X POST "http://localhost:8000/api/v1/usuarios" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "María",
    "apellido": "García",
    "email": "maria@example.com",
    "password": "password123",
    "telefono": "3005555555",
    "rol": "mesero",
    "activo": true
  }'
```

---

## 🐍 Ejemplos en Python

### Usando requests

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# 1. Login
response = requests.post(
    f"{BASE_URL}/auth/login",
    json={
        "email": "juan@example.com",
        "password": "mipassword123"
    }
)
token = response.json()["access_token"]

# Headers con token
headers = {"Authorization": f"Bearer {token}"}

# 2. Obtener mesas disponibles
response = requests.get(
    f"{BASE_URL}/mesas",
    params={"disponible": True, "tipo": "terraza"}
)
mesas = response.json()
print(f"Mesas disponibles: {len(mesas)}")

# 3. Crear pedido
response = requests.post(
    f"{BASE_URL}/pedidos",
    headers=headers,
    json={
        "tipo_servicio": "mesa",
        "mesa_id": 10,
        "metodo_pago": "efectivo",
        "items": [
            {
                "menu_item_id": 2,
                "cantidad": 2,
                "precio_unitario": 25000
            }
        ]
    }
)
pedido = response.json()
print(f"Pedido creado: {pedido['codigo_pedido']}")
```

---

## 🔍 Testing con PowerShell

En Windows PowerShell, usa `Invoke-RestMethod`:

```powershell
# Login
$loginData = @{
    email = "juan@example.com"
    password = "mipassword123"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/auth/login" `
    -Method Post `
    -ContentType "application/json" `
    -Body $loginData

$token = $response.access_token

# Usar token en headers
$headers = @{
    Authorization = "Bearer $token"
}

# Obtener perfil
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/usuarios/me" `
    -Method Get `
    -Headers $headers
```

---

## 📚 Más Información

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **OpenAPI JSON**: http://localhost:8000/api/openapi.json

Para ver todos los endpoints disponibles con sus parámetros y ejemplos, visita la documentación interactiva de Swagger.

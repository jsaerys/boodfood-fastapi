# 🏗️ Estructura Final del Panel de Administración - BoodFood

## 📁 Estructura de Archivos

```
Proyec11/
│
├── 📄 app.py                          # ✅ LIMPIO - Solo código Python
├── 📄 config.py                       # Configuración de DB
├── 📄 socket_events.py                # Eventos de Socket.IO
├── 📄 init_db.py                      # Inicializador de BD
│
├── 📂 models/                         # Modelos de SQLAlchemy
│   └── __init__.py
│
├── 📂 routes/                         # Blueprints de rutas
│   ├── __init__.py
│   ├── admin.py                      # ✅ API ADMIN (CRUD completo)
│   ├── admin_api.py
│   ├── auth.py
│   ├── caja.py
│   ├── cocina.py
│   ├── main.py
│   ├── pedidos.py
│   └── reservas.py
│
├── 📂 templates/
│   ├── base.html
│   ├── index.html
│   ├── menu.html
│   ├── domicilios.html
│   ├── reservas.html
│   │
│   ├── 📂 admin/                     # Templates del panel admin
│   │   ├── dashboard_content.html   # Dashboard
│   │   ├── menu_content.html        # ✅ Menú (CRUD)
│   │   ├── pedidos_content.html     # ✅ Pedidos (CRUD)
│   │   ├── inventario_content.html  # ✅ Inventario (CRUD)
│   │   ├── mesas_content.html       # ✅ Mesas (CRUD)
│   │   ├── reservas_content.html    # ✅ Reservas (CRUD)
│   │   ├── usuarios_content.html    # ✅ Usuarios (CRUD)
│   │   └── notificaciones_content.html # ✅ Notificaciones
│   │
│   ├── 📂 auth/
│   │   ├── login.html
│   │   └── register.html
│   │
│   ├── 📂 panels/
│   │   ├── admin.html               # Panel principal admin
│   │   ├── caja.html
│   │   └── cocina.html
│   │
│   └── 📂 errors/
│       ├── 404.html
│       └── 500.html
│
├── 📂 static/
│   ├── 📂 css/
│   │   ├── admin.css                # Estilos del panel admin
│   │   ├── style.css
│   │   └── styles.css
│   │
│   ├── 📂 js/
│   │   ├── main.js                  # Scripts generales
│   │   ├── adminPanel.js            # ✅ Controlador principal
│   │   ├── websocket.js             # WebSocket para tiempo real
│   │   │
│   │   └── 📂 admin/                # ✅ MÓDULOS COMPLETOS
│   │       ├── dashboard.js         # ✅ Dashboard con estadísticas
│   │       ├── menu.js              # ✅ CRUD Menú
│   │       ├── pedidos.js           # ✅ CRUD Pedidos (Mesa + Domicilio)
│   │       ├── inventario.js        # ✅ CRUD Inventario + Movimientos
│   │       ├── mesas.js             # ✅ CRUD Mesas + Toggle
│   │       ├── reservas.js          # ✅ CRUD Reservas + Asignación
│   │       ├── usuarios.js          # ✅ CRUD Usuarios + Roles
│   │       └── notificaciones.js    # ✅ Sistema de notificaciones
│   │
│   ├── 📂 images/
│   ├── 📂 sounds/
│   └── 📂 uploads/
│       ├── menu/
│       └── users/
│
├── 📂 utils/
│   ├── __init__.py
│   └── pedido_utils.py
│
└── 📂 tests/
    └── test_duplicate_pedido_item.py
```

---

## 🔄 Flujo de Funcionamiento

### 1. Carga del Panel de Administración

```
Usuario accede → /admin
           ↓
    admin.html carga
           ↓
    adminPanel.js se inicializa
           ↓
    Carga módulo por defecto (dashboard)
           ↓
    modules/dashboard.js ejecuta
           ↓
    API llama a /api/dashboard-stats
           ↓
    Renderiza estadísticas
```

### 2. Cambio de Módulo

```
Usuario hace clic en "Pedidos"
           ↓
    adminPanel.js detecta cambio
           ↓
    Verifica si pedidos.js ya está cargado
           ↓
    Si NO: fetch('/admin/pedidos-content')
           ↓
    Inyecta HTML en #admin-content
           ↓
    Carga <script src="admin/pedidos.js">
           ↓
    pedidos.js se inicializa automáticamente
           ↓
    cargarPedidos() ejecuta
           ↓
    API llama a /api/pedidos
           ↓
    Renderiza tabla de pedidos
```

### 3. Operación CRUD (Ejemplo: Crear Item de Inventario)

```
Usuario llena formulario
           ↓
    Click en "Guardar"
           ↓
    window.crearInventarioItem() ejecuta
           ↓
    Valida datos en frontend
           ↓
    API.post('/api/inventario/crear', data)
           ↓
    Backend valida y guarda en MySQL
           ↓
    Respuesta JSON al frontend
           ↓
    showToast('✅ Item creado')
           ↓
    cargarInventario() recarga la tabla
```

---

## 🔗 Arquitectura de API

### Pattern RESTful Utilizado

```
GET    /api/<recurso>           → Listar todos
GET    /api/<recurso>/<id>      → Obtener uno
POST   /api/<recurso>/crear     → Crear nuevo
PUT    /api/<recurso>/<id>/actualizar → Actualizar
DELETE /api/<recurso>/<id>      → Eliminar
PUT    /api/<recurso>/<id>/<accion> → Acción específica
```

### Ejemplos por Módulo

#### 📦 Pedidos
```python
GET    /api/pedidos                    # Listar todos
GET    /api/pedidos/<id>               # Detalles
PUT    /api/pedidos/<id>/estado        # Cambiar estado
```

#### 🍔 Inventario
```python
GET    /api/inventario                 # Listar items
POST   /api/inventario/crear           # Crear item
PUT    /api/inventario/<id>/actualizar # Editar item
DELETE /api/inventario/<id>/eliminar   # Eliminar
POST   /api/inventario/<id>/movimiento # Registrar entrada/salida
```

#### 🪑 Mesas
```python
GET    /api/mesas                      # Listar mesas
POST   /api/mesas/crear                # Crear mesa
PUT    /api/mesas/<id>/actualizar      # Editar mesa
PUT    /api/mesas/<id>/disponibilidad  # Toggle disponible/ocupada
DELETE /api/mesas/<id>                 # Eliminar
```

#### 📅 Reservas
```python
GET    /api/reservas                   # Listar reservas
GET    /api/reservas/<id>              # Detalles
PUT    /api/reservas/<id>/estado       # Cambiar estado
PUT    /api/reservas/<id>/asignar-mesa # Asignar mesa
```

#### 👥 Usuarios
```python
GET    /api/usuarios                   # Listar usuarios
POST   /api/usuarios/crear             # Crear usuario
PUT    /api/usuarios/<id>/actualizar   # Editar usuario
PUT    /api/usuarios/<id>/estado       # Activar/desactivar
DELETE /api/usuarios/<id>              # Eliminar
```

---

## 💾 Esquema de Base de Datos

### Tablas Principales

```sql
-- Usuarios
usuarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100),
    apellido VARCHAR(100),
    email VARCHAR(150) UNIQUE,
    telefono VARCHAR(20),
    password_hash VARCHAR(255),
    rol ENUM('admin', 'mesero', 'cocinero', 'cajero', 'cliente'),
    activo BOOLEAN DEFAULT TRUE,
    fecha_registro DATETIME
)

-- Pedidos
pedidos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    codigo_pedido VARCHAR(20) UNIQUE,
    usuario_id INT,
    mesa_id INT NULL,                    -- NULL = Domicilio
    direccion_entrega TEXT NULL,         -- NULL = Mesa
    telefono_contacto VARCHAR(20) NULL,
    nombre_receptor VARCHAR(100) NULL,
    instrucciones_entrega TEXT NULL,
    metodo_pago ENUM('efectivo', 'tarjeta', 'transferencia'),
    subtotal DECIMAL(10,2),
    impuestos DECIMAL(10,2),
    descuento DECIMAL(10,2),
    costo_envio DECIMAL(10,2),
    total DECIMAL(10,2),
    estado ENUM('pendiente', 'preparando', 'enviado', 'entregado', 'cancelado'),
    fecha_pedido DATETIME,
    fecha_preparacion DATETIME NULL,
    fecha_envio DATETIME NULL,
    fecha_entrega DATETIME NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (mesa_id) REFERENCES mesas(id)
)

-- Items del Pedido
pedido_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    pedido_id INT,
    menu_item_id INT,
    nombre_item VARCHAR(200),
    descripcion_item TEXT,
    cantidad INT,
    precio_unitario DECIMAL(10,2),
    subtotal DECIMAL(10,2),
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id) ON DELETE CASCADE,
    FOREIGN KEY (menu_item_id) REFERENCES menu_items(id)
)

-- Mesas
mesas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    numero INT UNIQUE,
    capacidad INT,
    ubicacion VARCHAR(50),
    tipo ENUM('interior', 'terraza', 'vip', 'privada'),
    disponible BOOLEAN DEFAULT TRUE,
    fecha_creacion DATETIME
)

-- Reservas
reservas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    codigo_reserva VARCHAR(20) UNIQUE,
    usuario_id INT NULL,
    nombre_reserva VARCHAR(100),
    email_reserva VARCHAR(150),
    telefono_reserva VARCHAR(20),
    fecha DATE,
    hora TIME,
    numero_personas INT,
    zona_mesa VARCHAR(50),
    mesa_asignada INT NULL,
    notas_especiales TEXT,
    estado ENUM('pendiente', 'confirmada', 'completada', 'cancelada', 'no_asistio'),
    fecha_creacion DATETIME,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (mesa_asignada) REFERENCES mesas(id)
)

-- Inventario
inventario (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(200),
    descripcion TEXT,
    categoria VARCHAR(100),
    cantidad DECIMAL(10,2),
    unidad VARCHAR(20),
    precio_unitario DECIMAL(10,2),
    stock_minimo DECIMAL(10,2),
    fecha_actualizacion DATETIME
)

-- Movimientos de Inventario
inventario_movimientos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    inventario_id INT,
    tipo ENUM('entrada', 'salida'),
    cantidad DECIMAL(10,2),
    motivo TEXT,
    usuario_id INT,
    fecha DATETIME,
    FOREIGN KEY (inventario_id) REFERENCES inventario(id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
)

-- Menú
menu_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(200),
    descripcion TEXT,
    categoria_id INT,
    precio DECIMAL(10,2),
    imagen VARCHAR(255),
    disponible BOOLEAN DEFAULT TRUE,
    fecha_creacion DATETIME,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id)
)

-- Categorías
categorias (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) UNIQUE,
    descripcion TEXT,
    orden INT
)
```

---

## 🎨 Sistema de Diseño

### Colores de Badges

```css
.badge-success  { background: #28a745; } /* Verde - OK, Activo, Disponible */
.badge-warning  { background: #ffc107; } /* Amarillo - Pendiente, Advertencia */
.badge-info     { background: #17a2b8; } /* Azul - Info, Domicilio */
.badge-danger   { background: #dc3545; } /* Rojo - Error, Cancelado, Stock Bajo */
.badge-secondary{ background: #6c757d; } /* Gris - Inactivo, Sin datos */
```

### Estados Visuales

```javascript
// Pedidos
pendiente   → 🟡 badge-warning
preparando  → 🔵 badge-info
enviado     → 🟠 badge-info
entregado   → 🟢 badge-success
cancelado   → 🔴 badge-danger

// Reservas
pendiente   → 🟡 badge-warning
confirmada  → 🟢 badge-success
completada  → ✅ badge-success
cancelada   → 🔴 badge-danger
no_asistio  → ⚫ badge-secondary

// Inventario
cantidad >= stock_minimo → ✅ badge-success
cantidad < stock_minimo  → ⚠️ badge-danger

// Mesas
disponible = true  → ✅ badge-success
disponible = false → 🔒 badge-warning

// Usuarios
activo = true  → ✅ badge-success
activo = false → ❌ badge-danger
```

---

## 🔐 Sistema de Roles y Permisos

```python
Roles implementados:
- ADMIN:     Acceso total al panel de administración
- MESERO:    Panel de pedidos y mesas
- COCINERO:  Panel de cocina (pedidos en preparación)
- CAJERO:    Panel de caja (cobros y reportes)
- CLIENTE:   Sin acceso al panel admin
```

### Rutas Protegidas

```python
@admin_bp.route('/admin')
@login_required
@admin_required
def admin_panel():
    # Solo admins pueden acceder
    ...

@admin_bp.route('/api/usuarios')
@login_required
@admin_required
def api_usuarios():
    # Solo admins pueden gestionar usuarios
    ...
```

---

## 📊 Funciones Helper Globales

### JavaScript (main.js)

```javascript
// Formateo de moneda
currency(amount) → "$12,345.67"

// Formateo de fechas
formatDate(dateString) → "12/12/2024"
formatDateTime(dateString) → "12/12/2024 10:30 AM"

// Notificaciones
showToast(message, type) → Toast visual

// API Helper
API.get(url)
API.post(url, data)
API.put(url, data)
API.delete(url)
```

### Python (utils/)

```python
# Generadores de código
generate_pedido_code() → "PED-20241212-001"
generate_reserva_code() → "RES-20241212-001"

# Validaciones
validate_email(email) → Boolean
validate_phone(phone) → Boolean
```

---

## ⚡ Optimizaciones Implementadas

1. **Lazy Loading de Módulos**
   - Solo se carga el JS del módulo activo
   - Flag `window.moduloModuleLoaded` previene re-carga

2. **Caché de Datos**
   - API responses cacheadas temporalmente
   - Evita llamadas duplicadas

3. **Batch Updates**
   - Actualización de múltiples items en una sola petición

4. **Debouncing en Búsqueda**
   - Evita llamadas excesivas durante tipeo

5. **Paginación**
   - Listados grandes paginados (pendiente implementar)

---

## 🚀 Comandos de Desarrollo

```bash
# Iniciar servidor
python app.py

# Inicializar base de datos
python init_db.py

# Verificar errores
pylint app.py routes/admin.py

# Ejecutar tests
pytest tests/
```

---

## 📱 Responsive Design

El panel se adapta a diferentes tamaños de pantalla:

- **Desktop (>1200px):** Vista completa con sidebar
- **Tablet (768px-1200px):** Sidebar colapsable
- **Mobile (<768px):** Navegación hamburger, tablas horizontalmente scrolleables

---

## 🔄 Flujo de Pedidos Completo

```
1. Cliente hace pedido → /menu o /domicilios
2. Pedido se guarda en DB con estado "pendiente"
3. Socket.IO notifica a Panel Admin
4. Administrador ve pedido en módulo "Pedidos"
5. Administrador cambia estado a "preparando"
6. Cocina recibe notificación
7. Al completar, se marca "enviado" (domicilio) o "entregado" (mesa)
8. Cliente recibe notificación
9. Pedido completado
```

---

## ✅ Checklist de Funcionalidades

### Módulo Pedidos
- [x] Ver listado completo
- [x] Diferenciar tipo (mesa/domicilio)
- [x] Ver detalles completos
- [x] Actualizar estado
- [x] Imprimir pedido
- [x] Filtrar por tipo/estado/fecha
- [x] Mostrar toda info del cliente

### Módulo Inventario
- [x] Ver listado completo
- [x] Crear item
- [x] Editar item
- [x] Eliminar item
- [x] Registrar entrada
- [x] Registrar salida
- [x] Alertas de stock bajo
- [x] Calcular valor total

### Módulo Mesas
- [x] Ver listado completo
- [x] Crear mesa
- [x] Editar mesa
- [x] Eliminar mesa
- [x] Toggle disponibilidad
- [x] Filtrar disponibles

### Módulo Reservas
- [x] Ver listado completo
- [x] Ver detalles completos
- [x] Actualizar estado
- [x] Asignar mesa
- [x] Mostrar toda info del cliente
- [x] Filtrar por estado/fecha

### Módulo Usuarios
- [x] Ver listado completo
- [x] Crear usuario
- [x] Editar usuario
- [x] Cambiar contraseña
- [x] Eliminar usuario
- [x] Toggle activo/inactivo
- [x] Filtrar por rol

---

**Última actualización:** Diciembre 2024  
**Status:** ✅ PRODUCCIÓN READY

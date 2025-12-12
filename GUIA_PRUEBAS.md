# 🧪 Guía de Pruebas - Panel de Administración BoodFood

## 🚀 Inicio Rápido

### 1. Arrancar la Aplicación

```powershell
# En la carpeta del proyecto
cd C:\Users\LENOVO\Desktop\Proyec11

# Activar entorno virtual (si lo tienes)
.\.venv\Scripts\Activate

# Iniciar servidor
python app.py
```

La aplicación debería iniciar en: **http://127.0.0.1:5000**

---

## 🔐 Acceso al Panel de Administración

### Credenciales de Admin

```
URL: http://127.0.0.1:5000/admin
Usuario: admin@boodfood.com (o el email de admin que creaste)
Contraseña: [tu contraseña de admin]
```

Si no tienes un usuario admin, créalo desde la terminal Python:

```python
from app import app, db
from models import Usuario
from werkzeug.security import generate_password_hash

with app.app_context():
    admin = Usuario(
        nombre='Admin',
        apellido='Principal',
        email='admin@boodfood.com',
        password_hash=generate_password_hash('admin123'),
        rol='admin',
        activo=True
    )
    db.session.add(admin)
    db.session.commit()
    print("✅ Usuario admin creado: admin@boodfood.com / admin123")
```

---

## 🧪 Plan de Pruebas por Módulo

### 📦 **1. Módulo de PEDIDOS**

#### Test 1: Ver Pedidos Existentes
1. Accede al panel admin
2. Click en "Pedidos" en el menú lateral
3. **Verificar:**
   - ✅ Se carga la tabla de pedidos
   - ✅ Las columnas muestran: ID, Código, Tipo, Cliente, Teléfono, Dirección, Total, Método Pago, Estado, Fecha
   - ✅ Los pedidos tienen badge de tipo: 🏠 Domicilio o 🍽️ Mesa

#### Test 2: Ver Detalles de Pedido a Domicilio
1. Click en el botón "👁️ Ver" de un pedido con tipo "Domicilio"
2. **Verificar que aparece:**
   - ✅ Modal con título "🏠 Pedido #XXXX"
   - ✅ Sección "Información General" con estado, método de pago, fechas
   - ✅ Sección "Información del Cliente" con:
     - Nombre del receptor
     - Teléfono de contacto
     - Dirección completa de entrega
     - Instrucciones (si las hay)
   - ✅ Tabla de items con cantidades y precios
   - ✅ Totales (subtotal, impuestos, envío, descuento, TOTAL)

#### Test 3: Ver Detalles de Pedido en Mesa
1. Click en el botón "👁️ Ver" de un pedido con tipo "Mesa"
2. **Verificar que aparece:**
   - ✅ Modal con título "🍽️ Pedido #XXXX"
   - ✅ Sección "Información del Mesa" mostrando número de mesa
   - ✅ NO muestra campos de dirección ni teléfono

#### Test 4: Cambiar Estado de Pedido
1. En un pedido con estado "pendiente"
2. Click en el selector de estado
3. Selecciona "preparando"
4. **Verificar:**
   - ✅ Aparece notificación "✅ Estado actualizado"
   - ✅ El badge cambia de color
   - ✅ La tabla se recarga automáticamente

#### Test 5: Imprimir Pedido
1. Click en "👁️ Ver" en cualquier pedido
2. Click en el botón "🖨️ Imprimir"
3. **Verificar:**
   - ✅ Se abre nueva ventana con formato de impresión
   - ✅ Muestra logo "BOODFOOD"
   - ✅ Incluye toda la información del pedido
   - ✅ Tiene botón "Imprimir" que abre diálogo de impresión

#### Test 6: Filtrar Pedidos
1. Usa el selector "Filtrar por Tipo"
2. Selecciona "Domicilio"
3. **Verificar:**
   - ✅ Solo aparecen pedidos a domicilio
4. Selecciona "Mesa"
5. **Verificar:**
   - ✅ Solo aparecen pedidos en mesa
6. Prueba filtrar por estado

---

### 🍽️ **2. Módulo de INVENTARIO**

#### Test 1: Ver Items del Inventario
1. Click en "Inventario" en el menú
2. **Verificar:**
   - ✅ Se muestra tabla con items
   - ✅ Columnas: ID, Nombre, Categoría, Cantidad, Unidad, Precio, Stock Mín, Valor Total, Estado
   - ✅ Items con stock bajo tienen badge rojo "⚠️ Stock Bajo"
   - ✅ Estadísticas en la parte superior

#### Test 2: Crear Nuevo Item
1. Llena el formulario "Nuevo Item":
   - Nombre: "Tomate"
   - Categoría: "Verduras"
   - Descripción: "Tomate fresco"
   - Cantidad: 50
   - Unidad: "kg"
   - Precio Unitario: 2.50
   - Stock Mínimo: 10
2. Click en "Crear Item"
3. **Verificar:**
   - ✅ Notificación "✅ Item creado"
   - ✅ El item aparece en la tabla
   - ✅ El formulario se limpia
   - ✅ Estadísticas se actualizan

#### Test 3: Editar Item
1. Click en "✏️ Editar" en cualquier item
2. Modifica algunos campos
3. Click en "Guardar Cambios"
4. **Verificar:**
   - ✅ Notificación "✅ Item actualizado"
   - ✅ Los cambios se reflejan en la tabla
   - ✅ El modal se cierra

#### Test 4: Registrar Entrada de Stock
1. Click en "➕ Entrada" en un item
2. Ingresa cantidad (ej: 25) y motivo (ej: "Compra a proveedor")
3. Click en "Registrar"
4. **Verificar:**
   - ✅ Notificación "✅ Entrada registrada"
   - ✅ La cantidad en la tabla aumenta
   - ✅ El stock se actualiza inmediatamente

#### Test 5: Registrar Salida de Stock
1. Click en "➖ Salida" en un item
2. Ingresa cantidad (ej: 10) y motivo (ej: "Uso en cocina")
3. Click en "Registrar"
4. **Verificar:**
   - ✅ Notificación "✅ Salida registrada"
   - ✅ La cantidad en la tabla disminuye
   - ✅ Si queda por debajo del mínimo, aparece badge de advertencia

#### Test 6: Eliminar Item
1. Click en "✏️ Editar" en un item
2. Click en el botón "Eliminar"
3. Confirma la eliminación
4. **Verificar:**
   - ✅ Notificación "✅ Item eliminado"
   - ✅ El item desaparece de la tabla

---

### 🪑 **3. Módulo de MESAS**

#### Test 1: Ver Listado de Mesas
1. Click en "Mesas"
2. **Verificar:**
   - ✅ Tabla con: Número, Capacidad, Ubicación, Tipo, Estado
   - ✅ Mesas disponibles con badge verde "✅ Disponible"
   - ✅ Mesas ocupadas con badge amarillo "🔒 Ocupada"

#### Test 2: Crear Nueva Mesa
1. Llena el formulario "Nueva Mesa":
   - Número: 15
   - Capacidad: 4
   - Ubicación: "Terraza"
   - Tipo: "terraza"
   - Disponible: Sí
2. Click en "Crear Mesa"
3. **Verificar:**
   - ✅ Notificación "✅ Mesa creada"
   - ✅ La mesa aparece en la tabla
   - ✅ El contador de mesas aumenta

#### Test 3: Editar Mesa
1. Click en "✏️ Editar" en una mesa
2. Cambia la capacidad o ubicación
3. Click en "Guardar Cambios"
4. **Verificar:**
   - ✅ Notificación "✅ Mesa actualizada"
   - ✅ Los cambios se reflejan

#### Test 4: Toggle Disponibilidad
1. En una mesa disponible, click en el botón "🔒"
2. **Verificar:**
   - ✅ Notificación "✅ Mesa ocupada"
   - ✅ El badge cambia a "🔒 Ocupada"
3. Click nuevamente en el botón (ahora será "✅")
4. **Verificar:**
   - ✅ Notificación "✅ Mesa liberada"
   - ✅ El badge vuelve a "✅ Disponible"

#### Test 5: Filtrar Solo Disponibles
1. Marca el checkbox "Solo disponibles"
2. **Verificar:**
   - ✅ Solo se muestran mesas con estado disponible

---

### 📅 **4. Módulo de RESERVAS**

#### Test 1: Ver Reservas
1. Click en "Reservas"
2. **Verificar:**
   - ✅ Tabla con: Código, Cliente, Fecha, Hora, Personas, Mesa, Estado
   - ✅ Estadísticas: Pendientes, Confirmadas Hoy, Canceladas, Total

#### Test 2: Ver Detalles de Reserva
1. Click en "👁️ Ver" en una reserva
2. **Verificar que aparece:**
   - ✅ Código de reserva
   - ✅ Nombre del cliente
   - ✅ Email
   - ✅ Teléfono
   - ✅ Fecha y hora
   - ✅ Número de personas
   - ✅ Zona preferida
   - ✅ Mesa asignada (o "Sin asignar")
   - ✅ Notas especiales (si las hay)

#### Test 3: Cambiar Estado de Reserva
1. En una reserva "pendiente", cambia el selector a "confirmada"
2. **Verificar:**
   - ✅ Notificación "✅ Estado actualizado"
   - ✅ El badge cambia de color
   - ✅ Las estadísticas se actualizan

#### Test 4: Asignar Mesa a Reserva
1. Click en "🪑 Mesa" en una reserva
2. Selecciona una mesa disponible
3. Selecciona zona (ej: "Terraza")
4. Click en "Asignar"
5. **Verificar:**
   - ✅ Notificación "✅ Mesa asignada"
   - ✅ La columna "Mesa" ahora muestra el número
   - ✅ El modal se cierra

#### Test 5: Filtrar Reservas por Estado
1. Usa el selector "Filtrar por Estado"
2. Selecciona "Confirmada"
3. **Verificar:**
   - ✅ Solo aparecen reservas confirmadas

---

### 👥 **5. Módulo de USUARIOS**

#### Test 1: Ver Listado de Usuarios
1. Click en "Usuarios"
2. **Verificar:**
   - ✅ Tabla con: ID, Nombre, Email, Teléfono, Rol, Estado
   - ✅ Badges de roles con colores diferentes
   - ✅ Badge de estado (Activo/Inactivo)

#### Test 2: Crear Nuevo Usuario
1. Llena el formulario "Nuevo Usuario":
   - Nombre: "Juan"
   - Apellido: "Pérez"
   - Email: "juan.perez@test.com"
   - Teléfono: "1234567890"
   - Rol: "mesero"
   - Contraseña: "mesero123"
   - Activo: Sí
2. Click en "Crear Usuario"
3. **Verificar:**
   - ✅ Notificación "✅ Usuario creado"
   - ✅ El usuario aparece en la tabla
   - ✅ El badge de rol es azul (mesero)

#### Test 3: Editar Usuario
1. Click en "✏️ Editar" en un usuario
2. Cambia el rol o teléfono
3. Click en "Guardar Cambios"
4. **Verificar:**
   - ✅ Notificación "✅ Usuario actualizado"
   - ✅ Los cambios se reflejan

#### Test 4: Cambiar Contraseña
1. Click en "✏️ Editar" en un usuario
2. Ingresa una nueva contraseña
3. Click en "Guardar Cambios"
4. **Verificar:**
   - ✅ Notificación "✅ Usuario actualizado"
5. Cierra sesión e intenta iniciar con la nueva contraseña
6. **Verificar:**
   - ✅ Login exitoso con nueva contraseña

#### Test 5: Toggle Estado de Usuario
1. En un usuario activo, click en el botón "🔒"
2. **Verificar:**
   - ✅ Notificación "✅ Usuario desactivado"
   - ✅ El badge cambia a "❌ Inactivo"
3. Click nuevamente (botón "✅")
4. **Verificar:**
   - ✅ Notificación "✅ Usuario activado"

#### Test 6: Filtrar por Rol
1. Usa el selector "Filtrar por Rol"
2. Selecciona "mesero"
3. **Verificar:**
   - ✅ Solo aparecen usuarios con rol "mesero"

#### Test 7: Buscar Usuario
1. Escribe en el campo de búsqueda
2. **Verificar:**
   - ✅ La tabla se filtra en tiempo real
   - ✅ Encuentra por nombre, email o teléfono

---

## 🔄 Pruebas de Integración

### Test 1: Flujo Completo de Pedido
1. Como cliente, realiza un pedido a domicilio en `/domicilios`
2. Como admin, ve el pedido en el panel
3. Cambia el estado a "preparando"
4. Imprime el pedido
5. Marca como "enviado"
6. Finalmente marca como "entregado"
7. **Verificar:**
   - ✅ Todas las transiciones de estado funcionan
   - ✅ Las fechas se registran correctamente
   - ✅ La información del cliente es completa

### Test 2: Flujo de Reserva
1. Como cliente, realiza una reserva en `/reservas`
2. Como admin, ve la reserva en el panel
3. Confirma la reserva
4. Asigna una mesa
5. El día de la reserva, marca como "completada"
6. **Verificar:**
   - ✅ Toda la información del cliente está presente
   - ✅ La mesa se asigna correctamente
   - ✅ El estado cambia correctamente

### Test 3: Control de Stock
1. Crea un pedido que use items del inventario
2. Registra una salida en inventario por ese pedido
3. Si el stock baja del mínimo, verifica la alerta
4. Registra una entrada para reponer
5. **Verificar:**
   - ✅ El stock se actualiza en tiempo real
   - ✅ Las alertas funcionan
   - ✅ Los movimientos se registran

---

## 📱 Pruebas de Responsividad

### Desktop (>1200px)
1. Abre el panel en pantalla completa
2. **Verificar:**
   - ✅ Sidebar visible permanentemente
   - ✅ Tablas muestran todas las columnas
   - ✅ Modales centrados

### Tablet (768px-1200px)
1. Ajusta el navegador a ~900px de ancho
2. **Verificar:**
   - ✅ Sidebar colapsable
   - ✅ Tablas con scroll horizontal
   - ✅ Modales responsivos

### Mobile (<768px)
1. Abre en un dispositivo móvil o emulador
2. **Verificar:**
   - ✅ Menú hamburger
   - ✅ Tablas scrolleables
   - ✅ Modales fullscreen

---

## 🐛 Casos de Error a Probar

### Test 1: Validación de Formularios
1. Intenta crear un item sin nombre
2. **Verificar:**
   - ✅ Aparece mensaje de error
   - ✅ No se envía la petición al servidor

### Test 2: Email Duplicado
1. Intenta crear un usuario con un email existente
2. **Verificar:**
   - ✅ Notificación de error "❌ Error: Email ya existe"

### Test 3: Mesa No Disponible
1. Intenta asignar una mesa ocupada a una reserva
2. **Verificar:**
   - ✅ El sistema no muestra mesas ocupadas en la lista

### Test 4: Conexión Perdida
1. Desconecta internet
2. Intenta hacer una operación
3. **Verificar:**
   - ✅ Notificación de error apropiada

---

## ✅ Checklist de Pruebas Completo

### Módulo Pedidos
- [ ] Ver listado de pedidos
- [ ] Diferenciar pedidos mesa vs domicilio
- [ ] Ver detalles completos de pedido a domicilio
- [ ] Ver detalles completos de pedido en mesa
- [ ] Cambiar estado de pedido
- [ ] Imprimir pedido
- [ ] Filtrar por tipo
- [ ] Filtrar por estado
- [ ] Filtrar por fecha

### Módulo Inventario
- [ ] Ver listado de items
- [ ] Crear nuevo item
- [ ] Editar item
- [ ] Eliminar item
- [ ] Registrar entrada de stock
- [ ] Registrar salida de stock
- [ ] Ver alertas de stock bajo
- [ ] Filtrar por categoría

### Módulo Mesas
- [ ] Ver listado de mesas
- [ ] Crear nueva mesa
- [ ] Editar mesa
- [ ] Eliminar mesa
- [ ] Toggle disponibilidad
- [ ] Filtrar solo disponibles

### Módulo Reservas
- [ ] Ver listado de reservas
- [ ] Ver detalles completos
- [ ] Cambiar estado
- [ ] Asignar mesa
- [ ] Filtrar por estado
- [ ] Filtrar por fecha

### Módulo Usuarios
- [ ] Ver listado de usuarios
- [ ] Crear nuevo usuario
- [ ] Editar usuario
- [ ] Cambiar contraseña
- [ ] Eliminar usuario
- [ ] Toggle estado
- [ ] Filtrar por rol
- [ ] Buscar usuario

### Funcionalidades Generales
- [ ] Login/Logout funciona
- [ ] Notificaciones toast aparecen
- [ ] Modales se abren y cierran correctamente
- [ ] Navegación entre módulos
- [ ] Estadísticas se actualizan
- [ ] No hay errores en consola
- [ ] Diseño responsive

---

## 📊 Métricas de Éxito

Al completar todas las pruebas, deberías tener:

- ✅ **100% de funcionalidades CRUD operativas**
- ✅ **Cero errores en consola del navegador**
- ✅ **Cero errores en logs del servidor**
- ✅ **Toda la información del cliente visible en los módulos**
- ✅ **Diferenciación clara entre pedidos mesa y domicilio**
- ✅ **Sistema de notificaciones funcional**
- ✅ **Estadísticas actualizadas en tiempo real**

---

## 🆘 Solución de Problemas Comunes

### Problema 1: No se carga el módulo
**Solución:**
1. Abre la consola del navegador (F12)
2. Busca errores de JavaScript
3. Verifica que el archivo .js existe en `static/js/admin/`
4. Revisa que el flag `window.moduloModuleLoaded` no esté duplicado

### Problema 2: Error 404 en API
**Solución:**
1. Verifica que el endpoint existe en `routes/admin.py`
2. Confirma que el blueprint está registrado
3. Revisa la URL en el archivo JS

### Problema 3: Datos no se actualizan
**Solución:**
1. Verifica conexión a base de datos
2. Revisa que la función `cargarModulo()` se llama después de operaciones
3. Comprueba que no hay errores en la consola

### Problema 4: Modal no se cierra
**Solución:**
1. Verifica que el modal tiene ID único
2. Confirma que existe el botón con `onclick="document.getElementById('modal-id').remove()"`
3. Revisa que no hay errores de JavaScript

---

## 📞 Soporte

Si encuentras algún error que no puedas resolver:

1. Revisa los logs del servidor (`app.py`)
2. Revisa la consola del navegador (F12)
3. Verifica la estructura de la base de datos
4. Comprueba que todas las dependencias están instaladas

---

**¡Listo para probar!** 🚀

Sigue esta guía paso a paso para verificar que todas las funcionalidades del panel de administración BoodFood están operativas y muestran toda la información que los clientes envían.

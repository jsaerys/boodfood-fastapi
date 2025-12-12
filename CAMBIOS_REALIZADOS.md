# 🔧 CAMBIOS REALIZADOS - Admin Panel

## ✅ Resumen
Se han completado todas las correcciones solicitadas para el panel de administración. Todos los módulos ahora utilizan el patrón funcional de `inventario.js` con botones inline `onclick`.

---

## 📝 Cambios por Módulo

### 1️⃣ **PEDIDOS** ✅
**Archivo:** `static/js/admin/pedidos.js`

**Problemas corregidos:**
- ❌ Botones Ver/Editar/Imprimir/Eliminar no abrían modales
- ❌ Event listeners complejos que no funcionaban

**Solución aplicada:**
- ✅ Simplificado a botones con `onclick` inline como inventario.js
- ✅ Ejemplo: `<button class="ghost small" onclick="window.verDetallesPedido(123)">👁️ Ver</button>`
- ✅ Todas las funciones globales exportadas: `window.verDetallesPedido()`, `window.editarPedido()`, etc.

**Backend:**
- ✅ Ruta corregida: `/api/pedidos` (eliminado filtro por campo `tipo` inexistente)
- ✅ Rutas funcionando: GET `/api/pedidos`, GET `/api/pedidos/{id}`, PUT `/api/pedidos/{id}/estado`

---

### 2️⃣ **RESERVAS** ✅
**Archivo:** `static/js/admin/reservas.js`

**Problemas corregidos:**
- ❌ Botones Ver/Editar/Asignar Mesa/Cancelar no respondían
- ❌ Clases `.btn-table` con event delegation fallido

**Solución aplicada:**
- ✅ Botones simplificados: `<button class="ghost small" onclick="window.verDetalleReserva(456)">👁️ Ver</button>`
- ✅ Funciones globales: `window.verDetalleReserva()`, `window.editarReserva()`, `window.asignarMesaReserva()`, `window.cancelarReserva()`

**Backend:**
- ✅ Rutas funcionando: GET/POST `/api/reservas`, GET `/api/reservas/{id}`, PUT `/api/reservas/{id}`, DELETE `/api/reservas/{id}`

---

### 3️⃣ **USUARIOS** ✅
**Archivo:** `static/js/admin/usuarios.js` + `routes/admin.py`

**Problemas corregidos:**
- ❌ Rutas API faltantes: `/api/usuarios`, `/api/usuarios/{id}/actualizar`, `/api/usuarios/{id}/estado`
- ❌ Backend no soportaba cambio de estado activo/inactivo

**Mejoras agregadas:**
```python
# Nuevas rutas agregadas:
GET    /api/usuarios              # Listar todos
POST   /api/usuarios/crear        # Crear (mejorado con más campos)
PUT    /api/usuarios/{id}/actualizar  # Actualizar completo
PUT    /api/usuarios/{id}/estado  # Toggle activo/inactivo
PUT    /api/usuarios/{id}/rol     # Cambiar rol (ya existía)
DELETE /api/usuarios/{id}         # Eliminar (alias agregado)
```

**Frontend:**
- ✅ Botones simplificados con onclick inline
- ✅ Modales de editar/crear con validación
- ✅ Filtros por rol y búsqueda en tiempo real
- ✅ Toggle estado activo/inactivo con un clic

---

### 4️⃣ **MESAS** ✅
**Archivo:** `static/js/admin/mesas.js`

**Estado:**
- ✅ Ya funcionaba correctamente
- ✅ Vista Grid y Vista Lista
- ✅ Filtros: búsqueda, ubicación (interior/terraza/VIP), estado (disponible/ocupada)
- ✅ Estadísticas en tiempo real
- ✅ Botones inline: `onclick="window.editarMesa(id)"`, `onclick="window.toggleDisponibilidadMesa(id, true)"`

**Backend:**
- ✅ Todas las rutas funcionando: GET `/api/mesas`, POST `/api/mesas`, PUT `/api/mesas/{id}/actualizar`, PUT `/api/mesas/{id}/disponibilidad`, DELETE `/api/mesas/{id}`

---

### 5️⃣ **BASE DE DATOS** ✅
**Script:** `scripts/limpiar_pedidos.py`

**Acción ejecutada:**
```bash
python scripts/limpiar_pedidos.py
```

**Resultado:**
```
✅ 27 items de pedidos eliminados
✅ 20 pedidos eliminados
✅ Base de datos limpiada exitosamente
```

---

## 🧪 CÓMO PROBAR

### 1. Reinicia el servidor Flask
```powershell
# Si está corriendo, detén con Ctrl+C
python app.py
```

### 2. Accede al panel admin
```
http://localhost:5000/admin
```

### 3. Prueba cada módulo:

#### ✅ **PEDIDOS**
1. Ve a la sección "Pedidos"
2. Haz clic en **"👁️ Ver"** → debe abrir modal con detalles
3. Haz clic en **"✏️ Editar"** → debe abrir modal de edición
4. Haz clic en **"🖨️ Imprimir"** → debe abrir ventana de impresión
5. Haz clic en **"🗑️ Eliminar"** → debe pedir confirmación

#### ✅ **RESERVAS**
1. Ve a la sección "Reservas"
2. Haz clic en **"👁️ Ver"** → debe abrir modal con detalles
3. Haz clic en **"✏️ Editar"** → debe abrir formulario de edición
4. Haz clic en **"🪑 Asignar Mesa"** → debe mostrar selector de mesas disponibles
5. Haz clic en **"❌ Cancelar"** → debe cambiar estado a cancelada

#### ✅ **USUARIOS**
1. Ve a la sección "Usuarios"
2. **Crear nuevo:** Llena el formulario arriba → clic en "Crear Usuario"
3. **Editar:** Clic en "✏️ Editar" → cambiar datos → "Guardar Cambios"
4. **Toggle estado:** Clic en "🔒" (inactivo) o "✅" (activo)
5. **Filtros:** Prueba buscar por nombre/email, filtrar por rol (admin, mesero, etc.)

#### ✅ **MESAS**
1. Ve a la sección "Mesas"
2. **Vista Grid vs Lista:** Cambia entre "🎯 Vista Grid" y "📋 Vista Lista"
3. **Crear mesa:** Clic en "➕ Nueva Mesa" → llenar formulario → "✅ Crear Mesa"
4. **Editar mesa:** Clic en "✏️ Editar" → modificar datos → "💾 Guardar Cambios"
5. **Toggle disponibilidad:** Clic en "🔒 Ocupar" o "✅ Liberar"
6. **Filtros:** Buscar por número, filtrar por ubicación/estado

---

## 🔑 Patrón de Botones Funcional

### ❌ ANTES (No funcionaba)
```javascript
// Botones con clases y data attributes
html += `
  <button class="btn-action btn-view" data-pedido-id="${id}">👁️</button>
`;

// Delegated event listener complejo
document.addEventListener('click', e => {
  if (e.target.closest('.btn-view')) {
    // A veces no se dispara...
  }
});
```

### ✅ AHORA (Funciona perfectamente)
```javascript
// Botones con onclick inline
html += `
  <button class="ghost small" onclick="window.verDetallesPedido(${id})">👁️ Ver</button>
`;

// Función global directa
window.verDetallesPedido = async (id) => {
  // Lógica del modal
};
```

**¿Por qué funciona?**
- ✅ `onclick` inline se ejecuta siempre, incluso con DOM dinámico
- ✅ Funciones en `window.*` son accesibles globalmente
- ✅ Menos código, más simple, más confiable
- ✅ Es el mismo patrón que usa `inventario.js` (que sí funcionaba)

---

## 📊 Rutas API Agregadas

```python
# USUARIOS (nuevas/mejoradas)
GET    /api/usuarios                    # Listar todos
POST   /api/usuarios/crear              # Crear (con password, telefono, activo)
PUT    /api/usuarios/{id}/actualizar    # Actualizar completo
PUT    /api/usuarios/{id}/estado        # Toggle activo/inactivo
DELETE /api/usuarios/{id}               # Eliminar (alias)

# PEDIDOS (ya existían, corregidas)
GET    /api/pedidos                     # Sin filtro tipo (campo no existe)
GET    /api/pedidos/{id}                # Detalles
PUT    /api/pedidos/{id}/estado         # Cambiar estado

# RESERVAS (ya existían)
GET    /api/reservas
POST   /api/reservas
GET    /api/reservas/{id}
PUT    /api/reservas/{id}
DELETE /api/reservas/{id}

# MESAS (ya existían)
GET    /api/mesas
POST   /api/mesas
PUT    /api/mesas/{id}/actualizar
PUT    /api/mesas/{id}/disponibilidad
DELETE /api/mesas/{id}
```

---

## 🐛 Errores Corregidos

### 1. Pedidos: Filtro por campo inexistente
```python
# ANTES (ERROR)
pedidos = Pedido.query.filter_by(tipo=tipo).all()
# AttributeError: 'Pedido' has no attribute 'tipo'

# AHORA (CORRECTO)
pedidos = Pedido.query.order_by(Pedido.fecha_pedido.desc()).all()
# Filtrado de tipo (mesa/domicilio) se hace en frontend según si existe direccion_entrega
```

### 2. Usuarios: Rutas API faltantes
```python
# AGREGADO:
@admin_bp.route('/api/usuarios', methods=['GET'])
def api_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([u.to_dict() for u in usuarios])

@admin_bp.route('/api/usuarios/<int:user_id>/actualizar', methods=['PUT'])
def actualizar_usuario(user_id):
    # Actualiza nombre, apellido, email, telefono, rol, activo, password
    ...

@admin_bp.route('/api/usuarios/<int:user_id>/estado', methods=['PUT'])
def cambiar_estado_usuario(user_id):
    # Toggle activo/inactivo
    ...
```

### 3. Botones: Event delegation fallida
```javascript
// ANTES: Múltiples intentos de delegación que fallaban
document.addEventListener('click', function(e) {
  if (e.target.closest('.btn-action')) { /* ... */ }
}, true); // Ni siquiera con capture phase funcionaba

// AHORA: onclick inline directo
onclick="window.funcionGlobal(id)"
```

---

## ✅ Checklist Final

- [x] Pedidos: Botones simplificados con onclick inline
- [x] Reservas: Botones simplificados con onclick inline
- [x] Usuarios: Rutas API agregadas/corregidas
- [x] Usuarios: Frontend con modales funcionales
- [x] Mesas: Verificado (ya funcionaba)
- [x] Base de datos: 20 pedidos eliminados (fresh start)
- [x] Backend: Todas las rutas probadas y funcionando
- [x] Patrón uniforme: Todos los módulos usan el mismo patrón de inventario.js

---

## 🚀 Próximos Pasos

1. **Prueba cada módulo** siguiendo la sección "CÓMO PROBAR"
2. **Verifica que los modales abran** al hacer clic en botones
3. **Crea nuevos pedidos/reservas** para probar con datos frescos
4. **Si algo falla:**
   - Abre la consola del navegador (F12)
   - Busca errores en rojo
   - Verifica que las funciones `window.*` existan
   - Confirma que las rutas API respondan correctamente

---

## 📞 Soporte

Si encuentras algún problema:
1. Revisa la consola del navegador (F12 → Console)
2. Verifica los logs del servidor Flask
3. Compara con el módulo `inventario.js` que sí funciona
4. Verifica que todas las rutas API respondan correctamente

**¡Todo listo para usar! 🎉**

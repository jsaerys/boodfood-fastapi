# Estructura Modular del Panel Admin - BoodFood

## 📋 Resumen de Cambios

Se ha reorganizado el panel de administración para seguir una arquitectura modular, separando cada sección en archivos independientes de HTML y JavaScript.

## 🗂️ Estructura de Archivos

### Templates HTML (templates/admin/)
Cada módulo tiene su propio archivo HTML con el contenido específico:

- `dashboard_content.html` - Vista principal del dashboard
- `pedidos_content.html` - Gestión de pedidos
- `reservas_content.html` - Gestión de reservas  
- `usuarios_content.html` - Gestión de usuarios
- `inventario_content.html` - Gestión de inventario
- `mesas_content.html` - Gestión de mesas
- `menu_content.html` - Gestión del menú
- `notificaciones_content.html` - Centro de notificaciones

### JavaScript Modular (static/js/admin/)
Cada módulo tiene su lógica en un archivo JS separado:

- `dashboard.js` - Lógica del dashboard
- `pedidos.js` - Gestión de pedidos
- `reservas.js` - Gestión de reservas
- `usuarios.js` - Gestión de usuarios
- `inventario.js` - Gestión de inventario
- `mesas.js` - Gestión de mesas
- `menu.js` - Gestión del menú
- `notificaciones.js` - Sistema de notificaciones

### Rutas Backend (routes/admin.py)
Cada módulo tiene su ruta para cargar el contenido:

```python
/admin/dashboard-content
/admin/pedidos-content
/admin/reservas-content
/admin/usuarios-content
/admin/inventario-content
/admin/mesas-content
/admin/menu-content
/admin/notificaciones-content
```

## 🔄 Cómo Funciona

### Carga Dinámica
1. El usuario hace clic en un botón de navegación (ej: "Pedidos")
2. `adminPanel.js` intercepta el clic y llama a `setActiveView('pedidos')`
3. La función `renderView()` carga dinámicamente:
   - El HTML desde `/admin/pedidos-content`
   - El JavaScript desde `/static/js/admin/pedidos.js`
4. El módulo JS se inicializa automáticamente

### Ejemplo de Flujo
```
Click en "Pedidos" 
  → setActiveView('pedidos')
  → renderView()
  → fetch('/admin/pedidos-content') → Carga HTML
  → loadScript('/static/js/admin/pedidos.js') → Carga JS
  → cargarPedidos() → Llena la tabla con datos del API
```

## ➕ Cómo Agregar un Nuevo Módulo

### 1. Crear el Template HTML
Crear `templates/admin/nuevo_modulo_content.html`:
```html
<div class="card">
  <div class="card-header"><strong>Título del Módulo</strong></div>
  <div class="card-body" id="contenido-modulo">
    <!-- Contenido aquí -->
  </div>
</div>
```

### 2. Crear el Archivo JavaScript
Crear `static/js/admin/nuevo_modulo.js`:
```javascript
// Función principal que se ejecuta al cargar el módulo
async function cargarContenido() {
  try {
    const datos = await API.get('/api/nuevo-modulo');
    // Renderizar datos
    document.getElementById('contenido-modulo').innerHTML = ...;
  } catch (err) {
    console.error('Error:', err);
  }
}

// Marcar el módulo como cargado
window.nuevo_moduloModuleLoaded = true;

// Inicializar
cargarContenido();
```

### 3. Agregar Ruta en el Backend
En `routes/admin.py`:
```python
@admin_bp.route('/nuevo_modulo-content')
@login_required
@admin_required
def nuevo_modulo_content():
    return render_template('admin/nuevo_modulo_content.html')
```

### 4. Agregar Botón de Navegación
En `templates/panels/admin.html`:
```html
<button class="nav-item" data-view="nuevo_modulo">Nuevo Módulo</button>
```

### 5. Actualizar Título en adminPanel.js
En la función `setActiveView()`:
```javascript
view === 'nuevo_modulo' ? 'Nuevo Módulo' :
```

## 🎨 Funciones Comunes Disponibles

### API Helper
```javascript
// GET
const data = await API.get('/api/endpoint');

// POST
const result = await API.post('/api/endpoint', { datos });

// PUT
await API.put('/api/endpoint/id', { datos });

// DELETE
await API.del('/api/endpoint/id');
```

### Utilidades
```javascript
// Formatear moneda
currency(15000) // "$15,000"

// Formatear fecha
formatDate('2025-10-29') // "29/10/2025"

// Formatear fecha y hora
formatDateTime('2025-10-29T14:30:00') // "29/10/2025, 2:30 PM"

// Mostrar notificación
showToast('Mensaje', 'success'); // success, error, info
```

## 📦 Archivos Eliminados

Se eliminaron los siguientes archivos innecesarios:
- ❌ `update_pedido_items.py` (script de migración ejecutado)
- ❌ `update_pedido_items.sql` (SQL de migración)
- ❌ `update_pedido_items_safe.sql` (backup de migración)
- ❌ `add_admin_user.py` (utilidad de un solo uso)

Se movió a `scripts/`:
- 📁 `init_db.py` (útil para reinicializar BD si es necesario)

## ✅ Beneficios de la Nueva Estructura

1. **Modularidad**: Cada sección es independiente y fácil de mantener
2. **Escalabilidad**: Agregar nuevos módulos es simple y rápido
3. **Rendimiento**: Solo se carga el código necesario para cada vista
4. **Organización**: Código limpio y bien estructurado
5. **Mantenibilidad**: Más fácil encontrar y corregir bugs
6. **Reutilización**: Funciones comunes disponibles para todos los módulos

## 🚀 Próximos Pasos

- [ ] Agregar validaciones más robustas en formularios
- [ ] Implementar paginación en tablas grandes
- [ ] Agregar sistema de caché para mejorar rendimiento
- [ ] Crear tests unitarios para cada módulo
- [ ] Documentar API endpoints

## 📝 Notas para Desarrolladores

- Cada módulo debe marcar `window.[modulo]ModuleLoaded = true` al finalizar la carga
- Usar siempre el helper `API` para llamadas al backend
- Incluir manejo de errores en todas las funciones async
- Usar `showToast()` para feedback al usuario
- Seguir la convención de nombres: `[modulo]_content.html` y `[modulo].js`

---

**Fecha de actualización**: 29 de octubre de 2025
**Versión**: 2.0 - Estructura Modular

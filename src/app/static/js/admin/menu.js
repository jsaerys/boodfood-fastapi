// static/js/admin/menu.js

// Cargar menú
async function cargarMenu() {
  try {
    // Cargar categorías y items en paralelo
    const [categorias, menuItems] = await Promise.all([
      API.get('/api/categorias/lista'),
      API.get('/api/menu/items')
    ]);
    
    // Guardar categorías globalmente
    window.categoriasMenu = categorias;
    
    // Actualizar contador
    document.getElementById('menu-items-count').textContent = menuItems.length;
    
    // Cargar categorías en el select del formulario
    const catSelect = document.getElementById('new-menu-categoria');
    if (catSelect) {
      catSelect.innerHTML = '<option value="">-- Sin categoría --</option>';
      categorias.forEach(cat => {
        catSelect.innerHTML += `<option value="${cat.id}">${cat.nombre}</option>`;
      });
    }
    
    // Generar tabla
    let html = `
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Nombre</th>
            <th>Descripción</th>
            <th>Precio</th>
            <th>Categoría</th>
            <th>Disponible</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
    `;
    
    if (menuItems.length === 0) {
      html += `
        <tr>
          <td colspan="7" style="text-align:center;padding:30px;color:#666;">
            📋 No hay items en el menú
          </td>
        </tr>
      `;
    } else {
      menuItems.forEach(item => {
        const categoria = categorias.find(c => c.id == item.categoria_id);
        const categoriaNombre = categoria ? categoria.nombre : 'Sin categoría';
        const disponibleBadge = item.disponible 
          ? '<span class="badge badge-success">✅ Disponible</span>' 
          : '<span class="badge badge-danger">❌ No disponible</span>';
        
        html += `
          <tr>
            <td>${item.id}</td>
            <td><strong>${item.nombre}</strong></td>
            <td>${item.descripcion || '-'}</td>
            <td><strong>${currency(item.precio)}</strong></td>
            <td><span class="badge badge-info">${categoriaNombre}</span></td>
            <td>${disponibleBadge}</td>
            <td>
              <button class="ghost small" onclick="window.editarMenuItem(${item.id}, ${JSON.stringify(item).replace(/"/g, '&quot;')})">✏️ Editar</button>
              <button class="ghost small" onclick="window.eliminarMenuItem(${item.id})">🗑️ Eliminar</button>
            </td>
          </tr>
        `;
      });
    }
    
    html += '</tbody></table>';
    document.getElementById('menu-table').innerHTML = html;
    
  } catch (err) {
    console.error('Error:', err);
    document.getElementById('menu-table').innerHTML = 
      `<p style="color:red;text-align:center;padding:20px;">Error al cargar menú: ${err.message}</p>`;
  }
}

// Crear nuevo item
window.crearMenuItem = async () => {
  try {
    const nombre = document.getElementById('new-menu-nombre').value.trim();
    const precio = parseFloat(document.getElementById('new-menu-precio').value);
    const categoria_id = document.getElementById('new-menu-categoria').value || null;
    const descripcion = document.getElementById('new-menu-descripcion').value.trim();
    const disponible = document.getElementById('new-menu-disponible').value === 'true';

    if (!nombre || isNaN(precio) || precio <= 0) {
      alert('Nombre y precio válido son requeridos');
      return;
    }

    const data = {
      nombre,
      precio,
      categoria_id,
      descripcion,
      disponible,
      restaurante_id: 1
    };
    
    await API.post('/api/menu/crear', data);
    showToast('✅ Item agregado al menú', 'success');
    
    // Limpiar formulario
    document.getElementById('form-crear-menu').reset();
    
    // Recargar tabla
    cargarMenu();
  } catch (err) {
    showToast('❌ Error: ' + (err.message || 'No se pudo crear'), 'error');
  }
};

// Editar item - PATRÓN EXACTO DE INVENTARIO
window.editarMenuItem = (id, item) => {
  const categorias = window.categoriasMenu || [];
  
  const modalHTML = `
    <div id="modal-editar-menu" class="modal-overlay">
      <div class="modal-content">
        <span class="close-modal" onclick="document.getElementById('modal-editar-menu').remove()">&times;</span>
        <h2>✏️ Editar Item del Menú</h2>
        <form id="form-editar-menu">
          <div class="row">
            <div>
              <label>Nombre *</label>
              <input type="text" id="edit-menu-nombre" value="${item.nombre}" required>
            </div>
            <div>
              <label>Precio *</label>
              <input type="number" id="edit-menu-precio" min="0" step="0.01" value="${item.precio}" required>
            </div>
          </div>
          <div class="row">
            <div>
              <label>Categoría</label>
              <select id="edit-menu-categoria">
                <option value="">-- Sin categoría --</option>
                ${categorias.map(cat => `
                  <option value="${cat.id}" ${cat.id == item.categoria_id ? 'selected' : ''}>${cat.nombre}</option>
                `).join('')}
              </select>
            </div>
            <div>
              <label>Disponible</label>
              <select id="edit-menu-disponible">
                <option value="true" ${item.disponible ? 'selected' : ''}>Sí</option>
                <option value="false" ${!item.disponible ? 'selected' : ''}>No</option>
              </select>
            </div>
          </div>
          <div class="row">
            <div>
              <label>Descripción</label>
              <textarea id="edit-menu-descripcion" rows="3">${item.descripcion || ''}</textarea>
            </div>
          </div>
          <div class="actions">
            <button type="submit" class="primary">💾 Guardar Cambios</button>
            <button type="button" class="ghost" onclick="document.getElementById('modal-editar-menu').remove()">Cancelar</button>
          </div>
        </form>
      </div>
    </div>
  `;
  
  document.body.insertAdjacentHTML('beforeend', modalHTML);
  
  document.getElementById('form-editar-menu').onsubmit = async (e) => {
    e.preventDefault();
    try {
      const data = {
        nombre: document.getElementById('edit-menu-nombre').value.trim(),
        precio: parseFloat(document.getElementById('edit-menu-precio').value),
        categoria_id: document.getElementById('edit-menu-categoria').value || null,
        descripcion: document.getElementById('edit-menu-descripcion').value.trim(),
        disponible: document.getElementById('edit-menu-disponible').value === 'true'
      };
      
      await API.put(`/api/menu/${id}/actualizar`, data);
      showToast('✅ Item actualizado', 'success');
      document.getElementById('modal-editar-menu').remove();
      cargarMenu();
    } catch (err) {
      showToast('❌ Error: ' + (err.message || 'No se pudo actualizar'), 'error');
    }
  };
};

// Eliminar item
window.eliminarMenuItem = async (id) => {
  if (!confirm('⚠️ ¿Eliminar este item del menú?')) return;
  
  try {
    await API.del(`/api/menu/${id}`);
    showToast('✅ Item eliminado', 'success');
    cargarMenu();
  } catch (err) {
    showToast('❌ Error: ' + (err.message || 'No se pudo eliminar'), 'error');
  }
};

// Función de notificaciones
function showToast(message, type = 'info') {
  if (typeof Toastify !== 'undefined') {
    Toastify({
      text: message,
      duration: 3000,
      gravity: "top",
      position: "right",
      backgroundColor: type === 'success' ? '#4caf50' : type === 'error' ? '#f44336' : '#2196f3',
    }).showToast();
  } else {
    alert(message);
  }
}

// Función para formatear moneda
function currency(val) {
  return new Intl.NumberFormat('es-CO', {
    style: 'currency',
    currency: 'COP',
    minimumFractionDigits: 0
  }).format(val);
}

// Inicialización del módulo
window.menuModuleLoaded = true;
cargarMenu();

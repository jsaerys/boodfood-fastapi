// static/js/admin/mesas.js
// Módulo completo de gestión de mesas

var mesasData = [];
var mesasFiltradas = [];
var vistaActual = 'grid';

// Módulo Mesas
window.Mesas = {
  init: async function() {
    console.log('🪑 Inicializando módulo Mesas...');
    await cargarMesas();
  }
};

// Cargar todas las mesas
async function cargarMesas() {
  try {
    const mesas = await window.API.get('/api/mesas');
    mesasData = mesas;
    mesasFiltradas = [...mesas];
    
    actualizarEstadisticasMesas(mesas);
    renderizarMesas(mesasFiltradas);
    
    console.log(`✅ ${mesas.length} mesas cargadas`);
  } catch (err) {
    console.error('❌ Error al cargar mesas:', err);
    document.getElementById('mesas-container').innerHTML = `
      <div style="text-align: center; padding: 40px; color: #ef4444;">
        <p style="font-size: 48px;">❌</p>
        <p style="font-size: 18px; margin-top: 16px;">Error al cargar mesas: ${err.message}</p>
        <button onclick="window.cargarMesas()" style="margin-top: 16px; padding: 10px 20px; background: #6366f1; color: white; border: none; border-radius: 8px; cursor: pointer;">
          🔄 Reintentar
        </button>
      </div>
    `;
  }
}

// Actualizar estadísticas
function actualizarEstadisticasMesas(mesas) {
  const disponibles = mesas.filter(m => m.disponible).length;
  const ocupadas = mesas.filter(m => !m.disponible).length;
  const total = mesas.length;
  
  document.getElementById('mesas-disponibles').textContent = disponibles;
  document.getElementById('mesas-ocupadas').textContent = ocupadas;
  document.getElementById('mesas-total').textContent = total;
}

// Renderizar mesas según vista actual
function renderizarMesas(mesas) {
  const container = document.getElementById('mesas-container');
  
  if (!mesas || mesas.length === 0) {
    container.innerHTML = `
      <div style="grid-column: 1/-1; text-align: center; padding: 60px 20px; color: #6b7280;">
        <p style="font-size: 48px; margin-bottom: 16px;">🪑</p>
        <p style="font-size: 18px; margin-bottom: 24px;">No hay mesas registradas</p>
        <button onclick="window.abrirModalCrearMesa()" style="padding: 12px 24px; background: linear-gradient(135deg, #10b981, #059669); color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: 600;">
          ➕ Crear Primera Mesa
        </button>
      </div>
    `;
    return;
  }
  
  if (vistaActual === 'grid') {
    renderizarVistaGrid(mesas, container);
  } else {
    renderizarVistaLista(mesas, container);
  }
}

// Vista en bloques/grid
function renderizarVistaGrid(mesas, container) {
  container.className = 'mesas-grid-view';
  
  const html = mesas.map(mesa => {
    const estadoClass = mesa.disponible ? 'disponible' : 'ocupada';
    const estadoBadge = mesa.disponible ? 'Disponible' : 'Ocupada';
    const tipoIcono = {
      'interior': '🏠',
      'terraza': '🌳',
      'vip': '👑'
    }[mesa.tipo] || '🪑';
    
    return `
      <div class="mesa-card ${estadoClass}">
        <div class="mesa-numero">Mesa ${mesa.numero}</div>
        
        <div class="mesa-info-item">
          <span>👥</span>
          <span>${mesa.capacidad} personas</span>
        </div>
        
        <div class="mesa-info-item">
          <span>${tipoIcono}</span>
          <span>${mesa.tipo.charAt(0).toUpperCase() + mesa.tipo.slice(1)}</span>
        </div>
        
        <div class="mesa-badge ${estadoClass}">
          ${mesa.disponible ? '✅' : '🔒'} ${estadoBadge}
        </div>
        
        <div class="mesa-actions">
          <button class="mesa-btn editar" onclick="window.editarMesa(${mesa.id})" title="Editar mesa">
            ✏️ Editar
          </button>
          <button class="mesa-btn toggle" onclick="window.toggleDisponibilidadMesa(${mesa.id}, ${!mesa.disponible})" title="${mesa.disponible ? 'Marcar ocupada' : 'Liberar mesa'}">
            ${mesa.disponible ? '🔒 Ocupar' : '✅ Liberar'}
          </button>
        </div>
      </div>
    `;
  }).join('');
  
  container.innerHTML = html;
}

// Vista en lista/tabla
function renderizarVistaLista(mesas, container) {
  container.className = 'mesas-list-view';
  
  const html = `
    <table>
      <thead>
        <tr>
          <th>Número</th>
          <th>Capacidad</th>
          <th>Tipo</th>
          <th>Estado</th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        ${mesas.map(mesa => {
          const estadoClass = mesa.disponible ? 'disponible' : 'ocupada';
          const estadoBadge = mesa.disponible ? 'Disponible' : 'Ocupada';
          const tipoIcono = {
            'interior': '🏠',
            'terraza': '🌳',
            'vip': '👑'
          }[mesa.tipo] || '🪑';
          
          return `
            <tr>
              <td><strong>Mesa ${mesa.numero}</strong></td>
              <td>👥 ${mesa.capacidad} personas</td>
              <td>${tipoIcono} ${mesa.tipo.charAt(0).toUpperCase() + mesa.tipo.slice(1)}</td>
              <td><span class="mesa-badge ${estadoClass}">${mesa.disponible ? '✅' : '🔒'} ${estadoBadge}</span></td>
              <td>
                <div style="display: flex; gap: 8px;">
                  <button class="mesa-btn editar" onclick="window.editarMesa(${mesa.id})" style="flex: none;">
                    ✏️ Editar
                  </button>
                  <button class="mesa-btn toggle" onclick="window.toggleDisponibilidadMesa(${mesa.id}, ${!mesa.disponible})" style="flex: none;">
                    ${mesa.disponible ? '🔒' : '✅'}
                  </button>
                </div>
              </td>
            </tr>
          `;
        }).join('')}
      </tbody>
    </table>
  `;
  
  container.innerHTML = html;
}

// Cambiar vista
window.cambiarVistaMesas = function(vista) {
  vistaActual = vista;
  
  // Actualizar botones activos
  document.querySelectorAll('.vista-btn').forEach(btn => {
    btn.classList.remove('active');
    if (btn.dataset.vista === vista) {
      btn.classList.add('active');
    }
  });
  
  renderizarMesas(mesasFiltradas);
};

// Filtrar mesas
window.filtrarMesas = function() {
  const buscar = document.getElementById('filter-buscar-mesa').value.toLowerCase();
  const ubicacion = document.getElementById('filter-ubicacion').value;
  const estado = document.getElementById('filter-estado').value;
  
  mesasFiltradas = mesasData.filter(mesa => {
    // Filtro de búsqueda
    if (buscar) {
      const coincide = 
        mesa.numero.toString().includes(buscar) ||
        (mesa.tipo && mesa.tipo.toLowerCase().includes(buscar));
      if (!coincide) return false;
    }
    
    // Filtro de ubicación
    if (ubicacion !== 'todas' && mesa.tipo !== ubicacion) return false;
    
    // Filtro de estado
    if (estado === 'disponible' && !mesa.disponible) return false;
    if (estado === 'ocupada' && mesa.disponible) return false;
    
    return true;
  });
  
  actualizarEstadisticasMesas(mesasFiltradas);
  renderizarMesas(mesasFiltradas);
};

// Limpiar filtros
window.limpiarFiltrosMesas = function() {
  document.getElementById('filter-buscar-mesa').value = '';
  document.getElementById('filter-ubicacion').value = 'todas';
  document.getElementById('filter-estado').value = 'todas';
  
  mesasFiltradas = [...mesasData];
  actualizarEstadisticasMesas(mesasFiltradas);
  renderizarMesas(mesasFiltradas);
};

// Abrir modal crear mesa
window.abrirModalCrearMesa = function() {
  const modalHTML = `
    <div id="modal-crear-mesa" class="modal-overlay" onclick="window.cerrarModalSiClickFuera(event, 'modal-crear-mesa')">
      <div class="modal-content" style="max-width: 500px;">
        <div class="modal-header">
          <h2>➕ Nueva Mesa</h2>
          <button class="close-modal" onclick="window.cerrarModal('modal-crear-mesa')">&times;</button>
        </div>
        <form id="form-crear-mesa" onsubmit="window.crearMesa(event); return false;">
          <div class="form-grid">
            <div class="form-group">
              <label>Número de Mesa *</label>
              <input type="number" id="new-mesa-numero" required min="1" placeholder="Ej: 1">
            </div>
            
            <div class="form-group">
              <label>Capacidad (personas) *</label>
              <input type="number" id="new-mesa-capacidad" required min="1" max="20" placeholder="Ej: 4">
            </div>
            
            <div class="form-group">
              <label>Tipo de Mesa *</label>
              <select id="new-mesa-tipo" required>
                <option value="interior">🏠 Interior</option>
                <option value="terraza">🌳 Terraza</option>
                <option value="vip">👑 VIP</option>
              </select>
            </div>
            
            <div class="form-group">
              <label>Estado Inicial</label>
              <select id="new-mesa-disponible">
                <option value="true">✅ Disponible</option>
                <option value="false">🔒 Ocupada</option>
              </select>
            </div>
          </div>
          
          <div class="modal-actions">
            <button type="submit" class="btn-primary">✅ Crear Mesa</button>
            <button type="button" class="btn-secondary" onclick="window.cerrarModal('modal-crear-mesa')">❌ Cancelar</button>
          </div>
        </form>
      </div>
    </div>
  `;
  
  document.body.insertAdjacentHTML('beforeend', modalHTML);
};

// Crear mesa
window.crearMesa = async function(event) {
  event.preventDefault();
  
  try {
    const data = {
      numero: parseInt(document.getElementById('new-mesa-numero').value),
      capacidad: parseInt(document.getElementById('new-mesa-capacidad').value),
      tipo: document.getElementById('new-mesa-tipo').value,
      disponible: document.getElementById('new-mesa-disponible').value === 'true'
    };
    
    await window.API.post('/api/mesas', data);
    showToast('✅ Mesa creada exitosamente', 'success');
    window.cerrarModal('modal-crear-mesa');
    await cargarMesas();
    
  } catch (err) {
    showToast('❌ Error: ' + err.message, 'error');
  }
};

// Editar mesa
window.editarMesa = async function(mesaId) {
  const mesa = mesasData.find(m => m.id === mesaId);
  if (!mesa) {
    showToast('❌ Mesa no encontrada', 'error');
    return;
  }
  
  const modalHTML = `
    <div id="modal-editar-mesa" class="modal-overlay" onclick="window.cerrarModalSiClickFuera(event, 'modal-editar-mesa')">
      <div class="modal-content" style="max-width: 500px;">
        <div class="modal-header">
          <h2>✏️ Editar Mesa ${mesa.numero}</h2>
          <button class="close-modal" onclick="window.cerrarModal('modal-editar-mesa')">&times;</button>
        </div>
        <form id="form-editar-mesa" onsubmit="window.guardarMesa(event, ${mesaId}); return false;">
          <div class="form-grid">
            <div class="form-group">
              <label>Número de Mesa *</label>
              <input type="number" id="edit-mesa-numero" required min="1" value="${mesa.numero}">
            </div>
            
            <div class="form-group">
              <label>Capacidad (personas) *</label>
              <input type="number" id="edit-mesa-capacidad" required min="1" max="20" value="${mesa.capacidad}">
            </div>
            
            <div class="form-group">
              <label>Tipo de Mesa *</label>
              <select id="edit-mesa-tipo" required>
                <option value="interior" ${mesa.tipo === 'interior' ? 'selected' : ''}>🏠 Interior</option>
                <option value="terraza" ${mesa.tipo === 'terraza' ? 'selected' : ''}>🌳 Terraza</option>
                <option value="vip" ${mesa.tipo === 'vip' ? 'selected' : ''}>👑 VIP</option>
              </select>
            </div>
            
            <div class="form-group">
              <label>Estado</label>
              <select id="edit-mesa-disponible">
                <option value="true" ${mesa.disponible ? 'selected' : ''}>✅ Disponible</option>
                <option value="false" ${!mesa.disponible ? 'selected' : ''}>🔒 Ocupada</option>
              </select>
            </div>
          </div>
          
          <div class="modal-actions">
            <button type="submit" class="btn-primary">💾 Guardar Cambios</button>
            <button type="button" class="btn-danger" onclick="window.eliminarMesa(${mesaId})">🗑️ Eliminar</button>
            <button type="button" class="btn-secondary" onclick="window.cerrarModal('modal-editar-mesa')">❌ Cancelar</button>
          </div>
        </form>
      </div>
    </div>
  `;
  
  document.body.insertAdjacentHTML('beforeend', modalHTML);
};

// Guardar cambios de mesa
window.guardarMesa = async function(event, mesaId) {
  event.preventDefault();
  
  try {
    const data = {
      numero: parseInt(document.getElementById('edit-mesa-numero').value),
      capacidad: parseInt(document.getElementById('edit-mesa-capacidad').value),
      tipo: document.getElementById('edit-mesa-tipo').value,
      disponible: document.getElementById('edit-mesa-disponible').value === 'true'
    };
    
    await window.API.put(`/api/mesas/${mesaId}/actualizar`, data);
    showToast('✅ Mesa actualizada exitosamente', 'success');
    window.cerrarModal('modal-editar-mesa');
    await cargarMesas();
    
  } catch (err) {
    showToast('❌ Error: ' + err.message, 'error');
  }
};

// Toggle disponibilidad
window.toggleDisponibilidadMesa = async function(mesaId, disponible) {
  try {
    await window.API.put(`/api/mesas/${mesaId}/disponibilidad`, { disponible });
    showToast(`✅ Mesa ${disponible ? 'liberada' : 'marcada como ocupada'}`, 'success');
    await cargarMesas();
  } catch (err) {
    showToast('❌ Error: ' + err.message, 'error');
  }
};

// Eliminar mesa
window.eliminarMesa = async function(mesaId) {
  if (!confirm('⚠️ ¿Estás seguro de eliminar esta mesa? Esta acción no se puede deshacer.')) {
    return;
  }
  
  try {
    await window.API.del(`/api/mesas/${mesaId}`);
    showToast('✅ Mesa eliminada exitosamente', 'success');
    window.cerrarModal('modal-editar-mesa');
    await cargarMesas();
  } catch (err) {
    showToast('❌ Error: ' + err.message, 'error');
  }
};

// Cerrar modal
window.cerrarModal = function(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) modal.remove();
};

// Cerrar modal si se hace clic fuera
window.cerrarModalSiClickFuera = function(event, modalId) {
  if (event.target.classList.contains('modal-overlay')) {
    window.cerrarModal(modalId);
  }
};

// Toast notification
function showToast(message, type = 'info') {
  if (typeof Toastify !== 'undefined') {
    Toastify({
      text: message,
      duration: 3000,
      gravity: "top",
      position: "right",
      backgroundColor: type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#6366f1',
    }).showToast();
  } else {
    alert(message);
  }
}

// Exportar para uso global
window.cargarMesas = cargarMesas;

// Marcar módulo como cargado
window.mesasModuleLoaded = true;

console.log('✅ Módulo Mesas cargado');

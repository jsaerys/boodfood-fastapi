// static/js/admin/pedidos.js
// Módulo completo de gestión de pedidos

var pedidosData = [];
var pedidosFiltrados = [];

// Módulo Pedidos
window.Pedidos = {
  init: async function() {
    console.log('🍽️ Inicializando módulo Pedidos...');
    await cargarPedidos();
    setInterval(async function() { await cargarPedidos(); }, 30000);
  },
  cargarPedidos: async function() {
    await cargarPedidos();
  }
};

async function cargarPedidos() {
  try {
    var pedidos = await window.API.get('/api/pedidos');
    pedidosData = pedidos;
    pedidosFiltrados = [].concat(pedidos);
    actualizarEstadisticasPedidos(pedidos);
    renderizarPedidos(pedidosFiltrados);
    console.log('✅ ' + pedidos.length + ' pedidos cargados');
  } catch (err) {
    console.error('❌ Error al cargar pedidos:', err);
    document.getElementById('pedidos-container').innerHTML = 
      '<div style="text-align: center; padding: 40px; color: #ef4444;">' +
        '<p style="font-size: 48px;">❌</p>' +
        '<p style="font-size: 18px; margin-top: 16px;">Error al cargar pedidos: ' + err.message + '</p>' +
        '<button onclick="window.cargarPedidos()" style="margin-top: 16px; padding: 10px 20px; background: #6366f1; color: white; border: none; border-radius: 8px; cursor: pointer;">🔄 Reintentar</button>' +
      '</div>';
  }
}

function actualizarEstadisticasPedidos(pedidos) {
  var pendientes = 0, preparando = 0, enviados = 0, entregadosHoy = 0, ventasHoy = 0, total = pedidos.length;
  var hoy = new Date().toISOString().split('T')[0];
  
  pedidos.forEach(function(p) {
    if (p.estado === 'pendiente') pendientes++;
    if (p.estado === 'preparando') preparando++;
    if (p.estado === 'enviado') enviados++;
    
    if (p.fecha_pedido && p.fecha_pedido.startsWith(hoy)) {
      if (p.estado === 'entregado') entregadosHoy++;
      if (p.estado !== 'cancelado' && p.estado !== 'rechazado') {
        ventasHoy += (p.total || 0);
      }
    }
  });
  
  document.getElementById('pedidos-pendientes').textContent = pendientes;
  document.getElementById('pedidos-preparando').textContent = preparando;
  document.getElementById('pedidos-enviados').textContent = enviados;
  document.getElementById('pedidos-entregados').textContent = entregadosHoy;
  document.getElementById('ventas-hoy-pedidos').textContent = formatCurrency(ventasHoy);
  document.getElementById('pedidos-total').textContent = total;
}

function renderizarPedidos(pedidos) {
  console.log('🎨 Renderizando', pedidos.length, 'pedidos...');
  var container = document.getElementById('pedidos-container');
  container.className = '';
  
  if (!pedidos || pedidos.length === 0) {
    container.innerHTML = '<div class="no-pedidos"><div class="no-pedidos-icon">📦</div><div class="no-pedidos-text">No hay pedidos registrados</div><div class="no-pedidos-subtext">Los pedidos aparecerán aquí automáticamente</div></div>';
    return;
  }
  
  var html = '<div class="pedidos-table-container"><table class="pedidos-table"><thead><tr><th>Código</th><th>Tipo</th><th>Cliente/Mesa</th><th>Teléfono</th><th>Items</th><th>Total</th><th>Pago</th><th>Estado</th><th>Fecha</th><th>Acciones</th></tr></thead><tbody id="tbody-pedidos">';
  
  pedidos.forEach(function(p) {
    // Detectar tipo de servicio correctamente
    var tipo = p.tipo_servicio || (p.direccion_entrega ? 'domicilio' : 'mesa');
    var tipoText = tipo.charAt(0).toUpperCase() + tipo.slice(1);
    var tipoIcon = {
      'piscina': '🏊',
      'billar': '🎱',
      'eventos': '🎉',
      'domicilio': '🏠',
      'mesa': '🍽️'
    }[tipo] || '🍽️';
    
    var clienteInfo = '';
    if (tipo === 'domicilio') {
      clienteInfo = p.nombre_receptor || 'Cliente';
    } else if (tipo === 'mesa') {
      clienteInfo = 'Mesa #' + (p.mesa_id || 'N/A');
    } else {
      clienteInfo = tipoText + ' - ' + (p.nombre_receptor || 'Cliente');
    }
    
    var telefono = p.telefono_contacto || '-';
    var numItems = (p.items && p.items.length) || 0;
    var fechaFormateada = p.fecha_pedido ? formatDateTime(p.fecha_pedido) : 'N/A';
    var fechaSolo = p.fecha_pedido ? p.fecha_pedido.split('T')[0] : '';
    var metodoPago = (p.metodo_pago || 'efectivo').toUpperCase();
    
    html += '<tr data-pedido-id="' + p.id + '" data-tipo="' + tipo + '" data-estado="' + p.estado + '" data-fecha="' + fechaSolo + '" data-metodo-pago="' + (p.metodo_pago || 'efectivo') + '">' +
      '<td><strong>#' + (p.codigo_pedido || p.id) + '</strong></td>' +
      '<td><span class="badge badge-' + tipo + '">' + tipoIcon + ' ' + tipoText + '</span></td>' +
      '<td>' + clienteInfo + '</td><td>' + telefono + '</td><td>' + numItems + ' items</td>' +
      '<td><strong>' + formatCurrency(p.total) + '</strong></td>' +
      '<td>' + metodoPago + '</td>' +
      '<td><select class="estado-select" data-pedido-id="' + p.id + '" onchange="window.cambiarEstadoPedido(' + p.id + ', this.value)">' +
        '<option value="pendiente" ' + (p.estado === 'pendiente' ? 'selected' : '') + '>⏳ Pendiente</option>' +
        '<option value="preparando" ' + (p.estado === 'preparando' ? 'selected' : '') + '>👨‍🍳 Preparando</option>' +
        '<option value="enviado" ' + (p.estado === 'enviado' ? 'selected' : '') + '>🚚 Enviado</option>' +
        '<option value="entregado" ' + (p.estado === 'entregado' ? 'selected' : '') + '>✅ Entregado</option>' +
        '<option value="cancelado" ' + (p.estado === 'cancelado' ? 'selected' : '') + '>❌ Cancelado</option>' +
        '<option value="rechazado" ' + (p.estado === 'rechazado' ? 'selected' : '') + '>🚫 Rechazado</option>' +
      '</select></td>' +
      '<td>' + fechaFormateada + '</td>' +
      '<td><div class="action-buttons">' +
        '<button class="ghost small" onclick="window.verDetallesPedido(' + p.id + ')">👁️ Ver</button>' +
        '<button class="ghost small" onclick="window.editarPedido(' + p.id + ')">✏️ Editar</button>' +
        '<button class="ghost small" onclick="window.imprimirPedido(' + p.id + ')">🖨️ Imprimir</button>' +
        '<button class="ghost small" onclick="window.eliminarPedido(' + p.id + ', \'' + (p.codigo_pedido || p.id) + '\')">🗑️ Eliminar</button>' +
      '</div></td></tr>';
  });
  
  html += '</tbody></table></div>';
  container.innerHTML = html;
  
  console.log('✅ Pedidos renderizados correctamente');
}

// Funciones de filtrado
window.filtrarPedidos = function() {
  var buscar = document.getElementById('filter-buscar-pedido').value.toLowerCase();
  var tipo = document.getElementById('filter-tipo-pedido').value;
  var estado = document.getElementById('filter-estado-pedido').value;
  var fecha = document.getElementById('filter-fecha-pedido').value;
  var metodoPago = document.getElementById('filter-metodo-pago').value;
  
  pedidosFiltrados = pedidosData.filter(function(pedido) {
    if (buscar) {
      var searchText = (pedido.codigo_pedido || '') + ' ' + (pedido.nombre_receptor || '') + ' ' + (pedido.telefono_contacto || '') + ' ' + (pedido.mesa_id || '');
      if (searchText.toLowerCase().indexOf(buscar) === -1) return false;
    }
    
    if (tipo !== 'todos') {
      var pedidoTipo = pedido.tipo_servicio || (pedido.direccion_entrega ? 'domicilio' : 'mesa');
      if (pedidoTipo !== tipo) return false;
    }
    
    if (estado !== 'todos' && pedido.estado !== estado) return false;
    
    if (fecha) {
      var pedidoFecha = pedido.fecha_pedido ? pedido.fecha_pedido.split('T')[0] : '';
      if (pedidoFecha !== fecha) return false;
    }
    
    if (metodoPago !== 'todos' && (pedido.metodo_pago || 'efectivo') !== metodoPago) return false;
    
    return true;
  });
  
  renderizarPedidos(pedidosFiltrados);
};

window.limpiarFiltrosPedidos = function() {
  document.getElementById('filter-buscar-pedido').value = '';
  document.getElementById('filter-tipo-pedido').value = 'todos';
  document.getElementById('filter-estado-pedido').value = 'todos';
  document.getElementById('filter-fecha-pedido').value = '';
  document.getElementById('filter-metodo-pago').value = 'todos';
  pedidosFiltrados = [].concat(pedidosData);
  renderizarPedidos(pedidosFiltrados);
};

window.cambiarEstadoPedido = async function(pedidoId, nuevoEstado) {
  console.log('🔄 Cambiando estado del pedido', pedidoId, 'a', nuevoEstado);
  try {
    await window.API.put('/api/pedidos/' + pedidoId + '/estado', { estado: nuevoEstado });
    showToast('✅ Estado actualizado correctamente', 'success');
    console.log('✅ Estado actualizado en backend, recargando...');
    await cargarPedidos();
    console.log('✅ Pedidos recargados');
  } catch (err) {
    console.error('❌ Error al cambiar estado:', err);
    showToast('❌ Error al actualizar estado: ' + err.message, 'error');
  }
};

window.verDetallesPedido = async function(pedidoId) {
  console.log('Ver detalles del pedido:', pedidoId);
  try {
    var pedido = await window.API.get('/api/pedidos/' + pedidoId);
    var tipo = pedido.direccion_entrega ? 'domicilio' : 'mesa';
    var tipoIcon = tipo === 'domicilio' ? '🏠' : '🍽️';
    var tipoText = tipo === 'domicilio' ? 'Domicilio' : 'En Mesa';
    
    var itemsHTML = (pedido.items || []).map(function(item, index) {
      return '<tr style="border-bottom: 1px solid #e2e8f0; ' + (index % 2 === 0 ? 'background: #f8fafc;' : '') + '">' +
        '<td style="padding: 12px;"><strong>' + item.nombre_item + '</strong></td>' +
        '<td style="padding: 12px; text-align: center;">' + item.cantidad + '</td>' +
        '<td style="padding: 12px; text-align: right;">' + formatCurrency(item.precio_unitario) + '</td>' +
        '<td style="padding: 12px; text-align: right;"><strong>' + formatCurrency(item.subtotal) + '</strong></td>' +
        '</tr>';
    }).join('');
    
    var clienteHTML = tipo === 'domicilio' ? 
      '<div style="display: grid; gap: 12px;">' +
        '<div style="display: flex; justify-content: space-between;"><strong>Nombre:</strong> <span>' + (pedido.nombre_receptor || 'N/A') + '</span></div>' +
        '<div style="display: flex; justify-content: space-between;"><strong>Teléfono:</strong> <span>' + (pedido.telefono_contacto || 'N/A') + '</span></div>' +
        '<div style="margin-top: 8px;"><strong>Dirección de Entrega:</strong><div style="margin-top: 8px; padding: 12px; background: white; border-radius: 8px; border: 1px solid #e2e8f0;">' + (pedido.direccion_entrega || 'N/A') + '</div></div>' +
      '</div>' : 
      '<div style="display: flex; justify-content: space-between;"><strong>Mesa:</strong> <span style="font-size: 20px; font-weight: 700; color: #3b82f6;">Mesa #' + (pedido.mesa_id || 'N/A') + '</span></div>';
    
    var botonEntregado = (pedido.estado !== 'entregado' && pedido.estado !== 'cancelado') ? 
      '<button onclick="window.cambiarEstadoPedido(' + pedidoId + ', \'entregado\'); window.cerrarModal(\'modal-detalle-pedido\');" style="padding: 10px 20px; background: linear-gradient(135deg, #10b981, #059669); color: white; border: none; border-radius: 8px; font-weight: 600; cursor: pointer;">✅ Marcar Entregado</button>' : '';
    
    var botonEnviar = (tipo === 'domicilio' && pedido.estado === 'preparando') ? 
      '<button onclick="window.enviarPedidoDomicilio(' + pedidoId + '); window.cerrarModal(\'modal-detalle-pedido\');" style="padding: 10px 20px; background: linear-gradient(135deg, #06b6d4, #0891b2); color: white; border: none; border-radius: 8px; font-weight: 600; cursor: pointer;">🚚 Enviar a Domicilio</button>' : '';
    
    var modalHTML = '<div id="modal-detalle-pedido" class="modal-overlay" onclick="window.cerrarModalSiClickFuera(event, \'modal-detalle-pedido\')">' +
        '<div class="modal-content" style="max-width: 800px; max-height: 90vh; overflow-y: auto;">' +
          '<div class="modal-header"><h2>' + tipoIcon + ' Pedido #' + (pedido.codigo_pedido || pedido.id) + '</h2>' +
            '<button class="close-modal" onclick="window.cerrarModal(\'modal-detalle-pedido\')">&times;</button></div>' +
          '<div style="padding: 24px;">' +
            '<div style="margin-bottom: 24px; padding: 20px; background: #f8fafc; border-radius: 12px;">' +
              '<h3 style="margin: 0 0 16px 0; font-size: 18px; color: #1e293b;">📋 Información General</h3>' +
              '<div style="display: grid; gap: 12px;">' +
                '<div style="display: flex; justify-content: space-between;"><strong>Tipo:</strong> <span class="badge badge-' + tipo + '">' + tipoText + '</span></div>' +
                '<div style="display: flex; justify-content: space-between;"><strong>Estado:</strong> <span class="badge badge-' + pedido.estado + '">' + pedido.estado + '</span></div>' +
                '<div style="display: flex; justify-content: space-between;"><strong>Método de Pago:</strong> <span>' + (pedido.metodo_pago || 'efectivo').toUpperCase() + '</span></div>' +
                '<div style="display: flex; justify-content: space-between;"><strong>Fecha Pedido:</strong> <span>' + formatDateTime(pedido.fecha_pedido) + '</span></div>' +
              '</div>' +
            '</div>' +
            '<div style="margin-bottom: 24px; padding: 20px; background: #f8fafc; border-radius: 12px;">' +
              '<h3 style="margin: 0 0 16px 0; font-size: 18px; color: #1e293b;">' + (tipo === 'domicilio' ? '👤 Información del Cliente' : '🍽️ Información de Mesa') + '</h3>' +
              clienteHTML +
            '</div>' +
            '<div style="margin-bottom: 24px;">' +
              '<h3 style="margin: 0 0 16px 0; font-size: 18px; color: #1e293b;">🍽️ Items del Pedido</h3>' +
              '<div style="overflow-x: auto;"><table style="width: 100%; border-collapse: collapse;">' +
                '<thead style="background: #f1f5f9;"><tr>' +
                  '<th style="padding: 12px; text-align: left; font-weight: 600; border-bottom: 2px solid #e2e8f0;">Producto</th>' +
                  '<th style="padding: 12px; text-align: center; font-weight: 600; border-bottom: 2px solid #e2e8f0;">Cant.</th>' +
                  '<th style="padding: 12px; text-align: right; font-weight: 600; border-bottom: 2px solid #e2e8f0;">Precio Unit.</th>' +
                  '<th style="padding: 12px; text-align: right; font-weight: 600; border-bottom: 2px solid #e2e8f0;">Subtotal</th>' +
                '</tr></thead>' +
                '<tbody>' + itemsHTML + '</tbody>' +
              '</table></div>' +
            '</div>' +
            '<div style="padding: 24px; background: linear-gradient(135deg, #f8fafc, #f1f5f9); border-radius: 12px; border: 2px solid #e2e8f0;">' +
              '<div style="display: flex; justify-content: space-between; margin-bottom: 12px; font-size: 16px;"><span>Subtotal:</span><span style="font-weight: 600;">' + formatCurrency(pedido.subtotal || pedido.total) + '</span></div>' +
              '<div style="display: flex; justify-content: space-between; font-size: 24px; font-weight: 700; border-top: 2px solid #cbd5e1; padding-top: 16px; margin-top: 12px; color: #1e293b;"><span>TOTAL:</span><span style="color: #10b981;">' + formatCurrency(pedido.total) + '</span></div>' +
            '</div>' +
          '</div>' +
          '<div style="padding: 0 24px 24px 24px; display: flex; gap: 12px; justify-content: flex-end; flex-wrap: wrap;">' +
            '<button onclick="window.cerrarModal(\'modal-detalle-pedido\')" style="padding: 10px 20px; background: #e2e8f0; color: #475569; border: none; border-radius: 8px; font-weight: 600; cursor: pointer;">Cerrar</button>' +
            '<button onclick="window.imprimirPedido(' + pedidoId + ')" style="padding: 10px 20px; background: linear-gradient(135deg, #9333ea, #7e22ce); color: white; border: none; border-radius: 8px; font-weight: 600; cursor: pointer;">🖨️ Imprimir</button>' +
            botonEnviar +
            botonEntregado +
          '</div>' +
        '</div>' +
      '</div>';
    
    document.body.insertAdjacentHTML('beforeend', modalHTML);
  } catch (err) {
    showToast('❌ Error al cargar detalles: ' + err.message, 'error');
  }
};

window.imprimirPedido = async function(pedidoId) {
  console.log('Imprimir pedido:', pedidoId);
  try {
    var pedido = await window.API.get('/api/pedidos/' + pedidoId);
    var tipo = pedido.direccion_entrega ? 'domicilio' : 'mesa';
    
    var itemsHTML = (pedido.items || []).map(function(item) {
      return '<tr><td style="padding: 8px; border-bottom: 1px solid #ddd;">' + item.nombre_item + '</td>' +
        '<td style="padding: 8px; text-align: center; border-bottom: 1px solid #ddd;">' + item.cantidad + '</td>' +
        '<td style="padding: 8px; text-align: right; border-bottom: 1px solid #ddd;">' + formatCurrency(item.precio_unitario) + '</td>' +
        '<td style="padding: 8px; text-align: right; border-bottom: 1px solid #ddd; font-weight: bold;">' + formatCurrency(item.subtotal) + '</td></tr>';
    }).join('');
    
    var printWindow = window.open('', '', 'width=800,height=600');
    printWindow.document.write('<html><head><title>Pedido #' + (pedido.codigo_pedido || pedido.id) + '</title>');
    printWindow.document.write('<style>body{font-family:Arial,sans-serif;padding:20px;max-width:800px;margin:0 auto;}' +
      '.header{text-align:center;border-bottom:3px solid #000;padding-bottom:20px;margin-bottom:20px;}' +
      '.header h1{margin:0;font-size:28px;color:#2563eb;}.header p{margin:5px 0;color:#666;}' +
      '.info-section{margin-bottom:20px;padding:15px;background:#f8fafc;border-radius:8px;}' +
      '.info-section h3{margin:0 0 10px 0;color:#1e293b;border-bottom:2px solid #cbd5e1;padding-bottom:8px;}' +
      '.info-row{display:flex;justify-content:space-between;margin:8px 0;padding:4px 0;}' +
      '.label{font-weight:bold;color:#475569;}.value{color:#1e293b;}' +
      'table{width:100%;border-collapse:collapse;margin:20px 0;}' +
      'th{background:#1e293b;color:white;padding:12px;text-align:left;font-weight:bold;}' +
      'td{padding:8px;border-bottom:1px solid #ddd;}' +
      '.totals{margin-top:20px;padding:15px;background:#f1f5f9;border-radius:8px;}' +
      '.total-row{display:flex;justify-content:space-between;margin:8px 0;font-size:16px;}' +
      '.grand-total{border-top:3px solid #000;padding-top:15px;margin-top:15px;font-size:24px;font-weight:bold;color:#10b981;}' +
      '.footer{text-align:center;margin-top:40px;padding-top:20px;border-top:2px solid #ddd;color:#666;font-size:14px;}' +
      '@media print{body{padding:10px;}.no-print{display:none;}}</style></head><body>');
    
    printWindow.document.write('<div class="header"><h1>RESTAURANTE</h1><p>Pedido #' + (pedido.codigo_pedido || pedido.id) + '</p>' +
      '<p>' + formatDateTime(pedido.fecha_pedido) + '</p></div>');
    
    printWindow.document.write('<div class="info-section"><h3>Información del Pedido</h3>' +
      '<div class="info-row"><span class="label">Tipo:</span><span class="value">' + (tipo === 'domicilio' ? 'Domicilio' : 'En Mesa') + '</span></div>' +
      '<div class="info-row"><span class="label">Estado:</span><span class="value">' + pedido.estado.toUpperCase() + '</span></div>' +
      '<div class="info-row"><span class="label">Método de Pago:</span><span class="value">' + (pedido.metodo_pago || 'efectivo').toUpperCase() + '</span></div></div>');
    
    if (tipo === 'domicilio') {
      printWindow.document.write('<div class="info-section"><h3>Información del Cliente</h3>' +
        '<div class="info-row"><span class="label">Nombre:</span><span class="value">' + (pedido.nombre_receptor || 'N/A') + '</span></div>' +
        '<div class="info-row"><span class="label">Teléfono:</span><span class="value">' + (pedido.telefono_contacto || 'N/A') + '</span></div>' +
        '<div class="info-row"><span class="label">Dirección:</span><span class="value">' + (pedido.direccion_entrega || 'N/A') + '</span></div></div>');
    } else {
      printWindow.document.write('<div class="info-section"><h3>Información de Mesa</h3>' +
        '<div class="info-row"><span class="label">Mesa:</span><span class="value" style="font-size:20px;font-weight:bold;color:#3b82f6;">Mesa #' + (pedido.mesa_id || 'N/A') + '</span></div></div>');
    }
    
    printWindow.document.write('<div class="info-section"><h3>Items del Pedido</h3><table><thead><tr>' +
      '<th>Producto</th><th style="text-align:center;">Cantidad</th><th style="text-align:right;">Precio Unit.</th>' +
      '<th style="text-align:right;">Subtotal</th></tr></thead><tbody>' + itemsHTML + '</tbody></table></div>');
    
    printWindow.document.write('<div class="totals"><div class="total-row"><span>Subtotal:</span><span>' + formatCurrency(pedido.subtotal || pedido.total) + '</span></div>' +
      '<div class="total-row grand-total"><span>TOTAL:</span><span>' + formatCurrency(pedido.total) + '</span></div></div>');
    
    printWindow.document.write('<div class="footer"><p>¡Gracias por su pedido!</p><p>Este es un comprobante válido de su pedido</p></div>');
    
    printWindow.document.write('<div class="no-print" style="text-align:center;margin-top:30px;">' +
      '<button onclick="window.print()" style="padding:12px 24px;background:#3b82f6;color:white;border:none;border-radius:8px;font-size:16px;cursor:pointer;margin-right:10px;">🖨️ Imprimir</button>' +
      '<button onclick="window.close()" style="padding:12px 24px;background:#e2e8f0;color:#475569;border:none;border-radius:8px;font-size:16px;cursor:pointer;">Cerrar</button></div>');
    
    printWindow.document.write('</body></html>');
    printWindow.document.close();
  } catch (err) {
    showToast('❌ Error al generar impresión: ' + err.message, 'error');
  }
};

window.editarPedido = async function(pedidoId) {
  console.log('Editar pedido:', pedidoId);
  try {
    var pedido = await window.API.get('/api/pedidos/' + pedidoId);
    var tipo = pedido.direccion_entrega ? 'domicilio' : 'mesa';
    
    var formHTML = '<div id="modal-editar-pedido" class="modal-overlay" onclick="window.cerrarModalSiClickFuera(event, \'modal-editar-pedido\')">' +
      '<div class="modal-content" style="max-width: 600px;">' +
        '<div class="modal-header"><h2>✏️ Editar Pedido #' + (pedido.codigo_pedido || pedido.id) + '</h2>' +
          '<button class="close-modal" onclick="window.cerrarModal(\'modal-editar-pedido\')">&times;</button></div>' +
        '<div style="padding: 24px;">' +
          '<form id="form-editar-pedido" onsubmit="event.preventDefault(); window.guardarEdicionPedido(' + pedidoId + ');">' +
            '<div style="margin-bottom: 20px;">' +
              '<label style="display: block; margin-bottom: 8px; font-weight: 600;">Estado:</label>' +
              '<select id="edit-estado" class="estado-select" style="width: 100%; padding: 10px;">' +
                '<option value="pendiente" ' + (pedido.estado === 'pendiente' ? 'selected' : '') + '>⏳ Pendiente</option>' +
                '<option value="preparando" ' + (pedido.estado === 'preparando' ? 'selected' : '') + '>👨‍🍳 Preparando</option>' +
                '<option value="enviado" ' + (pedido.estado === 'enviado' ? 'selected' : '') + '>🚚 Enviado</option>' +
                '<option value="entregado" ' + (pedido.estado === 'entregado' ? 'selected' : '') + '>✅ Entregado</option>' +
                '<option value="cancelado" ' + (pedido.estado === 'cancelado' ? 'selected' : '') + '>❌ Cancelado</option>' +
                '<option value="rechazado" ' + (pedido.estado === 'rechazado' ? 'selected' : '') + '>🚫 Rechazado</option>' +
              '</select>' +
            '</div>' +
            '<div style="margin-bottom: 20px;">' +
              '<label style="display: block; margin-bottom: 8px; font-weight: 600;">Método de Pago:</label>' +
              '<select id="edit-metodo-pago" style="width: 100%; padding: 10px; border: 1px solid #e2e8f0; border-radius: 8px;">' +
                '<option value="efectivo" ' + (pedido.metodo_pago === 'efectivo' ? 'selected' : '') + '>💵 Efectivo</option>' +
                '<option value="tarjeta" ' + (pedido.metodo_pago === 'tarjeta' ? 'selected' : '') + '>💳 Tarjeta</option>' +
                '<option value="transferencia" ' + (pedido.metodo_pago === 'transferencia' ? 'selected' : '') + '>🏦 Transferencia</option>' +
              '</select>' +
            '</div>';
    
    if (tipo === 'domicilio') {
      formHTML += '<div style="margin-bottom: 20px;">' +
          '<label style="display: block; margin-bottom: 8px; font-weight: 600;">Nombre del Receptor:</label>' +
          '<input type="text" id="edit-nombre-receptor" value="' + (pedido.nombre_receptor || '') + '" style="width: 100%; padding: 10px; border: 1px solid #e2e8f0; border-radius: 8px;">' +
        '</div>' +
        '<div style="margin-bottom: 20px;">' +
          '<label style="display: block; margin-bottom: 8px; font-weight: 600;">Teléfono:</label>' +
          '<input type="tel" id="edit-telefono" value="' + (pedido.telefono_contacto || '') + '" style="width: 100%; padding: 10px; border: 1px solid #e2e8f0; border-radius: 8px;">' +
        '</div>' +
        '<div style="margin-bottom: 20px;">' +
          '<label style="display: block; margin-bottom: 8px; font-weight: 600;">Dirección de Entrega:</label>' +
          '<textarea id="edit-direccion" rows="3" style="width: 100%; padding: 10px; border: 1px solid #e2e8f0; border-radius: 8px;">' + (pedido.direccion_entrega || '') + '</textarea>' +
        '</div>';
    } else {
      formHTML += '<div style="margin-bottom: 20px;">' +
          '<label style="display: block; margin-bottom: 8px; font-weight: 600;">Mesa:</label>' +
          '<input type="number" id="edit-mesa-id" value="' + (pedido.mesa_id || '') + '" min="1" style="width: 100%; padding: 10px; border: 1px solid #e2e8f0; border-radius: 8px;">' +
        '</div>';
    }
    
    formHTML += '<div style="margin-bottom: 20px;">' +
        '<label style="display: block; margin-bottom: 8px; font-weight: 600;">Instrucciones:</label>' +
        '<textarea id="edit-instrucciones" rows="2" style="width: 100%; padding: 10px; border: 1px solid #e2e8f0; border-radius: 8px;">' + (pedido.instrucciones_entrega || '') + '</textarea>' +
      '</div>' +
      '<div style="display: flex; gap: 12px; justify-content: flex-end; margin-top: 24px;">' +
        '<button type="button" onclick="window.cerrarModal(\'modal-editar-pedido\')" style="padding: 10px 20px; background: #e2e8f0; color: #475569; border: none; border-radius: 8px; font-weight: 600; cursor: pointer;">Cancelar</button>' +
        '<button type="submit" style="padding: 10px 20px; background: linear-gradient(135deg, #3b82f6, #2563eb); color: white; border: none; border-radius: 8px; font-weight: 600; cursor: pointer;">💾 Guardar Cambios</button>' +
      '</div>' +
    '</form>' +
  '</div></div></div>';
    
    document.body.insertAdjacentHTML('beforeend', formHTML);
  } catch (err) {
    showToast('❌ Error al cargar pedido: ' + err.message, 'error');
  }
};

window.guardarEdicionPedido = async function(pedidoId) {
  try {
    var data = {
      estado: document.getElementById('edit-estado').value,
      metodo_pago: document.getElementById('edit-metodo-pago').value,
      instrucciones_entrega: document.getElementById('edit-instrucciones').value
    };
    
    var nombreReceptor = document.getElementById('edit-nombre-receptor');
    var telefono = document.getElementById('edit-telefono');
    var direccion = document.getElementById('edit-direccion');
    var mesaId = document.getElementById('edit-mesa-id');
    
    if (nombreReceptor) data.nombre_receptor = nombreReceptor.value;
    if (telefono) data.telefono_contacto = telefono.value;
    if (direccion) data.direccion_entrega = direccion.value;
    if (mesaId) data.mesa_id = parseInt(mesaId.value) || null;
    
    await window.API.put('/api/pedidos/' + pedidoId, data);
    showToast('✅ Pedido actualizado correctamente', 'success');
    window.cerrarModal('modal-editar-pedido');
    await cargarPedidos();
  } catch (err) {
    showToast('❌ Error al actualizar: ' + err.message, 'error');
  }
};

window.eliminarPedido = async function(pedidoId, codigoPedido) {
  console.log('Eliminar pedido:', pedidoId, codigoPedido);
  if (!confirm('⚠️ ¿Estás seguro de eliminar el pedido #' + codigoPedido + '?\n\nEsta acción no se puede deshacer.')) {
    return;
  }
  
  try {
    await window.API.del('/api/pedidos/' + pedidoId);
    showToast('✅ Pedido eliminado correctamente', 'success');
    await cargarPedidos();
  } catch (err) {
    showToast('❌ Error al eliminar: ' + err.message, 'error');
  }
};

window.enviarPedidoDomicilio = async function(pedidoId) {
  if (!confirm('¿Confirmar que el pedido está listo para enviar a domicilio?')) {
    return;
  }
  
  try {
    await window.API.put('/api/pedidos/' + pedidoId + '/estado', { estado: 'enviado' });
    showToast('🚚 Pedido marcado como enviado', 'success');
    await cargarPedidos();
  } catch (err) {
    showToast('❌ Error al enviar: ' + err.message, 'error');
  }
};

window.cerrarModal = function(modalId) {
  var modal = document.getElementById(modalId);
  if (modal) modal.remove();
};

window.cerrarModalSiClickFuera = function(event, modalId) {
  if (event.target.classList.contains('modal-overlay')) {
    window.cerrarModal(modalId);
  }
};

function formatCurrency(amount) {
  if (amount == null || isNaN(amount)) return '$0';
  return new Intl.NumberFormat('es-CO', {
    style: 'currency',
    currency: 'COP',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(amount);
}

function formatDateTime(dateString) {
  if (!dateString) return 'N/A';
  try {
    var date = new Date(dateString);
    if (isNaN(date.getTime())) return 'Fecha inválida';
    return new Intl.DateTimeFormat('es-CO', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      hour12: true
    }).format(date);
  } catch (err) {
    return 'Error en fecha';
  }
}

function showToast(message, type) {
  if (typeof Toastify === 'undefined') {
    alert(message);
    return;
  }
  var bgColor = type === 'success' ? 'linear-gradient(to right, #10b981, #059669)' : 
                type === 'error' ? 'linear-gradient(to right, #ef4444, #dc2626)' : 
                'linear-gradient(to right, #3b82f6, #2563eb)';
  Toastify({
    text: message,
    duration: 3000,
    gravity: 'top',
    position: 'right',
    style: {
      background: bgColor
    },
    stopOnFocus: true
  }).showToast();
}

window.cargarPedidos = window.Pedidos.cargarPedidos;
window.pedidosModuleLoaded = true;
console.log('✅ Módulo de Pedidos cargado correctamente');
console.log('Funciones disponibles:', {
  verDetallesPedido: typeof window.verDetallesPedido,
  editarPedido: typeof window.editarPedido,
  eliminarPedido: typeof window.eliminarPedido,
  imprimirPedido: typeof window.imprimirPedido,
  enviarPedidoDomicilio: typeof window.enviarPedidoDomicilio
});

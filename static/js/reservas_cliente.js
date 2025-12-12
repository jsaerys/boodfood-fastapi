// static/js/reservas_cliente.js
// Sistema completo de reservas para clientes

let pasoActual = 1;
let tipoServicioActual = 'mesa';
let mesaSeleccionada = null;
let mesasDisponibles = [];
let precios = {
    mesa: 20000,
    piscina: { 3: 50000, 5: 80000, 8: 120000 },
    billar: { 1: 30000, 2: 55000, 3: 75000 },
    evento: 500000
};

// ========================================
// INICIALIZACIÓN
// ========================================
document.addEventListener('DOMContentLoaded', function() {
    inicializarFormulario();
    if (document.getElementById('mis-reservas-container')) {
        cargarMisReservas();
    }
});

function inicializarFormulario() {
    // Configurar fecha mínima (hoy + 2 horas)
    const ahora = new Date();
    ahora.setHours(ahora.getHours() + 2);
    document.getElementById('fecha').min = ahora.toISOString().split('T')[0];
    
    // Event listeners
    document.getElementById('fecha').addEventListener('change', verificarDisponibilidad);
    document.getElementById('hora').addEventListener('change', verificarDisponibilidad);
    document.getElementById('numero_personas').addEventListener('change', verificarDisponibilidad);
    
    // Envío del formulario
    document.getElementById('form-reserva').addEventListener('submit', enviarReserva);
}

// ========================================
// SELECCIÓN DE SERVICIO
// ========================================
function seleccionarServicio(tipo) {
    tipoServicioActual = tipo;
    document.getElementById('tipo_servicio').value = tipo;
    
    // Actualizar UI
    document.querySelectorAll('.servicio-card').forEach(card => {
        card.classList.remove('active');
    });
    document.querySelector(`[data-tipo="${tipo}"]`).classList.add('active');
    
    // Mostrar/ocultar campos específicos
    document.querySelectorAll('.campos-especificos').forEach(campo => {
        campo.style.display = 'none';
    });
    
    const campoEspecifico = document.getElementById(`campos-${tipo}`);
    if (campoEspecifico) {
        campoEspecifico.style.display = 'block';
    }
    
    // Actualizar título del paso 2
    const titulos = {
        mesa: '🪑 Selecciona tu Mesa',
        piscina: '🏊 Selecciona tu Horario',
        billar: '🎱 Selecciona tu Mesa de Billar',
        evento: '🎉 Configuración del Evento'
    };
    document.getElementById('titulo-paso-2').textContent = titulos[tipo] || 'Selección';
}

// ========================================
// NAVEGACIÓN DE PASOS
// ========================================
function siguientePaso(paso) {
    // Validar paso actual antes de avanzar
    if (!validarPaso(pasoActual)) {
        return;
    }
    
    // Ocultar paso actual
    document.querySelector(`.form-step[data-step="${pasoActual}"]`).classList.remove('active');
    
    // Mostrar siguiente paso
    pasoActual = paso;
    document.querySelector(`.form-step[data-step="${paso}"]`).classList.add('active');
    
    // Scroll al inicio
    window.scrollTo({ top: 0, behavior: 'smooth' });
    
    // Acciones específicas por paso
    if (paso === 2) {
        cargarMesasDisponibles();
    } else if (paso === 4) {
        actualizarResumen();
    }
}

function anteriorPaso(paso) {
    document.querySelector(`.form-step[data-step="${pasoActual}"]`).classList.remove('active');
    pasoActual = paso;
    document.querySelector(`.form-step[data-step="${paso}"]`).classList.add('active');
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function validarPaso(paso) {
    if (paso === 1) {
        const fecha = document.getElementById('fecha').value;
        const hora = document.getElementById('hora').value;
        const personas = document.getElementById('numero_personas').value;
        
        if (!fecha || !hora || !personas) {
            mostrarToast('Por favor completa todos los campos requeridos', 'error');
            return false;
        }
        
        // Validar que la fecha no sea en el pasado
        const fechaSeleccionada = new Date(fecha + 'T' + hora);
        const ahora = new Date();
        ahora.setHours(ahora.getHours() + 2);
        
        if (fechaSeleccionada < ahora) {
            mostrarToast('La reserva debe ser con al menos 2 horas de anticipación', 'error');
            return false;
        }
        
        return true;
    } else if (paso === 2) {
        if (tipoServicioActual === 'mesa' && !mesaSeleccionada) {
            mostrarToast('Por favor selecciona una mesa', 'error');
            return false;
        }
        return true;
    } else if (paso === 3) {
        const nombre = document.getElementById('nombre_reserva').value;
        const telefono = document.getElementById('telefono_reserva').value;
        const email = document.getElementById('email_reserva').value;
        
        if (!nombre || !telefono || !email) {
            mostrarToast('Por favor completa todos los campos de contacto', 'error');
            return false;
        }
        
        // Validar email
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            mostrarToast('Por favor ingresa un email válido', 'error');
            return false;
        }
        
        return true;
    }
    
    return true;
}

// ========================================
// CONTADOR DE PERSONAS
// ========================================
function cambiarPersonas(delta) {
    const input = document.getElementById('numero_personas');
    let valor = parseInt(input.value) || 2;
    valor += delta;
    
    if (valor < 1) valor = 1;
    if (valor > 20) valor = 20;
    
    input.value = valor;
    verificarDisponibilidad();
}

// ========================================
// DISPONIBILIDAD DE MESAS
// ========================================
async function verificarDisponibilidad() {
    const fecha = document.getElementById('fecha').value;
    const hora = document.getElementById('hora').value;
    
    if (!fecha || !hora) return;
    
    // Si estamos en el paso 2, recargar mesas
    if (pasoActual === 2) {
        cargarMesasDisponibles();
    }
}

async function cargarMesasDisponibles() {
    const container = document.getElementById('mesas-disponibles');
    container.innerHTML = '<div class="mesas-loading"><div class="spinner"></div><p>Cargando disponibilidad...</p></div>';
    
    try {
        const fecha = document.getElementById('fecha').value;
        const hora = document.getElementById('hora').value;
        const personas = document.getElementById('numero_personas').value;
        
        // Cargar todas las mesas
        const response = await fetch('/api/mesas');
        const mesas = await response.json();
        
        // Filtrar por capacidad
        mesasDisponibles = mesas.filter(m => m.disponible && m.capacidad >= parseInt(personas));
        
        if (mesasDisponibles.length === 0) {
            container.innerHTML = `
                <div class="no-mesas">
                    <div class="no-mesas-icon">😔</div>
                    <h3>No hay mesas disponibles</h3>
                    <p>Intenta con otra fecha, hora o reduce el número de personas</p>
                </div>
            `;
            return;
        }
        
        // Renderizar mesas
        let html = '';
        mesasDisponibles.forEach(mesa => {
            const seleccionada = mesaSeleccionada && mesaSeleccionada.id === mesa.id;
            html += `
                <div class="mesa-card ${seleccionada ? 'seleccionada' : ''}" 
                     data-id="${mesa.id}" 
                     data-zona="${mesa.ubicacion || mesa.tipo}"
                     onclick="seleccionarMesa(${mesa.id}, '${mesa.numero}', '${mesa.ubicacion || mesa.tipo}')">
                    <div class="mesa-numero">Mesa ${mesa.numero}</div>
                    <div class="mesa-info">
                        <span class="mesa-capacidad">👥 ${mesa.capacidad} personas</span>
                        <span class="mesa-tipo ${mesa.tipo}">${mesa.tipo}</span>
                    </div>
                    <div class="mesa-ubicacion">📍 ${mesa.ubicacion || mesa.tipo}</div>
                    ${seleccionada ? '<div class="mesa-check">✓</div>' : ''}
                </div>
            `;
        });
        
        container.innerHTML = html;
        
    } catch (error) {
        console.error('Error:', error);
        container.innerHTML = `
            <div class="error-mesas">
                <p>Error al cargar las mesas. Por favor intenta nuevamente.</p>
                <button class="btn btn-primary" onclick="cargarMesasDisponibles()">Reintentar</button>
            </div>
        `;
    }
}

function seleccionarMesa(id, numero, ubicacion) {
    mesaSeleccionada = { id, numero, ubicacion };
    document.getElementById('mesa_seleccionada').value = numero;
    document.getElementById('zona_mesa').value = ubicacion;
    
    // Actualizar UI
    document.querySelectorAll('.mesa-card').forEach(card => {
        card.classList.remove('seleccionada');
        const check = card.querySelector('.mesa-check');
        if (check) check.remove();
    });
    
    const cardSeleccionada = document.querySelector(`.mesa-card[data-id="${id}"]`);
    cardSeleccionada.classList.add('seleccionada');
    cardSeleccionada.insertAdjacentHTML('beforeend', '<div class="mesa-check">✓</div>');
    
    mostrarToast(`Mesa ${numero} seleccionada`, 'success');
}

function filtrarPorZona(zona) {
    // Actualizar botones
    document.querySelectorAll('.zona-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`[data-zona="${zona}"]`).classList.add('active');
    
    // Filtrar mesas
    document.querySelectorAll('.mesa-card').forEach(card => {
        const mesaZona = card.dataset.zona;
        if (zona === 'todas' || mesaZona === zona) {
            card.style.display = '';
        } else {
            card.style.display = 'none';
        }
    });
}

// ========================================
// RESUMEN Y CONFIRMACIÓN
// ========================================
function actualizarResumen() {
    const fecha = document.getElementById('fecha').value;
    const hora = document.getElementById('hora').value;
    const personas = document.getElementById('numero_personas').value;
    const nombre = document.getElementById('nombre_reserva').value;
    const telefono = document.getElementById('telefono_reserva').value;
    
    // Formatear fecha
    const fechaObj = new Date(fecha);
    const fechaFormateada = fechaObj.toLocaleDateString('es-ES', { 
        weekday: 'long', 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
    });
    
    // Actualizar resumen
    document.getElementById('resumen-servicio').textContent = tipoServicioActual.charAt(0).toUpperCase() + tipoServicioActual.slice(1);
    document.getElementById('resumen-fecha').textContent = fechaFormateada;
    document.getElementById('resumen-hora').textContent = hora;
    document.getElementById('resumen-personas').textContent = personas + ' personas';
    document.getElementById('resumen-ubicacion').textContent = mesaSeleccionada ? `Mesa ${mesaSeleccionada.numero} - ${mesaSeleccionada.ubicacion}` : 'Por asignar';
    document.getElementById('resumen-nombre').textContent = nombre;
    document.getElementById('resumen-telefono').textContent = telefono;
    
    // Calcular total
    let total = calcularTotal();
    document.getElementById('resumen-total').textContent = formatearPrecio(total);
}

function calcularTotal() {
    let total = 0;
    
    switch (tipoServicioActual) {
        case 'mesa':
            total = precios.mesa * parseInt(document.getElementById('numero_personas').value);
            break;
        case 'piscina':
            const duracionPiscina = parseInt(document.getElementById('duracion_piscina').value);
            total = precios.piscina[duracionPiscina];
            break;
        case 'billar':
            const duracionBillar = parseInt(document.getElementById('duracion_billar').value);
            total = precios.billar[duracionBillar];
            break;
        case 'evento':
            total = precios.evento;
            break;
    }
    
    return total;
}

function formatearPrecio(precio) {
    return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0
    }).format(precio);
}

// ========================================
// ENVÍO DE RESERVA
// ========================================
async function enviarReserva(e) {
    e.preventDefault();
    
    if (!document.getElementById('acepto_terminos').checked) {
        mostrarToast('Debes aceptar los términos y condiciones', 'error');
        return;
    }
    
    const btnConfirmar = document.getElementById('btn-confirmar');
    btnConfirmar.disabled = true;
    btnConfirmar.innerHTML = '<span class="spinner-small"></span> Procesando...';
    
    try {
        // Preparar datos base
        const formData = {
            fecha: document.getElementById('fecha').value,
            hora: document.getElementById('hora').value,
            numero_personas: parseInt(document.getElementById('numero_personas').value),
            zona_mesa: document.getElementById('zona_mesa').value,
            nombre_reserva: document.getElementById('nombre_reserva').value,
            telefono_reserva: document.getElementById('telefono_reserva').value,
            email_reserva: document.getElementById('email_reserva').value,
            total_reserva: calcularTotal(),
            estado: 'pendiente'
        };
        
        // Agregar notas
        const notas = document.getElementById('notas').value;
        
        // Preparar notas especiales según el tipo de servicio
        let notasEspeciales = {
            tipo_servicio: tipoServicioActual,
            detalles: {}
        };
        
        if (tipoServicioActual === 'piscina') {
            notasEspeciales.detalles = {
                duracion_horas: document.getElementById('duracion_piscina').value,
                area_ninos: document.getElementById('area_ninos').checked ? 'si' : 'no'
            };
        } else if (tipoServicioActual === 'billar') {
            notasEspeciales.detalles = {
                duracion_horas: document.getElementById('duracion_billar').value
            };
        } else if (tipoServicioActual === 'evento') {
            notasEspeciales.detalles = {
                tipo_evento: document.getElementById('tipo_evento').value,
                notas: document.getElementById('detalles_evento').value
            };
        }
        
        // Agregar notas del usuario
        if (notas) {
            notasEspeciales.notas_usuario = notas;
        }
        
        formData.notas_especiales = JSON.stringify(notasEspeciales);
        
        // Agregar mesa si fue seleccionada
        if (mesaSeleccionada) {
            formData.mesa_asignada = mesaSeleccionada.numero;
        }
        
        // Enviar reserva
        const response = await fetch('/api/reservas/crear', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (data.success || data.reserva) {
            const codigoReserva = data.reserva.codigo_reserva || 'R-' + data.reserva.id;
            mostrarModalExito(codigoReserva);
        } else {
            throw new Error(data.error || 'Error al crear la reserva');
        }
        
    } catch (error) {
        console.error('Error:', error);
        mostrarToast('Error al crear la reserva: ' + error.message, 'error');
        btnConfirmar.disabled = false;
        btnConfirmar.innerHTML = '<span class="btn-icon">✅</span> Confirmar Reserva';
    }
}

function mostrarModalExito(codigoReserva) {
    const modal = document.createElement('div');
    modal.className = 'modal-overlay';
    modal.innerHTML = `
        <div class="modal-exito">
            <div class="exito-icon">🎉</div>
            <h2>¡Reserva Confirmada!</h2>
            <p>Tu código de reserva es:</p>
            <div class="codigo-reserva">${codigoReserva}</div>
            <p class="exito-mensaje">
                Hemos enviado los detalles a tu correo electrónico.<br>
                ¡Nos vemos pronto en BoodFood!
            </p>
            <div class="exito-acciones">
                <button class="btn btn-primary" onclick="window.location.reload()">
                    Hacer Otra Reserva
                </button>
                <button class="btn btn-outline" onclick="window.location.href='/'">
                    Ir al Inicio
                </button>
            </div>
        </div>
    `;
    document.body.appendChild(modal);
}

// ========================================
// MIS RESERVAS
// ========================================
async function cargarMisReservas() {
    const container = document.getElementById('mis-reservas-container');
    if (!container) return;
    
    container.innerHTML = '<div class="reservas-loading"><div class="spinner"></div><p>Cargando...</p></div>';
    
    try {
        const response = await fetch('/api/mis-reservas');
        const reservas = await response.json();
        
        if (reservas.length === 0) {
            container.innerHTML = `
                <div class="no-reservas">
                    <p>No tienes reservas activas</p>
                </div>
            `;
            return;
        }
        
        let html = '<div class="reservas-list">';
        reservas.forEach(reserva => {
            const estadoClass = `estado-${reserva.estado}`;
            const estadoIcono = reserva.estado === 'confirmada' ? '✅' : 
                              reserva.estado === 'pendiente' ? '⏳' : 
                              reserva.estado === 'cancelada' ? '❌' : '✓';
            
            html += `
                <div class="reserva-item ${estadoClass}">
                    <div class="reserva-header">
                        <div class="reserva-codigo">${reserva.codigo_reserva || 'R-' + reserva.id}</div>
                        <div class="reserva-estado">${estadoIcono} ${reserva.estado}</div>
                    </div>
                    <div class="reserva-detalles">
                        <div class="reserva-info">
                            <span class="info-icon">📅</span>
                            ${new Date(reserva.fecha).toLocaleDateString('es-ES')} - ${reserva.hora}
                        </div>
                        <div class="reserva-info">
                            <span class="info-icon">👥</span>
                            ${reserva.numero_personas} personas
                        </div>
                        <div class="reserva-info">
                            <span class="info-icon">🪑</span>
                            ${reserva.mesa_asignada || 'Mesa por asignar'}
                        </div>
                    </div>
                    <div class="reserva-acciones">
                        ${reserva.estado !== 'cancelada' && reserva.estado !== 'completada' ? `
                            <button class="btn-small btn-outline" onclick="cancelarReserva(${reserva.id})">
                                Cancelar
                            </button>
                        ` : ''}
                        <button class="btn-small btn-primary" onclick="verDetalleReserva(${reserva.id})">
                            Ver Detalle
                        </button>
                    </div>
                </div>
            `;
        });
        html += '</div>';
        
        container.innerHTML = html;
        
    } catch (error) {
        console.error('Error:', error);
        container.innerHTML = '<div class="error-reservas"><p>Error al cargar tus reservas</p></div>';
    }
}

async function cancelarReserva(id) {
    if (!confirm('¿Estás seguro de que deseas cancelar esta reserva?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/reservas/${id}/estado`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ estado: 'cancelada' })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            mostrarToast('Reserva cancelada correctamente', 'success');
            cargarMisReservas();
        } else {
            throw new Error(data.error || 'Error al cancelar');
        }
    } catch (error) {
        mostrarToast('Error: ' + error.message, 'error');
    }
}

async function verDetalleReserva(id) {
    try {
        const response = await fetch(`/api/reservas/${id}`);
        const reserva = await response.json();
        
        let servicioInfo = '';
        try {
            if (reserva.notas_especiales) {
                const notas = typeof reserva.notas_especiales === 'string' 
                    ? JSON.parse(reserva.notas_especiales) 
                    : reserva.notas_especiales;
                
                if (notas.tipo_servicio) {
                    servicioInfo = `<div class="detalle-servicio">Tipo: ${notas.tipo_servicio}</div>`;
                }
            }
        } catch (e) {}
        
        const modal = document.createElement('div');
        modal.className = 'modal-overlay';
        modal.id = 'modal-detalle';
        modal.innerHTML = `
            <div class="modal-detalle-reserva">
                <span class="close-modal" onclick="cerrarModal('modal-detalle')">&times;</span>
                <h3>Detalle de Reserva</h3>
                <div class="detalle-codigo">${reserva.codigo_reserva || 'R-' + reserva.id}</div>
                ${servicioInfo}
                <div class="detalle-grid">
                    <div><strong>Fecha:</strong> ${new Date(reserva.fecha).toLocaleDateString('es-ES')}</div>
                    <div><strong>Hora:</strong> ${reserva.hora}</div>
                    <div><strong>Personas:</strong> ${reserva.numero_personas}</div>
                    <div><strong>Mesa:</strong> ${reserva.mesa_asignada || 'Por asignar'}</div>
                    <div><strong>Estado:</strong> ${reserva.estado}</div>
                    <div><strong>Total:</strong> ${formatearPrecio(reserva.total_reserva || 0)}</div>
                </div>
                <button class="btn btn-primary" onclick="cerrarModal('modal-detalle')">Cerrar</button>
            </div>
        `;
        document.body.appendChild(modal);
    } catch (error) {
        mostrarToast('Error al cargar el detalle', 'error');
    }
}

function cerrarModal(id) {
    const modal = document.getElementById(id);
    if (modal) modal.remove();
}

// ========================================
// TÉRMINOS Y CONDICIONES
// ========================================
function mostrarTerminos() {
    const modal = document.createElement('div');
    modal.className = 'modal-overlay';
    modal.id = 'modal-terminos';
    modal.innerHTML = `
        <div class="modal-terminos">
            <span class="close-modal" onclick="cerrarModal('modal-terminos')">&times;</span>
            <h3>Términos y Condiciones</h3>
            <div class="terminos-contenido">
                <h4>1. Reservas</h4>
                <p>Las reservas deben hacerse con al menos 2 horas de anticipación.</p>
                
                <h4>2. Tolerancia</h4>
                <p>La mesa se mantendrá reservada por 15 minutos después de la hora indicada.</p>
                
                <h4>3. Cancelaciones</h4>
                <p>Puedes cancelar tu reserva sin costo hasta 1 hora antes de la hora reservada.</p>
                
                <h4>4. Pagos</h4>
                <p>Algunos servicios requieren un depósito del 50% al momento de la reserva.</p>
                
                <h4>5. Política de No Show</h4>
                <p>Si no asistes a tu reserva sin previo aviso, podría afectar futuras reservas.</p>
            </div>
            <button class="btn btn-primary" onclick="cerrarModal('modal-terminos')">Entendido</button>
        </div>
    `;
    document.body.appendChild(modal);
}

// ========================================
// UTILIDADES
// ========================================
function mostrarToast(mensaje, tipo = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${tipo}`;
    toast.textContent = mensaje;
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.classList.add('show');
    }, 100);
    
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

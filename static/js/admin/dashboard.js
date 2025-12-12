// static/js/admin/dashboard.js
// Dashboard principal con estadísticas y gráficas

var ventasChart = null;
var estadosPedidosChart = null;
var alertasAcumuladas = [];

// Módulo Dashboard
window.Dashboard = {
  init: async function() {
    console.log('🚀 Inicializando Dashboard...');
    
    try {
      await this.cargarEstadisticas();
      await this.cargarGraficas();
      await this.cargarTopProductos();
      await this.cargarAlertas();
      
      // Actualizar cada 30 segundos
      if (window.dashboardInterval) {
        clearInterval(window.dashboardInterval);
      }
      
      window.dashboardInterval = setInterval(() => {
        if (window.currentView === 'dashboard') {
          this.cargarEstadisticas();
        }
      }, 30000);
      
      console.log('✅ Dashboard inicializado correctamente');
    } catch (error) {
      console.error('❌ Error al inicializar dashboard:', error);
    }
  },
  
  cargarEstadisticas: async function() {
    try {
      const stats = await window.API.get('/api/dashboard/stats');
      
      // Actualizar valores
      document.getElementById('ventas-hoy').textContent = 
        new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', minimumFractionDigits: 0 }).format(stats.ventas_hoy);
      
      document.getElementById('pedidos-hoy').textContent = stats.pedidos_hoy;
      document.getElementById('pedidos-pendientes-text').textContent = 
        `${stats.pedidos_pendientes} pendientes`;
      
      document.getElementById('reservas-hoy').textContent = stats.reservas_hoy;
      document.getElementById('reservas-mes-text').textContent = 
        `${stats.pedidos_mes} este mes`;
      
      document.getElementById('mesas-ocupadas').textContent = 
        `${stats.mesas_ocupadas}/${stats.total_mesas}`;
      
      const porcentajeMesas = stats.total_mesas > 0 
        ? (stats.mesas_ocupadas / stats.total_mesas * 100).toFixed(0) 
        : 0;
      document.getElementById('mesas-progress').style.width = `${porcentajeMesas}%`;
      
      document.getElementById('inventario-bajo').textContent = stats.inventario_bajo;
      document.getElementById('total-usuarios').textContent = stats.total_usuarios;
      
      // Actualizar badges
      document.getElementById('badge-pedidos-pendientes').textContent = stats.pedidos_pendientes;
      document.getElementById('badge-inventario').textContent = stats.inventario_bajo;
      
      // Calcular cambio de ventas (simulado por ahora)
      const ventasChange = document.getElementById('ventas-change');
      if (ventasChange) {
        ventasChange.textContent = '+12%'; // TODO: calcular real
      }
      
      return stats;
    } catch (error) {
      console.error('Error al cargar estadísticas:', error);
      return null;
    }
  },
  
  cargarGraficas: async function() {
    try {
      const stats = await window.API.get('/api/dashboard/stats');
      
      // Gráfica de ventas (últimos 7 días)
      this.crearGraficaVentas(stats.ventas_por_dia);
      
      // Gráfica de estados de pedidos
      this.crearGraficaEstadosPedidos(stats.estados_pedidos);
      
    } catch (error) {
      console.error('Error al cargar gráficas:', error);
    }
  },
  
  crearGraficaVentas: function(ventasPorDia) {
    const ctx = document.getElementById('ventasChart');
    if (!ctx) return;
    
    // Ordenar fechas
    const fechas = Object.keys(ventasPorDia || {}).sort();
    const valores = fechas.map(f => ventasPorDia[f] || 0);
    
    // Si no hay datos, mostrar mensaje
    if (fechas.length === 0 || valores.every(v => v === 0)) {
      const parent = ctx.parentElement;
      parent.innerHTML = '<div class="loading">No hay datos de ventas</div>';
      return;
    }
    
    // Formatear fechas
    const etiquetas = fechas.map(f => {
      const fecha = new Date(f);
      return fecha.toLocaleDateString('es-ES', { weekday: 'short', day: 'numeric' });
    });
    
    // Calcular total
    const total = valores.reduce((a, b) => a + b, 0);
    const totalElement = document.getElementById('ventas-7d-total');
    if (totalElement) {
      totalElement.textContent = 'Total: ' + 
        new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP', minimumFractionDigits: 0 }).format(total);
    }
    
    // Destruir gráfica anterior si existe
    if (ventasChart) {
      ventasChart.destroy();
    }
    
    ventasChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: etiquetas,
        datasets: [{
          label: 'Ventas',
          data: valores,
          backgroundColor: 'rgba(76, 175, 80, 0.1)',
          borderColor: 'rgba(76, 175, 80, 1)',
          borderWidth: 3,
          fill: true,
          tension: 0.4,
          pointBackgroundColor: 'rgba(76, 175, 80, 1)',
          pointBorderColor: '#fff',
          pointBorderWidth: 2,
          pointRadius: 5,
          pointHoverRadius: 7
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            padding: 12,
            titleFont: {
              size: 14
            },
            bodyFont: {
              size: 13
            },
            callbacks: {
              label: function(context) {
                return 'Ventas: ' + new Intl.NumberFormat('es-CO', { 
                  style: 'currency', 
                  currency: 'COP', 
                  minimumFractionDigits: 0 
                }).format(context.parsed.y);
              }
            }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              callback: function(value) {
                return '$' + (value / 1000).toFixed(0) + 'k';
              }
            },
            grid: {
              color: 'rgba(0, 0, 0, 0.05)'
            }
          },
          x: {
            grid: {
              display: false
            }
          }
        }
      }
    });
  },
  
  crearGraficaEstadosPedidos: function(estadosPedidos) {
    const ctx = document.getElementById('estadosPedidosChart');
    if (!ctx) return;
    
    const estados = {
      'pendiente': { label: 'Pendientes', color: '#ff9800' },
      'preparando': { label: 'Preparando', color: '#2196f3' },
      'enviado': { label: 'Enviados', color: '#9c27b0' },
      'entregado': { label: 'Entregados', color: '#4caf50' },
      'cancelado': { label: 'Cancelados', color: '#f44336' }
    };
    
    const labels = [];
    const data = [];
    const colors = [];
    
    Object.keys(estados).forEach(estado => {
      if (estadosPedidos[estado]) {
        labels.push(estados[estado].label);
        data.push(estadosPedidos[estado]);
        colors.push(estados[estado].color);
      }
    });
    
    // Si no hay datos, mostrar mensaje
    if (data.length === 0) {
      ctx.parentElement.innerHTML = '<div class="loading">No hay pedidos en los últimos 30 días</div>';
      return;
    }
    
    // Destruir gráfica anterior si existe
    if (estadosPedidosChart) {
      estadosPedidosChart.destroy();
    }
    
    estadosPedidosChart = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: labels,
        datasets: [{
          data: data,
          backgroundColor: colors,
          borderWidth: 0,
          hoverOffset: 10
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'right',
            labels: {
              padding: 15,
              font: {
                size: 13
              },
              generateLabels: function(chart) {
                const data = chart.data;
                return data.labels.map((label, i) => ({
                  text: `${label}: ${data.datasets[0].data[i]}`,
                  fillStyle: data.datasets[0].backgroundColor[i],
                  hidden: false,
                  index: i
                }));
              }
            }
          },
          tooltip: {
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            padding: 12,
            callbacks: {
              label: function(context) {
                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                const porcentaje = ((context.parsed / total) * 100).toFixed(1);
                return `${context.label}: ${context.parsed} (${porcentaje}%)`;
              }
            }
          }
        }
      }
    });
  },
  
  cargarTopProductos: async function() {
    try {
      const stats = await window.API.get('/api/dashboard/stats');
      const container = document.getElementById('top-productos-list');
      
      if (!stats.top_productos || stats.top_productos.length === 0) {
        container.innerHTML = '<div class="loading">No hay datos de productos</div>';
        return;
      }
      
      const medals = ['🥇', '🥈', '🥉', '4️⃣', '5️⃣'];
      
      const html = stats.top_productos.map((producto, index) => `
        <div class="producto-item">
          <span class="producto-rank">${medals[index] || (index + 1)}</span>
          <div class="producto-info">
            <div class="producto-nombre">${producto.nombre}</div>
          </div>
          <span class="producto-cantidad">${producto.cantidad}</span>
        </div>
      `).join('');
      
      container.innerHTML = html;
    } catch (error) {
      console.error('Error al cargar top productos:', error);
    }
  },
  
  cargarAlertas: async function() {
    try {
      const stats = await window.API.get('/api/dashboard/stats');
      
      // Agregar alerta de inventario bajo si existe
      if (stats.inventario_bajo > 0) {
        this.agregarAlerta({
          tipo: 'warning',
          icono: '⚠️',
          texto: `${stats.inventario_bajo} productos con stock bajo`,
          tiempo: 'Ahora',
          accion: () => window.setActiveView('inventario')
        });
      }
      
      // Agregar alerta de pedidos pendientes si existen
      if (stats.pedidos_pendientes > 0) {
        this.agregarAlerta({
          tipo: 'info',
          icono: '📦',
          texto: `${stats.pedidos_pendientes} pedidos pendientes de atención`,
          tiempo: 'Ahora',
          accion: () => window.setActiveView('pedidos')
        });
      }
      
      this.renderizarAlertas();
    } catch (error) {
      console.error('Error al cargar alertas:', error);
    }
  },
  
  agregarAlerta: function(alerta) {
    // Evitar duplicados
    const existe = alertasAcumuladas.some(a => 
      a.tipo === alerta.tipo && a.texto === alerta.texto
    );
    
    if (!existe) {
      alertasAcumuladas.unshift(alerta);
      // Mantener solo las últimas 10 alertas
      alertasAcumuladas = alertasAcumuladas.slice(0, 10);
    }
  },
  
  renderizarAlertas: function() {
    const container = document.getElementById('alertas-list');
    if (!container) return;
    
    if (alertasAcumuladas.length === 0) {
      container.innerHTML = `
        <div class="alert-item alert-success">
          <span class="alert-icon">✅</span>
          <span class="alert-text">Sistema funcionando correctamente</span>
          <span class="alert-time">Ahora</span>
        </div>
      `;
      return;
    }
    
    const html = alertasAcumuladas.map(alerta => `
      <div class="alert-item alert-${alerta.tipo}" ${alerta.accion ? `style="cursor: pointer;" onclick="(${alerta.accion.toString()})()"` : ''}>
        <span class="alert-icon">${alerta.icono}</span>
        <span class="alert-text">${alerta.texto}</span>
        <span class="alert-time">${alerta.tiempo}</span>
      </div>
    `).join('');
    
    container.innerHTML = html;
  },
  
  limpiarAlertas: function() {
    alertasAcumuladas = [];
    this.renderizarAlertas();
  }
};

// Marcar módulo como cargado
window.dashboardModuleLoaded = true;

console.log('✅ Módulo Dashboard cargado');


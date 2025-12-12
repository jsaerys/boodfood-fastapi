# Actualización de Dominio - Base de Datos

## Cambio Realizado
Se actualizó el dominio de la base de datos MySQL remota de `isladigital.xyz` a `mysql.enlinea.sbs`.

## Archivos Modificados

### 1. `config.py` (Principal)
**Cambio:**
```python
# Antes:
'mysql+pymysql://brandon:brandonc@isladigital.xyz:3311/f58_brandon'

# Ahora:
'mysql+pymysql://brandon:brandonc@mysql.enlinea.sbs:3311/f58_brandon'
```

### 2. Scripts de Base de Datos
Los siguientes scripts fueron actualizados:
- `scripts/ver_mesas_db.py`
- `scripts/activar_mesas.py`
- `scripts/agregar_mas_mesas.py`

**Cambio en todos:**
```python
# Antes:
host='isladigital.xyz'

# Ahora:
host='mysql.enlinea.sbs'
```

## Pruebas Realizadas ✅

Se ejecutó `scripts/test_conexion.py` con los siguientes resultados:

- ✅ Conexión exitosa a `mysql.enlinea.sbs:3311`
- ✅ 37 mesas encontradas
- ✅ 21 items del menú encontrados
- ✅ 7 usuarios encontrados

## Configuración Actual

**Servidor MySQL:**
- Host: `mysql.enlinea.sbs`
- Puerto: `3311`
- Base de datos: `f58_brandon`
- Usuario: `brandon`
- Password: `brandonc`

## Notas

- El puerto permanece igual: `3311`
- Las credenciales no cambiaron
- La base de datos `f58_brandon` sigue siendo la misma
- Todos los datos se mantienen intactos

## Dominio Administrativo

El panel administrativo puede accederse en:
- https://admin.enlinea.sbs/ (si está configurado el frontend)

---

**Fecha de actualización:** 27 de noviembre de 2025

import pymysql

# Conectar a la base de datos
conn = pymysql.connect(
    host='mysql.enlinea.sbs',
    port=3311,
    user='brandon',
    password='brandonc',
    database='f58_brandon'
)

cursor = conn.cursor()

print('\n🔄 Actualizando todas las mesas para que estén disponibles...\n')

# Actualizar todas las mesas a disponible=1
cursor.execute('UPDATE mesas SET disponible = 1')
conn.commit()

print(f'✅ {cursor.rowcount} mesas actualizadas')

# Verificar
cursor.execute('SELECT COUNT(*) FROM mesas WHERE disponible = 1')
disponibles = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM mesas')
total = cursor.fetchone()[0]

print(f'\n📊 Resultado:')
print(f'   Total de mesas: {total}')
print(f'   Mesas disponibles: {disponibles}')

# Mostrar algunas mesas
print(f'\n📋 Primeras 10 mesas disponibles:')
print('=' * 70)
cursor.execute('SELECT id, numero, capacidad, ubicacion, tipo FROM mesas WHERE disponible = 1 LIMIT 10')
for row in cursor.fetchall():
    print(f'  Mesa #{row[1]:2d} - {row[2]} personas - {row[3]:15s} - {row[4]}')

conn.close()
print('\n✅ ¡Listo! Todas las mesas están ahora disponibles para reservas.\n')

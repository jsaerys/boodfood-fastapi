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

# Ver estructura
print('\n📋 Estructura de la tabla mesas:\n')
print('=' * 60)
cursor.execute('DESCRIBE mesas')
for row in cursor.fetchall():
    print(f'  - {row[0]:20s} ({row[1]})')

# Contar mesas
cursor.execute('SELECT COUNT(*) FROM mesas')
total = cursor.fetchone()[0]
print('\n' + '=' * 60)
print(f'📊 Total de mesas en la base de datos: {total}')

# Ver primeras mesas si existen
if total > 0:
    print('\n🔍 Primeras 5 mesas:')
    print('=' * 60)
    cursor.execute('SELECT * FROM mesas LIMIT 5')
    for row in cursor.fetchall():
        print(f'  {row}')

conn.close()
print('\n✅ Conexión cerrada\n')

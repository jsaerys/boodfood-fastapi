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

# Verificar cuántas mesas tenemos
cursor.execute('SELECT COUNT(*) FROM mesas')
total_actual = cursor.fetchone()[0]

print(f'\n📊 Mesas actuales: {total_actual}')

# Si hay menos de 35 mesas, agregar más
if total_actual < 35:
    print(f'\n🔧 Agregando más mesas variadas...\n')
    
    # Obtener el número máximo actual
    cursor.execute('SELECT MAX(numero) FROM mesas')
    max_numero = cursor.fetchone()[0] or 0
    
    # Agregar mesas variadas
    nuevas_mesas = [
        # Mesas interiores pequeñas
        (max_numero + 1, 2, 'Interior - Ventana', 1, 'interior'),
        (max_numero + 2, 2, 'Interior - Ventana', 1, 'interior'),
        (max_numero + 3, 4, 'Interior - Centro', 1, 'interior'),
        (max_numero + 4, 4, 'Interior - Centro', 1, 'interior'),
        
        # Mesas terraza medianas
        (max_numero + 5, 6, 'Terraza - Vista jardín', 1, 'terraza'),
        (max_numero + 6, 6, 'Terraza - Vista jardín', 1, 'terraza'),
        (max_numero + 7, 8, 'Terraza - Grande', 1, 'terraza'),
        
        # Mesas VIP
        (max_numero + 8, 10, 'VIP - Privado', 1, 'vip'),
        (max_numero + 9, 12, 'VIP - Salón privado', 1, 'vip'),
    ]
    
    cursor.executemany(
        'INSERT INTO mesas (numero, capacidad, ubicacion, disponible, tipo) VALUES (%s, %s, %s, %s, %s)',
        nuevas_mesas
    )
    conn.commit()
    
    print(f'✅ {cursor.rowcount} nuevas mesas agregadas')

# Mostrar resumen final
cursor.execute('SELECT COUNT(*) FROM mesas')
total_final = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM mesas WHERE disponible = 1')
disponibles = cursor.fetchone()[0]

print(f'\n📊 Resumen Final:')
print(f'   Total de mesas: {total_final}')
print(f'   Mesas disponibles: {disponibles}')

# Agrupar por tipo
print(f'\n📋 Mesas por tipo:')
cursor.execute('SELECT tipo, COUNT(*) FROM mesas GROUP BY tipo')
for row in cursor.fetchall():
    print(f'   {row[0]:10s}: {row[1]} mesas')

# Mostrar mesas por capacidad
print(f'\n👥 Mesas por capacidad:')
cursor.execute('SELECT capacidad, COUNT(*) FROM mesas GROUP BY capacidad ORDER BY capacidad')
for row in cursor.fetchall():
    print(f'   {row[0]} personas: {row[1]} mesas')

conn.close()
print('\n✅ ¡Perfecto! Panel de reservas listo con variedad de mesas.\n')

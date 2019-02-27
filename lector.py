import glob
import json
import mysql.connector

conexion = mysql.connector.connect(user='manuel', password='12345',database='casas')
cursor = conexion.cursor()
files = glob.glob('*.json')
tipo = {'venta':1, 'renta':2}
origen = {'informador':1}

for file in files:
    with open(file) as f:
        casas = json.load(f)
        for casa in casas:
            #print (casa)
            select = 'SELECT * from municipio WHERE nombre = %s'
            cursor.execute(select, (casa['ubicacion'], ) )
            if len(cursor.fetchall()) == 0:

                insert = 'INSERT INTO municipio(nombre) VALUES(%s)'
                cursor.execute(insert, (casa['ubicacion'],))
                id_muni = cursor.lastrowid

                insert = 'INSERT INTO colonia(nombre, id_municipio) VALUES(%s, %s)'
                cursor.execute(insert, (casa['colonia'], id_muni))
                id_colonia = cursor.lastrowid

                select = 'SELECT * from fecha WHERE fecha = %s'
                cursor.execute(select, (file[0:-5], ))
                id_fecha = 0

                rows = cursor.fetchall()
                if len(rows) == 0:
                    insert = 'INSERT INTO fecha(fecha) VALUES(%s)'
                    cursor.execute(insert, (file[:-5], ))
                    id_fecha = cursor.lastrowid
                else:
                    id_fecha = rows[0][0]

                insert = 'INSERT INTO bienraiz(titulo, precio, m2, rooms, baths, cars, descripcion, id_tipo, id_origen, id_colonia, id_fecha) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                cursor.execute(insert, (casa['titulo'], casa['precio'], casa['m2'], casa['recamaras'], casa['wc'], casa['cars'], casa['descripcion'], tipo[casa['tipo']], 1, id_colonia, id_fecha))
                id_colonia = cursor.lastrowid
                conexion.commit()
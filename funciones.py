import mysql.connector
from datetime import *
import csv
import os

def conectar_mysql(usuario, password, host='localhost'):
    """Cuando es llamado, establece la conexión con el server autenticando usuario y contraseña, para luego poder conectar con la DB.
    Parámetros: usuario class <<str>>, password class <<str>>.
    Retorna el objeto "db" como variable para usar en la conexión si la conexión es exitosa.
    """
    try:
        db = mysql.connector.connect(
            host = host,
            user = usuario,
            password = password
        )
        print("Conexión exitosa.")
        return db
    except mysql.connector.Error as mal:
        print(f"Error: {mal}")
        raise ConnectionError("Conexión denegada")

def validacao(valor,tipovalue,correo=False,fecha=False,direccao=False,hora=False,telefono=False,ID=False,booleano=False,tipo_sangre=False):
    """Función que toma como parámetros el valor a validar y su tipo de valor. Retorna el valor en su tipo si es correcto;
    si no, permanece en un loop hasta que el valor satisfaga.
    Parametros: valor. tipo: str
                tipovalue. tipo: int/str
    Tiene aparte otros parámetros con valores Boolean predeterminados, que se pueden usar y definir al llamarse según se requiera.
    """
    while True:
        if tipovalue == int:
            if ID == True:
                if valor.isdigit() and len(valor) == 3:
                    return tipovalue(valor)
                else:
                    valor = input("Valor no válido. Ingrese el valor nuevamente: ")
            elif booleano == True:
                if valor.isdigit():
                    if valor == str(1) or valor == str(0):
                        return tipovalue(valor)
                    else:
                        valor = input("Valor no válido. Ingrese el valor nuevamente: ")
                else:
                    valor = input("Valor no válido. Ingrese el valor nuevamente: ")
            else:
                if valor.isdigit():
                    return tipovalue(valor)
                else:
                    valor = input("Valor no válido. Ingrese el valor nuevamente: ")
        elif tipovalue == str:
            if correo == True:
                if '@' in valor and '.' in valor.split('@')[1] and len(valor.split('@')[1].split('.')) > 1:
                    return valor
                else:
                    valor = input("Correo no válido. Ingrese el valor nuevamente: ")
            elif fecha == True:
                try:
                    fecha_str = valor[:10]
                    datetime.strptime(fecha_str, '%Y-%m-%d')
                    return fecha_str
                except ValueError:
                    valor = input("Fecha no válida. Ingrese una hora en el formato AAAA-MM-DD: ")
            elif direccao == True:
                partes_dir = valor.split(', ')
                if len(partes_dir) == 2 and all(parte.isascii() for parte in partes_dir):
                    return valor
                else:
                    valor = input("Dirección no valida, debe tener 2 elementos separados por ', '. Ingrese nuevamente: ")
            elif hora == True:
                try:
                    # Intenta analizar la cadena como una hora en formato de 24 horas
                    datetime.strptime(valor, '%H:%M')
                    return valor
                except ValueError:
                    valor = input("Hora no válida. Ingrese una hora en formato HH:MM (24 horas): ")
            elif telefono == True:
                if valor.isdigit() and len(valor) == 10:
                    valor = "+" + valor
                    return valor
                else:
                    valor = input("Valor de telefono no válido, ingrese nuevamente sin '+': ")
            elif tipo_sangre == True:
                if valor[-1] == "+" and valor.isascii():
                    return valor
                else:
                    valor = input("Valor no válido. Ingrese el valor nuevamente: ")
            else:
                partes = valor.split(' ')
                if all(parte.isalpha() for parte in partes):
                    return valor
                else:
                    valor = input("Valor no válido. Ingrese el valor nuevamente: ")

def menu_admin(cursor,query,db):
    """Menú específico para administradores, los cuales tienen Permiso_Medico y Permiso_Paciente como True en la tabla Usuarios.
    Este menú tiene acceso a todas las funciones del programa.
    Parámetros: cursor. tipo: Objeto mysql
                query. tipo: Int
                db. tipo: Objeto mysql
    """
    opciones = "Opciones:\n1. Consultar\n2. Añadir\n3. Editar\n4. Eliminar\n5. Salir"
    print(opciones)
    menu = input("Elija una opción para continuar: ")
    menu = validacao(menu,int)
    while menu != 5:
        if menu == 1:
            tabla = input("1. Medicos\n2. Pacientes\n3. Citas\n¿Qué desea consultar? ")
            tabla = validacao(tabla,int)
            while True:
                if tabla == 1 or tabla == 2 or tabla == 3:
                    consultar(cursor,query,tabla,acc_medico=True)
                    if tabla == 2:
                        query += 1
                    break
                else:
                    tabla = input("Valor no válido, ingrese el valor nuevamente: ")
                    tabla = validacao(tabla,int)
        elif menu == 2:
            print("1. Usuarios\n2. Medicos\n3. Pacientes\n4. Citas")
            donde_add = input("A qué tabla desea añadir valores?: ")
            donde_add = validacao(donde_add,int)
            while True:
                if donde_add == 1 or donde_add == 2 or donde_add == 3 or donde_add == 4:
                    agregar(db,cursor,donde_add)
                    break
                else:
                    donde_add = input("Valor no válido, ingrese el valor nuevamente: ")
                    donde_add = validacao(donde_add,int)
        elif menu == 3:
            print("1. Medicos\n2. Pacientes\n3. Usuarios\n4. Citas")
            donde_trocar = input("En qué tabla quiere editar algun valor? ")
            donde_trocar = validacao(donde_trocar,int)
            while True:
                if donde_trocar == 1 or donde_trocar == 2 or donde_trocar == 3 or donde_trocar == 4:
                    editar(db,cursor,donde_trocar)
                    break
                else:
                    donde_trocar = input("Valor no válido, ingrese el valor nuevamente: ")
                    donde_trocar = validacao(donde_trocar,int)
        elif menu == 4:
            print("1. Medicos\n2. Pacientes\n3. Usuarios\n4. Citas")
            donde_loschen = input("En qué tabla quiere eliminar alguna fila? ")
            donde_loschen = validacao(donde_loschen,int)
            while True:
                if donde_loschen == 1 or donde_loschen == 2 or donde_loschen == 3 or donde_loschen == 4:
                    eliminar(db,cursor,donde_loschen)
                    break
                else:
                    donde_loschen = input("Valor no válido, ingrese el valor nuevamente: ")
                    donde_loschen = validacao(donde_loschen,int)
        else:
            menu = input("Valor no válido, ingrese el valor nuevamente: ")
            menu = validacao(menu,int)
        print(opciones)
        menu = input("Elija una opción para continuar: ")
        menu = validacao(menu,int)

def menu_paciente(cursor, query, db):
    """Menú específico para Pacientes, los cuales tienen Permiso_Paciente como True en la tabla Usuarios.
    Este menú tiene acceso a todas las funciones del programa.
    Parámetros: cursor. tipo: Objeto mysql
                query. tipo: Int
                db. tipo: Objeto mysql
    """
    opciones = "Opciones:\n1. Consultar\n2. Añadir\n3. Editar\n4. Eliminar\n5. Salir"
    opciones = "Opciones:\n1. Consultar\n2. Añadir\n3. Editar\n4. Eliminar\n5. Salir"
    print(opciones)
    menu = input("Elija una opción para continuar: ")
    menu = validacao(menu,int)
    while menu != 5:
        if menu == 1:
            tabla = input("Qué desea consultar?\n1. Pacientes\n2. Citas\nIngrese una opción: ")
            tabla = validacao(tabla,int)
            while True:
                if tabla == 1:
                    consultar(cursor, query,tabla=2)
                    query += 1
                    break
                elif tabla == 2:
                    consultar(cursor, query,tabla=3)
                    break
                else:
                    tabla = input("Valor no válido, ingrese el valor nuevamente: ")
                    tabla = validacao(tabla,int)
        elif menu == 2:
            #Pacientes no tienen permiso para agregar citas
            agregar(db,cursor,donde_add=3)
        elif menu == 3:
            print("1. Pacientes\n2. Citas")
            donde_trocar = input("En qué tabla quiere editar algun valor? ")
            donde_trocar = validacao(donde_trocar,int)
            while True:
                if donde_trocar == 1:
                    editar(db,cursor,donde_trocar=2)
                    break
                elif donde_trocar == 2:
                    editar(db,cursor,donde_trocar=4)
                    break
                else:
                    donde_trocar = input("Valor no válido, ingrese el valor nuevamente: ")
                    donde_trocar = validacao(donde_trocar,int)
        elif menu == 4:
            print("1. Pacientes\n2. Citas")
            donde_loschen = input("En qué tabla quiere eliminar alguna fila? ")
            donde_loschen = validacao(donde_loschen,int)
            while True:
                if donde_loschen == 1:
                    eliminar(db,cursor,donde_loschen=2)
                    break
                elif donde_loschen == 2:
                    eliminar(db,cursor,donde_loschen=4)
                    break
                else:
                    donde_loschen = input("Valor no válido, ingrese el valor nuevamente: ")
                    donde_loschen = validacao(donde_loschen,int)
        else:
            menu = input("Valor no válido, ingrese el valor nuevamente: ")
            menu = validacao(menu,int)
        print(opciones)
        menu = input("Elija una opción para continuar: ")
        menu = validacao(menu,int)

def menu_medico(cursor,query,db):
    """Menú específico para Médicos, los cuales tienen Permiso_Medico como True en la tabla Usuarios.
    Esta clase tiene más privilegios que pacientes pero no absolutos como admin.
    Este menú tiene acceso a todas las funciones del programa.
    Parámetros: cursor. tipo: Objeto mysql
                query. tipo: Int
                db. tipo: Objeto mysql
    """
    opciones = "Opciones:\n1. Consultar\n2. Añadir\n3. Editar\n4. Eliminar\n5. Salir"
    opciones = "Opciones:\n1. Consultar\n2. Añadir\n3. Editar\n4. Eliminar\n5. Salir"
    print(opciones)
    menu = input("Elija una opción para continuar: ")
    menu = validacao(menu,int)
    while menu != 5:
        if menu == 1:
            tabla = input("Qué desea consultar?\n1. Médicos\n2. Citas\nIngrese una opción: ")
            tabla = validacao(tabla,int)
            while True:
                if tabla == 1:
                    consultar(cursor,query,tabla,acc_medico=True)
                    break
                elif tabla == 2:
                    consultar(cursor,query,tabla=3,acc_medico=True)
                    break
                else:
                    tabla = input("Valor no válido, ingrese el valor nuevamente: ")
                    tabla = validacao(tabla,int)
        elif menu == 2:
            donde_add = input("Qué desea añadir?\n1. Médico\n2. Cita\nIngrese una opción: ")
            donde_add = validacao(donde_add,int)
            while True:
                if donde_add == 1:
                    agregar(db,cursor,donde_add=2)
                    break
                elif donde_add == 2:
                    agregar(db,cursor,donde_add=4)
                    break
                else:
                    donde_add = input("Valor no válido, ingrese el valor nuevamente: ")
                    donde_add = validacao(donde_add,int)                    
        elif menu == 3:
            print("1. Medicos\n2. Citas")
            donde_trocar = input("En qué tabla quiere editar algun valor? ")
            donde_trocar = validacao(donde_trocar,int)
            while True:
                if donde_trocar == 1:
                    editar(db,cursor,donde_trocar=1)
                    break
                elif donde_trocar == 2:
                    editar(db,cursor,donde_trocar=4)
                    break
                else:
                    donde_trocar = input("Valor no válido, ingrese el valor nuevamente: ")
                    donde_trocar = validacao(donde_trocar,int)
        elif menu == 4:
            print("1. Medicos\n2. Citas")
            donde_loschen = input("En qué tabla quiere eliminar alguna fila? ")
            donde_loschen = validacao(donde_loschen,int)
            while True:
                if donde_loschen == 1:
                    eliminar(db,cursor,donde_loschen=1)
                    break
                elif donde_loschen == 2:
                    eliminar(db,cursor,donde_loschen=4)
                    break
                else:
                    donde_loschen = input("Valor no válido, ingrese el valor nuevamente: ")
                    donde_loschen = validacao(donde_loschen,int)
        else:
            menu = input("Valor no válido, ingrese el valor nuevamente: ")
            menu = validacao(menu,int)
        print(opciones)
        menu = input("Elija una opción para continuar: ")
        menu = validacao(menu,int)

#Función para verificar las citas
def disponibilidad_cita(cursor, id_medico, fecha, hora):
    """Verifica si hay una cita existente para el médico en la fecha y hora especificadas.
    Parámetros: cursor. tipo: objeto mysql
                id_medico. tipo: int
                fecha. tipo: str
                hora. tipo: str
    """
    cursor.execute("""SELECT * FROM Citas WHERE ID_Medico = %s AND Fecha = %s AND Hora = %s""", (id_medico, fecha, hora))
    return cursor.fetchone() is None

def agregar(db,cursor,donde_add):
    """Añade elementos a la base de datos. Función aplicable para cada tabla.
    El parámetro donde_add define a qué tabla se va a añadir la información
    Parámetros: db. tipo: objeto mysql
                cursor. tipo: objeto mysql
                donde_add. tipo: int
    """
    while True:
        if donde_add == 1:
            lista_elementos = ["ID", "Usuario", "Password", "Permiso_Medico", "Permiso_Paciente"]
            listinha = []
            for i in range(5):
                elementinho = input("Ingrese {}: ".format(lista_elementos[i]))
                if i == 2 or i >= 3:
                    if i == 1:
                        elementinho = validacao(elementinho,int,ID=True)
                    elif i >= 3:
                        elementinho = validacao(elementinho,int,booleano=True)
                else:
                    elementinho = validacao(elementinho,str)
                listinha.append(elementinho)
            cursor.execute("SELECT 1 FROM mysql.user WHERE user = %s AND host = 'localhost'", (listinha[1],))
            usuario_existe = cursor.fetchone()
            if not usuario_existe:
                cursor.execute("""INSERT IGNORE INTO Usuarios (ID, Usuario, Password, Permiso_Medico, Permiso_Paciente)
                       VALUES (%s,%s,%s,%s,%s)""", listinha)
                cursor.execute("""CREATE USER %s@'localhost' IDENTIFIED BY %s;""", (listinha[1], listinha[2]))
                cursor.execute("""GRANT ALL PRIVILEGES ON informatica1.* TO %s@'localhost' WITH GRANT OPTION;""", (listinha[1],))
            else:
                print("El usuario ya existe")
            break
        elif donde_add == 2:
            lista_elementos = ["ID", "Nombre", "Especialidad", "Telefono", "Email", "Disponible"]
            listinha = []
            print("Añadir médico: ")
            for i in range(6):
                if i == 5:
                    print("1. Disponible\n 0. No disponible")
                elementinho = input("Ingrese {}: ".format(lista_elementos[i]))
                if i == 0 or i == 3:
                    if i == 3:
                        elementinho = validacao(elementinho,str,telefono=True)
                    elif i == 0:
                        elementinho = validacao(elementinho,int,ID=True)
                elif i == 4:
                    elementinho = validacao(elementinho,str,correo=True)
                elif i == 5:
                    elementinho = validacao(elementinho,int,booleano=True)
                else:
                    elementinho = validacao(elementinho,str)
                listinha.append(elementinho)
            cursor.execute("""INSERT IGNORE INTO Medicos (ID, Nombre, Especialidad, Telefono, Email, Disponible)
                   VALUES (%s,%s,%s,%s,%s,%s)""", listinha)
            break
        elif donde_add == 3:
            lista_elementos = ["ID", "Nombre", "Nacimiento", "Genero", "Tipo_Sangre", "Telefono", "Direccion", "Email"]
            listinha = []
            print("Añadir paciente: ")
            for i in range(8):
                elementinho = input("Ingrese {}: ".format(lista_elementos[i]))
                if i == 0:
                    elementinho = validacao(elementinho,int,ID=True)
                elif i == 2:
                    elementinho = validacao(elementinho,str,fecha=True)
                elif i == 4:
                    elementinho = validacao(elementinho,str,tipo_sangre=True)
                elif i == 5:
                    elementinho = validacao(elementinho,str,telefono=True)
                elif i == 6:
                    elementinho = validacao(elementinho,str,direccao=True)
                elif i == 7:
                    elementinho = validacao(elementinho,str,correo=True)
                else:
                    elementinho = validacao(elementinho,str)
                listinha.append(elementinho)
            cursor.execute("""INSERT IGNORE INTO Pacientes (ID, Nombre, Nacimiento, Genero, Tipo_Sangre, Telefono, Direccion, Email)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""", listinha)
            break
        elif donde_add == 4:
            lista_elementos = ["ID", "ID_Medico", "ID_Paciente", "Fecha", "Hora"]
            listinha = []
            for i in range(5):
                elementinho = input("Ingrese {}: ".format(lista_elementos[i]))
                if i <= 2:
                    elementinho = validacao(elementinho,int,ID=True)
                elif i == 3:
                    elementinho = validacao(elementinho,str,fecha=True)
                elif i == 4:
                    elementinho = validacao(elementinho, str, hora=True)
                else:
                    elementinho = validacao(elementinho,str)
                listinha.append(elementinho)
            if not disponibilidad_cita(cursor, listinha[1], listinha[3], listinha[4]):
                print("No hay cita disponible en la fecha y hora dadas.")
                return
            else:
                cursor.execute("""INSERT IGNORE INTO Citas (ID, ID_Medico, ID_Paciente, Fecha, Hora)
                   VALUES (%s,%s,%s,%s,%s)""", listinha)
            break
        else:
            donde_add = input("Valor no válido, ingrese el valor nuevamente: ")
            donde_add = validacao(donde_add,int)
    db.commit()

def exportar_a_csv(datos, nombre_archivo):
    with open(nombre_archivo, 'w', newline='') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        # Escribir encabezados basados en las claves del primer registro
        encabezados = list(datos[next(iter(datos))].keys())
        escritor_csv.writerow(encabezados)
       
        # Escribir datos de cada individuo
        for clave, valor in datos.items():
            escritor_csv.writerow([valor[columna] for columna in encabezados])
    print(f"Archivo {nombre_archivo} generado con éxito.")

def consultar(cursor,query,tabla,acc_medico=False):
    """Consulta para tabla medicos. Por temas de seguridad, la tabla usuarios no se muestra para ninguna clase, pese a tener todos los permisos.
    Parámetros: cursor. tipo: objeto mysql
                query. tipo: int
                tabla. tipo: int
                acc_medico. tipo: Boolean (Identifica si tiene permiso medico o no)
    """
    while True:
        if tabla == 1:
            id = input("ingrese el ID del médico que desea buscar: ")
            id = validacao(id,int,ID=True)
            cursor.execute("SELECT * FROM Medicos WHERE ID = {}".format(id))
            for medico in cursor.fetchall():
                #medico es tupla de cada row
                print("ID: {}, Nombre: {}, Especialidad: {}, Telefono: {}, Email: {}, Disponible: {}".format(medico[0], medico[1], medico[2], medico[3], medico[4], medico[5]))
            break
        elif tabla == 2:
            todo_nada = input("Desea buscar 1 solo paciente o todos?\n1. 1 Paciente\n2. Todos\nElija una opción: ")
            todo_nada = validacao(todo_nada,int)
            while True:
                if todo_nada == 1 or todo_nada == 2:
                    break
                else:
                    todo_nada = input("Valor no válido. Ingrese el valor nuevamente: ")
                    todo_nada = validacao(tabla,int)
            if todo_nada == 1:
                id = input("ingrese el ID del paciente que desea buscar: ")
                id = validacao(id,int)
                cursor.execute("SELECT * FROM Pacientes WHERE ID = {}".format(id))
            elif todo_nada == 2:
                cursor.execute("SELECT * FROM Pacientes")
                resultados = cursor.fetchall()
                pacientes = {} #Pacientes es el <<dict>> que pasa a CSV
                for fila in resultados:
                    id_paciente = fila[0]
                    datos_paciente = {
                        'nombre': fila[1],
                        'nacimiento': fila[2],
                        'correo': fila[3],
                        'genero': fila[4],
                        'Tipo_de_sangre': fila[5],
                        'Telefono': fila[6],
                        'direccion': fila[7]
                    }
                    pacientes[id_paciente] = datos_paciente
                name = "Pacientes"
                if os.path.isfile("{0}_{1}.csv".format(name,query)):
                    query += 1
                name = "{0}_{1}.csv".format(name, query)
                exportar_a_csv(pacientes, name)
                print(pacientes)
            break
        elif tabla == 3:
            #CAMBIAR AQUÍ FORMATO
            if acc_medico:
                id = input("ingrese el ID del Médico de la cita que desea buscar: ")
                id = validacao(id,int,ID=True)
                cursor.execute("SELECT * FROM Citas WHERE ID_Medico = {}".format(id))
                resultados = cursor.fetchall()
                citas = {} #citas es el <<dict>> que pasa a la función
                for fila in resultados:
                    id_cita = str(fila[0])
                    datos_cita = {
                        'ID_Medico': fila[1],
                        'ID_Paciente': fila[2],
                        'Fecha': fila[3],
                        'Hora': fila[4],
                    }
                    citas[id_cita] = datos_cita
                while True:
                    print("1. Buscar coincidencias para el día actual")
                    print("2. Buscar coincidencias para la semana actual")
                    print("3. Salir")
                    opcion = input("Seleccione una opción (1-3): ")

                    if opcion == '1':
                        coincidencias_dia_actual = coincidencia_fecha_actual(citas, 'dia')
                        mostrar_coincidencias(coincidencias_dia_actual, 'día')
                    elif opcion == '2':
                        coincidencias_semana_actual = coincidencia_fecha_actual(citas, 'semana')
                        mostrar_coincidencias(coincidencias_semana_actual, 'semana')
                    elif opcion == '3':
                        print("¡Hasta luego!")
                        break
                    else:
                        print("Opción no válida. Por favor, seleccione una opción válida (1-3).")        
            else:
                id = input("ingrese el ID del paciente de la cita que desea buscar: ")
                id = validacao(id,int,ID=True)
                cursor.execute("SELECT ID, ID_Medico, Fecha, Hora FROM Citas WHERE ID_Paciente = {}".format(id))
                for cita in cursor.fetchall():
                    #Cita es tupla de cada row
                    print("ID: {}, ID_Medico: {}, Fecha: {}, Hora: {}".format(cita[0], cita[1], cita[2], cita[3]))
            break
        else:
            tabla = input("Valor no válido, ingrese el valor nuevamente: ")
            tabla = validacao(tabla,int)

#FUNCIONES PARA HACER EL QUERY DE MEDICOS SEGUN DIA Y SEMANA    
def coincidencia_fecha_actual(datos, lapso_tiempo):
    hoy = datetime.now()
    coincidencias = []
    for clave, valor in datos.items():
        fecha_cita = datetime.strptime(valor['Fecha'] + ' ' + valor['Hora'], '%Y-%m-%d %H:%M')
        if lapso_tiempo == 'dia' and fecha_cita.date() == hoy.date():
            coincidencias.append((clave, valor))
        elif lapso_tiempo == 'semana' and hoy - timedelta(days=7) <= fecha_cita <= hoy:
            coincidencias.append((clave, valor))
    return coincidencias

def mostrar_coincidencias(coincidencias, lapso_tiempo):
    if coincidencias:
        print(f"Coincidencias para el {lapso_tiempo} actual:")
        for cita in coincidencias:
            print(f"ID: {cita[0]}, Datos: {cita[1]}")
    else:
        print(f"No se encontraron coincidencias para el {lapso_tiempo} actual.")

def editar(db,cursor,donde_trocar):
    """Edita el valor correspondiente a una columna de una fila específica, dada por la primary key ID.
    Parámetros: db. tipo: objeto mysql
                cursor. tipo: objeto mysql
                donde_trocar. tipo: int
    """
    update_query = "UPDATE {0} SET {1} = {2} WHERE {3} = {4}"
    while True:
        if donde_trocar == 1:
            donde_trocar = "Medicos" #{0}
            print("1. ID\n2. Nombre\n3. Especialidad\n4. Telefono\n5. Email\n6. Disponible")
            columnas = ["ID", "Nombre", "Especialidad", "Telefono", "Email","Disponible"]
            qual_columna = input("Escriba exactamente el nombre de la columna en la cual quiere editar: ")
            while True:
                if qual_columna in columnas:
                    if qual_columna != columnas[0]:
                        qual_columna = validacao(qual_columna,str) #{1}
                        break
                    else:
                        qual_columna = input("No se pueden cambiar los valores de esta columna, ingrese un valor nuevamente: ")
                else:
                    qual_columna = input("Valor no valido, ingrese la columna nuevamente: ")
            qual_ID = input(f"Ingrese el ID en el cual quiere que cambiar el valor de {qual_columna}: ")
            qual_ID = validacao(qual_ID, int, ID=True)  # {4}
            if qual_columna == columnas[3]:
                novo_valor = input("Ingrese el nuevo valor por el que desea actualizar: ")
                novo_valor = validacao(novo_valor,str,telefono=True) #{2}
            elif qual_columna == columnas[4]:
                novo_valor = input("Ingrese el nuevo valor por el que desea actualizar: ")
                novo_valor = validacao(novo_valor,str,correo=True)
            elif qual_columna == columnas[5]:
                print("Disponible toma como valores: (1, 0) enteros")
                novo_valor = input("Ingrese el nuevo valor por el que desea actualizar: ")
                novo_valor = validacao(novo_valor,int,booleano=True)
            else:
                novo_valor = input("Ingrese el nuevo valor por el que desea actualizar: ")
                novo_valor = validacao(novo_valor,str)
            cursor.execute(update_query.format(donde_trocar,qual_columna,novo_valor,"ID",qual_ID))
            break            
        elif donde_trocar == 2:
            donde_trocar = "Pacientes"  #{0}
            print("1. ID\n2. Nombre\n3. Nacimiento\n4. Genero\n5. Tipo_Sangre\n6. Telefono\n7. Direccion\n8. Email")
            columnas = ["ID", "Nombre", "Nacimiento", "Genero", "Tipo_Sangre", "Telefono", "Direccion", "Email"]
            qual_columna = input("Escriba exactamente el nombre de la columna en la cual quiere editar: ")
            while True:
                if qual_columna in columnas:
                    if qual_columna != columnas[0]:
                        qual_columna = validacao(qual_columna,str) #{1}
                        break
                    else:
                        qual_columna = input("No se pueden cambiar los valores de esta columna, ingrese un valor nuevamente: ")
                else:
                    qual_columna = input("Valor no valido, ingrese la columna nuevamente: ")
            qual_ID = input(f"Ingrese el ID en el cual quiere que cambiar el valor de {qual_columna}: ")
            qual_ID = validacao(qual_ID, int, ID=True)  # {4}
            if qual_columna == columnas[2]:
                novo_valor = input("Ingrese el nuevo valor por el que desea actualizar: ")
                novo_valor = validacao(novo_valor,str,fecha=True) #{2}
            elif qual_columna == columnas[6]:
                novo_valor = input("Ingrese el nuevo valor por el que desea actualizar: ")
                novo_valor = validacao(novo_valor,str,direccao=True)
            elif qual_columna == columnas[5]:
                novo_valor = input("Ingrese el nuevo valor por el que desea actualizar: ")
                novo_valor = validacao(novo_valor,str,telefono=True)
            elif qual_columna == columnas[7]:
                novo_valor = input("Ingrese el nuevo valor por el que desea actualizar: ")
                novo_valor = validacao(novo_valor,str,correo=True)
            else:
                novo_valor = input("Ingrese el nuevo valor por el que desea actualizar: ")
                novo_valor = validacao(novo_valor,str)
            cursor.execute(update_query.format(donde_trocar,qual_columna,novo_valor,"ID",qual_ID))
            break
        elif donde_trocar == 3:
            donde_trocar = "Usuarios" #{0}
            print("1. ID\n2. Usuario\n3. Password\n4. Permiso_Medico\n5. Permiso_Paciente")
            columnas = ["ID", "Usuario", "Password", "Permiso_Medico", "Permiso_Paciente"]
            qual_columna = input("Escriba exactamente el nombre de la columna en la cual quiere editar: ")
            while True:
                if qual_columna in columnas:
                    if qual_columna != columnas[0]:
                        qual_columna = validacao(qual_columna,str) #{1}
                        break
                    else:
                        qual_columna = input("No se pueden cambiar los valores de esta columna, ingrese un valor nuevamente: ")
                else:
                    qual_columna = input("Valor no valido, ingrese la columna nuevamente: ")
            qual_ID = input(f"Ingrese el ID en el cual quiere que cambiar el valor de {qual_columna}: ")
            qual_ID = validacao(qual_ID, int, ID=True)  # {4}
            if qual_columna == columnas[3] or qual_columna == columnas[4]:
                print("Esta columna toma como valores: (1, 0) enteros")
                novo_valor = input("Ingrese el nuevo valor por el que desea actualizar: ")
                novo_valor = validacao(novo_valor,int,booleano=True) #{2}
            else:
                novo_valor = input("Ingrese el nuevo valor por el que desea actualizar: ")
                novo_valor = validacao(novo_valor,str)
            cursor.execute(update_query.format(donde_trocar,qual_columna,novo_valor,"ID",qual_ID))
            break
        elif donde_trocar == 4:
            donde_trocar = "Citas" #{0}
            print("1. ID\n2. ID_Medico\n3. ID_Paciente\n4. Fecha\n5. Hora")
            columnas = ["ID", "ID_Medico", "ID_Paciente", "Fecha", "Hora"]
            qual_columna = input("Escriba exactamente el nombre de la columna en la cual quiere editar: ")
            while True:
                if qual_columna in columnas:
                    if qual_columna != columnas[0] and qual_columna != columnas[1] and qual_columna != columnas[2]:
                        qual_columna = validacao(qual_columna, str)  # {1}
                        break
                    else:
                        qual_columna = input("No se pueden cambiar los valores de esta columna, ingrese un valor nuevamente: ")
                else:
                    qual_columna = input("Valor no valido, ingrese la columna nuevamente: ")
            qual_ID = input(f"Ingrese el ID en el cual quiere que cambiar el valor de {qual_columna}: ")
            qual_ID = validacao(qual_ID, int, ID=True)  # {4}
            if qual_columna == columnas[3]:
                novo_valor = input("Ingrese el nuevo valor por el que desea actualizar (formato AAAA-MM-DD): ")
                novo_valor = validacao(novo_valor, str, fecha=True)  # {2}
            elif qual_columna == columnas[4]:
                #ARREGLAR ESTO LA HORA 24
                novo_valor = input("Ingrese el nuevo valor por el que desea actualizar (formato HH:MM): ")
                novo_valor = validacao(novo_valor,str,hora=True)
            else:
                novo_valor = input("Ingrese el nuevo valor por el que desea actualizar: ")
                novo_valor = validacao(novo_valor, str)
            update_query = f"UPDATE {donde_trocar} SET {qual_columna} = %s WHERE ID = %s"
            cursor.execute(update_query, (novo_valor, qual_ID))
            break
        else:
            donde_trocar = input("Valor no válido, ingrese el valor nuevamente: ")
            donde_trocar = validacao(donde_trocar,int)
    db.commit()

def eliminar(db,cursor,donde_loschen):
    loschen_query = "DELETE FROM {0} WHERE ID = {1}"
    while True:
        if donde_loschen == 1:
            donde_loschen = "Medicos" #{0}
            qual_ID = input("Escriba el nombre del ID del médico que quiere eliminar: ")
            qual_ID = validacao(qual_ID,int,ID=True) #{1}
            cursor.execute(loschen_query.format(donde_loschen,qual_ID))
            break
        elif donde_loschen == 2:
            donde_loschen = "Pacientes" #{0}
            qual_ID = input("Escriba el nombre del ID del paciente que quiere eliminar: ")
            qual_ID = validacao(qual_ID,int,ID=True)
            cursor.execute(loschen_query.format(donde_loschen,qual_ID))
            break
        elif donde_loschen == 3:
            donde_loschen = "Usuarios" #{0}
            qual_ID = input("Escriba el nombre del ID del usuario que quiere eliminar: ")
            qual_ID = validacao(qual_ID,int,ID=True)
            try:
                cursor.execute("SELECT Usuario FROM Usuarios WHERE ID = %s", (qual_ID,))
                resultado = cursor.fetchone()
                for i in resultado:
                    nome_usuario = i
                cursor.execute("DROP USER %s@'localhost'", (nome_usuario,))
                cursor.execute(loschen_query.format(donde_loschen, qual_ID))
            except Exception as e:
                db.rollback()
                print(f"Error: {e}")
            break
        elif donde_loschen == 4:
            donde_loschen = "Citas" #{0}
            qual_ID = input("Escriba el nombre del ID de la cita que quiere eliminar: ")
            qual_ID = validacao(qual_ID,int,ID=True)
            cursor.execute(loschen_query.format(donde_loschen,qual_ID))
            break
        else:
            donde_loschen = input("Valor no válido, ingrese el valor nuevamente: ")
            donde_loschen = validacao(donde_loschen,int,ID=True)
    db.commit()
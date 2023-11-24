from funciones import conectar_mysql
import json

#GRANT ALL PRIVILEGES ON informatica1.* TO 'informatica1'@'localhost' WITH GRANT OPTION;
nome_usuario = input("Ingrese el nombre de usuario: ") or 'informatica1'
password_db = input("Ingrese la contraseña: ") or 'bio123'
db = conectar_mysql(nome_usuario, password_db)
if db:
    cursor = db.cursor()
else:
    print("Conexión fallida")

cursor.execute("CREATE DATABASE IF NOT EXISTS informatica1")
cursor.execute("USE informatica1")

cursor.execute("""CREATE TABLE IF NOT EXISTS Medicos (ID int PRIMARY KEY, Nombre VARCHAR (60), Especialidad VARCHAR (60),
               Telefono VARCHAR (60), Email VARCHAR (60), Disponible BOOLEAN)""")
cursor.execute("""CREATE TABLE IF NOT EXISTS Pacientes (ID int PRIMARY KEY, Nombre VARCHAR (60), Nacimiento VARCHAR (60), Genero ENUM('F', 'M'),
               Tipo_Sangre VARCHAR (60), Telefono VARCHAR (60), Direccion VARCHAR (60), Email VARCHAR (60))""")
cursor.execute("""CREATE TABLE IF NOT EXISTS Citas (ID int PRIMARY KEY,
               ID_Medico int, FOREIGN KEY(ID_Medico) REFERENCES Medicos(ID), ID_Paciente int, FOREIGN KEY(ID_Paciente) REFERENCES Pacientes(ID),
               Fecha VARCHAR (60), Hora VARCHAR (60))""")
cursor.execute("""CREATE TABLE IF NOT EXISTS Usuarios (ID int PRIMARY KEY, Usuario VARCHAR (60), Password VARCHAR (60),
               Permiso_Medico BOOLEAN, Permiso_Paciente BOOLEAN)""")

#Los valores inicales están guardados en archivos .json
with open("Valores iniciales/medicos.json", "r", encoding='utf8') as archivo:
    medicos = json.load(archivo)
    #(medicos) variable es class <<list>> hecha de tuplas con valores del dict de json
with open("Valores iniciales/pacientes.json", "r", encoding='utf8') as archivo:
    pacientes = json.load(archivo)
with open("Valores iniciales/citas.json", "r", encoding='utf8') as archivo:
    citas = json.load(archivo)
with open("Valores iniciales/usuarios.json", "r", encoding='utf8') as archivo:
    usuarios = json.load(archivo)

#Ciclo para añadir de la lista con medicos/paientes/citas a la DB
tupla1 = []
for medico in medicos:
    tupla = tuple(medico.values())
    tupla1.append(tupla)
cursor.executemany("""INSERT IGNORE INTO Medicos (ID, Nombre, Especialidad, Telefono, Email, Disponible)
                   VALUES (%s,%s,%s,%s,%s,%s)""", tupla1)
tupla1 = []
for paciente in pacientes:
    tupla = tuple(paciente.values())
    tupla1.append(tupla)
cursor.executemany("""INSERT IGNORE INTO Pacientes (ID, Nombre, Nacimiento, Genero, Tipo_Sangre, Telefono, Direccion, Email)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""", tupla1)
tupla1 = []
for cita in citas:
    tupla = tuple(cita.values())
    tupla1.append(tupla)
cursor.executemany("""INSERT IGNORE INTO Citas (ID, ID_Medico, ID_Paciente, Fecha, Hora)
                   VALUES (%s,%s,%s,%s,%s)""", tupla1)
tupla1 = []
for usuario in usuarios:
    tupla = tuple(usuario.values())
    tupla1.append(tupla)
cursor.executemany("""INSERT IGNORE INTO Usuarios (ID, Usuario, Password, Permiso_Medico, Permiso_Paciente)
                   VALUES (%s,%s,%s,%s,%s)""", tupla1)
db.commit()
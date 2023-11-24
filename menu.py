"""Integrantes:
Daniel Iván Lozano Simanca. CC: 1137974802
Juan Cuadro Calume Pablo
"""
from funciones import *
print("BIENVENIDO AL SISTEMA\nCRUD BASE DE DATOS IPS")
from conexion import *

cursor.execute("SELECT Permiso_Medico, Permiso_Paciente FROM Usuarios WHERE Usuario = %s", (nome_usuario,))

lista_permisos = []
for fila in cursor:
    #Lista_permisos tiene los valores de las columnas Permiso_Medico y Permiso_Paciente respectivamente, desde fila
    lista_permisos.append(fila[0])
    lista_permisos.append(fila[1])

#Condicional donde se define a qué tipo de menú puede acceder el usuario dependiendo sus permisos
if lista_permisos[0] == 1 and lista_permisos[1] == 1:
    query = 1
    menu_admin(cursor,query,db)
elif lista_permisos[0] == 1:
    query = 1
    menu_medico(cursor,query,db)
elif lista_permisos[1] == 1:
    query = 1
    menu_paciente(cursor, query, db)


#conexion

import mysql.connector

conexion = mysql.connector.connect(
    host="localhost", 
    user="root",
    password="Mar200528$", 
    database="tienda_pitico"
)

cursor = conexion.cursor()

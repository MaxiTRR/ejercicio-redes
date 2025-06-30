import mysql.connector
from mysql.connector import Error


#Funcion para gestionar la base de datos
def connect_db():
        db_config = {
            "host": "localhost",  # O la IP de tu servidor MySQL
            "user": "root",
            "password": "",
            "database": "db_github_api"
        }
        try:
            conn = mysql.connector.connect(**db_config)
            print("Conexión exitosa a la base de datos MySQL!")
            return conn
        except mysql.connector.Error as err:
            if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
                print("Algo está mal con tu nombre de usuario o contraseña")
            elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                print("La base de datos no existe")
            else:
                print(f"Error: {err}")


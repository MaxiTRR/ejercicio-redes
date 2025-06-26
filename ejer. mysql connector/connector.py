import mysql.connector


db_config = {
    "host": "localhost",  # O la IP de tu servidor MySQL
    "user": "root",
    "password": "",
    "database": "redes_ifts4"
}

try:
    conn = mysql.connector.connect(**db_config)
    print("Conexión exitosa a la base de datos MySQL!")

    cursor = conn.cursor()

    query = "SELECT id, name, last_name, age FROM usuario_redes" 

    cursor.execute(query)

    results = cursor.fetchall()
    print(results)

    if results:
        print("\nResultados de la consulta:")
        for row in results:
            print(f"ID: {row[0]}, Nombre: {row[1]}, Apellido: {row[2]}, Edad: {row[3]}")
    else:
        print("\nNo se encontraron resultados para la consulta.")

except mysql.connector.Error as err:
    if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
        print("Algo está mal con tu nombre de usuario o contraseña")
    elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
        print("La base de datos no existe")
    else:
        print(f"Error: {err}")

finally:
    if 'cursor' in locals() and cursor is not None:
        cursor.close()
        print("\nCursor cerrado.")
    if 'conn' in locals() and conn.is_connected():
        conn.close()
        print("Conexión a la base de datos MySQL cerrada.")

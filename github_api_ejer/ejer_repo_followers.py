import requests
import mysql.connector

def main():
    db_config = {
        "host": "localhost",  # O la IP de tu servidor MySQL
        "user": "root",
        "password": "",
        "database": "db_github_api"
    }

    def connect_db():
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

    user=input("Ingrese su nombre de Usuario de Github: ")

    url_repo = f'https://api.github.com/users/{user}/repos'
    url_followers = f'https://api.github.com/users/{user}/followers'
    
    params = {
        'sort':'creates',
        'direction':'desc'
    }

    response_repo = requests.get(url_repo, params=params)
    response_followers = requests.get(url_followers, params=params)

    #Estado de la consulta de los Repos
    if response_repo.status_code == 200:
        conn = connect_db()

        repositorios = response_repo.json()

        print("------------------------------")
        print("REPOSITORIOS")
        print("------------------------------")

        for repo in repositorios[:5]:
            print(f'- {repo['name']}({repo['html_url']})')
            cursor = conn.cursor()
            query=f"INSERT INTO repositorios (name, html_url) VALUES('{repo['name']}','{repo['html_url']}')"
            cursor.execute(query)
            conn.commit()
    else:
        print(f'Error: {response_repo.status_code}')

    #Estado de la consulta de los followers
    if response_followers.status_code == 200:
        conn = connect_db()
        followers = response_followers.json()
        
        print("------------------------------")
        print("FOLLOWERS")
        print("------------------------------")

        for follower in followers[:5]:
            print(f'- {follower['login']}({follower['html_url']})')
            cursor = conn.cursor()
            query=f"INSERT INTO followers (login, html_url) VALUES('{follower['login']}','{follower['html_url']}')"
            cursor.execute(query)
            conn.commit()
    else:
        print(f'Error: {response_followers.status_code}')

main()
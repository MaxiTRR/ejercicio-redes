import socket
import threading
import requests

#Parametros asignadas para que el servidor pueda crear el socket
HOST = '127.0.0.1'
PORT = 12345

#Aca se crear el socket, especificanco con AF_INET que la ip es ipv4, y con SOCK_STREAM, que es una conexion TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
# Se conecta el server con la ip y el puerto antes definidos
server.bind((HOST, PORT)) 
#Se pone al servidor en modo escucha
server.listen() 

menu = "Ingrese algunas de las opciones:\n 1-Ingrese Usuario\n 2- Ver Repositorios de Github\n 3- Ver seguidores de Github\n 4- Finalizar Conexion"

#Bandera para indicar si el cliente esta conectado o no. Si camba a False, el cliente se desconecto, finalizando el loop y los hilos de ejecucion
client_connected = True 

#Inicializamos la variable usuario
usuario = '' 

#Parametros para las consultas a la api (github)
params = {
        'sort':'creates',
        'direction':'desc'
    }

#Funcion que gestiona la conexion al cliente y las respuestas que el servidor envia.
#Recibe como parametro un objeto client cuendo este se conecta al servidor.
def handle_client(client):
    #Accedemos a esta bandera global 
    global client_connected, usuario
    while client_connected:
        #Intentamos recibir correctamente las respuestas del cliente. Sino, un error ocurrio y se finaliza la conexion.
        try:
            msg = client.recv(1024) #El servidor recive un mensaje del cliente
            msg_decoded = msg.decode('utf-8').strip() #Decodificammos el mensaje para leerlo como string y usamos strip() para limpiar espacios en blanco al inicio y final del string

            #Si el cliente eligio 1, se solicita el nombre de usuario
            if msg_decoded == '1':
                #Solicitamos el nombre de usuario(nickname) del cliente
                client.send("Usuario: ".encode('utf-8')) #Servidor envia un mensaje solicitando el nombre de usuario de github
                usuario = client.recv(1024).decode('utf-8') #Aca recibe la respuesta del cliente.
                print(f"Usuario: {usuario}")
            
            #Si el cliente eligio 2, el servidor solicita los repos de github de ese usuario y los envia de nuevo al cliente
            elif msg_decoded == '2':
                #Si se elige la opcion 2, chequeamos que el cliente no haya respondido con un usuario vacio (no eligio la opcion 1 previamente para ingresar el usuario)
                if usuario != '':
                    #Contruimos la url de la api de github para consultar los repos del usuario que ingreso el cliente
                    url_repo = f'https://api.github.com/users/{usuario}/repos' 
                    #Hacemos una peticion get a la url de la api, adjuntando la url y los parametros.
                    response_repo = requests.get(url_repo, params=params)

                    #Estado de la consulta de los Repos
                    if response_repo.status_code == 200:
                        #Parseamos la respuesta de la Api que viene en json
                        repositories = response_repo.json()

                        #Recorremos la respuesta de la api (limitado a mostrar solo 5 repos)
                        for repo in repositories[:5]:
                            #Contruimos una respuesta con los datos de la api
                            msg_to_client = f'- {repo['name']}({repo['html_url']})'
                            #Le enviamos la respuesta al cliente
                            client.send(msg_to_client.encode('utf-8'))
            
                    #Surgio un error al realizar la peticion a la api.
                    else: 
                        print(f'Error: {response_repo.status_code}')
            
            #Si el cliente elige 3, se consulta a la api por los followers del usuario
            elif msg_decoded == '3':
                #Si se elige la opcion 3, chequeamos que el cliente no haya respondido con un usuario vacio (no eligio la opcion 1 previamente para ingresar el usuario)
                if usuario != '':
                    #Contruimos la url de la api de github para consultar los followers del usuario que ingreso el cliente
                    url_followers = f'https://api.github.com/users/{usuario}/followers'
                    #Hacemos una peticion get a la url de la api, adjuntando la url y los parametros.
                    response_followers = requests.get(url_followers, params=params)

                    #Estado de la consulta de los followers
                    if response_followers.status_code == 200:
                        #Parseamos la respuesta de la Api que viene en json
                        followers = response_followers.json()

                        #Recorremos la respuesta de la api (limitado a mostrar solo 5 followers)
                        for follower in followers[:5]:
                            #Contruimos una respuesta con los datos de la api
                            msg_to_client = f'- {follower['login']}({follower['html_url']})'
                            #Le enviamos la respuesta al cliente
                            client.send(msg_to_client.encode('utf-8'))
            
                    #Surgio un error al realizar la peticion a la api.
                    else: 
                        print(f'Error: {response_followers.status_code}')
            
            #Si el cliente eligio 4, cerramos la conexion con el cliente
            elif msg_decoded == '4':
                msg_to_client = 'Se cerrara la conexion'
                #Enviamos un mensaje al cliente informando que se cerrara la conexion
                client.send(msg_to_client.encode('utf-8'))
                #Cerramos la conexion con el cliente
                client.close()
                #Cambiamos la bandera a false para terminar el bucle
                client_connected = False
                break
            #Si el cliente envia algo que no sea alguna de las opciones mostradas, lo informaos como invalido y reenviamos el menu.
            else:
                msg_to_client=f'Opcion invalida.\n{menu}'
                client.send(msg_to_client.encode('utf-8'))
        except Exception as e:
            # Manejo de errores y desconexión del cliente
            print(f"Error handling client: {e}")
            client.close()
            client_connected = False

#Funcion para recibir y aceptar la conexion de un cliente
def receive():
    while True:
        client, address = server.accept() #Cuando un cliente se conecta al socket del servidor, client devuelve la conexion con ese cliente y adress una tupla que contiene la ip y el puerto del cliente.
        print(f"Conectado con {str(address)}")
        client.send(menu.encode('utf-8')) #Le enviamos el menu con las opciones al cliente apenas este se conecta.

        # Iniciar un hilo para manejar al cliente
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

print("Servidor esperando conexiones.")
receive() #Se ejecuta por defecto la funcion receive cuando ejecutamos este script. El servidor se quedara esperando a recibir una conexion de un cliente.
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

# Diccionario para almacenar el estado de cada cliente
# La clave será el objeto socket del cliente, y el valor será un diccionario con su 'username', que consisitra en algun mensaje que el cliente envia al servidor,
# y un indicador 'awaiting_username' de valor boolean para saber si estamos esperando su nombre de usuario.
client_states = {}

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
#Recibe como parametro un objeto client y la addrees cuendo este se conecta al servidor.
def handle_client(client, address):
    #Accedemos a esta bandera global 
    global client_connected, usuario

    print(f"Manejando cliente: {address}")

    # Inicializar el estado para este cliente. AL inicio, el username esta vacio ya que no se recibio ningun mensaje del cliente aun, y awaiting... se setea a False
    client_states[client] = {'username': '', 'awaiting_username': False}

    #Le enviamos el menu con las opciones al cliente 
    client.send(menu.encode('utf-8')) 

    while client_connected:
        #Intentamos recibir correctamente las respuestas del cliente. Sino, un error ocurrio y se finaliza la conexion.
        try:
            msg = client.recv(1024) #El servidor recive un mensaje del cliente

            #Verificamos primero que el cliente haya enviado algun mensaje. Si no, asumimos que el client se desconecto y ejecutamos la sentencia break para finalizar el bucle
            if not msg:
                print(f"Cliente {address} desconectado (mensaje vacío).")
                break 

            #Si el cliente envio un mensaje, lo dcodificammos el mensaje para leerlo como string y usamos strip() para limpiar espacios en blanco al inicio y final del string
            msg_decoded = msg.decode('utf-8').strip() 
            print(f"Recibido de {address}: '{msg_decoded}'") 

            #Lógica de Manejo de Estado
            #Si el servidor está esperando el nombre de usuario de este cliente
            if client_states[client]['awaiting_username']:
                #El mensaje actual es el nombre de usuario
                client_states[client]['username'] = msg_decoded
                #Ya no esperamos el nombre de usuario
                client_states[client]['awaiting_username'] = False 
                #Le enviamos un mensaje al cliente, en conjunto con el menu
                client.send(f"Usuario '{client_states[client]['username']}' registrado exitosamente.\n{menu}".encode('utf-8'))
                print(f"Usuario registrado para {address}: {client_states[client]['username']}")
                continue # Volver al inicio del bucle para esperar la siguiente opción

            #Procesar opciones del menu
            #Si el cliente eligio 1, se solicita el nombre de usuario
            if msg_decoded == '1':
                #Le enviamos un mensaje al cliente solicitando que ingrese su usuario de Github
                client.send("Por favor, ingresa tu usuario de GitHub: ".encode('utf-8'))
                #Actualizamos el valor de awaiting... de los estados de cliente a True, para indicar que estamos esperando a que el cliente ingrese y envie el nombre de usuario
                client_states[client]['awaiting_username'] = True 
            
            #Si el cliente eligio 2, el servidor solicita los repos de github de ese usuario y los envia de nuevo al cliente
            elif msg_decoded == '2':
                #Establecemos una variable del usuario actual con el usuario ingresado por el cliente, la cual se guardo en el diccionario client_states
                current_user = client_states[client]['username']
                #Verificamos que se haya asignado algun valor a esta variable para comtinuar
                if current_user:
                    #Contruimo el endpoint de la api de github con el usuario enviado por el cliente
                    url_repo = f'https://api.github.com/users/{current_user}/repos'
                    #Realizamos la peticion a la api
                    response_repo = requests.get(url_repo, params=params)

                    #Verificamos que la consulta haya salido bien
                    if response_repo.status_code == 200:
                        #Convertimos la respuesta json de la api.
                        repositories = response_repo.json()
                        #Verificamos que la variable haya obtenido algun valor (que existan repositorios en el usuario)
                        if repositories:
                            response_str = "Repositorios de " + current_user + ":\n"
                            #Recorremos los repositorios traidos por la consulta y mostramos solo los primeros 5
                            for repo in repositories[:5]: 
                                response_str += f'- {repo['name']} ({repo['html_url']})\n'
                            #Le enviamos al cliente un mensaje mostrando los primeros 5 repositorios encontrados
                            client.send((response_str + f"\n{menu}").encode('utf-8'))
                        #Si no se encontraron repositorios, se lo indicamos al cliente
                        else:
                            client.send(f"No se encontraron repositorios para el usuario '{current_user}'.\n{menu}".encode('utf-8'))
                    #Si la consulta arrojo un error, se lo indicamos al cliente
                    else:
                        client.send(f"Error al consultar repositorios (Código: {response_repo.status_code}). Asegúrate de que el usuario exista.\n{menu}".encode('utf-8'))
                #Si la variable current user no posee ningun valor, es porque el cliente no envio ningun nombre de usuario todavia
                else:
                    #Le enviamos un mensaje al cliente pidiendo que elija primero la opcion 1
                    client.send(f"Por favor, ingresa tu usuario primero (Opción 1).\n{menu}".encode('utf-8'))
            
            #Si el cliente elige 3, se consulta a la api por los followers del usuario. Es basicamente la misma logica para consultar repositorios, cambiando la url del endpoint, variables y mensajes enviados para reflejar que se trata de consultar los followers del usuario
            elif msg_decoded == '3':
                current_user = client_states[client]['username']
                if current_user:
                    url_followers = f'https://api.github.com/users/{current_user}/followers'
                    response_followers = requests.get(url_followers, params=params)

                    if response_followers.status_code == 200:
                        followers = response_followers.json()
                        if followers:
                            response_str = "Seguidores de " + current_user + ":\n"
                            for follower in followers[:5]: # Mostrar solo los primeros 5
                                response_str += f'- {follower['login']} ({follower['html_url']})\n'
                            client.send((response_str + f"\n{menu}").encode('utf-8'))
                        else:
                            client.send(f"No se encontraron seguidores para el usuario '{current_user}'.\n{menu}".encode('utf-8'))
                    else:
                        client.send(f"Error al consultar seguidores (Código: {response_followers.status_code}). Asegúrate de que el usuario exista.\n{menu}".encode('utf-8'))
                else:
                    client.send(f"Por favor, ingresa tu usuario primero (Opción 1).\n{menu}".encode('utf-8'))
            
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
        #Manejo de excepciones
        except ConnectionResetError:
            print(f"Cliente {address} cerró la conexión forzosamente.")
            break
        except Exception as e:
            print(f"Error manejando cliente {address}: {e}")
            break
        finally:
            # Este bloque se ejecuta cuando el bucle se rompe (cliente desconectado o error)
            pass

    #Limpiar datos del cliente y cerrar socket fuera del bucle
    #Verificamos que el cliente este dentro del diccionario de estados de cliente
    if client in client_states:
        #Usamos del para eliminar el cliente del diccionario
        del client_states[client]
    #Intentamos cerra la conexion
    try:
        client.close()
    except OSError:
        pass # El socket ya podría estar cerrado
    print(f"Manejador de conexión para cliente {address} terminado.")

#Funcion para recibir y aceptar la conexion de un cliente
def receive():
    while True:
        client, address = server.accept() #Cuando un cliente se conecta al socket del servidor, client devuelve la conexion con ese cliente y adress una tupla que contiene la ip y el puerto del cliente.
        print(f"Conectado con {str(address)}")
        
        # Iniciar un hilo para manejar al cliente
        thread = threading.Thread(target=handle_client, args=(client, address))
        thread.start()

print("Servidor esperando conexiones.")
receive() #Se ejecuta por defecto la funcion receive cuando ejecutamos este script. El servidor se quedara esperando a recibir una conexion de un cliente.
import socket
import threading
import requests

# Parámetros asignados para que el servidor pueda crear el socket
HOST = '127.0.0.1'
PORT = 12345

# Creamos el socket para el servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

menu = (
    "Ingrese algunas de las opciones:\n"
    " 1- Ingresar Usuario\n"
    " 2- Ver Repositorios de Github\n"
    " 3- Ver seguidores de Github\n"
    " 4- Finalizar Conexión"
)

# Diccionario para almacenar el estado de cada cliente
# La clave será el objeto socket del cliente, y el valor será un diccionario con su 'username'
# y un indicador 'awaiting_username' para saber si estamos esperando su nombre de usuario.
client_states = {}

# Parámetros para las consultas a la API (GitHub)
params = {
    'sort': 'creates',
    'direction': 'desc'
}

# Función que gestiona la conexión al cliente y las respuestas que el servidor envía.
def handle_client(client_socket, client_address):
    print(f"Manejando cliente: {client_address}")

    # Inicializar el estado para este cliente
    client_states[client_socket] = {'username': '', 'awaiting_username': False}

    # Enviar el menú inicial al cliente
    client_socket.send(menu.encode('utf-8'))

    while True:
        try:
            # Recibir mensaje del cliente
            msg = client_socket.recv(1024)
            if not msg:
                print(f"Cliente {client_address} desconectado (mensaje vacío).")
                break # El cliente se desconectó

            msg_decoded = msg.decode('utf-8').strip()
            print(f"Recibido de {client_address}: '{msg_decoded}'")

            # --- Lógica de Manejo de Estado ---
            # Si el servidor está esperando el nombre de usuario de este cliente
            if client_states[client_socket]['awaiting_username']:
                # El mensaje actual es el nombre de usuario
                client_states[client_socket]['username'] = msg_decoded
                client_states[client_socket]['awaiting_username'] = False # Ya no esperamos el nombre de usuario
                client_socket.send(f"Usuario '{client_states[client_socket]['username']}' registrado exitosamente.\n{menu}".encode('utf-8'))
                print(f"Usuario registrado para {client_address}: {client_states[client_socket]['username']}")
                continue # Volver al inicio del bucle para esperar la siguiente opción

            # --- Procesar Opciones del Menú ---
            if msg_decoded == '1':
                client_socket.send("Por favor, ingresa tu usuario de GitHub: ".encode('utf-8'))
                client_states[client_socket]['awaiting_username'] = True # Indicar que esperamos el nombre de usuario
            elif msg_decoded == '2':
                current_user = client_states[client_socket]['username']
                if current_user:
                    url_repo = f'https://api.github.com/users/{current_user}/repos'
                    response_repo = requests.get(url_repo, params=params)

                    if response_repo.status_code == 200:
                        repositories = response_repo.json()
                        if repositories:
                            response_str = "Repositorios de " + current_user + ":\n"
                            for repo in repositories[:5]: # Mostrar solo los primeros 5
                                response_str += f'- {repo['name']} ({repo['html_url']})\n'
                            client_socket.send((response_str + f"\n{menu}").encode('utf-8'))
                        else:
                            client_socket.send(f"No se encontraron repositorios para el usuario '{current_user}'.\n{menu}".encode('utf-8'))
                    else:
                        client_socket.send(f"Error al consultar repositorios (Código: {response_repo.status_code}). Asegúrate de que el usuario exista.\n{menu}".encode('utf-8'))
                else:
                    client_socket.send(f"Por favor, ingresa tu usuario primero (Opción 1).\n{menu}".encode('utf-8'))
            elif msg_decoded == '3':
                current_user = client_states[client_socket]['username']
                if current_user:
                    url_followers = f'https://api.github.com/users/{current_user}/followers'
                    response_followers = requests.get(url_followers, params=params)

                    if response_followers.status_code == 200:
                        followers = response_followers.json()
                        if followers:
                            response_str = "Seguidores de " + current_user + ":\n"
                            for follower in followers[:5]: # Mostrar solo los primeros 5
                                response_str += f'- {follower['login']} ({follower['html_url']})\n'
                            client_socket.send((response_str + f"\n{menu}").encode('utf-8'))
                        else:
                            client_socket.send(f"No se encontraron seguidores para el usuario '{current_user}'.\n{menu}".encode('utf-8'))
                    else:
                        client_socket.send(f"Error al consultar seguidores (Código: {response_followers.status_code}). Asegúrate de que el usuario exista.\n{menu}".encode('utf-8'))
                else:
                    client_socket.send(f"Por favor, ingresa tu usuario primero (Opción 1).\n{menu}".encode('utf-8'))
            elif msg_decoded == '4':
                msg_to_client = 'Se cerrará la conexión.'
                client_socket.send(msg_to_client.encode('utf-8'))
                print(f"Cliente {client_address} solicitó desconexión.")
                break # Salir del bucle para cerrar la conexión
            else:
                msg_to_client=f'Opción inválida. Por favor, elige una opción del menú.\n{menu}'
                client_socket.send(msg_to_client.encode('utf-8'))

        except ConnectionResetError:
            print(f"Cliente {client_address} cerró la conexión forzosamente.")
            break
        except Exception as e:
            print(f"Error manejando cliente {client_address}: {e}")
            break
        finally:
            # Este bloque se ejecuta cuando el bucle se rompe (cliente desconectado o error)
            pass

    # Limpiar datos del cliente y cerrar socket fuera del bucle
    if client_socket in client_states:
        del client_states[client_socket]
    try:
        client_socket.close()
    except OSError:
        pass # El socket ya podría estar cerrado
    print(f"Manejador de conexión para cliente {client_address} terminado.")


# Función para recibir y aceptar la conexión de un cliente
def receive_connections():
    print("Servidor esperando conexiones.")
    while True:
        client_socket, client_address = server.accept()
        print(f"Conectado con {str(client_address)}")

        # Iniciar un hilo para manejar al cliente
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()

# Iniciar la función para recibir conexiones
receive_connections()
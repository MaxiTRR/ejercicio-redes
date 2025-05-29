import socket
import threading

HOST = '127.0.0.1'
PORT = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Aca se crear el socket, especificanco con AF_INET que la ip es ipv4, y con SOCK_STREAM, que es una conexion TCP
server.bind((HOST, PORT)) # Se conecta el server con la ip y el puerto antes definidos
server.listen() #Se pone al servidor en modo escucha

clients = [] #Aca se almacenan cada objeto de socket de los clientes que se conecten
usuarios = [] #Aca se almacenan los nombres de los usuarios que se conecte (o sea, de los clientes)

#Funcion que envia cada mensaje a todos los clientes (usuarios conectados). Recorre la lista de clients y les envia un mensaje a cada uno.
def broadcast(message):
    for client in clients:
        client.send(message)

# funcion de atencion del thread. Maneja cada objecto de socket de cliente: recive los mensajes e invoca
#a la funcion broadcast para retransmitirlo a todos los clientes que esta guardados en la lista clients.
#Si hay un error (por ej., un cliente se desconecta) lo elimina de la lista clientes y envia un mensaje
#a los demas avisando que se desconecto.
def handle_client(client):
    while True:
        try:
            # Recibir mensaje del cliente y retransmitirlo
            msg = client.recv(1024)
            msg_decoded = msg.decode('utf-8').strip()
            if msg_decoded == '1':
                response = 'Eligio Login'
                client.send(response.encode('utf-8'))
            elif msg_decoded == '2':
                response = 'Eligio Send'
                client.send(response.encode('utf-8'))
            elif msg_decoded == '3':
                response = 'Eligio Sendall'
                client.send(response.encode('utf-8'))
            elif msg_decoded == '4':
                response = 'Eligio Show'
                client.send(response.encode('utf-8'))
            elif msg_decoded == '5':
                response = 'Eligio Exit'
                client.send(response.encode('utf-8'))
                index = clients.index(client) #Obtinee el indice del objeto socket del cliente guarado ene sta lista para poder encontrarlo luego en la lista de usuarios (que guarda los nicknames)
                clients.remove(client)
                client.close()
                usuario = usuarios[index]
                broadcast(f"{usuario} abandonó el chat.".encode('utf-8'))
                usuarios.remove(usuario)
                break
            
            broadcast(msg_decoded)
        except:
            # Si hay error, eliminar al cliente
            index = clients.index(client) #Obtinee el indice del objeto socket del cliente guarado ene sta lista para poder encontrarlo luego en la lista de usuarios (que guarda los nicknames)
            clients.remove(client)
            client.close()
            usuario = usuarios[index]
            broadcast(f"{usuario} abandonó el chat.".encode('utf-8'))
            usuarios.remove(usuario)
            break

# Función para aceptar conexiones
def receive():
    while True:
        client, address = server.accept() #Cuando un cliente se conecta al socket del servidor, client devuelve la conexion con ese cliente y adress una tupla que contiene la ip y el puerto del cliente.
        print(f"Conectado con {str(address)}")

        # Solicitar nickname al cliente
        client.send("Usuario: ".encode('utf-8')) #Cuando el cliente se conecta, el servidor le envia al cliente este mensjae solicitnado el nombre de Usuario. En ese momento, el clinete ingresa su nickname y lo envia al servidor.
        usuario = client.recv(1024).decode('utf-8') #Aca recibe la respuesta del cliente.
        usuarios.append(usuario)
        clients.append(client)

        print(f"Usuario: {usuario}")
        broadcast(f"{usuario} se unió al chat!".encode('utf-8')) #Le envia un mensaje a todos los clinetes
        client.send("Conectado al servidor.".encode('utf-8')) #Aca, se lo envia al cliente particular que inicio esta conexion
        client.send("Ingrese algunas de las opciones:\n 1-Login\n 2-Send\n 3-sendall\n 4-show\n 5-exit".encode('utf-8'))
        
        # Iniciar un hilo para manejar al cliente
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

print("Servidor esperando conexiones.")
receive()
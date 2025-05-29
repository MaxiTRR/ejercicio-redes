import socket
import threading

HOST = '127.0.0.1' # en este caso se tetea laip a mano
PORT = 12345 #puerto se puede usar del 0 al 65535 evitar los 0-1023

# Inicializar socket del cliente
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Función para recibir mensajes del servidor
def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            print(message)
        except:
            print("Error en la conexión.")
            client.close()
            break

# Función para enviar mensajes al servidor
def send():
    while True:
        message = f"{usuario}: {input('')}"
        client.send(message.encode('utf-8'))

# Solicitar nickname al usuario
usuario = input("Ingresa el usuario: ")

# Iniciar hilos para recibir mensajes
receive_thread = threading.Thread(target=receive) #En el constructor de la clase Thread, el parametro       target es la funcion a la que apunta cuando se inicia el thread
receive_thread.start()

# Iniciar hilos para enviar mensajes
write_thread = threading.Thread(target=send)
write_thread.start()
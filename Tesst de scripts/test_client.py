import socket
import threading
import requests

# Parámetros asignados para que el cliente pueda crear el socket
HOST = '127.0.0.1'
PORT = 12345

# Creamos el socket para el cliente y nos conectamos al mismo
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Bandera para detectar cuando el servidor termina la conexión y hacer lo mismo con el cliente
should_run = True

# Lista con opciones del menú que el cliente puede enviar al servidor
options = ['1', '2', '3', '4']

# Variable para almacenar el usuario (se actualizará al recibir el prompt del servidor)
usuario = ''

# Función para recibir mensajes del servidor
def receive():
    global should_run, usuario
    while should_run:
        try:
            message = client.recv(1024).decode('utf-8')

            if not message:
                print("\nServidor cerró la conexión. Desconectando...")
                should_run = False
                client.close()
                break
            # Si el servidor envía un mensaje que solicita el usuario
            elif message.startswith("Por favor, ingresa tu usuario de GitHub: "):
                temp_usuario = input(message) # Usa el mensaje del servidor como prompt
                # Envía el nombre de usuario ingresado al servidor
                client.send(temp_usuario.encode('utf-8'))
                print(f"El usuario ingresado fue: {temp_usuario}")
                usuario = temp_usuario # Actualiza la variable global usuario
            elif message == 'Se cerrará la conexión.':
                print(message)
                print("Desconectando del servidor...")
                should_run = False
                client.close()
                break
            else:
                print(message)
        except Exception as e:
            if should_run:
                print(f"Error en la conexión: {e}")
            should_run = False
            try:
                client.close()
            except:
                pass
            break

# Función para enviar mensajes al servidor
def send():
    global should_run
    while should_run:
        try:
            user_input = input("--: ")
            if not should_run:
                break

            # Envía la opción elegida al servidor
            if user_input in options:
                client.send(user_input.encode('utf-8'))
                if user_input == '4': # Si el usuario eligió 4, rompe el bucle de envío
                    break
            else:
                print("Opción inválida. Por favor, elige entre 1, 2, 3 o 4.")

        except Exception as e:
            if should_run:
                print(f"Error al enviar mensaje: {e}")
            should_run = False
            try:
                client.close()
            except:
                pass
            break

# Iniciar hilos
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=send)
write_thread.start()

# Esperar a que los hilos terminen (opcional, para mantener el programa principal vivo)
receive_thread.join()
write_thread.join()
print("Cliente desconectado y programa finalizado.")
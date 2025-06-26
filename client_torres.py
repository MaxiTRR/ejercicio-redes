import socket
import threading

HOST = '127.0.0.1'
PORT = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

usuario = ""
connected_and_named = False
should_run = True 
options=['1', '2', '3', '4', '5']

# Función para recibir mensajes del servidor
def receive():
    global usuario, connected_and_named, should_run
    while should_run:
        try:
            message = client.recv(1024).decode('utf-8')
            
            if not message: # Si recv devuelve una cadena vacía, el servidor cerró la conexión
                print("\nServidor cerró la conexión. Desconectando...")
                should_run = False
                client.close()
                break 
            
            #if message.startswith("Usuario: "):
            #    if not connected_and_named:
            #        print("Servidor solicitando usuario, por favor ingresa tu nickname.")
            elif message == "Conectado al servidor.":
                print(message)
                connected_and_named = True
            elif message == "Eligio Exit": # Capturar el mensaje de confirmación de salida
                print(message)
                print("Desconectando del servidor...")
                should_run = False # Indicar a los hilos que deben terminar
                client.close() # Cerrar el socket del cliente
                break 
            else:
                print(message)
        except Exception as e:
            # Si el socket ya está cerrado por el servidor o por el hilo send,
            # recv lanzará un error. Si should_run ya es False, es un cierre esperado.
            if should_run: # Si el error ocurre y should_run aún es True, es un error inesperado
                print(f"Error en la conexión: {e}")
            
            should_run = False # Asegurar que todos los hilos sepan que deben parar
            try:
                client.close()
            except:
                pass # El socket ya puede estar cerrado
            break # Salir del bucle receive

# Función para enviar mensajes al servidor
def send():
    global usuario, should_run
    while should_run: 
        try:
            user_input = input("--: ") 
            if not should_run: # Si el estado cambió mientras esperábamos input
                break

            if connected_and_named and user_input not in options:
                message_to_send = f"{usuario}: {user_input}"
            else:
                message_to_send = user_input
            
            #Si el usuario elije 1, ingresa su nickname y lo envia al servidor
            if message_to_send == '1':
                #usuario = input("Ingresa tu nickname: ")
                client.send(usuario.encode('utf-8'))
            
            #El cliente envia la opcion 4 para que el servidor elija la opcion
            if message_to_send == '4':
                client.send(message_to_send.encode('utf-8'))

            # Si el usuario eligió '5', enviarlo y luego esperar la desconexión
            if message_to_send == '5':
                client.send(message_to_send.encode('utf-8'))
                break
            else:
                client.send(message_to_send.encode('utf-8'))
        except Exception as e:
            if should_run: # Si el error ocurre y should_run aún es True, es un error inesperado
                print(f"Error al enviar mensaje: {e}")
            
            should_run = False 
            try:
                client.close()
            except:
                pass # El socket ya puede estar cerrado
            break # Salir del bucle send

# Iniciar hilos
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=send)
write_thread.start()

# Esperar a que los hilos terminen (opcional, para mantener el programa principal vivo)
receive_thread.join()
write_thread.join()
print("Cliente desconectado y programa finalizado.")

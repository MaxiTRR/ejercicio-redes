import socket
import threading
import requests

#Parametros asignadas para que el cliente pueda crear el socket
HOST = '127.0.0.1'
PORT = 12345

#Creamos el socket para el cliente y nos conectamos al mismo
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

#Bandera para detectar cuando el servidor termina la conexion y hacer lo mismo con el cliente
should_run = True 

#Lista con opciones del menu que el cliente puede enviar al servidor
options=['1', '2', '3', '4']

#Iniciamos la variable de usuario
usuario = ''

#Función para recibir mensajes del servidor
def receive():
    #Usamos la variable global para acceder y modificar su valor desde dentro de esta funcion
    global should_run, usuario
    #Iniciamos el bucle con la bandera. Si se modifica a false, el bucle termina
    while should_run:
        #Intentamos recibir mensajes del servidor
        try:
            #Reciimos algun mensaje del servidor y lo decodificamos
            message = client.recv(1024).decode('utf-8')

            #Si el servidor devuelve una cadena vacía, el servidor cerró la conexión. Cerramos la conexion del lado del cliente.
            if not message: 
                print("\nServidor cerró la conexión. Desconectando...")
                # Indicar a los hilos que deben terminar
                should_run = False
                # Cerrar el socket del cliente
                client.close()
                break 
            #Si el servidor envia este mensaje porque el cliente eliio la opcion 4 y la mando previamente el servidor, cerramos la conexion del lado del cliente.

            #Si el cliente le envio previamente al servidor la opcion 1, este deberia constestar con un mensaje solicitando al usuario. De ser asi, el cliente escribe su usuario.
            if message.startswith("Usuario: "):
                #Preguntamos por el usuario
                temp_usuario = input("Ingresa tu usuario: ")
                #Enviamos el usuario al servidor
                client.send(temp_usuario.encode('utf-8'))
                print(f"El usuario ingresado fue: {temp_usuario}")
                #Actualizamos la variable global de usuario
                usuario = temp_usuario
            elif message == 'Se cerrara la conexion':
                print(message)
                print("Desconectando del servidor...")
                # Indicar a los hilos que deben terminar
                should_run = False 
                # Cerrar el socket del cliente
                client.close() 
                break 
            else:
                print(message)
        except Exception as e:
            # Si el socket ya está cerrado por el servidor o por el hilo send,
            # recv lanzará un error. Si should_run ya es False, es un cierre esperado.
            # Si el error ocurre y should_run aún es True, es un error inesperado
            if should_run: 
                print(f"Error en la conexión: {e}")
            # Asegurar que todos los hilos sepan que deben parar
            should_run = False 
            try:
                client.close()
            except:
                # El socket ya puede estar cerrado
                pass 
            break 

# Función para enviar mensajes al servidor
def send():
    #Usamos la variable global para acceder y modificar su valor desde dentro de esta funcion
    global should_run
    #Iniciamos el bucle con la bandera. Si se modifica a false, el bucle termina
    while should_run:
        #Intentamos enviar mensajes del servidor
        try:
            #Establecemos una variable con input para que el cliente pueda escribir en la consola
            user_input = input("--: ") 
            # Si el estado cambió mientras esperábamos input, cerramos el bucle
            if not should_run: 
                break

            if user_input not in options:
                message_to_send = user_input
            #Si el estado no cambio, determinas una variable con los input del cliente
            else:
                message_to_send = user_input

            #Si el usuario elige 1, ingresa su usuario y lo envia al servidor
            if message_to_send == '1':
                client.send(usuario.encode('utf-8'))

            #El cliente envia la opcion 2 para que el servidor elija la opcion (repos)
            if message_to_send == '2':
                client.send(message_to_send.encode('utf-8'))

            #El cliente envia la opcion 3 para que el servidor elija la opcion (followers)
            if message_to_send == '3':
                client.send(message_to_send.encode('utf-8'))
            
            # Si el usuario eligió '4', enviarlo y luego esperar la desconexión
            if message_to_send == '4':
                client.send(message_to_send.encode('utf-8'))
                break
        
        #Si ocurriese algun error al intentar enviar un mensaje, lanzamos una excepcion
        except Exception as e:
            # Si el error ocurre y should_run aún es True, es un error inesperado
            if should_run: 
                print(f"Error al enviar mensaje: {e}")
            should_run = False 
            try:
                client.close()
            except:
                # El socket ya puede estar cerrado
                pass 
            break 

# Iniciar hilos
#Creamos un hilo para recibir mensajes del servidor y le pasamos como argumento la funcion receive, y lo iniciamos
receive_thread = threading.Thread(target=receive) 
receive_thread.start()

#Creamos un hilo para enviar mensajes del servidor y le pasamos como argumento la funcion send, y lo iniciamos
write_thread = threading.Thread(target=send)
write_thread.start()

# Esperar a que los hilos terminen (opcional, para mantener el programa principal vivo)
receive_thread.join()
write_thread.join()
print("Cliente desconectado y programa finalizado.")
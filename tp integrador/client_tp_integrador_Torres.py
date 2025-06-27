import socket
import threading


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

#Una bandera boolean para controlar si el hilo de envío (send) debe esperar a que el usuario ingrese el nombre de usuario.Esto es crucial para sincronizar los inputs.
awaiting_input_username = False
#Un candado para proteger la variable `awaiting_user_input_for_username` y `usuario`
username_lock = threading.Lock() 

user_choice_1 = False #############

#Función para recibir mensajes del servidor
def receive():
    #Usamos la variable global para acceder y modificar su valor desde dentro de esta funcion
    global should_run, usuario, awaiting_input_username

    #Iniciamos el bucle con la bandera. Si se modifica a false, el bucle termina
    while should_run:
        #Intentamos recibir mensajes del servidor
        try:
            #Recibimos algun mensaje del servidor y lo decodificamos
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
            elif message.startswith("Por favor, ingresa tu usuario de GitHub: "):
                #Usamos with para iniciar el bloqueo y liberarlo una vez que la variable haya cambiado a True. Nos aseguramos el hilo de send no pueda hacer uso de esta varibale hasta que esta no terminado de ser usado por el hilo receive
                with username_lock:
                    awaiting_input_username = True 

                # Usa el mensaje del servidor como prompt para el input del usuario ("Por favor, ingresa tu usuario de Github")
                temp_usuario = input(message)
                #Enviamos el usuario al servidor
                client.send(temp_usuario.encode('utf-8'))
                print(f"El usuario ingresado fue: {temp_usuario}")

                #Volvemos a iniciar el bloqueo del hilo para asegurarnos de que las variables hayan sido actualizados antes de que puedan ser usadas por el hilo de send
                with username_lock:
                    usuario = temp_usuario # Actualiza la variable global usuario
                    awaiting_input_username = False # Ya no esperamos el nombre de usuario
            #Si el servidor envio este mensaje, significa que el finalizo la conexion de su lado, por lo cual el cliente hace lo mismo
            elif message == 'Se cerrara la conexion':
                print(message)
                print("Desconectando del servidor...")
                # Indicar a los hilos que deben terminar
                should_run = False 
                # Cerrar el socket del cliente
                client.close() 
                break 
            else:
                #Imprime mensajes generales del servidor, como el menú o resultados de la API
                print(message)
                #Asegúrate de que el input del usuario se pida solo después de recibir un mensaje general, pero no si estamos esperando un usuario específico.
                if not awaiting_input_username:
                    print("--: ", flush=True) # Muestra el prompt para la siguiente opción
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
    global should_run, awaiting_input_username, user_choice_1 #############3
    #Iniciamos el bucle con la bandera. Si se modifica a false, el bucle termina
    while should_run:
        #Actvamos el bloqueo para el hilo receive
        with username_lock:
            # Si estamos esperando un input de usuario específico (nombre de GitHub),
            # este hilo debe pausarse para no mostrar un input extra.
            if awaiting_input_username:
                continue # Vuelve a chequear en la siguiente iteración

        #Intentamos enviar mensajes del servidor
        try:
            #Se pide el input solo si no estamos esperando un nombre de usuario específico
            # El prompt "--C: " lo pone el hilo receive()
            user_input = input("//")  

            # Si el estado cambió mientras esperábamos input, cerramos el bucle
            if not should_run: 
                break

            #Envía la opción elegida al servidor si esta dentro de la lista de options
            if user_input in options:
                if user_input == '1':
                    user_choice_1 = 1 ####################
                client.send(user_input.encode('utf-8'))
                #Si el cliente ingreso la opcion 4, automaticamente finalizamos el bucle while
                if user_input == '4':
                    break
            else:
                if not user_choice_1:
                    print("Opción inválida. Por favor, elige entre 1, 2, 3 o 4.")
                print("--: ", end="", flush=True) # Repone el prompt
        
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

#Iniciar hilos
#Creamos un hilo para recibir mensajes del servidor y le pasamos como argumento la funcion receive, y lo iniciamos
receive_thread = threading.Thread(target=receive) 
receive_thread.start()

#Creamos un hilo para enviar mensajes del servidor y le pasamos como argumento la funcion send, y lo iniciamos
write_thread = threading.Thread(target=send)
write_thread.start()

#Esperar a que los hilos terminen (opcional, para mantener el programa principal vivo)
receive_thread.join()
write_thread.join()
print("Cliente desconectado y programa finalizado.")
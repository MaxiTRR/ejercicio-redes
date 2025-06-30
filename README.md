# Trabajos paracticos de Programacion sobre Redes IFTS 2025

## Carpetas
En las carpetas ejer.mysql connector, se encuenta el script del ejercicio para conectarse a una base de datos mysql y leer algun registro (debe haber una base de datos creada previamente en utilizando algun servicio como xampp)
<br>
<br>
En la carpeta github_api_ejer, se encuentra el ejercico para acceder a la api de github, obtener los repositorios y los followers e insertarlos en una base de datos (debe haber una base de datos creada previamente en utilizando algun servicio como xampp, se adjunta el schema para poder importarlo directamente)
<br>
<br>
En la carpeta sockets se encuentra el primer ejercicio de sockets con multiples conexions utilizando multiples hilos de conexion. El estado actual del ejercicio:
<ul>
  <li>Permite ingresar un usuario y Loguearse</li>
  <li>Las opciones de mandar mensajes a usuarios especificos y multiples usuarios no estan implementadas al no poder emular multiples conexiones</li>
  <li>La opcion show muestra la cantidad de usuarios conectados</li>
  <li>La opcion 5 finaliza la conexion</li>
</ul>

# Tp Integrador
## Estado actual 
<ul>
  <li>El programa pide al cliente ingresar un usuario, y el servidor puece consular la api de github para trar repositorios y followers al mismo, grabarlos en una base de datos sql y enviarselos al usuario</li>
</ul>

# Notas adicionales
Existe un pequeño bug de diseño, en el cual el programa no maneja del todo correctamente cuando el cliente ingresa su nombre de usuario (El programa no distingue este input de una respuesta no valida en ciertas ocasiones, seguramente por como el mismo maneja los multiples hilos de send() y write(), mostrando el mensaje correspondiente de respuesta no validas aunque igualmente envia la respuesta del servidor solicitando el usuario)
<br><br>
Se adjunta imagen de como ingresar correctamente los input para que el programa funcione correctamente.
![Captura tp integrador](https://github.com/user-attachments/assets/2c0e2e01-889a-4274-81a5-42c038ab5369)

<br>
La base de datos utilizada es la misma que la utilizada en el ejercicio de github_api, se adjunta el schema para poder importar la base de datos directamente (para el desarrollo, se utilizo Xammp)

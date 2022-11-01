# Tenemos tus datos
- **Categoría:** Forense/Programming
- **Dificultad:** ★★★☆☆
- **Autor:** [isaaclo97](https://isaaclo97.github.io/)

### Descripción
Tras el análisis de una máquina en un centro de operaciones incautado, se ha detectado un fichero que contiene información sensible sobre diferentes servidores, estos servidores es dónde operaban los cibercriminales.  

Sabemos por el nombre del mismo que usaban FileZilla para conectarse.  

### Archivos e instrucciones
Ficheros necesarios: FileZilla.xml  

Es necesario cambiar la IP en el documento FileZilla.xml por la IP real del servidor y desplegar el contenedor (`docker-compose up —build`), que creará un servidor FTP en el puerto por 21. Una vez creado conectarse y añadir el fichero Flag.txt. Modificar permisos para evitar que eliminen el fichero.


### Hints
1. Parece que es un trabajo que no puede ser manual.
2. Base64, usuarios, contraseñas, scripts.
3. Tarda mucho, ¿podemos optimizarlo?


### Flag
`CTFUni{v1V4_lA_aUt0m4tIz4c10N}`  
  

<br>

# Writeup

### Analizando como funciona el reto

La descripción muestra que existen diferentes servidores por lo que se puede intuir que es necesario conectarse a uno o varios de ellos para continuar con el reto: 

Analizando el fichero contiene 68647 lineas correspondiendo a más de 4900 servidores, por lo cual ir mano a mano puede realizarse pero igual se hace muy largo.


### Ideas

1. Descargar Filezilla, importar el fichero e ir probando uno por uno los servidores.
2. Analizar el fichero de Filezilla y automatizar un script.

Observando el fichero, se tienen los siguientes campos por cada servidor.

```
<Server> 
	<Host>115.239.15.6</Host>  <- IP del servidor
	<Port>22</Port>  <- Puerto
	<Protocol>1</Protocol> 
	<Type>0</Type> 
	<User>Milla</User>  <- Nombre usuario (generado basado en nombres reales)
	<Pass encoding="base64">dGRZWW1DczNhVU5pYUJ0S3Vn</Pass> <- Contraseña encoding en base64
	<Logontype>1</Logontype> 
	<EncodingType>Auto</EncodingType> 
	<BypassProxy>0</BypassProxy> 
	<Name>Vehmaa</Name>  <- Nombre del servidor generado con nombre de ciudades
	<SyncBrowsing>0</SyncBrowsing> 
	<DirectoryComparison>0</DirectoryComparison> 
</Server> 
```

Es necesario obtener la contraseña real del base64.

La idea para automatizar entonces sería.

1. Leer el archivo XML.
2. Por cada uno de los servidores obtener los datos de Host, Port, User, Pass.
3. Conectarse mediante FTP hasta que uno funcione.
4. En caso de que uno funcione parar, probar a conectarse como cada uno prefiera y analizar lo que se tiene dentro.
5. Se obtiene un fichero codificado con varios base64 que cualquier herramienta lo detecta.


### Conexión FTP mediante Python

Yo particularmente utilizo el siguiente código para poder tener conexiones a FTP en Python.

```
from ftplib import FTP
import base64
IPList = []
UserList = []
PasswordList = []

with open('filezilla.xml', 'r',encoding='utf-8') as f:
    data = f.readlines()
    for i in data:
        if '<Pass encoding="base64">' in i:
            base64_bytes = i.replace('<Pass encoding="base64">', '').replace('</Pass>', '').strip().encode('ascii')
            message_bytes = base64.b64decode(base64_bytes)
            message = message_bytes.decode('ascii')
            PasswordList.append(message)
        elif '<Host>' in i:
            IPList.append(i.replace('<Host>', '').replace('</Host>', '').strip())
        elif '<User>' in i:
            UserList.append(i.replace('<User>','').replace('</User>','').strip())

for i in range(len(PasswordList)):
    try:
        ftp = FTP(IPList[i], user=UserList[i], passwd=PasswordList[i], timeout=2.)
        print("Bingo! -> " + str(i))
        break
    except:
        print(str(i) + " no es la solucion")
        continue
```

El timeout=2. es muy **importante** (2 segundos o pasar al siguiente), el servidor se encuentra en mitad de la tabla, lo que serían unas 2000 iteraciones, es decir unos 4000 segundos es decir en torno a una hora (siempre y cuando no se paralelice). El valor por defecto de timeout es 60 segundos (2000 minutos si no se modifica).
<br>


## Autor
* Isaac Lozano Osorio
* [Twitter](https://twitter.com/isaac_lozano_97)
* [Linkedin](https://www.linkedin.com/in/isaaclozanoosorio/)
* [Web](https://isaaclo97.github.io/)
* [Github](https://github.com/isaaclo97/)
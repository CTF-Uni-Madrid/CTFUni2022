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


### Formato de la flag
``CTFUni{}``

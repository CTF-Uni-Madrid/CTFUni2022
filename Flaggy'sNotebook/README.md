# Flaggy's Notebook
- **Categoría:** Web
- **Dificultad:** ★★★★☆
- **Autor:** [ineesdv](linkedin.com/in/ineesdv/)

### Descripción
¡Se acabaron las notas cutres! Flaggy ha implementado un cuaderno interactivo para que todos los universitarios puedan tomar notas rápidamente.

¡Hasta puedes añadirle imágenes en alta calidad a tus notas!   
Nota: el objetivo de este reto es explotar una vulnerabilidad web para leer el contenido de flag.txt

            
<br>

### Archivos e instrucciones
Conexión por HTTP al puerto ``5000``  
**Lanzar contenedor:** se incluyen los ficheros necesarios en /challenge. Ejecutando ./run.sh buildeará y deployeará el contenedor, exponiendo el puerto 5000.   

### Hints
1. La funcionalidad que más llama la atención es la de renderizar PDFs, que carga tres elementos: título de la nota, su descripción y una imagen. 
2. Qué raro que solamente deje subir SVGs, ¿será por algo?
3. Se utiliza la librería svglib


### Formato de la flag
``CTFUni{}``  


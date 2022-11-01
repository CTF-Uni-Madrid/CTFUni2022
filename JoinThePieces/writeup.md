#  Join the pieces
- **Categoría:** Crypto
- **Dificultad:** ★★☆☆☆
- **Autor:** [isHaacK](https://twitter.com/_ishaack)

### Descripción
¿Podrás juntar todas las piezas y obtener el mensaje oculto?

Nota: debes juntar todas las piezas para construir la flag. Dentro de las llaves, todo el texto debe estar en mayúsculas. Si hay más de una palabra, sepáralas con barras bajas "_".   
Ejemplo de flag: CTFUni{TEXTO_EN_MAYUSCULAS}

### Archivos e instrucciones
piezas.zip

### Hints
1. Cada pieza es un cifrado distinto. Deberás decodificar cada parte para obtener un trozo de la flag que debes ir juntando.
2. ¿De verdad creías que eso es morse? Te hemos engañado...
3. Hay una pieza que gira y gira... muchas veces...

### Flag
``CTFUni{EASY_FUN_CRYPTO}``
<br>

# Writeup
Obtenemos 4 piezas que habrá que resolver por separado.  

### Pieza 1
Obtenemos lo siguiente: `==AIvpnclVnZzVGI1RHIy9GcgsHIvlUblJHcg4UVgMXZjVmcl1GI5Byb0l2YpxWZGBSZUByboNUZoBibllmY`   

Se trata de un base64 del revés.  

Obtenemos: `bien heCho Te Felicito y mereces UN premIo { por tu esfuerzo`  

Cogiendo solamente las mayúsculas: `CTFUni{`


### Pieza 2
Segunda pieza:  
```
aaAaaAaaaAAaaAaaaaaaAaaaAaAaAAAaaAAAaAAaaaaAaaaAaaAaaaaaaaAaaaaaa
aAAaAAaAaAAaAaAaAAaAaAAaAAaAaAAaAaAaAAaAAaAaAAaAaAAaAaAAaAaAAaAaA
```

Se trata de un Bacon cipher con mayúsculas/minúsculas. Al descifrarlo obtenemos:

```
ESTASMUYCERCA
OXXOOXXOXXXXX
```

Cogiendo las letras en las que hay una X: ``EASY``  

 

### Pieza 3
Tercera pieza:  
```
56= 7:?2= 56 EF =2C8@ 42>:?@ 6? 6DE6 C6E@
BF6 [ 96>@D   [ AC6A2C25@ [ >6E:4F=@D2>6?E6
``` 

Se podría haber pasado por un cipher identifier, donde aparecerá que es un **ROT47**.  

```
del final de tu largo camino en este reto
que , hemos   , preparado , meticulosamente
```

Cogiendo las letras en las posiciones de las comas: ``FUN``


### Pieza 4
Esta vez obtenemos un texto que parece morse:
```
--.---.--.----.-.....-....----....---.-..----..-----.-..--..-.-.-.....--..-.---.---..-.....--.--..--....-.-.....---.-..-.-..-.--....---.--.----....--....-.-.--...-.....-.--..---....-.-.....-.-....---.-.---..-.---..-..--..-.----..--.-.....--..-.----..---.-.-..--....----..-..-.....-..-------..-.--..------.-.---.--..--.--..--.-------..----.---------.-
```
  
Sin embargo no lo es. Se trata de binario (los '-' son 1s, y los '.' son 0s), de longitud 7.   

```
no Caiste en la tRampa, Ya Puedes esTar Orgulloso}
```

Cogiendo las mayúsculas de nuevo: ``CRYPTO}``   


### Uniendo las piezas
Juntando todas las piezas como se indica en el enunciado, obtenemos la flag.  

**Flag:** CTFUni{EASY_FUN_CRYPTO}
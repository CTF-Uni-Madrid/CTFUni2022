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

  
### Formato de la flag
``CTFUni{}``  


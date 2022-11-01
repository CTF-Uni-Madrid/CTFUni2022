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
  

### Formato de la flag
``CTFUni{}``  


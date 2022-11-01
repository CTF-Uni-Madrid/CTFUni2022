# Lo barato sale caro
- **Categoría:** Forense
- **Dificultad:** ★★★★☆
- **Autor:** [ElMagoFlags](https://twitter.com/elmagoflags)

### Descripción
Hace un par de días compré un ordenador de segunda mano para poder llevarlo a la universidad. Como buen ingeniero precavido a la par que inseguro saqué un volcado del disco duro **antes** de desinstalar nada por si rompía algo. Sin embargo, al borrar uno de los programas que el vendedor me dejó instalado ¡¡¡empezaron a aparecerme pestañas emergentes diciendo que me habían hackeado!!! ¿Podrías analizar el disco y decirme que está pasando? 


### Archivos e instrucciones
Volcado del disco duro (chall.E01)  
[Link de descarga](https://urjc-my.sharepoint.com/:u:/g/personal/i_martinmi_2019_alumnos_urjc_es/EXYQqODTQxxHvP9hqyDLRQUBgRT-hYtZeZDkW_cnDAJWkw?e=lDqFhL)

### Hints
1. Cuáles de los programas en el equipo no vienen instalados normalmente con Windows? 
2. El programa a analizar se suele usar para comprimir y descomprimir archivos
3. Busca información sobre la desinstalación del programa en cuestión

## Flag
``CTFUni{n3Ver_trUst_w1nd0Ws_Un1nStAl1_PathS}``

<br> 


### Writeup 
Para poder resolver este reto, primeramente necesitamos conocer el contexto del reto.  

Partimos de un volcado del disco el cual está infectado mediante un "Path Uninstall Hijacking", de tal forma que en el momento que se ejecute el desinstalador de el programa en cuestión (en este caso 7z) en vez de ejecutar el desinstalador normal ejecutará un programa del atacante tal y como podemos ver en esta imagen:  

![](https://i.imgur.com/CbYgJP4.png)


#### Pasos para obtener la Flag (FORMA 1): 

1- Cargaremos las evidencias en Autopsy para analizarla

2- Una de las formas de resolver el reto es analizar el disco manualmente en el que encontraremos una archivo en `C:\Windows\System32\system.exe`, ya que este programa es mediante el cual se ha realizado el path uninstall hijacking, y dumpearlo para analizarlo y ver lo siguiente:  

![](https://i.imgur.com/y8iG6pn.png)

Como vemos en esta funcion, se cambia el uninstaller de 7z por otro situado en otro path, en este caso `C:\Program Files\Microsoft Update Health Tools\Logs\uninstall.exe`.

3- Finalmente, si extraemos ese archivo y lo decompilamos, obtendremos la flag en una message box:   

![](https://i.imgur.com/qfnc09M.png)

<br>


####  Pasos para obtener la Flag (FORMA 2): 

1- Dumpearemos las claves de registro de Software para encontrar la clave de registro en cuestión y encontraremos un path para un desinstalador poco común, ya que no está en el directorio del programa:   
  
![](https://i.imgur.com/v27Zaua.png)



2- Nos moveremos al directorio y encontraremos el archivo en cuestión:  

![](https://i.imgur.com/REolLGp.png)

3- Finalmente, como en la forma 1, dumpearemos el archivo y al analizarlo encontraremos la flag:   
  
![](https://i.imgur.com/qfnc09M.png)  

  
**Flag:** ``CTFUni{n3Ver_trUst_w1nd0Ws_Un1nStAl1_PathS}``
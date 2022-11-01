# Martin Hell Yeah
- **Categoría:** Crypto
- **Dificultad:** ★★★★☆
- **Autor:** [isHaacK](https://twitter.com/_ishaack)

### Descripción
Bob: ¿Ya lo tienes?   
Alice: ¡Claro! ¡Y lo mejor de todo es que puedo elegir la clave que quiera!  
Bob: De 2048 bits quieres decir, ¿No?  
Alice: ¿Qué?  
Bob: [...]  

### Archivos e instrucciones
Martin_Hell_Yeah.zip

### Hints
1. El sistema utiliza Diffie-Hellman
2. La clave privada de Alice no es segura y se puede obtener
3. El Secreto compartido para obtener la flag se puede obtener bruteforceando la clave Privada de Alice


### Flag
``CTFUni{m0r3_l1k3_d1ff13_h3ll_N444h!}``  

<br>

# Writeup
Se trata de un sistema Diffie-Hellman. La clave privada elegida por Alice es muy pequeña y se puede sacar con fuerza bruta.  

Una vez obtenida su clave se puede sacar el secreto compartido de Alice y Bob de manera trivial y utilizarlo para descifrar el zip que contiene la flag.
  
### Solver.py
```python
g = 173247436685893593416376928
p = 271046059989500989696377226

gA = 182351711645430656964122520
gB = 60508729390849113619409504


for i in range(1_000_000_000):
	if pow(g, i, p) == gA:
		# La clave privada de Alice es 13371337
		a = i
		break

s = pow(gB, a, p)

password = pow(s, 3)
print(password)
# 429510821326930172105816360926313675131966431026074624878063710041611525184
```

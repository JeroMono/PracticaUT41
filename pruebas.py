LIBRO = True
REVISTA = True
PELICULA = False
primera_coma = ", " if (LIBRO and (REVISTA or PELICULA)) else ""
segunda_coma = ", " if (REVISTA and PELICULA and LIBRO) else ""
texto_recursos = ("(L)ibro" if LIBRO else "") + primera_coma + ("(R)evista" if REVISTA else "") + segunda_coma + ("(P)elícula" if PELICULA else "")

print(texto_recursos)
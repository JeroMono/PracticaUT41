import json
from dataclasses import dataclass, field

@dataclass
class Recurso:
    id: str
    descripcion: str



@dataclass
class Libro(Recurso):
    autor: str
    titulo: str
    editorial: str

    def __hash__(self):
        return hash((self.id, self.autor, self.titulo, self.editorial))

@dataclass
class EjemplarLibro:
    libro: str
    nro_ejemplar: int
    estado_accion: str = ''

@dataclass
class Revista(Recurso):
    nombre: str
    fecha_publicacion: str
    editorial: str
    estado_consulta: bool = False

    def __hash__(self):
        return hash((self.id, self.nombre, self.fecha_publicacion, self.editorial))

@dataclass
class Pelicula(Recurso):
    titulo: str
    actores_principales: tuple
    actores_secundarios: tuple
    fecha_publicacion: str

    def  __hash__(self):
        return hash((self.id, self.titulo, self.fecha_publicacion))

@dataclass
class PeliculaBiblioteca:
    pelicula: str
    estado_local: bool

@dataclass
class PeliculaPrestamo:
    pelicula: str
    estado_prestamo: bool

@dataclass
class Usuario:
    nif: str
    nombre: str
    telefono: str
    direccion: str

@dataclass
class Socio(Usuario):
    nro_socio: str
    ejemplares_prestados: list = field(default_factory=list)
    recursos_en_consulta: any = None
    fecha_solicitud_consulta: any = None
    hora_solicitud_consulta: any = None

@dataclass
class Ocasional(Usuario):
    recuso_en_consulta: any = None
    fecha_solicitud_consulta: any = None
    hora_solicitud_consulta: any = None

@dataclass
class Accion:
    fecha_solicitud: str
    hora_solicitud: str
    nif: str
    id_uso: str
    id_recurso: str

@dataclass
class Consulta(Accion):
    hora_devolucion: any = None

@dataclass
class Prestamo(Accion):
    nro_socio: str
    fecha_max_devolucion: str
    fecha_devuelto: any = None

class Biblioteca:
    def __init__(self):
        self.libros = []
        self.revistas = []
        self.peliculas = []
        self.prestamos = []
        self.socios = []
        self.ocasionales = []
        self.nro_prestamo = 0
        self.nro_id_libro = 0
        self.nro_id_revista = 0
        self.nro_id_pelicula = 0
        self.nro_socio = 0
        self.nro_consulta = 0
        self.ejemplares = {}

    def agregar_ejemplar(self, ejemplar):
        self.ejemplares.append(ejemplar)

    def agregar_socio(self, socio):
        self.socios.append(socio)

    def buscar_socio(self, nif):
        for socio in self.socios:
            if socio.nif == nif:
                return socio
        return None

    def agregar_ocasional(self, ocasional):
        self.ocasionales.append(ocasional)

    def buscar_ocasional(self, nif):
        for ocasional in self.ocasionales:
            if ocasional.nif == nif:
                return ocasional
        return None

    def generar_id_recurso(self, tipo):
        if tipo == "libro":
            self.nro_id_libro += 1
            return "L" + f"{self.nro_id_libro:010d}"
        elif tipo == "revista":
            self.nro_id_revista += 1
            return "R" + f"{self.nro_id_revista:010d}"
        elif tipo == "pelicula":
            self.nro_id_pelicula += 1
            return "P" + f"{self.nro_id_pelicula:010d}"

    def generar_nro_socio(self):
        self.nro_socio += 1
        return f"S{self.nro_socio:010d}"

    def generar_nro_consulta(self):
        self.nro_consulta += 1
        return f"CON-{self.nro_consulta:04d}"

    def generar_nro_prestamo(self):
        self.nro_prestamo += 1
        return f"PREST-{self.nro_prestamo:04d}"

    def guardar_datos(self):
        with open("datos.json", "w", encoding="utf-8") as file:
            data = {
                "libros": [libro.__dict__ for libro in self.libros],
                "revistas": [revista.__dict__ for revista in self.revistas],
                "peliculas": [pelicula.__dict__ for pelicula in self.peliculas],
                "prestamos": [prestamo.__dict__ for prestamo in self.prestamos],
                "socios": [socio.__dict__ for socio in self.socios],
                "ocasionales": [ocasional.__dict__ for ocasional in self.ocasionales],
                "nro_prestamo": self.nro_prestamo,
                "nro_id_libro": self.nro_id_libro,
                "nro_id_revista": self.nro_id_revista,
                "nro_id_pelicula": self.nro_id_pelicula,
                "nro_socio": self.nro_socio,
                "nro_consulta": self.nro_consulta
            }
            json.dump(data, file, indent=4)

    def cargar_datos(self):
        try:
            with open("datos.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                self.libros = [Libro(**libro) for libro in data["libros"]]
                self.revistas = [Revista(**{k: v for k, v in revista.items() if k != 'nro_ejemplares'}) for revista in data["revistas"]]
                self.peliculas = [Pelicula(**pelicula) for pelicula in data["peliculas"]]
                self.prestamos = [Prestamo(**prestamo) for prestamo in data["prestamos"]]
                self.socios = [Socio(**socio) for socio in data["socios"]]
                self.ocasionales = [Ocasional(**ocasional) for ocasional in data["ocasionales"]]
                self.nro_prestamo = data["nro_prestamo"]
                self.nro_id_libro = data["nro_id_libro"]
                self.nro_id_revista = data["nro_id_revista"]
                self.nro_id_pelicula = data["nro_id_pelicula"]
                self.nro_socio = data["nro_socio"]
                self.nro_consulta = data["nro_consulta"]
        except FileNotFoundError:
            print("No se encontró el archivo de datos.")


def mostrar_menu_principal():
    while True:
        print("1. Recursos")
        print("2. Prestamos")
        print("3. Socios")
        print("4. Salir")
        try:
            opcion = input("Seleccione una opción: ")
        except ValueError:
            print("Opción inválida. Intente nuevamente.")
            continue
        except KeyboardInterrupt:
            print("\nCerrando el programa")
            exit()
        if opcion == "1":
            mostrar_menu_recursos()
        elif opcion == "2":
            mostrar_menu_prestamos()
        elif opcion == "3":
            mostrar_menu_socios()
        elif opcion == "4":
            print("\nCerrando el programa")
            break
        else:
            print("Opción inválida")

def mostrar_menu_recursos():
    while True:
        print("1. Añadir")
        print("2. Eliminar")
        print("3. Consultar estado")
        print("4. Regresar al menú principal")
        try:
            opcion = input("Seleccione una opción: ")
        except KeyboardInterrupt:
            print("\nVolviendo al menú principal")
            return
        if opcion == "1":
            mostrar_menu_añadir_recurso()
        elif opcion == "2":
            mostrar_menu_eliminar_recurso()
        elif opcion == "3":
            mostrar_menu_consultar_estado()
        elif opcion == "4":
            print("\nVolviendo al menú principal")
            break
        else:
            print("Opción inválida")

def mostrar_menu_prestamos():
    while True:
        print("1. Prestamo - Consulta")
        print("2. Devolver")
        print("3. Renovar")
        print("4. Regresar al menú principal")
        try:
            opcion = input("Seleccione una opción: ")
        except KeyboardInterrupt:
            print("\nVolviendo al menú principal")
            return
        if opcion == "1":
            mostrar_menu_prestamo_consulta()
        elif opcion == "2":
            mostrar_menu_devolver()
        elif opcion == "3":
            mostrar_menu_renovar()
        elif opcion == "4":
            print("\nVolviendo al menú principal")
            break
        else:
            print("Opción inválida")

def mostrar_menu_socios():
    while True:
        print("1. Añadir - Socio")
        print("2. Eliminar - Socio")
        print("3. Consultar libros en préstamo")
        print("4. Regresar al menú principal")
        try:
            opcion = input("Seleccione una opción: ")
        except KeyboardInterrupt:
            print("\nVolviendo al menú principal")
            return
        if opcion == "1":
            mostrar_menu_añadir_socio()
        elif opcion == "2":
            mostrar_menu_eliminar_socio()
        elif opcion == "3":
            mostrar_menu_consultar_libros_en_prestamo()
        elif opcion == "4":
            print("\nVolviendo al menú principal")
            break
        else:
            print("Opción inválida")

def mostrar_menu_añadir_recurso():
    while True:
        print("1. Libro")
        print("2. Revista")
        print("3. Película")
        print("4. Regresar al menú de recursos")
        try:
            opcion = input("Seleccione el tipo de recurso a añadir: ")
        except KeyboardInterrupt:
            print("\nVolviendo al menú de recursos")
            return
        if opcion == "1":
            configurar_libro()
        elif opcion == "2":
            configurar_revista()
        elif opcion == "3":
            configurar_pelicula()
        elif opcion == "4":
            print("\nVolviendo al menú de recursos")
            break
        else:
            print("Opción inválida")


def mostrar_menu_eliminar_recurso():
    pass

def mostrar_menu_consultar_estado():
    pass

def mostrar_menu_prestamo_consulta():
    while True:
        try:
            eleccion = input("Realizar un (P)restamo o (C)onsulta:").upper()
        except KeyboardInterrupt:
            print("\nVolviendo al menú de recursos")
            return
        if eleccion in ["P", "C"]:
            break
        else:
            print("Opción inválida. Debe ser P o C")
            continue
    if eleccion == "P":
        while True:
            try:
                nif = input("Introduce el NIF del socio: ")
                if len(nif) != 9:
                    raise ValueError
            except ValueError:
                print("El NIF debe tener 9 caracteres.")
                continue
            except KeyboardInterrupt:
                print("\nVolviendo al menú de recursos")
                return
            socio = biblioteca.buscar_socio(nif)
            if socio:
                print(f"El socio {socio.nombre} tiene {len(socio.ejemplares_prestados)} ejemplares prestados.")
                if len(socio.ejemplares_prestados) >= 3:
                    print("El socio no puede tener más de 3 ejemplares prestados.")
                    break
                else:
                    while True:
                        try:
                            eleccion_tipo = input("Introduce el ID del recurso a prestar: ").upper()
                        except KeyboardInterrupt:
                            print("\nVolviendo al menú de recursos")
                            return
                        # // TODO


                        # -->--->-->-->-->-->-->
                        # -->--->-->-->-->-->-->
                        # -->--->-->-->-->-->-->
                        pass
            else:
                print("El socio no existe.")
                while True:
                    try:
                        opcion = input("¿Deseas volver a ingresar el NIF? (S/N): ").upper()
                    except KeyboardInterrupt:
                        print("\nVolviendo al menú de recursos")
                        return
                    if opcion == "S":
                        break
                    elif opcion == "N":
                        print("Volviendo al menú de recursos")
                        return
                    else:
                        print("Opción inválida")
                        continue
    elif eleccion == "C":
        while True:
            try:
                nif = input("Introduce el NIF de la persona: ")
            except KeyboardInterrupt:
                print("\nVolviendo al menú de recursos")
                return
            if comprobar_dni(nif):
                break
            else:
                print("El NIF, NIE introducido no es válido.")
                continue
        usuario = biblioteca.buscar_socio(nif)
        if usuario:
            print("La persona es un socio.")
            if usuario.recursos_en_consulta:
                print(f"El usuario {usuario.nombre} ya tiene un recurso en consulta.")
                return
        else:
            usuario = biblioteca.buscar_ocasional(nif)
            if usuario:
                print("La persona es un usuario ocasional.")
                if usuario.recuso_en_consulta:
                    print(f"El usuario ocasional {usuario.nombre} ya tiene un recurso en consulta.")
                    return
            else:
                print("La persona no está registrada en la biblioteca.")
                print("Registrando nuevo usuario ocasional.")
                while True:
                    try:
                        nombre = input("Introduce el nombre del usuario: ")
                    except KeyboardInterrupt:
                        print("\nVolviendo al menú de recursos")
                        return
                    if nombre:
                        break
                    else:
                        print("El nombre no puede estar vacío.")
                        continue
                
                while True:
                    try:
                        telefono = input("Introduce el teléfono del usuario: ")
                        if not telefono.isdigit():
                            raise ValueError
                    except ValueError:
                        print("El teléfono debe ser un número.")
                        continue
                    except KeyboardInterrupt:
                        print("\nVolviendo al menú de recursos")
                        return
                    break
                
                while True:
                    try:
                        direccion = input("Introduce la dirección del usuario: ")
                    except KeyboardInterrupt:
                        print("\nVolviendo al menú de recursos")
                        return
                    if direccion:
                        break
                    else:
                        print("La dirección no puede estar vacía.")
                        continue

                usuario = Ocasional(nif, nombre, telefono, direccion)
                biblioteca.agregar_ocasional(usuario)
                print(f"El usuario ocasional {nombre} ha sido registrado.")
                biblioteca.guardar_datos()
        while True:
            recurso_consulta = encontrar_recurso()
            if recurso_consulta:
                pass

            


            
                
                    





                           

def mostrar_menu_devolver():
    pass

def mostrar_menu_renovar():
    pass

def mostrar_menu_añadir_socio():
    while True:
        try:
            nif = input("Introduce el NIF/NIE del socio: ")
        except KeyboardInterrupt:
            print("\nVolviendo al menú de Usuarios")
            return
        if not comprobar_dni(nif):
            print("El NIF, NIE introducido no es válido.")
            continue
        socio = biblioteca.buscar_socio(nif)
        if socio:
            print(f"El socio {socio.nombre} ya existe.")
            while True:
                opcion = input("¿Deseas cancelar el registro? (S/N): ").upper()
                if opcion == "S":
                    print("Registro cancelado.")
                    return
                elif opcion == "N":
                    print("Volviendo a intentar el registro.")
                    break
            continue
        else:
            print(f"Registrando nuevo socio con NIF {nif}.")
            break

    while True:
        try:
            nombre = input("Introduce el nombre del socio: ")
        except KeyboardInterrupt:
            print("\nVolviendo al menú de Usuarios")
            return
        if nombre:
            break
        else:
            print("El nombre no puede estar vacío.")
            continue
    
    while True:
        try:
            telefono = input("Introduce el teléfono del socio: ")
            if not telefono.isdigit():
                raise ValueError
        except ValueError:
            print("El teléfono debe ser un número.")
            continue
        except KeyboardInterrupt:
            print("\nVolviendo al menú de Usuarios")
            return
        break

    while True:
        try:
            direccion = input("Introduce la dirección del socio: ")
        except KeyboardInterrupt:
            print("\nVolviendo al menú de Usuarios")
            return
        if direccion:
            break
        else:
            print("La dirección no puede estar vacía.")
            continue

    nro_socio = biblioteca.generar_nro_socio()
    nuevo_socio = Socio(nro_socio, nif, nombre, telefono, direccion)
    biblioteca.agregar_socio(nuevo_socio)
    print(f"El socio {nombre} ha sido registrado con el número de socio {nro_socio}.")
    biblioteca.guardar_datos()
    
            


def mostrar_menu_eliminar_socio():
    pass

def mostrar_menu_consultar_libros_en_prestamo():
    pass

def configurar_libro():
    try:
        titulo = input("Introduce el título del libro: ")
    except KeyboardInterrupt:
        print("\nVolviendo al menú de recursos")
        return
    try:
        autor = input("Introduce el autor del libro: ")
    except KeyboardInterrupt:
        print("\nVolviendo al menú de recursos")
        return
    try:
        editorial = input("Introduce la editorial del libro: ")
    except KeyboardInterrupt:
        print("\nVolviendo al menú de recursos")
        return
    libro = buscar_libro(titulo, autor, editorial)
    if libro:
        while True:
            print(f"El libro '{titulo}' de {autor} ya existe en la biblioteca.")
            try:
                opcion = input("Elija una opción: \n1. Añadir ejemplares\n2. Volver\n")
            except KeyboardInterrupt:
                print("\nVolviendo al menú de recursos")
                return
            if opcion == "1":
                while True:
                    try:
                        ejemplares = int(input("¿Cuántos ejemplares desea añadir? "))
                        if ejemplares <= 0:
                            raise ValueError
                    except ValueError:
                        print("Entrada inválida. Debe ser un número entero mayor que 0.")
                        continue
                    except KeyboardInterrupt:
                        print("\nVolviendo al menú de recursos")
                    libro.nro_ejemplares += ejemplares
                    print(f"Se han añadido {ejemplares} ejemplares del libro '{titulo}'.")
                    break
            elif opcion == "2":
                print("\nVolviendo al menú de recursos")
                break
            else:
                print("Opción inválida")
    else:
        while True:
            try:
                ejemplares = int(input("¿Cuántos ejemplares desea añadir? "))
                if ejemplares <= 0:
                    raise ValueError
            except ValueError:
                print("Entrada inválida. Debe ser un número entero mayor que 0.")
                continue
            except KeyboardInterrupt:
                print("\nVolviendo al menú de recursos")
            break
        id_libro = biblioteca.generar_id_recurso("libro")
        libro = Libro(id_libro, "Descripción del libro", autor, titulo, editorial)
        ejemplares[libro]= ejemplares
        biblioteca.libros.append(libro)
        print(f"Se ha añadido el libro '{titulo}' de {autor} a la biblioteca.")
        biblioteca.guardar_datos()
        print(f"Se han añadido {ejemplares[libro]} ejemplares del libro '{titulo}'.")

def configurar_revista():
    try:
        nombre = input("Introduce el nombre de la revista: ")
    except KeyboardInterrupt:
        print("\nVolviendo al menú de recursos")
        return
    try:
        fecha_publicacion = input("Introduce la fecha de publicación de la revista: ")
    except KeyboardInterrupt:
        print("\nVolviendo al menú de recursos")
        return
    try:
        editorial = input("Introduce la editorial de la revista: ")
    except KeyboardInterrupt:
        print("\nVolviendo al menú de recursos")
        return
    revista = buscar_revista(nombre, fecha_publicacion, editorial)
    if revista:
        print(f"La revista '{nombre}' ya existe en la biblioteca.")
        return
    else:
        id_revista = biblioteca.generar_id_recurso("revista")
        revista = Revista(id_revista, "Descripción de la revista", nombre, fecha_publicacion, editorial)
        biblioteca.revistas.append(revista)
        print(f"Se ha añadido la revista '{nombre}' con fecha {fecha_publicacion} a la biblioteca.")
        biblioteca.guardar_datos()

def configurar_pelicula():
    try:
        titulo = input("Introduce el título de la película: ")
    except KeyboardInterrupt:
        print("\nVolviendo al menú de recursos")
        return
    try:
        actores_principales = input("Introduce los actores principales (separados por comas): ").split(",")
    except KeyboardInterrupt:
        print("\nVolviendo al menú de recursos")
        return
    try:
        actores_secundarios = input("Introduce los actores secundarios (separados por comas): ").split(",")
    except KeyboardInterrupt:
        print("\nVolviendo al menú de recursos")
        return
    try:
        fecha_publicacion = input("Introduce la fecha de publicación de la película: ")
    except KeyboardInterrupt:
        print("\nVolviendo al menú de recursos")
        return
    pelicula = buscar_pelicula(titulo, fecha_publicacion)
    if pelicula:
        while True:
            print(f"La película '{titulo}' ya existe en la biblioteca.")
            try:
                opcion = input("Elija una opción: \n1. Añadir ejemplares\n2. Volver\n")
            except KeyboardInterrupt:
                print("\nVolviendo al menú de recursos")
                return
            if opcion == "1":
                while True:
                    try:
                        ejemplares = int(input("¿Cuántos ejemplares desea añadir?: "))
                        if ejemplares <= 0:
                            raise ValueError
                    except ValueError:
                        print("Entrada inválida. Debe ser un número entero mayor que 0.")
                        continue
                    except KeyboardInterrupt:
                        print("\nVolviendo al menú de recursos")
                        return
                    if pelicula.nro_ejemplares + ejemplares > 2:
                        print(f"El número total de ejemplares de la película '{titulo}' no puede superar 2.")
                        continue
                    pelicula.nro_ejemplares += ejemplares
                    print(f"Se han añadido {ejemplares} ejemplares de la película '{titulo}'.")
                    break
            elif opcion == "2":
                print("\nVolviendo al menú de recursos")
                break
            else:
                print("Opción inválida")
    else:
        while True:
            try:
                ejemplares = int(input("¿Cuántos ejemplares desea añadir? "))
                if ejemplares <= 0 or ejemplares > 2:
                    raise ValueError
            except ValueError:
                print("Entrada inválida. Debe ser un número entero entre 0 y 2.")
                continue
            except KeyboardInterrupt:
                print("\nVolviendo al menú de recursos")
            break
        id_pelicula = biblioteca.generar_id_recurso("pelicula")
        pelicula = Pelicula(id_pelicula, "Descripción de la película", ejemplares, titulo, actores_principales, actores_secundarios, fecha_publicacion, True)
        biblioteca.peliculas.append(pelicula)
        print(f"Se ha añadido la película '{titulo}' a la biblioteca.")
        biblioteca.guardar_datos() 

def encontrar_recurso():
    while True:
        try:
            tipo = input("Introduce el tipo de recurso (libro/revista/pelicula): ").lower()
        except KeyboardInterrupt:
            print("\nVolviendo al menú de recursos")
            return
        if tipo in ["libro", "revista", "pelicula"]:
            break
        else:
            print("Opción inválida. Debe ser libro, revista o pelicula.")
            continue
    if tipo == "libro":
        filtro = []
        while True:
            try:
                titulo = input("Introduce el título del libro: ")
            except KeyboardInterrupt:
                print("\nVolviendo al menú de recursos")
                return
            else:
                if titulo:
                    break
                else:
                    print("El título no puede estar vacío.")
                    continue
        for libro in biblioteca.libros:
            if isinstance(libro, Libro) and libro.titulo == titulo:
                filtro.append(libro)
        if filtro:
            if len(filtro) == 1:
                print(f"Solo hay un título llamado '{titulo}' en la biblioteca.")
                return filtro[0]
            else:
                print(f"Existen varios libros con el título '{titulo}' en la biblioteca.")
                for libro in filtro:
                    print(f"ID: {libro.id}, Autor: {libro.autor}, Editorial: {libro.editorial}")
        else:
            print(f"No se encontró ningún libro con el título '{titulo}'.")
            return None
        while True:
            try:
                autor = input("Introduce el autor del libro: ")
            except KeyboardInterrupt:
                print("\nVolviendo al menú de recursos")
                return
            else:
                if autor:
                    break
                else:
                    print("El autor no puede estar vacío.")
                    continue
        for libro in filtro:
            if libro.autor != autor:
                filtro.remove(libro)
        if filtro:
            if len(filtro) == 1:
                print(f"El libro '{titulo}' de {autor} existe en la biblioteca.")
                return filtro[0]
            else:
                print(f"El libro '{titulo}' de {autor} tiene {len(filtro)} editoriales en la biblioteca.")
                for libro in filtro:
                    print(f"Libro: {titulo}, Editorial: {libro.editorial}")
        else:
            print(f"No se encontró ningún libro de {autor} con el título '{titulo}'.")
            return None
        while True:
            try:
                editorial = input("Introduce la editorial del libro: ")
            except KeyboardInterrupt:
                print("\nVolviendo al menú de recursos")
                return
            else:
                if editorial:
                    break
                else:
                    print("La editorial no puede estar vacía.")
                    continue
        for libro in filtro:
            if libro.editorial == editorial:
                return libro
        print(f"No se encontró ningún libro de {autor} con el título '{titulo}' y editorial '{editorial}'.")
        return None
    elif tipo == "revista":
        while True:
            try:
                nombre = input("Introduce el nombre de la revista: ")
            except KeyboardInterrupt:
                print("\nVolviendo al menú de recursos")
                return
            else:
                if nombre:
                    break
                else:
                    print("El nombre no puede estar vacío.")
                    continue
        filtro = []
        for revista in biblioteca.revistas:
            if isinstance(revista, Revista) and revista.nombre == nombre:
                filtro.append(revista)

        if filtro:
            if len(filtro) == 1:
                print(f"Solo hay una revista llamada '{nombre}' en la biblioteca.")
                return filtro[0]
            else:
                print(f"Existen varias revistas con el nombre '{nombre}' en la biblioteca.")
                for revista in filtro:
                    print(f"ID: {revista.id}, Fecha de publicación: {revista.fecha_publicacion}, Editorial: {revista.editorial}")

        else:
            print(f"No se encontró ninguna revista con el nombre '{nombre}'.")
            return None
        
        while True:
            try:
                editorial = input("Introduce la editorial de la revista: ")
            except KeyboardInterrupt:
                print("\nVolviendo al menú de recursos")
                return
            else:
                if editorial:
                    break
                else:
                    print("La editorial no puede estar vacía.")
                    continue
        for revista in filtro:
            if revista.editorial != editorial:
                filtro.remove(revista)
        if filtro:
            if len(filtro) == 1:
                print(f"Solo hay una revista llamada '{nombre}' de {editorial} en la biblioteca.")
                return filtro[0]
            else:
                print(f"Existen varias revistas con el nombre '{nombre}' y editorial '{editorial}' en la biblioteca.")
                for revista in filtro:
                    print(f"Revista: {revista.nombre}, Fecha de publicación: {revista.fecha_publicacion}")
        else:
            print(f"No se encontró ninguna revista con el nombre '{nombre}' y editorial '{editorial}'.")

        while True:
            fecha_publicacion = configurar_fecha_publicacion()
            if fecha_publicacion:
                break
            else:
                print("Cancelando búsqueda de revista.")
                return None
        for revista in filtro:
            if revista.fecha_publicacion == fecha_publicacion:
                return revista
        print(f"No se encontró ninguna revista con el nombre '{nombre}', editorial '{editorial}' y fecha de publicación '{fecha_publicacion}'.")
        return None
    elif tipo == "pelicula":
        while True:
            try:
                titulo = input("Introduce el título de la película: ")
            except KeyboardInterrupt:
                print("\nVolviendo al menú de recursos")
                return
            else:
                if titulo:
                    break
                else:
                    print("El título no puede estar vacío.")
                    continue
        filtro = []
        for pelicula in biblioteca.peliculas:
            if isinstance(pelicula, Pelicula) and pelicula.titulo == titulo:
                filtro.append(pelicula)
        if filtro:
            if len(filtro) == 1:
                print(f"Solo hay una película llamada '{titulo}' en la biblioteca.")
                return filtro[0]
            else:
                print(f"Existen varias películas con el título '{titulo}' en la biblioteca.")
                for pelicula in filtro:
                    print(f"ID: {pelicula.id}, Fecha de publicación: {pelicula.fecha_publicacion}")
        else:
            print(f"No se encontró ninguna película con el título '{titulo}'.")
            return None
        while True:
            try:
                fecha_publicacion = input("Introduce la fecha de publicación de la película: ")
            except KeyboardInterrupt:
                print("\nVolviendo al menú de recursos")
                return
            else:
                if fecha_publicacion:
                    break
                else:
                    print("La fecha de publicación no puede estar vacía.")
                    continue
        for pelicula in filtro:
            if pelicula.fecha_publicacion != fecha_publicacion:
                filtro.remove(pelicula)
        if filtro:
            print(f"Encontrada una película llamada '{titulo}' con fecha de publicación {fecha_publicacion} en la biblioteca.")
        else:
            print(f"No se encontró ninguna película con el título '{titulo}' y fecha de publicación {fecha_publicacion}.")
        return None
        
            


def buscar_libro(titulo:str, autor:str, editorial:str) -> Recurso:
    for libro in biblioteca.libros:
        if isinstance(libro, Libro):
            if libro.titulo == titulo and libro.autor == autor and libro.editorial == editorial:
                return libro
    return None

def buscar_revista(nombre:str, fecha_publicacion:str, editorial:str) -> Recurso:
    for revista in biblioteca.revistas:
        if isinstance(revista, Revista):
            if revista.nombre == nombre and revista.fecha_publicacion == fecha_publicacion and revista.editorial == editorial:
                return revista
    return None

def buscar_pelicula(titulo:str, fecha_publicacion:str) -> Recurso:
    for pelicula in biblioteca.peliculas:
        if isinstance(pelicula, Pelicula):
            if pelicula.titulo == titulo and pelicula.fecha_publicacion == fecha_publicacion:
                return pelicula
    return None

def configurar_fecha_publicacion() -> str:
    """Pide una fecha(mes/año) y la devuelve en formato AAAA-MM"""
    while True:
        try:
            fecha = input("Introduce la fecha de publicación (mes/año): ")
            fecha = fecha.split("/")
        except KeyboardInterrupt:
            print("\nVolviendo al menú de recursos")
            return
        if len(fecha) != 2:
            print("Formato inválido. Debe ser mes/año.")
            continue
        else:
            try:
                mes = int(fecha[0])
                año = int(fecha[1])
                if mes < 1 or mes > 12 or año  < 1900 or año > 2025:
                    raise ValueError
            except ValueError:
                print("Entrada inválida. Debe ser un número entero entre 1 y 12 para el mes y mayor a 1900 para el año.")
                continue
            except KeyboardInterrupt:
                print("\nVolviendo al menú de recursos")
                return
            break


def comprobar_dni(dni:str) -> tuple[bool, bool]:
    """ Comprueba si un DNI, NIE válido"""
    LETRAS_NIF = "TRWAGMYFPDXBNJZSQVHLCKE"
    LETRAS_NIE = "XYZ"
    if len(dni) == 9 and dni[-1].isalpha():
        # Validación de NIE
        if((dni[0].upper() in LETRAS_NIE) and dni[1:-1].isdigit()):
            combinado = int(str(LETRAS_NIE.index(dni[0])) + dni[1:-1])
            if (dni[-1] == LETRAS_NIF[(combinado%23)]):
                return True
        # Validación de NIF
        elif (dni[:-1].isdigit()):
            if dni[-1] == LETRAS_NIF[(int(dni[:-1]) % 23)]:
                return True
        else:
            return False
    return False


if __name__ == "__main__":
    biblioteca = Biblioteca()
    # biblioteca.cargar_datos()
    biblioteca = Biblioteca()
    libro1= Libro("1", "Libro de prueba", "Autor", "Título", "Editorial")
    pelicula1 = Pelicula("1", "Descripción de la película", "Título", ("Actor1", "Actor2"), ("Secundario1"), "2023-10-01")
    revista1 = Revista("1", "Descripción de la revista", "Nombre", "2023-10-01", "Editorial")
    biblioteca.ejemplares[libro1] = [EjemplarLibro(libro1.id, 1, False), EjemplarLibro(libro1.id, 2, False)]
    biblioteca.ejemplares[pelicula1] = [PeliculaBiblioteca(pelicula1.id, False), PeliculaPrestamo(pelicula1.id, False)]
    biblioteca.ejemplares[revista1] = revista1
    biblioteca.libros.append(libro1)
    biblioteca.guardar_datos()
    print(biblioteca.libros)
    print(biblioteca.revistas)
    print(biblioteca.peliculas)
    print(biblioteca.socios)
    print(biblioteca.ocasionales)
    print(biblioteca.ejemplares)
    mostrar_menu_principal()

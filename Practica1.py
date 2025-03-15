import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta

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
        return hash((self.id, self.descripcion, self.autor, self.titulo, self.editorial))
    
    def __repr__(self):
        return f"Libro(titulo={self.titulo}, autor={self.autor}, editorial={self.editorial}, id={self.id})"

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

    def __hash__(self):
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

    def __hash__(self):
        return hash((self.nif, self.nombre, self.telefono, self.direccion, self.nro_socio))

@dataclass
class Ocasional(Usuario):
    recurso_en_consulta: any = None
    fecha_solicitud_consulta: any = None
    hora_solicitud_consulta: any = None

    def __hash__(self):
        return hash((self.nif, self.nombre, self.telefono, self.direccion))

@dataclass
class Accion:
    nif: str
    id_uso: str
    id_recurso: str
    fecha_solicitud: str
    hora_solicitud: str

@dataclass
class Consulta(Accion):
    hora_devolucion: any = None

    def __hash__(self):
        return hash((self.nif, self.id_uso, self.id_recurso, self.fecha_solicitud, self.hora_solicitud))

@dataclass
class Prestamo(Accion):
    nro_socio: str
    fecha_max_devolucion: str
    fecha_devuelto: any = None

    def __hash__(self):
        return hash((self.nif, self.id_uso, self.id_recurso, self.fecha_solicitud, self.hora_solicitud, self.fecha_max_devolucion))

class Biblioteca:
    def __init__(self):
        self.libros = {}
        self.revistas = set()
        self.peliculas = {}
        self.prestamos = []
        self.consultas = {}
        self.socios = {}
        self.ocasionales = {}
        self.nro_prestamo = 0
        self.nro_id_libro = 0
        self.nro_id_revista = 0
        self.nro_id_pelicula = 0
        self.nro_socio = 0
        self.nro_consulta = 0

    def agregar_ejemplar(self, ejemplar):
        self.ejemplares.append(ejemplar)

    def agregar_socio(self, socio):
        self.socios[socio.nif] = socio

    def buscar_socio_nif(self, nif) -> Socio | None:
        return self.socios.get(nif)
    
    def buscar_socio_nro_socio(self, nro_socio) -> Socio | None:
        for socio in self.socios.values():
            if socio.nro_socio == nro_socio:
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
                "libros": [[libro.__dict__, [ejemplar.__dict__ for ejemplar in self.libros[libro]]] for libro in self.libros],
                "revistas": [revista.__dict__ for revista in self.revistas],
                "peliculas": [[pelicula.__dict__, [ejemplar.__dict__ for ejemplar in self.peliculas[pelicula]]] for pelicula in self.peliculas],
                "prestamos": [prestamo.__dict__ for prestamo in self.prestamos],
                "consultas": [[key, value.__dict__] for key, value in self.consultas.items()],
                "socios": [[socio, self.socios[socio].__dict__] for socio in self.socios],
                "ocasionales": [[ocasional,self.ocasionales[ocasional].__dict__] for ocasional in self.ocasionales],
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
                self.libros = {}
                for libro_data in data["libros"]:
                    libro_dict = libro_data[0]
                    libro = Libro(
                        id=libro_dict["id"],
                        descripcion=libro_dict["descripcion"],
                        autor=libro_dict["autor"],
                        titulo=libro_dict["titulo"],
                        editorial=libro_dict["editorial"]
                    )
                    ejemplares = [EjemplarLibro(**ejemplar) for ejemplar in libro_data[1]]
                    self.libros[libro] = ejemplares                
                self.revistas = {Revista(**revista) for revista in data["revistas"]}
                self.peliculas = {Pelicula(**pelicula[0]): [PeliculaBiblioteca(**ejemplar) if 'estado_local' in ejemplar else PeliculaPrestamo(**ejemplar) for ejemplar in pelicula[1]] for pelicula in data["peliculas"]}
                self.prestamos = [Prestamo(**prestamo) for prestamo in data["prestamos"]]
                self.consultas = {consulta[0]: Consulta(**consulta[1]) for consulta in data["consultas"]}
                self.socios = {socio[0]: Socio(**socio[1]) for socio in data["socios"]}
                self.ocasionales = {ocasional[0]: Ocasional(**ocasional[1]) for ocasional in data["ocasionales"]}
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
    recurso_prestamo = encontrar_recurso(LIBRO = True, REVISTA=True, PELICULA = True)
    if isinstance(recurso_prestamo,Revista):
        if comprobar_estado_recurso(recurso_prestamo, True):
            print(f"El libro '{recurso_prestamo.nombre}' está disponible para consulta.")
        else:
            print(f"El libro '{recurso_prestamo.nombre}' no está disponible para consulta.")
    elif isinstance(recurso_prestamo, Libro):
        if comprobar_estado_recurso(recurso_prestamo, True):
            print(f"La revista '{recurso_prestamo.titulo}' está disponible para consulta.")
        else:
            print(f"La revista '{recurso_prestamo.titulo}' no está disponible para consulta.")
        if comprobar_estado_recurso(recurso_prestamo, False):
            print(f"La revista '{recurso_prestamo.titulo}' está disponible para préstamo.")
        else:
            print(f"La revista '{recurso_prestamo.titulo}' no está disponible para préstamo.")
    elif isinstance(recurso_prestamo, Pelicula):
        if comprobar_estado_recurso(recurso_prestamo, True):
            print(f"La película '{recurso_prestamo.titulo}' está disponible para consulta.")
        else:
            print(f"La película '{recurso_prestamo.titulo}' no está disponible para consulta.")
        if comprobar_estado_recurso(recurso_prestamo, False):
            print(f"El recurso '{recurso_prestamo.titulo}' está disponible para préstamo.")
        else:
            print(f"El recurso '{recurso_prestamo.titulo}' no está disponible para préstamo.")

        


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
            socio = biblioteca.buscar_socio_nif(nif)
            if socio:
                print(f"El socio {socio.nombre} tiene {len(socio.ejemplares_prestados)} ejemplares prestados.")
                if len(socio.ejemplares_prestados) >= 3:
                    print("El socio no puede tener más de 3 ejemplares prestados.")
                    return
                else:
                    break
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
        while True:
            recurso_prestamo = encontrar_recurso(LIBRO = True, PELICULA = True)
            if recurso_prestamo:
                break
            else:
                print("Saliendo del préstamo.")
                return
        ejemplar = comprobar_estado_recurso(recurso_prestamo, True)
        if ejemplar:
            ejemplar.estado_accion = "Prestamo"
            id_prestamo = biblioteca.generar_nro_prestamo()
            if isinstance(recurso_prestamo, Libro):
                print(f"El libro '{recurso_prestamo.titulo}' ha sido prestado a {socio.nombre}.")
                recurso_prestamo = (recurso_prestamo.__dict__['titulo'], ejemplar.__dict__['nro_ejemplar'])
            elif isinstance(recurso_prestamo, Pelicula):
                print(f"La película '{recurso_prestamo.titulo}' ha sido prestada a {socio.nombre}.")
                recurso_prestamo = recurso_prestamo.id
            prestamo = Prestamo(socio.nif, id_prestamo, recurso_prestamo, datetime.now().strftime("%d/%m/%Y"), datetime.now().strftime("%H:%M:%S"), socio.nro_socio, (datetime.now() + timedelta(days=7)).strftime("%d/%m/%Y"))
            biblioteca.prestamos.append(prestamo)
            socio.ejemplares_prestados.append(id_prestamo)
            biblioteca.guardar_datos()
            return
        else:
            print("El recurso no está disponible para préstamo.")
            return
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
        usuario = biblioteca.buscar_socio_nif(nif)
        if usuario:
            print("La persona es un socio.")
            if usuario.recursos_en_consulta:
                print(f"El usuario {usuario.nombre} ya tiene un recurso en consulta.")
                return
        else:
            usuario = biblioteca.buscar_ocasional(nif)
            if usuario:
                print("La persona es un usuario ocasional.")
                if usuario.recurso_en_consulta:
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
            recurso_consulta = encontrar_recurso(LIBRO=True, REVISTA=True, PELICULA=True)
            print(f"El recurso '{recurso_consulta}' ha sido registrado para consulta.")
            input("Presiona Enter para continuar...")
            if recurso_consulta:
                ejemplar = comprobar_estado_recurso(recurso_consulta, True)
                print(f"El recurso '{ejemplar}' está disponible para consulta.")
                input("Presiona Enter para continuar...")
                if ejemplar:
                    id_consulta = biblioteca.generar_nro_consulta()

                    if isinstance(ejemplar, EjemplarLibro):
                        ejemplar.estado_accion = "Consulta "
                        print(f"El libro '{recurso_consulta.titulo}' ha sido registrado para consulta.")
                        recurso_consulta = (recurso_consulta.__dict__['titulo'], ejemplar.__dict__['nro_ejemplar'])
                    
                    elif isinstance(ejemplar, Revista):
                        ejemplar.estado_consulta = True
                        print(f"La revista '{ejemplar.nombre}' ha sido registrada para consulta.")
                        recurso_consulta = ejemplar.id
                    
                    elif isinstance(ejemplar, PeliculaBiblioteca):
                        ejemplar.estado_local = True
                        recurso_consulta = recurso_consulta.id
                        print(f"La película '{recurso_consulta.titulo}' ha sido registrada para consulta.")

                    consulta = generar_consulta(usuario.nif, id_consulta, recurso_consulta)
                    biblioteca.consultas[id_consulta] = consulta
                    usuario.recursos_en_consulta = id_consulta
                    usuario.fecha_solicitud_consulta = datetime.now().strftime("%d/%m/%Y")
                    usuario.hora_solicitud_consulta = datetime.now().strftime("%H:%M:%S")

                    biblioteca.guardar_datos()
                    print("Consulta registrada.")
                    return
            else:
                print("Saliendo de la consulta.")
                return


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
        socio = biblioteca.buscar_socio_nif(nif)
        if socio:
            print(f"El socio {socio.nombre} ya existe.")
            while True:
                try:
                    opcion = input("¿Deseas cancelar el registro? (S/N): ").upper()
                except KeyboardInterrupt:
                    opcion = "S"
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
                    for unidad in range(1, ejemplares + 1):
                        biblioteca.ejemplares[libro].append(EjemplarLibro(libro, biblioteca.ejemplares[libro][-1].__dict__['nro_ejemplar'] + 1))
                    print(f"Se han añadido {ejemplares} ejemplares del libro '{titulo}'.")
                    return
            elif opcion == "2":
                print("\nVolviendo al menú de recursos")
                break
            else:
                print("Opción inválida")
    else:
        print("El libro no existe en la biblioteca.")
        while True:
            try:
                descripcion = input("Introduce la descripción del libro: ")
            except KeyboardInterrupt:
                print("\nVolviendo al menú de recursos")
                return
            if descripcion:
                break
            print("La descripción no puede estar vacía.")

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
        libro = Libro(id_libro, descripcion, autor, titulo, editorial)
        biblioteca.ejemplares[libro] = []
        for unidad in range(1, ejemplares + 1):
            biblioteca.ejemplares[libro].append(EjemplarLibro(libro, unidad))
        print(f"Se ha añadido el libro '{titulo}' de {autor} a la biblioteca.")
        biblioteca.guardar_datos()
        print(f"Se han añadido {ejemplares} ejemplares del libro '{titulo}'.")

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
        biblioteca.revistas.add(revista)
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

def encontrar_recurso(LIBRO:bool = False, REVISTA:bool = False, PELICULA:bool = False):
    while True:
        primera_coma = ", " if (LIBRO and (REVISTA or PELICULA)) else ""
        segunda_coma = ", " if (REVISTA and PELICULA and LIBRO) else ""
        texto_recursos = ("(L)ibro" if LIBRO else "") + primera_coma + ("(R)evista" if REVISTA else "") + segunda_coma + ("(P)elícula" if PELICULA else "")
        lista_posibles = []
        if LIBRO:
            lista_posibles.append("libro")
            lista_posibles.append("l")
        if REVISTA:
            lista_posibles.append("revista")
            lista_posibles.append("r")
        if PELICULA:
            lista_posibles.append("pelicula")
            lista_posibles.append("p")
        try:
            tipo = input(f"Introduce el tipo de recurso ({texto_recursos}): ").lower()
        except KeyboardInterrupt:
            print("\nVolviendo al menú de recursos")
            return
        if tipo in lista_posibles:
            if LIBRO and (tipo in ["libro", "l"]):
                tipo = "libro"
                break
            elif REVISTA and (tipo in ["revista", "r"]):
                tipo = "revista"
                break
            elif PELICULA and (tipo in ["pelicula", "p"]):
                tipo = "pelicula"
                break
        else:
            print(f"Opción inválida. Debe ser {texto_recursos}.")
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
                print(filtro[0])
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
    for libro in biblioteca.libros.keys():
        if isinstance(libro, Libro) and libro.titulo == titulo and libro.autor == autor and libro.editorial == editorial:
            return libro
    return False

def buscar_revista(nombre:str, fecha_publicacion:str, editorial:str) -> Recurso:
    for revista in biblioteca.revistas:
        if isinstance(revista, Revista) and revista.nombre == nombre and revista.fecha_publicacion == fecha_publicacion and revista.editorial == editorial:
            return revista
    return False

def buscar_pelicula(titulo:str, fecha_publicacion:str) -> Recurso:
    for pelicula in biblioteca.peliculas.keys():
        if isinstance(pelicula, Pelicula) and pelicula.titulo == titulo and pelicula.fecha_publicacion == fecha_publicacion:
            return pelicula
    return False

def generar_consulta(nif:str, id_uso:str, id_recurso:str) -> Consulta:
    """Genera una consulta a partir del NIF y el ID del recurso"""
    fecha = datetime.now().strftime("%Y-%m-%d")
    hora = datetime.now().strftime("%H:%M")
    return Consulta(nif, id_uso, id_recurso, fecha, hora, None)


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

def comprobar_estado_recurso(recurso:Recurso, consulta:bool = False) -> str:
    if not consulta:
        if isinstance(recurso, Libro):
            ejemplar_disponible = False
            ejemplar_en_consulta = False
            for ejemplar in biblioteca.libros[recurso]:
                if ejemplar.estado_accion == "" and ejemplar_disponible == False:
                    ejemplar_disponible = True
                elif ejemplar.estado_accion == "Consulta":
                    ejemplar_en_consulta = True
                elif ejemplar.estado_accion == "" and (ejemplar_disponible == True or ejemplar_en_consulta == True):
                    return ejemplar
            else:
                return None
        elif isinstance(recurso, Pelicula):
            for ejemplar in biblioteca.peliculas[recurso]:
                if isinstance(ejemplar, PeliculaPrestamo):
                    if ejemplar.estado_prestamo:
                        return None
                    else:
                        return ejemplar
                
    else:
        if isinstance(recurso, Libro):
            for ejemplar in biblioteca.libros[recurso]:
                if ejemplar.estado_accion == "":
                    return ejemplar
            else:
                return None
        elif isinstance(recurso, Revista):
            if recurso.estado_consulta:
                return None
            else:
                return recurso
        elif isinstance(recurso, Pelicula):
            for ejemplar in biblioteca.peliculas[recurso]:
                if isinstance(ejemplar, PeliculaBiblioteca):
                    if ejemplar.estado_local:
                        return None
                    else:
                        return ejemplar
            else:
                return None


def test1():
    libro1 = Libro("L1", "Libro de prueba", "Autor", "LIBRAZO", "Editorial")
    libro2 = Libro("L2", "Libro de prueba", "Autor", "LIBRAZO2", "Editorial")
    libro3 = Libro("L3", "Libro de prueba", "Autor", "LIBRAZO3", "Editorial")
    libro4 = Libro("L4", "Libro de prueba", "Autor", "LIBRAZO", "Santillana")
    pelicula1 = Pelicula("P1", "Descripción de la película", "Título", ("Actor1", "Actor2"), ("Secundario1"), "2023-10-01")
    revista1 = Revista("R1", "Descripción de la revista", "Nombre", "2023-10-01", "Editorial")
    # biblioteca.ejemplares[libro1] = [EjemplarLibro(libro1.id, 1, ''), EjemplarLibro(libro1.id, 2,'')]
    # biblioteca.ejemplares[pelicula1] = [PeliculaBiblioteca(pelicula1.id, False), PeliculaPrestamo(pelicula1.id, False)]
    # biblioteca.ejemplares[revista1] = revista1
    biblioteca.libros[libro1] = [EjemplarLibro(libro1.id, 1, ''), EjemplarLibro(libro1.id, 2,'')]
    biblioteca.libros[libro2] = [EjemplarLibro(libro2.id, 1, ''), EjemplarLibro(libro2.id, 2,'')]
    biblioteca.libros[libro3] = [EjemplarLibro(libro3.id, 1, ''), EjemplarLibro(libro3.id, 2,'')]
    biblioteca.libros[libro4] = [EjemplarLibro(libro4.id, 1, ''), EjemplarLibro(libro4.id, 2,'')]
    biblioteca.peliculas[pelicula1] = [PeliculaBiblioteca(pelicula1.id, False), PeliculaPrestamo(pelicula1.id, False)]
    biblioteca.revistas.add(revista1)
    biblioteca.nro_id_libro = 1
    biblioteca.nro_id_pelicula = 1
    biblioteca.nro_id_revista = 1
    print(f"los libros {libro1} y {libro2} son iguales -> {libro1 == libro2}")
    #biblioteca.libros.append(libro1)
    # print(biblioteca.libros)
    # print(biblioteca.revistas)
    # print(biblioteca.peliculas)
    # print(biblioteca.socios)
    # print(biblioteca.ocasionales)
    # print(biblioteca.ejemplares)
    print()
    # print(biblioteca.ejemplares)
    print()
    # for elemento in biblioteca.ejemplares.keys():
    #     print(elemento)
    #     print(elemento.__class__.__name__)
    #     if elemento.__class__.__name__ == "Libro":
    #         print(elemento.__dict__)
    #         print(biblioteca.ejemplares[elemento][0].__dict__['estado_accion'])

    print("Aumentando el número de ejemplares")
    ultimo_indice = biblioteca.libros[libro1][-1].__dict__['nro_ejemplar']
    print(ultimo_indice)	
    biblioteca.libros[libro1].append(EjemplarLibro(libro1.id, ultimo_indice + 1,''))
    print(biblioteca.libros[libro1])
    ultimo_indice = len(biblioteca.libros[libro1])
    print(ultimo_indice)	
    biblioteca.libros[libro1].append(EjemplarLibro(libro1.id, ultimo_indice + 1,''))
    print(biblioteca.libros[libro1])



    print("buscando libro")
    print(buscar_libro("LIBRAZO", "Autor", "Editorial"))

    print("Buscando revista")
    print(buscar_revista("Nombre", "2023-10-01", "Editorial"))

    print("Buscando película")
    print(buscar_pelicula("Título", "2023-10-01"))

    #print(biblioteca.ejemplares.keys())

    usuario1 = Socio( "43491650F", "Juan Pérez", "123456789", "Calle Falsa 123", "1")
    usuario2 = Socio("87654321B", "Ana García", "987654321", "Calle Verdadera 456","2")
    biblioteca.socios["43491650F"] = usuario1
    biblioteca.socios["87654321B"] = usuario2
    print(biblioteca.socios)

    ocasional1 = Ocasional("23456789C", "Luis López", "234567890", "Calle Real 789")
    ocasional2 = Ocasional("34567890D", "María Fernández", "345678901", "Calle Imaginaria 012")
    biblioteca.ocasionales["23456789C"] = ocasional1
    biblioteca.ocasionales["34567890D"] = ocasional2
    print(biblioteca.ocasionales)
    
    biblioteca.guardar_datos()
    print()
    print(biblioteca.libros)
    print()
    print([ejemplar.__dict__ for ejemplar in biblioteca.libros])


if __name__ == "__main__":
    
    biblioteca = Biblioteca()
    testing = False
    if testing:
        test1()
    else:
        biblioteca = Biblioteca()
        biblioteca.cargar_datos()
        mostrar_menu_principal()

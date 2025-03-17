import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta

@dataclass
class Recurso:
    """Dataclass base para los recursos de la biblioteca. Tiene un ID, y la descripción del recurso."""
    id: str
    descripcion: str

@dataclass
class Libro(Recurso):
    """Dataclass para los libros de la biblioteca. Añade el autor, el título y la editorial del libro."""
    autor: str
    titulo: str
    editorial: str

    def __hash__(self):
        """Hash para poder usar el libro como clave en el diccionario biblioteca.libros"""
        return hash((self.id, self.descripcion, self.autor, self.titulo, self.editorial))
    
    def __repr__(self):
        """Representación del libro para mostrar en la consola"""
        return f"Libro(titulo={self.titulo}, autor={self.autor}, editorial={self.editorial}, id={self.id})"

@dataclass
class EjemplarLibro:
    """Dataclass para los ejemplares de libros. Tiene la referencia al libro, el número de ejemplar y el estado de la acción ("", "Prestamo" o "Consulta")."""
    libro: str
    nro_ejemplar: int
    estado_accion: str = ''
    

@dataclass
class Revista(Recurso):
    """""Dataclass para las revistas de la biblioteca. Añade el nombre, la fecha de publicación y la editorial de la revista. Al no usar ejemplares, se añade el estado de consulta directamente."""
    nombre: str
    fecha_publicacion: str
    editorial: str
    estado_consulta: bool = False

    def __hash__(self):
        """Hash para poder usar la revista como clave en el diccionario biblioteca.revistas"""
        return hash((self.id, self.nombre, self.fecha_publicacion, self.editorial))

@dataclass
class Pelicula(Recurso):
    """Dataclass para las películas de la biblioteca. Añade el título, los actores principales y secundarios, y la fecha de publicación de la película."""
    titulo: str
    actores_principales: tuple
    actores_secundarios: tuple
    fecha_publicacion: str

    def __hash__(self):
        """Hash para poder usar la película como clave en el diccionario biblioteca.peliculas"""
        return hash((self.id, self.titulo, self.fecha_publicacion))

@dataclass
class PeliculaBiblioteca:
    """Dataclass para los ejemplares de películas para uso en la biblioteca. Tiene la referencia a la película y el estado local (False -> Disponible, True -> En consulta)."""
    pelicula: str
    estado_local: bool

@dataclass
class PeliculaPrestamo:
    """Dataclass para los ejemplares de películas para préstamo. Tiene la referencia a la película y el estado del prestamo (False -> Disponible, True -> En préstamo)."""
    pelicula: str
    estado_prestamo: bool

@dataclass
class Usuario:
    """Dataclass base para los usuarios de la biblioteca. Tiene el NIF, el nombre, el teléfono y la dirección del usuario."""
    nif: str
    nombre: str
    telefono: str
    direccion: str

@dataclass
class Socio(Usuario):
    """Dataclass que hereda de Usuario. Añade el número de socio y una lista de ejemplares prestados. También las variables para las consultas"""
    nro_socio: str
    ejemplares_prestados: list = field(default_factory=list)
    recurso_en_consulta: EjemplarLibro | Revista | Pelicula = None
    fecha_solicitud_consulta: str = None
    hora_solicitud_consulta: str = None


    def __hash__(self):
        """Hash para poder usar el socio como clave en el diccionario biblioteca.socios"""
        return hash((self.nif, self.nombre, self.telefono, self.direccion, self.nro_socio))

@dataclass
class Ocasional(Usuario):
    """Dataclass que hereda de Usuario. Permite registrar consultas: su recurso, fecha y hora la última solicitud."""
    recurso_en_consulta: EjemplarLibro | Revista | Pelicula = None
    fecha_solicitud_consulta: str = None
    hora_solicitud_consulta: str = None

    def __hash__(self):
        """Hash para poder usar el ocasional como clave en el diccionario biblioteca.ocasionales"""
        return hash((self.nif, self.nombre, self.telefono, self.direccion))

@dataclass
class Accion:
    """Dataclass base para las acciones de la biblioteca. Tiene el NIF del usuario, el ID de la acción, el ID del recurso, la fecha y la hora de la solicitud."""
    nif: str
    id_uso: str
    id_recurso: str
    fecha_solicitud: str
    hora_solicitud: str

@dataclass
class Consulta(Accion):
    """Dataclass que hereda de Accion. Añade la hora de devolución."""
    hora_devolucion: str = None

    def __hash__(self):
        """Hash para poder usar la consulta como clave en el diccionario biblioteca.consultas"""
        return hash((self.nif, self.id_uso, self.id_recurso, self.fecha_solicitud, self.hora_solicitud))

@dataclass
class Prestamo(Accion):
    """Dataclass que hereda de Accion. Añade el número de socio, la fecha máxima de devolución, la fecha de devolución y las veces que se ha renovado."""
    nro_socio: str
    fecha_max_devolucion: str
    fecha_devuelto: str = None
    renovacion: int = 0

    def __hash__(self):
        """Hash para poder usar el préstamo como clave en el diccionario biblioteca.prestamos"""
        return hash((self.nif, self.id_uso, self.id_recurso, self.fecha_solicitud, self.hora_solicitud, self.fecha_max_devolucion))

class Biblioteca:
    """Clase que representa la biblioteca. Contiene los recursos, los préstamos, las consultas y los socios. También contiene los métodos para agregar, eliminar y buscar recursos, préstamos y socios."""
    def __init__(self):
        self.libros = {}
        self.revistas = set()
        self.peliculas = {}
        self.prestamos = {}
        self.consultas = {}
        self.socios = {}
        self.ocasionales = {}
        self.nro_prestamo = 0
        self.nro_id_libro = 0
        self.nro_id_revista = 0
        self.nro_id_pelicula = 0
        self.nro_socio = 0
        self.nro_consulta = 0

    def agregar_socio(self, socio) -> None:
        """Agrega el socio introducido a la biblioteca."""
        self.socios[socio.nif] = socio

    def eliminar_socio(self, nif) -> None:
        """Elimina un socio de la biblioteca."""
        del self.socios[nif]

    def buscar_socio_nif(self, nif) -> Socio | None:
        """Busca un socio por su NIF. Devuelve el socio si lo encuentra, None si no."""
        return self.socios.get(nif)
    
    def buscar_socio_nro_socio(self, nro_socio) -> Socio | None:
        """Busca un socio por su número de socio. Devuelve el socio si lo encuentra, None si no."""
        for socio in self.socios.values():
            if socio.nro_socio == nro_socio:
                return socio
        return None

    def agregar_ocasional(self, ocasional) -> None:
        """Agrega el usuario ocasional introducido a la biblioteca."""
        self.ocasionales.append(ocasional)

    def buscar_ocasional(self, nif) -> Ocasional | None:
        """Busca un usuario ocasional por su NIF. Devuelve el usuario ocasional si lo encuentra, None si no."""
        return self.ocasionales.get(nif)

    def generar_id_recurso(self, tipo) -> str:
        """Genera un ID para el recurso introducido. El ID es un string que empieza con la letra del tipo de recurso y sigue con un número de 10 dígitos. Aumenta el número de ID cada vez que se llama."""
        if tipo == "libro":
            self.nro_id_libro += 1
            return "L" + f"{self.nro_id_libro:010d}"
        elif tipo == "revista":
            self.nro_id_revista += 1
            return "R" + f"{self.nro_id_revista:010d}"
        elif tipo == "pelicula":
            self.nro_id_pelicula += 1
            return "P" + f"{self.nro_id_pelicula:010d}"

    def generar_nro_socio(self) -> str:
        """Genera un número de socio. El número es un string de 10 dígitos. Aumenta el número de socio cada vez que se llama."""
        self.nro_socio += 1
        return f"S{self.nro_socio:010d}"

    def generar_nro_consulta(self) -> str:
        """Genera un número de consulta. El número es un string de 10 dígitos. Aumenta el número de consulta cada vez que se llama."""
        self.nro_consulta += 1
        return f"CON-{self.nro_consulta:010d}"

    def generar_nro_prestamo(self) -> str:
        """Genera un número de préstamo. El número es un string de 10 dígitos. Aumenta el número de préstamo cada vez que se llama."""
        self.nro_prestamo += 1
        return f"PREST-{self.nro_prestamo:010d}"

    def guardar_datos(self) -> None:
        """Guarda los datos de la biblioteca en un archivo JSON. Los datos guardados son los libros, revistas, películas, préstamos, consultas y socios.
        Así como los últimos números de préstamo, ID de libro, ID de revista, ID de película, número de socio y número de consulta."""
        with open("datos.json", "w", encoding="utf-8") as file:
            data = {
                "libros": [[libro.__dict__, [ejemplar.__dict__ for ejemplar in self.libros[libro]]] for libro in self.libros],
                "revistas": [revista.__dict__ for revista in self.revistas],
                "peliculas": [[pelicula.__dict__, [ejemplar.__dict__ for ejemplar in self.peliculas[pelicula]]] for pelicula in self.peliculas],
                "prestamos": [[key, value.__dict__] for key, value in self.prestamos.items()],
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

    def cargar_datos(self) -> None:
        """Carga los datos de la biblioteca desde un archivo JSON. Los datos cargados son los libros, revistas, películas, préstamos, consultas y socios.
        Así como los últimos números de préstamo, ID de libro, ID de revista, ID de película, número de socio y número de consulta.
        Se carga en la instancia de la clase Biblioteca. Si el archivo no existe, no se cargan los datos. Si el archivo no es un JSON válido, se muestra un mensaje de error."""
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
                self.prestamos = {prestamo[0]: Prestamo(**prestamo[1]) for prestamo in data["prestamos"]}
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
        except json.JSONDecodeError:
            print("Error al cargar los datos del archivo JSON.")


def mostrar_menu_principal() -> None:
    """Muestra el menú principal de la biblioteca. Permite seleccionar entrar en los menú de recursos, préstamos, socios o salir."""
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

def mostrar_menu_recursos() -> None:
    """Muestra el menú de recursos de la biblioteca. Permite seleccionar añadir, eliminar o consultar el estado de un recurso."""
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

def mostrar_menu_prestamos() -> None:
    """Muestra el menú de préstamos de la biblioteca. Permite entrar en el menú de préstamo - consulta, devolver, renovar o regresar al menú principal."""
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

def mostrar_menu_socios() -> None:
    """Muestra el menú de socios de la biblioteca. Permite entrar en el menú de añadir y eliminar Socios o consultar los libros en préstamo de un Socio."""
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

def mostrar_menu_añadir_recurso() -> None:
    """Muestra el menú de añadir recurso de la biblioteca. Permite seleccionar añadir un libro, revista o película."""
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


def mostrar_menu_eliminar_recurso() -> None:
    """Muestra el menú de eliminar recurso de la biblioteca. Permite seleccionar eliminar un libro, revista o película si no está en uso.
    Se pueden eliminar ejemplares de libros y películas, o eliminar un recurso si no tiene ejemplares. Las revistas se eliminan directamente"""
    recurso_seleccionado = encontrar_recurso(LIBRO = True, REVISTA=True, PELICULA = True)
    if not recurso_seleccionado:
        print("No se encontró el recurso.")
        return
    if isinstance(recurso_seleccionado, Libro):
        print(f"El libro tiene {len(biblioteca.libros[recurso_seleccionado])} ejemplares.")
        if not biblioteca.libros[recurso_seleccionado]:
            print("No hay ejemplares disponibles para eliminar.")
            while True:
                try:
                    opcion = input("¿Deseas eliminar el libro? (S/N): ").upper()
                except KeyboardInterrupt:
                    opcion = "N"
                if opcion == "S":
                    biblioteca.libros.pop(recurso_seleccionado)
                    print(f"El libro '{recurso_seleccionado.titulo}' ha sido eliminado.")
                    biblioteca.guardar_datos()
                    presionar_intro()
                    return
                else:
                    print("El libro no ha sido eliminado.")
                    presionar_intro()
                    return
        for ejemplar in biblioteca.libros[recurso_seleccionado]:
            print(f"Ejemplar {ejemplar.nro_ejemplar}: {ejemplar.estado_accion if ejemplar.estado_accion else 'Disponible'}")
        while True:
            try:
                seleccion = input("Seleccione el/los ejemplares a eliminar (separados por comas) o (T)odos: ").upper()
            except KeyboardInterrupt:
                print("\nVolviendo al menú de recursos")
                return
            if seleccion == "T":
                for ejemplar in biblioteca.libros[recurso_seleccionado]:
                    if ejemplar.estado_accion != '':
                        print(f"El ejemplar {ejemplar.nro_ejemplar} no se puede eliminar porque está en uso.")
                        print("No se pueden eliminar todos los ejemplares.")
                        presionar_intro()
                        break
                else:
                    biblioteca.libros[recurso_seleccionado] = []
                    biblioteca.guardar_datos()
                    print(f"Todos los ejemplares del libro '{recurso_seleccionado.titulo}' han sido eliminados.")
                    try:
                        opcion = input("¿Deseas eliminar el libro? (S/N): ").upper()
                    except KeyboardInterrupt:
                        opcion = "N"
                    if opcion == "S":
                        biblioteca.libros.pop(recurso_seleccionado)
                        print(f"El libro '{recurso_seleccionado.titulo}' ha sido eliminado.")
                        biblioteca.guardar_datos()
                        presionar_intro()
                        return
                    else:
                        print("El libro no ha sido eliminado.")
                        presionar_intro()
                        return
            try:
                seleccion = [int(i) for i in seleccion.split(",")]
            except ValueError:
                print("Selección inválida.")
                continue
            except KeyboardInterrupt:
                print("\nVolviendo al menú de recursos")
                return
            
            ejemplares = []
            for ejemplar in seleccion:
                for ejemplar_libro in biblioteca.libros[recurso_seleccionado]:
                    if ejemplar_libro.nro_ejemplar == ejemplar:
                        if ejemplar_libro.estado_accion != '':
                            print(f"El ejemplar {ejemplar} no se puede eliminar porque está en uso.")
                        else:
                            ejemplares.append(ejemplar_libro)
                        break
            if not ejemplares:
                print("No se pueden eliminar los ejemplares seleccionados.")
                presionar_intro()
                continue
            while True:
                print("Ejemplares seleccionados para eliminar:")
                for ejemplar in ejemplares:
                    print(f"Ejemplar {ejemplar.nro_ejemplar}")
                try:
                    opcion = input("¿Deseas eliminar los ejemplares seleccionados? (S/N): ").upper()
                except KeyboardInterrupt:
                    print("\nVolviendo al menú de recursos")
                    return
                if opcion == "S":
                    break
                elif opcion == "N":
                    print("Los ejemplares no han sido eliminados.")
                    return
            for ejemplar in ejemplares:
                for ejemplar_libro in biblioteca.libros[recurso_seleccionado]:
                    if ejemplar_libro.nro_ejemplar == ejemplar.nro_ejemplar:
                        biblioteca.libros[recurso_seleccionado].remove(ejemplar_libro)
                        break
            if not biblioteca.libros[recurso_seleccionado]:
                print(f"Todos los ejemplares del libro '{recurso_seleccionado.titulo}' han sido eliminados.")
                try:
                    opcion = input("¿Deseas eliminar el libro? (S/N): ").upper()
                except KeyboardInterrupt:
                    opcion = "N"
                if opcion == "S":
                    biblioteca.libros.pop(recurso_seleccionado)
                    print(f"El libro '{recurso_seleccionado.titulo}' ha sido eliminado.")
                    biblioteca.guardar_datos()
                    presionar_intro()
                    return
                else:
                    print("El libro no ha sido eliminado.")
                    presionar_intro()
                    return
            else:
                print(f"Los ejemplares seleccionados han sido eliminados.")
                biblioteca.guardar_datos()
                presionar_intro()
                return
    
    elif isinstance(recurso_seleccionado, Revista):
        if recurso_seleccionado.estado_consulta:
            print("No se puede eliminar la revista porque está en consulta.")
            presionar_intro()
            return
        while True:
            try:
                opcion = input("¿Deseas eliminar la revista? (S/N): ").upper()
            except KeyboardInterrupt:
                print("\nVolviendo al menú de recursos")
                return
            if opcion == "S":
                biblioteca.revistas.remove(recurso_seleccionado)
                biblioteca.guardar_datos()
                print(f"La revista '{recurso_seleccionado.nombre}' ha sido eliminada.")
                presionar_intro()
                return
            else:
                print("La revista no ha sido eliminada.")
                return
            
    elif isinstance(recurso_seleccionado, Pelicula):
        print(f"La película tiene {len(biblioteca.peliculas[recurso_seleccionado])} ejemplares.")
        opciones = []
        for ejemplar in biblioteca.peliculas[recurso_seleccionado]:
            if isinstance(ejemplar, PeliculaBiblioteca):
                print(f"Ejemplar Biblioteca{ejemplar.pelicula['titulo']}: {'En uso' if ejemplar.estado_local else 'Disponible'}")
                opciones.append("C")
            elif isinstance(ejemplar, PeliculaPrestamo):
                print(f"Ejemplar Préstamo {ejemplar.pelicula['titulo']}: {'En uso' if ejemplar.estado_prestamo else 'Disponible'}")
                opciones.append("P")
        
        if not opciones:
            print("No hay ejemplares disponibles para eliminar.")
            while True:
                try:
                    opcion = input("¿Deseas eliminar la película? (S/N): ").upper()
                except KeyboardInterrupt:
                    opcion = "N"
                    return
                if opcion == "S":
                    biblioteca.peliculas.pop(recurso_seleccionado)
                    biblioteca.guardar_datos()
                    print(f"La película '{recurso_seleccionado.titulo}' ha sido eliminada.")
                    presionar_intro()
                    return
                elif opcion == "N":
                    print("La película no ha sido eliminada.")
                    presionar_intro()
                    return
                else:
                    print("Opción inválida.")
                    continue
        
        if len (opciones) == 1:
            if opciones[0] == "C":
                texto_opciones = "(C)onsulta"
            elif opciones[0] == "P":
                texto_opciones = "(P)restamo"
        
        else:
            texto_opciones = "(C)onsulta, (P)restamo o (T)odo"
            opciones.append("T")


        while True:
            try:
                seleccion = input(f"Deseas borrar la película {recurso_seleccionado.titulo} de:  {texto_opciones}: ").upper()
            except KeyboardInterrupt:
                print("\nVolviendo al menú de recursos")
                return
            if seleccion in opciones:
                break
            else:
                print("Selección inválida.")
                continue
        if seleccion == "C" and "C" in opciones:
            for ejemplar in biblioteca.peliculas[recurso_seleccionado]:
                if isinstance(ejemplar, PeliculaBiblioteca):
                    biblioteca.peliculas[recurso_seleccionado].remove(ejemplar)
                    print(f"El ejemplar {ejemplar.pelicula} ha sido eliminado.")
                    break
        elif seleccion == "P" and "P" in opciones:
            for ejemplar in biblioteca.peliculas[recurso_seleccionado]:
                if isinstance(ejemplar, PeliculaPrestamo):
                    biblioteca.peliculas[recurso_seleccionado].remove(ejemplar)
                    print(f"El ejemplar {ejemplar.pelicula} ha sido eliminado.")
                    break
        elif seleccion == "T":
            biblioteca.peliculas[recurso_seleccionado] = []
        if not biblioteca.peliculas[recurso_seleccionado]:
            print(f"Todos los ejemplares de la película '{recurso_seleccionado.titulo}' han sido eliminados.")
            while True:
                try:
                    opcion = input("¿Deseas eliminar la película? (S/N): ").upper()
                except KeyboardInterrupt:
                    opcion = "N"
                    return
                if opcion == "S":
                    biblioteca.peliculas.pop(recurso_seleccionado)
                    biblioteca.guardar_datos()
                    print(f"La película '{recurso_seleccionado.titulo}' ha sido eliminada.")
                    presionar_intro()
                    return
                elif opcion == "N":
                    print("La película no ha sido eliminada.")
                    presionar_intro()
                    return
                else:
                    print("Opción inválida.")
                    continue
        else:
            print(f"Los ejemplares seleccionados han sido eliminados.")
            presionar_intro()


def mostrar_menu_consultar_estado() -> None:
    """Muestra el menú de consultar estado de la biblioteca. Permite seleccionar consultar un libro, revista o película y ver su estado."""
    recurso_prestamo = encontrar_recurso(LIBRO = True, REVISTA=True, PELICULA = True)
    if not recurso_prestamo:
        print("No se encontró el recurso.")
        return
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
    presionar_intro()


def mostrar_menu_prestamo_consulta() -> None:
    """Muestra el menú de préstamo - consulta de la biblioteca. Permite seleccionar realizar un préstamo o una consulta."""
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
                    presionar_intro()
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
                presionar_intro()
                return
        ejemplar = comprobar_estado_recurso(recurso_prestamo)
        if ejemplar:
            if isinstance(recurso_prestamo, Libro):
                for recurso in socio.ejemplares_prestados:
                    tipo = biblioteca.prestamos[recurso].id_recurso.get("libro", None)
                    if tipo:
                        libro = Libro(**biblioteca.prestamos[recurso].id_recurso["libro"])
                        if libro == recurso_prestamo:
                            print("El socio ya tiene el libro en préstamo.")
                            presionar_intro()
                            return
                print(f"El libro '{recurso_prestamo.titulo}' ha sido prestado a {socio.nombre}.")
                ejemplar.estado_accion = "Prestamo"
                recurso_prestamo = ejemplar.__dict__
            elif isinstance(recurso_prestamo, Pelicula):
                print(f"La película '{recurso_prestamo.titulo}' ha sido prestada a {socio.nombre}.")
                recurso_prestamo = recurso_prestamo.__dict__
                ejemplar.estado_prestamo = True
                
            id_prestamo = biblioteca.generar_nro_prestamo()
            dia = configurar_fecha_prestamo()
            if not dia:
                print("No se ha podido registrar el préstamo.")
                presionar_intro()
                return
            hora = datetime.now().strftime("%H:%M:%S")
            fecha_max = (datetime.strptime(dia, "%Y-%m-%d") + timedelta(days=7)).strftime("%Y-%m-%d")
            prestamo = Prestamo(socio.nif, id_prestamo, recurso_prestamo, dia, hora, socio.nro_socio, fecha_max)
            biblioteca.prestamos[id_prestamo] = prestamo
            socio.ejemplares_prestados.append(id_prestamo)
            print(f"El préstamo ha sido registrado con el ID {id_prestamo}.")
            biblioteca.guardar_datos()
            presionar_intro()
            return
        else:
            print("El recurso no está disponible para préstamo.")
            presionar_intro()
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
            if usuario.recurso_en_consulta:
                print(f"El usuario {usuario.nombre} ya tiene un recurso en consulta.")
                presionar_intro()
                return
        else:
            usuario = biblioteca.buscar_ocasional(nif)
            if usuario:
                print("La persona es un usuario ocasional.")
                if usuario.recurso_en_consulta:
                    print(f"El usuario ocasional {usuario.nombre} ya tiene un recurso en consulta.")
                    presionar_intro()
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
                presionar_intro()
        while True:
            recurso_consulta = encontrar_recurso(LIBRO=True, REVISTA=True, PELICULA=True)
            if recurso_consulta:
                ejemplar = comprobar_estado_recurso(recurso_consulta, True)
                if ejemplar:
                    id_consulta = biblioteca.generar_nro_consulta()

                    if isinstance(ejemplar, EjemplarLibro):
                        ejemplar.estado_accion = "Consulta"
                        print(f"El libro '{recurso_consulta.titulo}' ha sido registrado para consulta.")
                        recurso_consulta = ejemplar.__dict__
                    
                    elif isinstance(ejemplar, Revista):
                        ejemplar.estado_consulta = True
                        print(f"La revista '{ejemplar.nombre}' ha sido registrada para consulta.")
                        recurso_consulta = ejemplar.__dict__
                    
                    elif isinstance(ejemplar, PeliculaBiblioteca):
                        ejemplar.estado_local = True
                        recurso_consulta = recurso_consulta.__dict__
                        print(f"La película '{ejemplar.__dict__['pelicula']['titulo']}' ha sido registrada para consulta.")

                    fecha = str(configurar_fecha_prestamo())
                    if not fecha:
                        print("No se ha podido registrar la consulta.")
                        presionar_intro()
                        return
                    hora = str(datetime.now().strftime("%H:%M:%S"))
                    consulta = generar_consulta(usuario.nif, id_consulta, recurso_consulta, fecha, hora)
                    biblioteca.consultas[id_consulta] = consulta
                    usuario.recurso_en_consulta = id_consulta
                    usuario.fecha_solicitud_consulta = fecha
                    usuario.hora_solicitud_consulta = hora

                    biblioteca.guardar_datos()
                    print("Consulta registrada.")
                    presionar_intro()
                    return
            else:
                print("Saliendo de la consulta.")
                presionar_intro()
                return


def mostrar_menu_devolver() -> None:
    """Muestra el menú de devolución de la biblioteca. Permite seleccionar devolver un libro, revista o película, tanto prestado como de consulta."""
    while True:
        try:
            nif = input("Introduce el NIF/NIE de la persona: ")
            if comprobar_dni(nif):
                break
        except KeyboardInterrupt:
            print("\nVolviendo al menú de recursos")
            return
        else:
            print("El NIF, NIE introducido no es válido.")
            continue
    usuario = biblioteca.buscar_socio_nif(nif)
    if usuario:
        print("La persona es un socio.")
        if not usuario.ejemplares_prestados and not usuario.recurso_en_consulta:
            print("El socio no tiene ejemplares prestados ni recursos en consulta.")
            return
        while True:
            recurso_numero = 1
            print(f"El socio {usuario.nombre} tiene {len(usuario.ejemplares_prestados)} ejemplares prestados y {(1 if usuario.recurso_en_consulta else 0)} recursos en consulta.")
            for prestamo in usuario.ejemplares_prestados:
                print(f"{recurso_numero}. {prestamo}")
                recurso_numero += 1
            if usuario.recurso_en_consulta:
                print(f"{recurso_numero}. {usuario.recurso_en_consulta}")
                recurso_numero += 1
            print("0. Volver")
            try:
                recurso = input("Seleccione el número del recurso a devolver o (T)odos: ")
            except KeyboardInterrupt:
                print("\nVolviendo al menú de recursos")
                return
            if recurso.upper() == "T":
                for prestamo in usuario.ejemplares_prestados:
                    biblioteca.prestamos[prestamo].fecha_devuelto = datetime.now().strftime("%Y-%m-%d")
                    if isinstance(prestamo, EjemplarLibro):
                        libro = Libro(**prestamo.id_recurso["libro"])
                        ejemplar = EjemplarLibro(**prestamo.id_recurso)
                        biblioteca.libros[libro][biblioteca.libros[libro].index(ejemplar)].estado_accion = ""
                    elif isinstance(prestamo, PeliculaPrestamo):
                        biblioteca.peliculas[prestamo.id_recurso['pelicula']][1].estado_prestamo = False
                    print(f"El recurso {prestamo} ha sido devuelto.")
                if usuario.recurso_en_consulta:
                    biblioteca.consultas[usuario.recurso_en_consulta].hora_devolucion = datetime.now().strftime("%H:%M:%S")
                    if isinstance(usuario.recurso_en_consulta, Revista):
                        biblioteca.revistas[usuario.recurso_en_consulta].estado_consulta = False
                    elif isinstance(usuario.recurso_en_consulta, PeliculaBiblioteca):
                        biblioteca.peliculas[usuario.recurso_en_consulta][0].estado_local = False
                    elif isinstance(usuario.recurso_en_consulta, EjemplarLibro):
                        biblioteca.libros[usuario.recurso_en_consulta.libro][biblioteca.libros[usuario.recurso_en_consulta.libro].index(usuario.recurso_en_consulta)].estado_accion = ""
                    print(f"El recurso {usuario.recurso_en_consulta} ha sido devuelto.")
                    usuario.recurso_en_consulta = None
                usuario.ejemplares_prestados = []
                biblioteca.guardar_datos()
                print("Todos los recursos han sido devueltos.")
                presionar_intro()
                return
            elif recurso == '0':
                print("Volviendo al menú de recursos")
                presionar_intro()
                return
            try:
                recurso = int(recurso) - 1
                if recurso < 0 or recurso >= len(usuario.ejemplares_prestados) + (1 if usuario.recurso_en_consulta else 0):
                    raise ValueError
            except ValueError:
                print("Número inválido.")
                continue
            if recurso < len(usuario.ejemplares_prestados):
                prestamo = usuario.ejemplares_prestados[recurso]
                recurso_prestamo = biblioteca.prestamos[prestamo].id_recurso
                tipo = recurso_prestamo.get("libro", "id")
                if tipo  != "id":
                    libro = Libro(**recurso_prestamo["libro"])
                    ejemplar = EjemplarLibro(**recurso_prestamo)
                    biblioteca.libros[libro][biblioteca.libros[libro].index(ejemplar)].estado_accion = ""
                    biblioteca.prestamos[prestamo].fecha_devuelto = datetime.now().strftime("%Y-%m-%d")
                    usuario.ejemplares_prestados.remove(prestamo)
                    print(f"El recurso {prestamo} ha sido devuelto.")

                else:
                    pelicula = Pelicula(**recurso_prestamo)
                    biblioteca.peliculas[pelicula][1].estado_prestamo = False
                    biblioteca.prestamos[prestamo].fecha_devuelto = datetime.now().strftime("%Y-%m-%d")
                    usuario.ejemplares_prestados.remove(prestamo)
                    print(f"El recurso {prestamo} ha sido devuelto.")
                if biblioteca.prestamos[prestamo].fecha_max_devolucion < biblioteca.prestamos[prestamo].fecha_devuelto:
                    print(f"El recurso {prestamo} ha sido devuelto fuera de plazo.")
                else:
                    print(f"El recurso {prestamo} ha sido devuelto a tiempo.")
                biblioteca.guardar_datos()
                presionar_intro()

            elif recurso < len(usuario.ejemplares_prestados) + (1 if usuario.recurso_en_consulta else 0):
                consulta = usuario.recurso_en_consulta
                recurso_consulta = biblioteca.consultas[consulta]
                tipo = recurso_consulta.id_recurso.get("libro", "id")
                if tipo != "id":
                    libro = Libro(**recurso_consulta.id_recurso["libro"])
                    ejemplar = EjemplarLibro(**recurso_consulta.id_recurso)
                    biblioteca.libros[libro][biblioteca.libros[libro].index(ejemplar)].estado_accion = ""
                
                elif recurso_consulta.id_recurso["id"][0] == "R":
                    for revista in biblioteca.revistas:
                        if revista.id == recurso_consulta.id_recurso:
                            revista.estado_consulta = False
                            break

                else:
                    pelicula = Pelicula(**recurso_consulta.id_recurso)
                    biblioteca.peliculas[pelicula][1].estado_prestamo = False
                
                biblioteca.consultas[consulta].hora_devolucion = datetime.now().strftime("%H:%M:%S")
                
                usuario.recurso_en_consulta = None
                biblioteca.guardar_datos()
                print(f"El recurso {consulta} ha sido devuelto.")
                presionar_intro()
                
            
    else:
        usuario = biblioteca.buscar_ocasional(nif)
        if usuario:
            print("La persona es un usuario ocasional.")
            if not usuario.recurso_en_consulta:
                print("El usuario ocasional no tiene recursos en consulta.")
                return
            eliminar_consulta(usuario)

        else:
            print("La persona no está registrada en la biblioteca. No tiene recursos en su poder.")
            return
            

def mostrar_menu_renovar() -> None:
    """Muestra el menú de renovación de la biblioteca. Permite seleccionar renovar un libro ó película prestada."""
    while True:
        try:
            nif = input("Introduce el NIF/NIE de la persona: ")
            if comprobar_dni(nif):
                break
        except KeyboardInterrupt:
            print("\nVolviendo al menú de recursos")
            return
        else:
            print("El NIF, NIE introducido no es válido.")
            continue
    usuario = biblioteca.buscar_socio_nif(nif)
    if usuario:
        print("La persona es un socio.")
        if not usuario.ejemplares_prestados and not usuario.recurso_en_consulta:
            print("El socio no tiene ejemplares prestados ni recursos en consulta.")
            return
    while True:
        recurso_numero = 1
        print(f"El socio {usuario.nombre} tiene {len(usuario.ejemplares_prestados)} ejemplares prestados.")
        for prestamo in usuario.ejemplares_prestados:
            print(f"{recurso_numero}. {prestamo}")
            recurso_numero += 1
        print("0. Volver")
        try:
            recurso = int(input("Seleccione el número del recurso a renovar: "))
            if recurso < 0 or recurso > len(usuario.ejemplares_prestados):
                raise ValueError
        except ValueError:
            print("Opción inválida.")
            continue
        except KeyboardInterrupt:
            print("\nVolviendo al menú de recursos")
            return
        if recurso == 0:
            print("Volviendo al menú de recursos")
            return
        prestamo = usuario.ejemplares_prestados[recurso - 1]
        if biblioteca.prestamos[prestamo].renovacion >= 3:
            print("El préstamo no se puede renovar más de 3 veces.")
            presionar_intro()
            return
        if biblioteca.prestamos[prestamo].fecha_max_devolucion < datetime.now().strftime("%Y-%m-%d"):
            print("El préstamo no se puede renovar porque está fuera de plazo.")
            presionar_intro()
            return
        fecha_max_devolucion = datetime.strptime(biblioteca.prestamos[prestamo].fecha_max_devolucion, "%Y-%m-%d")
        if fecha_max_devolucion >= (datetime.now() + timedelta(days=3)):
            print("El préstamo no se puede renovar porque está a más de 3 días de la fecha máxima de devolución.")
            print(f"Cuando estés a 3 días de {fecha_max_devolucion}, podrás renovarlo.")
            while True:
                try:
                    opcion_saltar = input("¿Deseas saltar la restricción? (S/N): ").upper()
                except KeyboardInterrupt:
                    opcion_saltar = "N"
                if opcion_saltar == "S":
                    break
                elif opcion_saltar == "N":
                    print("No se puede renovar el préstamo.")
                    presionar_intro()
                    return
                else:
                    print("Opción inválida.")
                    continue

        recurso_prestamo = biblioteca.prestamos[prestamo].id_recurso
        tipo = recurso_prestamo.get("libro", None)
        if tipo:
            biblioteca.prestamos[prestamo].fecha_max_devolucion = (fecha_max_devolucion + timedelta(days=7)).strftime("%Y-%m-%d")
            biblioteca.prestamos[prestamo].renovacion += 1
            print(f"El libro '{recurso_prestamo['libro']['titulo']}' ha sido renovado hasta {biblioteca.prestamos[prestamo].fecha_max_devolucion}.")
            print(f"Renacion numero:{biblioteca.prestamos[prestamo].renovacion}")
            biblioteca.guardar_datos()
            presionar_intro()
            return
        else:
            biblioteca.prestamos[prestamo].fecha_max_devolucion = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
            biblioteca.prestamos[prestamo].renovacion += 1
            print(f"La película '{recurso_prestamo['titulo']}' ha sido renovada hasta {biblioteca.prestamos[prestamo].fecha_max_devolucion}.")
            print(f"Renacion numero:{biblioteca.prestamos[prestamo].renovacion}")
            biblioteca.guardar_datos()
            presionar_intro()
            return
 

def mostrar_menu_añadir_socio() -> None:
    """Muestra el menú de añadir socio. Permite registrar un nuevo socio en la biblioteca."""
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
    nuevo_socio = Socio(nif, nombre, telefono, direccion, nro_socio)
    biblioteca.agregar_socio(nuevo_socio)
    print(f"El socio {nombre} ha sido registrado con el número de socio {nro_socio}.")
    biblioteca.guardar_datos()
    presionar_intro()
    

def mostrar_menu_eliminar_socio() -> None:
    """Muestra el menú de eliminar socio. Permite eliminar un socio de la biblioteca."""
    while True:
        try:
            opcion = input("Buscar socio por NIF o Número de socio (N/S): ").upper()
        except KeyboardInterrupt:
            print("\nVolviendo al menú de Usuarios")
            return
        if opcion in ["N", "NIF","DNI","NIE"]:
            opcion = "NIF"
            break
        elif opcion in ["S", "NUMERO", "NRO_SOCIO","SOCIO"]:
            opcion = "NUMERO"
            break
        else:
            print("Opción inválida.")
            continue

    if opcion == "NIF":
        while True:
            try:
                nif = input("Introduce el NIF/NIE del socio: ")
            except KeyboardInterrupt:
                print("\nVolviendo al menú de Usuarios")
                return
            if comprobar_dni(nif):
                break
            else:
                print("El NIF, NIE introducido no es válido.")
                continue
        socio = biblioteca.buscar_socio_nif(nif)
    elif opcion == "NUMERO":
        while True:
            try:
                nro_socio = input("Introduce el número de socio (numero o S[numero]): ").upper()
                if nro_socio[0] == "S" and nro_socio[1:].isdigit():
                    nro_socio = nro_socio[1:]
                elif nro_socio.isdigit():
                    nro_socio = nro_socio
                nro_socio = int(nro_socio)
                nro_socio = f"S{nro_socio:010d}"
            except TypeError:
                print("El número de socio no es válido.")
            except ValueError:
                print("El número de socio debe ser un número, puede empezar con S.")
                continue
            except KeyboardInterrupt:
                print("\nVolviendo al menú de Usuarios")
                return
            socio = biblioteca.buscar_socio_nro_socio(nro_socio)
            if socio:
                break
            else:
                print("El número de socio no existe.")
                continue
    if socio:
        if socio.ejemplares_prestados or socio.recurso_en_consulta:
            print(f"El socio {socio.nombre} tiene {len(socio.ejemplares_prestados)} ejemplares prestados y {(1 if socio.recurso_en_consulta else 0)} recursos en consulta.")
            print("No se puede eliminar el socio porque tiene ejemplares prestados o recursos en consulta.")
            presionar_intro()
            return
        while True:
            print(f"El socio a eliminar con DNI: {socio.nif} y Número de socio: {socio.nro_socio} es:")
            try:
                opcion = input("¿Deseas eliminar el socio? (S/N): ").upper()
            except KeyboardInterrupt:
                opcion = "N"
            if opcion == "S":
                biblioteca.eliminar_socio(socio.nif)
                biblioteca.guardar_datos()
                print(f"El socio {socio.nombre} ha sido eliminado.")
                presionar_intro()
                return
            elif opcion == "N":
                print("El socio no ha sido eliminado.")
                presionar_intro()
                return
            else:
                print("Opción inválida.")
                continue

def mostrar_menu_consultar_libros_en_prestamo() -> None:
    """Muestra el menú de consultar los recursos en uso de una persona. Permite buscar por NIF o número de socio. En el caso del NIF se busca en los socios y en los usuarios ocasionales."""
    while True:
        try:
            opcion = input("Buscar socio por NIF o Número de socio (N/S): ").upper()
        except KeyboardInterrupt:
            print("\nVolviendo al menú de Usuarios")
            return
        if opcion in ["N", "NIF","DNI","NIE"]:
            opcion = "NIF"
            break
        elif opcion in ["S", "NUMERO", "NRO_SOCIO","SOCIO"]:
            opcion = "NUMERO"
            break
        else:
            print("Opción inválida.")
            continue
    ocasional = None
    if opcion == "NIF":
        while True:
            try:
                nif = input("Introduce el NIF/NIE del socio: ")
            except KeyboardInterrupt:
                print("\nVolviendo al menú de Usuarios")
                return
            if comprobar_dni(nif):
                break
            else:
                print("El NIF, NIE introducido no es válido.")
                continue
        socio = biblioteca.buscar_socio_nif(nif)
        if not socio:
            ocasional = biblioteca.buscar_ocasional(nif)
    elif opcion == "NUMERO":
        while True:
            try:
                nro_socio = input("Introduce el número de socio (numero o S[numero]): ").upper()
                if nro_socio[0] == "S" and nro_socio[1:].isdigit():
                    nro_socio = nro_socio[1:]
                elif nro_socio.isdigit():
                    nro_socio = nro_socio
                nro_socio = int(nro_socio)
                nro_socio = f"S{nro_socio:010d}"
            except TypeError:
                print("El número de socio no es válido.")
            except ValueError:
                print("El número de socio debe ser un número, puede empezar con S.")
                continue
            except KeyboardInterrupt:
                print("\nVolviendo al menú de Usuarios")
                return
            socio = biblioteca.buscar_socio_nro_socio(nro_socio)
            if socio:
                break
            else:
                print("El número de socio no existe.")
                continue
    if socio:
        print(f"El socio {socio.nombre} tiene {len(socio.ejemplares_prestados)} ejemplares prestados y {(1 if socio.recurso_en_consulta else 0)} recursos en consulta.")
        if not socio.ejemplares_prestados:
            print("El socio no tiene ejemplares prestados.")
            presionar_intro()
            return
        else:
            print("Ejemplares tiene en préstamo:")
            for prestamo in socio.ejemplares_prestados:
                recurso = biblioteca.prestamos[prestamo].id_recurso
                tipo = recurso.get("libro", None)
                if tipo:
                    libro = Libro(**recurso["libro"])
                    ejemplar = EjemplarLibro(**recurso)
                    print(f"  Libro: {libro.titulo} ({libro.autor}) -> Ejemplar Nº: {ejemplar.nro_ejemplar}")
                else:
                    pelicula = Pelicula(**recurso)
                    print(f"  Pelicula: {pelicula.titulo} ({pelicula.fecha_publicacion})")
                print(f"\tFecha de préstamo: {biblioteca.prestamos[prestamo].fecha_solicitud}")
                print(f"\tHora de préstamo: {biblioteca.prestamos[prestamo].hora_solicitud}")
                print(f"\tFecha de devolución: {biblioteca.prestamos[prestamo].fecha_max_devolucion}")
        if socio.recurso_en_consulta:
            print("Recurso en consulta:")
            consulta = socio.recurso_en_consulta
            recurso_consulta = biblioteca.consultas[consulta]
            tipo = recurso_consulta.id_recurso.get("libro", None)
            if tipo:
                libro = Libro(**recurso_consulta.id_recurso["libro"])
                ejemplar = EjemplarLibro(**recurso_consulta.id_recurso)
                print(f"  Libro: {libro.titulo} ({libro.autor}) -> Ejemplar Nº: {ejemplar.nro_ejemplar}")
            elif recurso_consulta.id_recurso["id"][0] == "R":
                revista = Revista(**recurso_consulta.id_recurso)
                print(f"  Revista: {revista.nombre} ({revista.fecha_publicacion})")
            else:
                pelicula = Pelicula(**recurso_consulta.id_recurso)
                print(f"  Pelicula: {pelicula.titulo} ({pelicula.fecha_publicacion})")
            print(f"\tFecha de consulta: {biblioteca.consultas[consulta].fecha_solicitud}")
            print(f"\tHora de consulta: {biblioteca.consultas[consulta].hora_solicitud}")
    elif ocasional:
        if ocasional.recurso_en_consulta:
            print(f"El usuario ocasional {ocasional.nombre} tiene un recurso en consulta.")
            consulta = ocasional.recurso_en_consulta
            recurso_consulta = biblioteca.consultas[consulta]
            tipo = recurso_consulta.id_recurso.get("libro", None)
            if tipo:
                libro = Libro(**recurso_consulta.id_recurso["libro"])
                ejemplar = EjemplarLibro(**recurso_consulta.id_recurso)
                print(f"  Libro: {libro.titulo} ({libro.autor}) -> Ejemplar Nº: {ejemplar.nro_ejemplar}")
            elif recurso_consulta.id_recurso["id"][0] == "R":
                revista = Revista(**recurso_consulta.id_recurso)
                print(f"  Revista: {revista.nombre} ({revista.fecha_publicacion})")
            else:
                pelicula = Pelicula(**recurso_consulta.id_recurso)
                print(f"  Pelicula: {pelicula.titulo} ({pelicula.fecha_publicacion})")
            print(f"\tFecha de consulta: {biblioteca.consultas[consulta].fecha_solicitud}")
            print(f"\tHora de consulta: {biblioteca.consultas[consulta].hora_solicitud}")
        else:
            print("El usuario ocasional no tiene recursos en consulta.")
            presionar_intro()
            return
    else:
        print("El socio no existe.")



def configurar_libro() -> None:
    """Configura un libro en la biblioteca. Permite añadir un nuevo libro o ejemplares de un libro existente."""
    while True:
        try:
            titulo = input("Introduce el título del libro: ")
        except KeyboardInterrupt:
            print("\nVolviendo al menú de recursos")
            return
        if titulo:
            break
        print("El título no puede estar vacío.")
        presionar_intro()
    while True:
        try:
            autor = input("Introduce el autor del libro: ")
        except KeyboardInterrupt:
            print("\nVolviendo al menú de recursos")
            return
        if autor:
            break
        print("El autor no puede estar vacío.")
        presionar_intro()
    while True:
        try:
            editorial = input("Introduce la editorial del libro: ")
        except KeyboardInterrupt:
            print("\nVolviendo al menú de recursos")
            return
        if editorial:
            break
        print("La editorial no puede estar vacía.")
        presionar_intro()
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
                        biblioteca.libros[libro].append(EjemplarLibro(libro.__dict__, biblioteca.libros[libro][-1].__dict__['nro_ejemplar'] + 1))
                    print(f"Se han añadido {ejemplares} ejemplares del libro '{titulo}'.")
                    biblioteca.guardar_datos()
                    presionar_intro()
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
            presionar_intro()
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
        biblioteca.libros[libro] = []
        for unidad in range(1, ejemplares + 1):
            biblioteca.libros[libro].append(EjemplarLibro(libro.__dict__, unidad))
        print(f"Se ha añadido el libro '{titulo}' de {autor} a la biblioteca.")
        biblioteca.guardar_datos()
        print(f"Se han añadido {ejemplares} ejemplares del libro '{titulo}'.")
        presionar_intro()

def configurar_revista() -> None:
    """Configura una revista en la biblioteca. Permite configurar los valores para añadir una nueva revista"""
    while True:
        try:
            nombre = input("Introduce el nombre de la revista: ")
        except KeyboardInterrupt:
            print("\nVolviendo al menú de recursos")
            return
        if nombre:
            break
        print("El nombre no puede estar vacío.")
        continue
    fecha_publicacion = configurar_fecha_publicacion_revista()
    if not fecha_publicacion:
        print("Fecha de publicación no válida.")
        return
    while True:
        try:
            editorial = input("Introduce la editorial de la revista: ")
        except KeyboardInterrupt:
            print("\nVolviendo al menú de recursos")
            return
        if editorial:
            break
        print("La editorial no puede estar vacía.")
        presionar_intro()
    revista = buscar_revista(nombre, fecha_publicacion, editorial)
    if revista:
        print(f"La revista '{nombre}' ya existe en la biblioteca.")
        return
    else:
        while True:
            try:
                descripcion = input("Introduce la descripción de la revista: ")
            except KeyboardInterrupt:
                print("\nVolviendo al menú de recursos")
                return
            if descripcion:
                break
            print("La descripción no puede estar vacía.")
            presionar_intro()

        id_revista = biblioteca.generar_id_recurso("revista")
        revista = Revista(id_revista, descripcion, nombre, fecha_publicacion, editorial)
        biblioteca.revistas.add(revista)
        print(f"Se ha añadido la revista '{nombre}' con fecha {fecha_publicacion} a la biblioteca.")
        biblioteca.guardar_datos()
        presionar_intro()

def configurar_pelicula() -> None:
    """Configura una película en la biblioteca. Permite configurar los valores para añadir una nueva película.
    Permite añadir un ejemplar para consulta y otro para préstamo."""
    while True:
        try:
            titulo = input("Introduce el título de la película: ")
        except KeyboardInterrupt:
            print("\nVolviendo al menú de recursos")
            return
        if titulo:
            break
        print("El título no puede estar vacío.")
        presionar_intro()
    
    fecha_publicacion = configurar_fecha_pelicula()
    if not fecha_publicacion:
        print("Fecha de publicación no válida.")
        presionar_intro()
        return
    pelicula = buscar_pelicula(titulo, fecha_publicacion)
    if pelicula:
        
        print(f"La película '{titulo}' de {fecha_publicacion} ya existe en la biblioteca.")
        if len(biblioteca.peliculas[pelicula]) == 2:
            print("La película ya tiene 2 ejemplares.")
            presionar_intro()
            return
        while True:
            try:
                print("1. Añadir ejemplares\n2. Volver")
                opcion = input("Elija una opción: ")
            except KeyboardInterrupt:
                print("\nVolviendo al menú de recursos")
                return
            if opcion not in ["1", "2"]:
                print("Opción inválida.")
                continue
            break
        if opcion == "1":
            while True:
                try:
                    ejemplares = int(input("¿Cuántos ejemplares desea añadir?: "))
                    if ejemplares <= 0:
                        raise ValueError
                except ValueError:
                    print("\nEntrada inválida. Debe ser un número entero mayor que 0.")
                    continue
                except KeyboardInterrupt:
                    print("\nVolviendo al menú de recursos")
                    return
                if len(biblioteca.peliculas[pelicula]) + ejemplares > 2:
                    print(f"El número total de ejemplares de la película '{titulo}' no puede superar 2.")
                    presionar_intro()
                    continue
                if ejemplares == 1:
                    if isinstance(biblioteca.peliculas[pelicula][0], PeliculaBiblioteca):
                        biblioteca.peliculas[pelicula].append(PeliculaPrestamo(pelicula.__dict__, False))
                        print(f"Se ha añadido 1 ejemplar de la película '{titulo}' a la biblioteca para préstamo.")
                    else:
                        biblioteca.peliculas[pelicula].insert(0, PeliculaBiblioteca(pelicula.__dict__, False))
                        print(f"Se ha añadido 1 ejemplar de la película '{titulo}' a la biblioteca para consulta.")
                else:
                    biblioteca.peliculas[pelicula] = [PeliculaBiblioteca(pelicula.__dict__, False), PeliculaPrestamo(pelicula.__dict__, False)]
                    print(f"Se ha añadido 2 ejemplates de la película '{titulo}' a la biblioteca para consulta y préstamo.")
                biblioteca.guardar_datos()
                presionar_intro()
                break
        elif opcion == "2":
            print("\nVolviendo al menú de recursos")
            presionar_intro()
            return
    else:
        while True:
            try:
                actores_principales = input("Introduce los actores principales (separados por comas): ")
            except KeyboardInterrupt:
                print("\nVolviendo al menú de recursos")
                return
            if actores_principales:
                actores_principales = actores_principales.split(",")
                if len(actores_principales) > 2:
                    print("La película no puede tener más de 2 actores principales.")
                    presionar_intro()
                    continue
                break
            confirmacion = input("La película no tiene actores principales. ¿Es correcto? (S/N): ").upper()
            if confirmacion == "S":
                actores_principales = []
                break
            elif confirmacion == "N":
                continue
            else:
                print("Opción inválida, reintentando.")
        while True:
            try:
                actores_secundarios = input("Introduce los actores secundarios (separados por comas): ")
            except KeyboardInterrupt:
                print("\nVolviendo al menú de recursos")
                return
            if actores_secundarios:
                actores_secundarios = actores_secundarios.split(",")
                if len(actores_secundarios) > 2:
                    print("La película no puede tener más de 2 actores secundarios.")
                    presionar_intro()
                    continue
                break
            confirmacion = input("La película no tiene actores secundarios. ¿Es correcto? (S/N): ").upper()
            if confirmacion == "S":
                actores_secundarios = []
                break
            elif confirmacion == "N":
                continue
            else:
                print("Opción inválida, reintentando.")
                
        while True:
            try:
                descripcion = input("Introduce la descripción de la película: ")
            except KeyboardInterrupt:
                print("\nVolviendo al menú de recursos")
                return
            if descripcion:
                break
            print("La descripción no puede estar vacía.")
        while True:
            try:
                ejemplares = int(input("¿Cuántos ejemplares desea añadir? "))
                if ejemplares <= 0 or ejemplares > 2:
                    raise ValueError
            except ValueError:
                print("Entrada inválida. Debe ser un número entero entre 1 y 2.")
                continue
            except KeyboardInterrupt:
                print("\nVolviendo al menú de recursos")
            break
        id_pelicula = biblioteca.generar_id_recurso("pelicula")
        pelicula = Pelicula(id_pelicula, descripcion, titulo, actores_principales, actores_secundarios, fecha_publicacion)
        if ejemplares == 1:
            biblioteca.peliculas[pelicula] = [PeliculaBiblioteca(pelicula.__dict__, False)]
            print(f"Se ha añadido 1 ejemplar de la película '{titulo}' a la biblioteca para consulta.")
        else:
            biblioteca.peliculas[pelicula] = [PeliculaBiblioteca(pelicula.__dict__, False), PeliculaPrestamo(pelicula.__dict__, False)]
            print(f"Se ha añadido 2 ejemplates de la película '{titulo}' a la biblioteca para consulta y préstamo.")
        biblioteca.guardar_datos()
        presionar_intro()

def encontrar_recurso(LIBRO:bool = False, REVISTA:bool = False, PELICULA:bool = False) -> Recurso:
    """Busca un recurso en la biblioteca. Permite buscar por título, autor y editorial para libros, por título y fecha de publicación para las películas y nombre, editorial y fecha para las revistas."""
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
        filtro2 = []
        for libro in filtro:
            if libro.autor == autor:
                filtro2.append(libro)
        del filtro
        if filtro2:
            if len(filtro2) == 1:
                print(f"El libro '{titulo}' de {autor} existe en la biblioteca.")
                return filtro2[0]
            else:
                print(f"El libro '{titulo}' de {autor} tiene {len(filtro2)} editoriales en la biblioteca.")
                for libro in filtro2:
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
        for libro in filtro2:
            if libro.editorial == editorial:
                return libro
        print(f"No se encontró ningún libro de {autor} con el título '{titulo}' y editorial '{editorial}'.")
        presionar_intro()
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
            presionar_intro()
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
        filtro2 = []
        for revista in filtro:
            if revista.editorial == editorial:
                filtro2.append(revista)
        del filtro
        if filtro2:
            if len(filtro2) == 1:
                print(f"Solo hay una revista llamada '{nombre}' de {editorial} en la biblioteca.")
                return filtro2[0]
            else:
                print(f"Existen varias revistas con el nombre '{nombre}' y editorial '{editorial}' en la biblioteca.")
                for revista in filtro2:
                    print(f"Revista: {revista.nombre}, Fecha de publicación: {revista.fecha_publicacion}")
        else:
            print(f"No se encontró ninguna revista con el nombre '{nombre}' y editorial '{editorial}'.")
            presionar_intro()

        while True:
            fecha_publicacion = configurar_fecha_publicacion_revista()
            if fecha_publicacion:
                break
            else:
                print("Cancelando búsqueda de revista.")
                return None
        for revista in filtro2:
            if revista.fecha_publicacion == fecha_publicacion:
                return revista
        print(f"No se encontró ninguna revista con el nombre '{nombre}', editorial '{editorial}' y fecha de publicación '{fecha_publicacion}'.")
        presionar_intro()
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
            presionar_intro()
            return None
        
        fecha_publicacion = configurar_fecha_pelicula()
        if not fecha_publicacion:
            print("Fecha de publicación no válida.")
            presionar_intro()
            return None

        filtro2 = []
        for pelicula in filtro:
            if pelicula.fecha_publicacion == fecha_publicacion:
                filtro2.append(pelicula)
        del filtro
        if filtro2:
            if len(filtro2) == 1:
                print(f"Encontrada una película llamada '{titulo}' con fecha de publicación {fecha_publicacion} en la biblioteca.")
                return filtro2[0]
            else:                
                cantidad = range(1, len(filtro2) + 1)
                while True:
                    print(f"Existen varias películas con el título '{titulo}' y fecha de publicación {fecha_publicacion} en la biblioteca.")
                    for i in cantidad:
                        print(f"Película: {filtro2[i-1].titulo}, ID: {filtro2[i-1].id}")
                    try:
                        opcion = int(input("Seleccione el número de la película que desea: "))
                    except ValueError:
                        print("Entrada inválida. Debe ser un número entero.")
                        continue
                    except KeyboardInterrupt:
                        print("\nVolviendo al menú de recursos")
                        return
                    if opcion in cantidad:
                        return filtro2[opcion - 1]
                
        else:
            print(f"No se encontró ninguna película con el título '{titulo}' y fecha de publicación {fecha_publicacion}.")
            presionar_intro()
        return None
    
def eliminar_consulta(usuario:Usuario) -> None:
    """Elimina una consulta de un usuario, restableciendo el estado del recurso."""
    consulta = usuario.recurso_en_consulta
    recurso_consulta = biblioteca.consultas[consulta]
    tipo = recurso_consulta.id_recurso.get("libro",None)
    if tipo:
        libro = Libro(**recurso_consulta.id_recurso["libro"])
        ejemplar = EjemplarLibro(**recurso_consulta.id_recurso)
        biblioteca.libros[libro][biblioteca.libros[libro].index(ejemplar)].estado_accion = ""
    else:
        if recurso_consulta.id_recurso["id"][0] == "R":
            for revista in biblioteca.revistas:
                if revista.id == recurso_consulta.id_recurso["id"]:
                    revista.estado_consulta = False
                    break

        else:
            pelicula = Pelicula(**recurso_consulta.id_recurso)
            biblioteca.peliculas[pelicula][0].estado_local = False
    
    biblioteca.consultas[consulta].hora_devolucion = datetime.now().strftime("%H:%M:%S")
    
    usuario.recurso_en_consulta = None
    usuario.fecha_solicitud_consulta = None
    usuario.hora_solicitud_consulta = None
    biblioteca.guardar_datos()
    print(f"El recurso {consulta} ha sido devuelto.")
    presionar_intro()
        

def buscar_libro(titulo:str, autor:str, editorial:str) -> Recurso | None:
    """Busca un libro en la biblioteca. Busca por título, autor y editorial."""
    for libro in biblioteca.libros.keys():
        if isinstance(libro, Libro) and libro.titulo == titulo and libro.autor == autor and libro.editorial == editorial:
            return libro
    return None

def buscar_revista(nombre:str, fecha_publicacion:str, editorial:str) -> Recurso | None:
    """Busca una revista en la biblioteca. Busca por nombre, fecha de publicación y editorial."""
    for revista in biblioteca.revistas:
        if isinstance(revista, Revista) and revista.nombre == nombre and revista.fecha_publicacion == fecha_publicacion and revista.editorial == editorial:
            return revista
    return None

def buscar_pelicula(titulo:str, fecha_publicacion:str) -> Recurso | None:
    """Busca una película en la biblioteca. Busca por título y fecha de publicación."""
    for pelicula in biblioteca.peliculas.keys():
        if isinstance(pelicula, Pelicula) and pelicula.titulo == titulo and pelicula.fecha_publicacion == fecha_publicacion:
            return pelicula
    return None

def generar_consulta(nif:str, id_uso:str, id_recurso:str, fecha:str, hora:str) -> Consulta:
    """Genera una consulta a partir del NIF y el ID del recurso"""
    return Consulta(nif, id_uso, id_recurso, fecha, hora, None)

def configurar_fecha_prestamo() -> str:
    """Deja elegir si quieres la fecha real o una fecha manual"""
    while True:
        try:
            opcion = input("¿Quieres la fecha real o una fecha manual? (R/M): ").upper()
        except KeyboardInterrupt:
            print("\nVolviendo al menú de recursos")
            return None
        if opcion in ["R", "REAL"]:
            return datetime.now().strftime("%Y-%m-%d")
        elif opcion in ["M", "MANUAL"]:
                fecha = configurar_fecha_manual()
                if not fecha:
                    return None
                return fecha
        else:
            print("Opción inválida. Debe ser R o M.")
            continue


def configurar_fecha_publicacion_revista() -> str:
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
            return f"{año}-{mes:02d}"
        
def configurar_fecha_manual() -> str:
    """Pide una fecha(aaaa-mm-dd) y la devuelve en formato AAAA-MM-DD"""
    while True:
        try:
            fecha = input("Introduce la fecha de (día/mes/año): ")
            fecha = fecha.split("/")
        except KeyboardInterrupt:
            print("\nVolviendo al menú de recursos")
            return
        if len(fecha) != 3:
            print("Formato inválido. Debe ser mes/día/año.")
            continue
        else:
            try:
                dia = int(fecha[0])
                mes = int(fecha[1])
                año = int(fecha[2])
                if mes < 1 or mes > 12 or dia < 1 or dia > 31 or año < 1900 or año > 2025:
                    raise ValueError
            except ValueError:
                print("Entrada inválida. Debe ser un número entero entre 1 y 12 para el mes, entre 1 y 31 para el día y mayor a 1900 para el año.")
                continue
            except KeyboardInterrupt:
                print("\nVolviendo al menú de recursos")
                return
            return datetime(año, mes, dia).strftime("%Y-%m-%d")

def configurar_fecha_pelicula() -> str:
    """Pide una fecha(aaaa-mm-dd) y la devuelve en formato AAAA-MM-DD"""
    while True:
        try:
            fecha = input("Introduce la fecha de publicación (día/mes/año): ")
            fecha = fecha.split("/")
        except KeyboardInterrupt:
            print("\nVolviendo al menú de recursos")
            return
        if len(fecha) != 3:
            print("Formato inválido. Debe ser mes/día/año.")
            continue
        else:
            try:
                dia = int(fecha[0])
                mes = int(fecha[1])
                año = int(fecha[2])
                if mes < 1 or mes > 12 or dia < 1 or dia > 31 or año < 1900 or año > 2025:
                    raise ValueError
            except ValueError:
                print("Entrada inválida. Debe ser un número entero entre 1 y 12 para el mes, entre 1 y 31 para el día y mayor a 1900 para el año.")
                continue
            except KeyboardInterrupt:
                print("\nVolviendo al menú de recursos")
                return
            return datetime(año, mes, dia).strftime("%Y-%m-%d")

def comprobar_dni(dni:str) -> bool:
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

def comprobar_estado_recurso(recurso:Recurso, consulta:bool = False) -> EjemplarLibro | PeliculaBiblioteca | PeliculaPrestamo | Revista | None:
    """Comprueba el estado de un recurso. Si el recurso es un libro, devuelve el ejemplar disponible. Si es una revista devuelve el recurso. Si es una película, devuelve el ejemplar disponible."""
    if not consulta:
        if isinstance(recurso, Libro):
            ejemplar_disponible = False
            ejemplar_en_consulta = False
            for ejemplar in biblioteca.libros[recurso]:
                if not ejemplar.estado_accion and not ejemplar_disponible:
                    ejemplar_disponible = True
                elif ejemplar.estado_accion == "Consulta":
                    ejemplar_en_consulta = True
                elif not ejemplar.estado_accion and (ejemplar_disponible or ejemplar_en_consulta):
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

def presionar_intro() -> None:
    """Función para pausar la ejecución del programa hasta que el usuario presione Enter"""
    try:
        input("Presiona Enter para continuar...")
    except KeyboardInterrupt:
        pass

def test1():
    libro1 = Libro("L0000000001", "Libro de prueba", "Autor", "LIBRAZO", "Editorial")
    libro2 = Libro("L0000000002", "Libro de prueba", "Autor", "LIBRAZO2", "Editorial")
    libro3 = Libro("L0000000003", "Libro de prueba", "Autor", "LIBRAZO3", "Editorial")
    libro4 = Libro("L0000000004", "Libro de prueba", "Autor", "LIBRAZO", "Santillana")
    pelicula1 = Pelicula("P0000000001", "Descripción de la película", "Título", ("Actor1", "Actor2"), ("Secundario1"), "2023-10-01")
    pelicula2 = Pelicula("P0000000002", "Descripción de la película", "Título2", ("Actor1", "Actor2"), ("Secundario1"), "2023-10-01")
    pelicula3 = Pelicula("P0000000003", "Descripción de la película", "Título3", ("Actor1", "Actor2"), ("Secundario1"), "2023-10-01")
    pelicula4 = Pelicula("P0000000004", "Descripción de la película", "Título4", ("Actor1", "Actor2"), ("Secundario1"), "2023-10-01")
    biblioteca.revistas.add(Revista("R0000000001", "Descripción de la revista", "Revista1", "2023-10", "Editorial"))
    biblioteca.revistas.add(Revista("R0000000002", "Descripción de la revista", "Revista1", "2023-11", "Editorial"))
    biblioteca.revistas.add(Revista("R000000000", "Descripción de la revista", "Revista2", "2023-10", "Editorial"))
    biblioteca.revistas.add(Revista("R0000000004", "Descripción de la revista", "Revista2", "2023-09", "Editorial"))
    biblioteca.libros[libro1] = [EjemplarLibro(libro1.__dict__, 1, ''), EjemplarLibro(libro1.__dict__, 2,'')]
    biblioteca.libros[libro2] = [EjemplarLibro(libro2.__dict__, 1, ''), EjemplarLibro(libro2.__dict__, 2,'')]
    biblioteca.libros[libro3] = [EjemplarLibro(libro3.__dict__, 1, ''), EjemplarLibro(libro3.__dict__, 2,'')]
    biblioteca.libros[libro4] = [EjemplarLibro(libro4.__dict__, 1, ''), EjemplarLibro(libro4.__dict__, 2,'')]
    biblioteca.peliculas[pelicula1] = [PeliculaBiblioteca(pelicula1.__dict__, False), PeliculaPrestamo(pelicula1.__dict__, False)]
    biblioteca.peliculas[pelicula2] = [PeliculaBiblioteca(pelicula2.__dict__, False), PeliculaPrestamo(pelicula2.__dict__, False)]
    biblioteca.peliculas[pelicula3] = [PeliculaBiblioteca(pelicula3.__dict__, False), PeliculaPrestamo(pelicula3.__dict__, False)]
    biblioteca.peliculas[pelicula4] = [PeliculaBiblioteca(pelicula4.__dict__, False)]
    biblioteca.nro_id_libro = 4
    biblioteca.nro_id_pelicula = 4
    biblioteca.nro_id_revista = 4
    ultimo_indice = biblioteca.libros[libro1][-1].__dict__['nro_ejemplar']
    biblioteca.libros[libro1].append(EjemplarLibro(libro1.__dict__, ultimo_indice + 1,''))
    ultimo_indice = len(biblioteca.libros[libro1])
    biblioteca.libros[libro1].append(EjemplarLibro(libro1.__dict__, ultimo_indice + 1,''))
    usuario1 = Socio("43491650F", "Juan Pérez", "123456789", "Calle Falsa 123", "S0000000001")
    usuario2 = Socio("87654321X", "Ana García", "987654321", "Calle Verdadera 456","S0000000002")
    usuario3 = Socio("12345678Z", "Pedro Martínez", "123456789", "Calle Inventada 789","S0000000003")
    usuario4 = Socio("87654321X", "María López", "987654321", "Calle Imaginaria 012","S0000000004")
    usuario5 = Socio("98765432M", "Luis Fernández", "234567890", "Calle Real 345","S0000000005")
    usuario6 = Socio("56789012B", "Laura Sánchez", "345678901", "Calle Soñada 678","S0000000006")

    biblioteca.nro_socio = 6

    biblioteca.socios["43491650F"] = usuario1
    biblioteca.socios["87654321X"] = usuario2
    biblioteca.socios["12345678Z"] = usuario3
    biblioteca.socios["87654321X"] = usuario4
    biblioteca.socios["98765432M"] = usuario5
    biblioteca.socios["56789012B"] = usuario6

    ocasional1 = Ocasional("23456789D", "Luis López", "234567890", "Calle Real 789")
    ocasional2 = Ocasional("34567890V", "María Fernández", "345678901", "Calle Imaginaria 012")
    biblioteca.ocasionales["23456789D"] = ocasional1
    biblioteca.ocasionales["34567890V"] = ocasional2

    biblioteca.guardar_datos()
    print("Datos de prueba cargados correctamente.")

if __name__ == "__main__":

    biblioteca = Biblioteca()
    testing = False
    if testing:
        test1()
    biblioteca = Biblioteca()
    biblioteca.cargar_datos()
    mostrar_menu_principal()


# ============================================================
# SOFTWARE FJ
# Archivo: gui.py
# Interfaz gráfica y gestión de eventos de usuario
# ============================================================

# Importación de Tkinter para crear la interfaz gráfica.
import tkinter as tk
from tkinter import ttk, messagebox

# Importación de las clases del sistema.
from sistema.entidades import Cliente

from sistema.servicios import (
    ReservaSala,
    AlquilerEquipos,
    AsesoriaEspecializada
)

from sistema.reservas import Reserva, EstadoReserva
from sistema.gestor import GestorSoftwareFJ
from sistema.excepciones import ErrorSistema
from sistema.logger import logger


# ============================================================
# CLASE PRINCIPAL DE LA INTERFAZ GRÁFICA
# ============================================================

class SoftwareFJApp:

    """
    Clase principal encargada de construir y administrar
    la interfaz gráfica de Software FJ.
    """

    def __init__(self, ventana):

        # Configuración de la ventana principal.
        self.ventana = ventana
        self.ventana.title(
            "Software FJ | Sistema Integral de Gestión"
        )
        self.ventana.geometry("1050x700")
        self.ventana.minsize(850, 600)

        # Se crea el gestor que administra los objetos.
        self.gestor = GestorSoftwareFJ()

        # Diccionario para relacionar las reservas
        # mostradas en pantalla con sus objetos.
        self.reservas_visibles = {}

        # Configuración visual.
        self.configurar_estilos()

        # Construcción de los componentes.
        self.crear_encabezado()
        self.crear_pestanas()
        self.crear_pie()

        # Acción al cerrar la ventana.
        self.ventana.protocol(
            "WM_DELETE_WINDOW",
            self.cerrar_aplicacion
        )

    # ========================================================
    # CONFIGURACIÓN DE ESTILOS
    # ========================================================

    def configurar_estilos(self):

        """Define los estilos visuales de la aplicación."""

        estilo = ttk.Style()

        estilo.theme_use("clam")

        estilo.configure(
            "TNotebook.Tab",
            padding=(15, 8),
            font=("Arial", 10, "bold")
        )

        estilo.configure(
            "Titulo.TLabel",
            font=("Arial", 20, "bold"),
            foreground="#FFFFFF",
            background="#17365D"
        )

        estilo.configure(
            "Subtitulo.TLabel",
            font=("Arial", 10),
            foreground="#FFFFFF",
            background="#17365D"
        )

        estilo.configure(
            "Accion.TButton",
            padding=7,
            font=("Arial", 10, "bold")
        )

        estilo.configure(
            "Treeview",
            rowheight=28,
            font=("Arial", 9)
        )

        estilo.configure(
            "Treeview.Heading",
            font=("Arial", 9, "bold")
        )

    # ========================================================
    # ENCABEZADO PRINCIPAL
    # ========================================================

    def crear_encabezado(self):

        """Construye el encabezado de Software FJ."""

        encabezado = tk.Frame(
            self.ventana,
            bg="#17365D",
            height=100
        )

        encabezado.pack(fill="x")

        encabezado.pack_propagate(False)

        titulo = ttk.Label(
            encabezado,
            text="SOFTWARE FJ",
            style="Titulo.TLabel"
        )

        titulo.pack(pady=(15, 3))

        subtitulo = ttk.Label(
            encabezado,
            text="Sistema Integral de Gestión de Clientes, Servicios y Reservas",
            style="Subtitulo.TLabel"
        )

        subtitulo.pack()

    # ========================================================
    # CREACIÓN DE PESTAÑAS
    # ========================================================

    def crear_pestanas(self):

        """Organiza la aplicación en diferentes secciones."""

        self.pestanas = ttk.Notebook(self.ventana)

        self.pestanas.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        # Pestaña de clientes.
        self.tab_clientes = ttk.Frame(self.pestanas)

        # Pestaña de servicios.
        self.tab_servicios = ttk.Frame(self.pestanas)

        # Pestaña de reservas.
        self.tab_reservas = ttk.Frame(self.pestanas)

        # Pestaña de información.
        self.tab_inicio = ttk.Frame(self.pestanas)

        self.pestanas.add(
            self.tab_inicio,
            text="Inicio"
        )

        self.pestanas.add(
            self.tab_clientes,
            text="Clientes"
        )

        self.pestanas.add(
            self.tab_servicios,
            text="Servicios"
        )

        self.pestanas.add(
            self.tab_reservas,
            text="Reservas"
        )

        # Construcción de cada sección.
        self.crear_inicio()
        self.crear_clientes()
        self.crear_servicios()
        self.crear_reservas()

    # ========================================================
    # PESTAÑA INICIO
    # ========================================================

    def crear_inicio(self):

        """Muestra información general del sistema."""

        contenedor = ttk.Frame(
            self.tab_inicio,
            padding=30
        )

        contenedor.pack(
            fill="both",
            expand=True
        )

        ttk.Label(
            contenedor,
            text="Bienvenido a Software FJ",
            font=("Arial", 22, "bold")
        ).pack(pady=20)

        ttk.Label(
            contenedor,
            text=(
                "Sistema de administración de clientes,\n"
                "servicios y reservas empresariales."
            ),
            font=("Arial", 12),
            justify="center"
        ).pack(pady=10)

        # Información de los módulos.
        opciones = [
            "Gestión y registro de clientes",
            "Administración de servicios",
            "Creación y seguimiento de reservas",
            "Control de estados de las reservas",
            "Registro de eventos y errores"
        ]

        for opcion in opciones:

            ttk.Label(
                contenedor,
                text="• " + opcion,
                font=("Arial", 11)
            ).pack(pady=5)

        ttk.Button(
            contenedor,
            text="Consultar resumen del sistema",
            style="Accion.TButton",
            command=self.mostrar_resumen
        ).pack(pady=25)

    # ========================================================
    # PESTAÑA CLIENTES
    # ========================================================

    def crear_clientes(self):

        """Construye el formulario de registro de clientes."""

        contenedor = ttk.LabelFrame(
            self.tab_clientes,
            text="Registrar nuevo cliente",
            padding=15
        )

        contenedor.pack(
            fill="x",
            padx=15,
            pady=15
        )

        # Campos de entrada.
        self.id_cliente = tk.StringVar()
        self.nombre_cliente = tk.StringVar()
        self.correo_cliente = tk.StringVar()
        self.telefono_cliente = tk.StringVar()

        campos = [
            ("Identificación:", self.id_cliente),
            ("Nombre completo:", self.nombre_cliente),
            ("Correo electrónico:", self.correo_cliente),
            ("Teléfono:", self.telefono_cliente)
        ]

        for fila, (texto, variable) in enumerate(campos):

            ttk.Label(
                contenedor,
                text=texto
            ).grid(
                row=fila,
                column=0,
                sticky="w",
                pady=6
            )

            ttk.Entry(
                contenedor,
                textvariable=variable,
                width=40
            ).grid(
                row=fila,
                column=1,
                padx=10,
                pady=6
            )

        ttk.Button(
            contenedor,
            text="Registrar cliente",
            style="Accion.TButton",
            command=self.registrar_cliente
        ).grid(
            row=4,
            column=1,
            sticky="e",
            pady=10
        )

        # Tabla de clientes registrados.
        tabla = ttk.LabelFrame(
            self.tab_clientes,
            text="Clientes registrados",
            padding=10
        )

        tabla.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=5
        )

        columnas = (
            "id",
            "nombre",
            "correo",
            "telefono"
        )

        self.tabla_clientes = ttk.Treeview(
            tabla,
            columns=columnas,
            show="headings"
        )

        encabezados = {
            "id": "Identificación",
            "nombre": "Nombre",
            "correo": "Correo",
            "telefono": "Teléfono"
        }

        for columna in columnas:

            self.tabla_clientes.heading(
                columna,
                text=encabezados[columna]
            )

            self.tabla_clientes.column(
                columna,
                width=180
            )

        self.tabla_clientes.pack(
            fill="both",
            expand=True
        )

    # --------------------------------------------------------
    # REGISTRAR CLIENTE
    # --------------------------------------------------------

    def registrar_cliente(self):

        """Recibe los datos y registra un cliente."""

        try:

            cliente = Cliente(
                self.id_cliente.get(),
                self.nombre_cliente.get(),
                self.correo_cliente.get(),
                self.telefono_cliente.get()
            )

            resultado = self.gestor.registrar_cliente(
                cliente
            )

            self.actualizar_tabla_clientes()

            messagebox.showinfo(
                "Registro exitoso",
                resultado
            )

            # Limpia los campos después del registro.
            self.id_cliente.set("")
            self.nombre_cliente.set("")
            self.correo_cliente.set("")
            self.telefono_cliente.set("")

        except ErrorSistema as error:

            logger.exception(
                "Error al registrar cliente desde GUI"
            )

            messagebox.showerror(
                "Error de registro",
                str(error)
            )

        except Exception as error:

            logger.exception(
                "Error inesperado al registrar cliente"
            )

            messagebox.showerror(
                "Error inesperado",
                str(error)
            )

    # --------------------------------------------------------
    # ACTUALIZAR TABLA DE CLIENTES
    # --------------------------------------------------------

    def actualizar_tabla_clientes(self):

        """Actualiza visualmente la lista de clientes."""

        for elemento in self.tabla_clientes.get_children():

            self.tabla_clientes.delete(elemento)

        for cliente in self.gestor.clientes:

            self.tabla_clientes.insert(
                "",
                "end",
                values=(
                    cliente.identificador,
                    cliente.nombre,
                    cliente.correo,
                    cliente.telefono
                )
            )

    # ========================================================
    # PESTAÑA SERVICIOS
    # ========================================================

    def crear_servicios(self):

        """Construye el formulario para agregar servicios."""

        contenedor = ttk.LabelFrame(
            self.tab_servicios,
            text="Registrar servicio",
            padding=15
        )

        contenedor.pack(
            fill="x",
            padx=15,
            pady=15
        )

        self.id_servicio = tk.StringVar()
        self.tipo_servicio = tk.StringVar(value="Sala")
        self.tarifa_servicio = tk.StringVar()
        self.extra_servicio = tk.StringVar()

        ttk.Label(
            contenedor,
            text="Código:"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=7
        )

        ttk.Entry(
            contenedor,
            textvariable=self.id_servicio,
            width=30
        ).grid(
            row=0,
            column=1,
            padx=10
        )

        ttk.Label(
            contenedor,
            text="Tipo de servicio:"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=7
        )

        tipo = ttk.Combobox(
            contenedor,
            textvariable=self.tipo_servicio,
            values=[
                "Sala",
                "Equipos",
                "Asesoria"
            ],
            state="readonly",
            width=27
        )

        tipo.grid(
            row=1,
            column=1,
            padx=10
        )

        tipo.bind(
            "<<ComboboxSelected>>",
            self.actualizar_etiqueta_extra
        )

        ttk.Label(
            contenedor,
            text="Tarifa:"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            pady=7
        )

        ttk.Entry(
            contenedor,
            textvariable=self.tarifa_servicio,
            width=30
        ).grid(
            row=2,
            column=1,
            padx=10
        )

        self.etiqueta_extra = ttk.Label(
            contenedor,
            text="Capacidad:"
        )

        self.etiqueta_extra.grid(
            row=3,
            column=0,
            sticky="w",
            pady=7
        )

        ttk.Entry(
            contenedor,
            textvariable=self.extra_servicio,
            width=30
        ).grid(
            row=3,
            column=1,
            padx=10
        )

        ttk.Button(
            contenedor,
            text="Agregar servicio",
            style="Accion.TButton",
            command=self.agregar_servicio
        ).grid(
            row=4,
            column=1,
            sticky="e",
            pady=12
        )

        # Tabla de servicios.
        tabla = ttk.LabelFrame(
            self.tab_servicios,
            text="Servicios disponibles",
            padding=10
        )

        tabla.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=5
        )

        columnas = (
            "codigo",
            "nombre",
            "tarifa",
            "descripcion"
        )

        self.tabla_servicios = ttk.Treeview(
            tabla,
            columns=columnas,
            show="headings"
        )

        titulos = [
            "Código",
            "Servicio",
            "Tarifa",
            "Descripción"
        ]

        for columna, titulo in zip(columnas, titulos):

            self.tabla_servicios.heading(
                columna,
                text=titulo
            )

            self.tabla_servicios.column(
                columna,
                width=190
            )

        self.tabla_servicios.pack(
            fill="both",
            expand=True
        )

    # --------------------------------------------------------
    # ACTUALIZAR CAMPO ADICIONAL
    # --------------------------------------------------------

    def actualizar_etiqueta_extra(self, evento=None):

        """Cambia el campo adicional según el servicio."""

        tipo = self.tipo_servicio.get()

        if tipo == "Sala":

            self.etiqueta_extra.config(
                text="Capacidad:"
            )

        elif tipo == "Equipos":

            self.etiqueta_extra.config(
                text="Inventario:"
            )

        else:

            self.etiqueta_extra.config(
                text="No requiere dato adicional:"
            )

    # --------------------------------------------------------
    # AGREGAR SERVICIO
    # --------------------------------------------------------

    def agregar_servicio(self):

        """Crea y registra el servicio seleccionado."""

        try:

            codigo = self.id_servicio.get().strip()

            tarifa = float(
                self.tarifa_servicio.get()
            )

            tipo = self.tipo_servicio.get()

            if tipo == "Sala":

                servicio = ReservaSala(
                    codigo,
                    tarifa,
                    int(self.extra_servicio.get())
                )

            elif tipo == "Equipos":

                servicio = AlquilerEquipos(
                    codigo,
                    tarifa,
                    int(self.extra_servicio.get())
                )

            else:

                servicio = AsesoriaEspecializada(
                    codigo,
                    tarifa
                )

            resultado = self.gestor.agregar_servicio(
                servicio
            )

            self.actualizar_tabla_servicios()

            self.actualizar_combos_reservas()

            messagebox.showinfo(
                "Servicio agregado",
                resultado
            )

            # Limpia los campos.
            self.id_servicio.set("")
            self.tarifa_servicio.set("")
            self.extra_servicio.set("")

        except ErrorSistema as error:

            logger.exception(
                "Error al agregar servicio desde GUI"
            )

            messagebox.showerror(
                "Error de servicio",
                str(error)
            )

        except (ValueError, TypeError) as error:

            logger.exception(
                "Error en los datos del servicio"
            )

            messagebox.showerror(
                "Datos incorrectos",
                "Verifique que la tarifa y el dato adicional "
                "sean números válidos."
            )

        except Exception as error:

            logger.exception(
                "Error inesperado al agregar servicio"
            )

            messagebox.showerror(
                "Error inesperado",
                str(error)
            )

    # --------------------------------------------------------
    # ACTUALIZAR TABLA DE SERVICIOS
    # --------------------------------------------------------

    def actualizar_tabla_servicios(self):

        """Muestra todos los servicios registrados."""

        for elemento in self.tabla_servicios.get_children():

            self.tabla_servicios.delete(elemento)

        for servicio in self.gestor.servicios:

            self.tabla_servicios.insert(
                "",
                "end",
                values=(
                    servicio.codigo,
                    servicio.nombre,
                    f"${servicio.tarifa_base:,.0f}",
                    servicio.describir()
                )
            )

    # ========================================================
    # PESTAÑA RESERVAS
    # ========================================================

    def crear_reservas(self):

        """Construye el formulario de creación de reservas."""

        contenedor = ttk.LabelFrame(
            self.tab_reservas,
            text="Crear reserva",
            padding=15
        )

        contenedor.pack(
            fill="x",
            padx=15,
            pady=15
        )

        self.id_reserva = tk.StringVar()

        self.cliente_reserva = tk.StringVar()

        self.servicio_reserva = tk.StringVar()

        self.duracion_reserva = tk.StringVar()

        self.parametro_reserva = tk.StringVar()

        # Identificador.
        ttk.Label(
            contenedor,
            text="Código de reserva:"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=6
        )

        ttk.Entry(
            contenedor,
            textvariable=self.id_reserva,
            width=30
        ).grid(
            row=0,
            column=1,
            padx=10
        )

        # Cliente.
        ttk.Label(
            contenedor,
            text="Cliente:"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=6
        )

        self.combo_clientes = ttk.Combobox(
            contenedor,
            textvariable=self.cliente_reserva,
            state="readonly",
            width=27
        )

        self.combo_clientes.grid(
            row=1,
            column=1,
            padx=10
        )

        # Servicio.
        ttk.Label(
            contenedor,
            text="Servicio:"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            pady=6
        )

        self.combo_servicios = ttk.Combobox(
            contenedor,
            textvariable=self.servicio_reserva,
            state="readonly",
            width=27
        )

        self.combo_servicios.grid(
            row=2,
            column=1,
            padx=10
        )

        self.combo_servicios.bind(
            "<<ComboboxSelected>>",
            self.actualizar_parametro_reserva
        )

        # Duración.
        ttk.Label(
            contenedor,
            text="Duración:"
        ).grid(
            row=3,
            column=0,
            sticky="w",
            pady=6
        )

        ttk.Entry(
            contenedor,
            textvariable=self.duracion_reserva,
            width=30
        ).grid(
            row=3,
            column=1,
            padx=10
        )

        # Parámetro específico.
        self.etiqueta_parametro = ttk.Label(
            contenedor,
            text="Parámetro:"
        )

        self.etiqueta_parametro.grid(
            row=4,
            column=0,
            sticky="w",
            pady=6
        )

        self.combo_parametro = ttk.Combobox(
            contenedor,
            textvariable=self.parametro_reserva,
            width=27
        )

        self.combo_parametro.grid(
            row=4,
            column=1,
            padx=10
        )

        ttk.Button(
            contenedor,
            text="Crear reserva",
            style="Accion.TButton",
            command=self.crear_reserva
        ).grid(
            row=5,
            column=1,
            sticky="e",
            pady=12
        )

        # Tabla de reservas.
        tabla = ttk.LabelFrame(
            self.tab_reservas,
            text="Administración de reservas",
            padding=10
        )

        tabla.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=5
        )

        columnas = (
            "codigo",
            "cliente",
            "servicio",
            "duracion",
            "estado",
            "costo"
        )

        self.tabla_reservas = ttk.Treeview(
            tabla,
            columns=columnas,
            show="headings"
        )

        titulos = [
            "Código",
            "Cliente",
            "Servicio",
            "Duración",
            "Estado",
            "Costo"
        ]

        for columna, titulo in zip(columnas, titulos):

            self.tabla_reservas.heading(
                columna,
                text=titulo
            )

            self.tabla_reservas.column(
                columna,
                width=130
            )

        self.tabla_reservas.pack(
            fill="both",
            expand=True
        )

        # Botones de administración.
        botones = ttk.Frame(
            self.tab_reservas
        )

        botones.pack(
            pady=12
        )

        ttk.Button(
            botones,
            text="Confirmar",
            command=self.confirmar_reserva
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            botones,
            text="Procesar",
            command=self.procesar_reserva
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            botones,
            text="Cancelar",
            command=self.cancelar_reserva
        ).pack(
            side="left",
            padx=5
        )

        # Carga los clientes y servicios existentes.
        self.actualizar_combos_reservas()

    # --------------------------------------------------------
    # ACTUALIZAR COMBOS DE CLIENTES Y SERVICIOS
    # --------------------------------------------------------

    def actualizar_combos_reservas(self):

        """Carga los objetos registrados en los selectores."""

        self.combo_clientes["values"] = [
            f"{x.identificador} - {x.nombre}"
            for x in self.gestor.clientes
        ]

        self.combo_servicios["values"] = [
            f"{x.codigo} - {x.nombre}"
            for x in self.gestor.servicios
        ]

    # --------------------------------------------------------
    # ACTUALIZAR PARÁMETROS SEGÚN EL SERVICIO
    # --------------------------------------------------------

    def actualizar_parametro_reserva(self, evento=None):

        """Determina qué parámetro necesita cada servicio."""

        seleccion = self.servicio_reserva.get()

        codigo = seleccion.split(" - ")[0]

        servicio = next(
            (
                x for x in self.gestor.servicios
                if x.codigo == codigo
            ),
            None
        )

        if isinstance(servicio, ReservaSala):

            self.etiqueta_parametro.config(
                text="Cantidad de personas:"
            )

            self.combo_parametro.configure(
                values=[],
                state="normal"
            )

            self.parametro_reserva.set("")

        elif isinstance(servicio, AlquilerEquipos):

            self.etiqueta_parametro.config(
                text="Cantidad de equipos:"
            )

            self.combo_parametro.configure(
                values=[],
                state="normal"
            )

            self.parametro_reserva.set("")

        elif isinstance(servicio, AsesoriaEspecializada):

            self.etiqueta_parametro.config(
                text="Nivel de asesoría:"
            )

            self.combo_parametro.configure(
                values=[
                    "basico",
                    "intermedio",
                    "avanzado"
                ],
                state="readonly"
            )

            self.parametro_reserva.set("basico")

    # --------------------------------------------------------
    # CREAR RESERVA
    # --------------------------------------------------------

    def crear_reserva(self):

        """Crea una reserva utilizando los datos del formulario."""

        try:

            codigo = self.id_reserva.get().strip()

            cliente_codigo = (
                self.cliente_reserva.get().split(" - ")[0]
            )

            servicio_codigo = (
                self.servicio_reserva.get().split(" - ")[0]
            )

            # Busca los objetos correspondientes.
            cliente = self.gestor.buscar_cliente(
                cliente_codigo
            )

            servicio = next(
                (
                    x for x in self.gestor.servicios
                    if x.codigo == servicio_codigo
                ),
                None
            )

            if servicio is None:

                raise ErrorSistema(
                    "Debe seleccionar un servicio válido."
                )

            duracion = float(
                self.duracion_reserva.get()
            )

            # Determina los parámetros de cada servicio.
            if isinstance(servicio, ReservaSala):

                parametros = {
                    "personas": int(
                        self.parametro_reserva.get()
                    )
                }

            elif isinstance(servicio, AlquilerEquipos):

                parametros = {
                    "cantidad": int(
                        self.parametro_reserva.get()
                    )
                }

            else:

                parametros = {
                    "nivel": self.parametro_reserva.get()
                }

            # Construye el objeto Reserva.
            reserva = Reserva(
                codigo,
                cliente,
                servicio,
                duracion,
                parametros
            )

            # Registra la reserva en el gestor.
            resultado = self.gestor.crear_reserva(
                reserva
            )

            self.actualizar_tabla_reservas()

            messagebox.showinfo(
                "Reserva creada",
                resultado + "\nEstado: Pendiente"
            )

            # Limpia los campos.
            self.id_reserva.set("")
            self.duracion_reserva.set("")

        except ErrorSistema as error:

            logger.exception(
                "Error al crear reserva desde GUI"
            )

            messagebox.showerror(
                "Error de reserva",
                str(error)
            )

        except (ValueError, TypeError) as error:

            logger.exception(
                "Datos incorrectos al crear reserva"
            )

            messagebox.showerror(
                "Datos incorrectos",
                "Verifique los campos numéricos y "
                "los datos seleccionados."
            )

        except Exception as error:

            logger.exception(
                "Error inesperado al crear reserva"
            )

            messagebox.showerror(
                "Error inesperado",
                str(error)
            )

    # --------------------------------------------------------
    # OBTENER RESERVA SELECCIONADA
    # --------------------------------------------------------

    def obtener_reserva_seleccionada(self):

        """Obtiene el objeto Reserva seleccionado en la tabla."""

        seleccion = self.tabla_reservas.selection()

        if not seleccion:

            messagebox.showwarning(
                "Selección requerida",
                "Seleccione una reserva de la tabla."
            )

            return None

        codigo = self.tabla_reservas.item(
            seleccion[0],
            "values"
        )[0]

        return next(
            (
                x for x in self.gestor.reservas
                if x.identificador == codigo
            ),
            None
        )

    # --------------------------------------------------------
    # CONFIRMAR RESERVA
    # --------------------------------------------------------

    def confirmar_reserva(self):

        """Confirma la reserva seleccionada."""

        try:

            reserva = self.obtener_reserva_seleccionada()

            if reserva is None:
                return

            costo = reserva.confirmar()

            self.actualizar_tabla_reservas()

            messagebox.showinfo(
                "Reserva confirmada",
                f"Reserva confirmada correctamente.\n"
                f"Costo: ${costo:,.2f}"
            )

        except ErrorSistema as error:

            logger.exception(
                "Error al confirmar reserva"
            )

            messagebox.showerror(
                "No se pudo confirmar",
                str(error)
            )

        except Exception as error:

            logger.exception(
                "Error inesperado al confirmar reserva"
            )

            messagebox.showerror(
                "Error inesperado",
                str(error)
            )

    # --------------------------------------------------------
    # PROCESAR RESERVA
    # --------------------------------------------------------

    def procesar_reserva(self):

        """Procesa una reserva confirmada."""

        try:

            reserva = self.obtener_reserva_seleccionada()

            if reserva is None:
                return

            resultado = reserva.procesar()

            self.actualizar_tabla_reservas()

            messagebox.showinfo(
                "Procesamiento",
                resultado
            )

        except ErrorSistema as error:

            logger.exception(
                "Error al procesar reserva"
            )

            messagebox.showerror(
                "Operación no permitida",
                str(error)
            )

        except Exception as error:

            logger.exception(
                "Error inesperado al procesar reserva"
            )

            messagebox.showerror(
                "Error inesperado",
                str(error)
            )

    # --------------------------------------------------------
    # CANCELAR RESERVA
    # --------------------------------------------------------

    def cancelar_reserva(self):

        """Cancela la reserva seleccionada."""

        try:

            reserva = self.obtener_reserva_seleccionada()

            if reserva is None:
                return

            respuesta = messagebox.askyesno(
                "Confirmar cancelación",
                "¿Desea cancelar esta reserva?"
            )

            if not respuesta:
                return

            resultado = reserva.cancelar()

            self.actualizar_tabla_reservas()

            messagebox.showinfo(
                "Reserva cancelada",
                resultado
            )

        except ErrorSistema as error:

            logger.exception(
                "Error al cancelar reserva"
            )

            messagebox.showerror(
                "No se pudo cancelar",
                str(error)
            )

        except Exception as error:

            logger.exception(
                "Error inesperado al cancelar reserva"
            )

            messagebox.showerror(
                "Error inesperado",
                str(error)
            )

    # --------------------------------------------------------
    # ACTUALIZAR TABLA DE RESERVAS
    # --------------------------------------------------------

    def actualizar_tabla_reservas(self):

        """Actualiza los datos mostrados en la tabla."""

        for elemento in self.tabla_reservas.get_children():

            self.tabla_reservas.delete(elemento)

        self.reservas_visibles.clear()

        for reserva in self.gestor.reservas:

            costo = (
                f"${reserva.costo:,.2f}"
                if reserva.costo is not None
                else "Pendiente"
            )

            self.tabla_reservas.insert(
                "",
                "end",
                values=(
                    reserva.identificador,
                    reserva.cliente.nombre,
                    reserva.servicio.nombre,
                    reserva.duracion,
                    reserva.estado.value,
                    costo
                )
            )

            self.reservas_visibles[
                reserva.identificador
            ] = reserva

    # ========================================================
    # RESUMEN GENERAL
    # ========================================================

    def mostrar_resumen(self):

        """Muestra las cantidades registradas en el sistema."""

        mensaje = (
            "RESUMEN GENERAL - SOFTWARE FJ\n\n"
            f"Clientes registrados: "
            f"{len(self.gestor.clientes)}\n\n"
            f"Servicios registrados: "
            f"{len(self.gestor.servicios)}\n\n"
            f"Reservas registradas: "
            f"{len(self.gestor.reservas)}\n\n"
            "Los datos se mantienen en memoria "
            "durante la ejecución."
        )

        messagebox.showinfo(
            "Resumen del sistema",
            mensaje
        )

    # ========================================================
    # PIE DE VENTANA
    # ========================================================

    def crear_pie(self):

        """Muestra información institucional."""

        pie = tk.Frame(
            self.ventana,
            bg="#E8EDF3",
            height=35
        )

        pie.pack(
            side="bottom",
            fill="x"
        )

        ttk.Label(
            pie,
            text="Software FJ | Sistema de gestión empresarial",
            font=("Arial", 9)
        ).pack(pady=8)

    # ========================================================
    # CERRAR APLICACIÓN
    # ========================================================

    def cerrar_aplicacion(self):

        """Registra el cierre de la aplicación."""

        logger.info(
            "Aplicación Software FJ cerrada."
        )

        self.ventana.destroy()


# ============================================================
# FUNCIÓN PARA INICIAR LA INTERFAZ
# ============================================================

def iniciar_gui():

    """
    Crea la ventana principal y ejecuta
    el ciclo de eventos de Tkinter.
    """

    ventana = tk.Tk()

    aplicacion = SoftwareFJApp(ventana)

    ventana.mainloop()


# ============================================================
# PUNTO DE ENTRADA INDEPENDIENTE
# ============================================================

if __name__ == "__main__":

    iniciar_gui()

# ============================================================
# SOFTWARE FJ
# Archivo: gestor.py
# Administración general de clientes, servicios y reservas
# ============================================================

# Importación de las clases principales.
from sistema.entidades import Cliente
from sistema.servicios import Servicio
from sistema.reservas import Reserva

# Importación de excepciones personalizadas.
from sistema.excepciones import (
    ClienteDuplicadoError,
    ServicioDuplicadoError,
    ReservaDuplicadaError,
    RecursoNoEncontradoError
)

# Importación del sistema de logs.
from sistema.logger import logger


# ------------------------------------------------------------
# CLASE GESTOR SOFTWARE FJ
# ------------------------------------------------------------

class GestorSoftwareFJ:

    """
    Administra los objetos del sistema mediante listas
    en memoria, sin utilizar bases de datos.
    """

    def __init__(self):

        # Lista para almacenar los clientes.
        self.clientes = []

        # Lista para almacenar los servicios.
        self.servicios = []

        # Lista para almacenar las reservas.
        self.reservas = []

    # --------------------------------------------------------
    # REGISTRAR CLIENTES
    # --------------------------------------------------------

    def registrar_cliente(self, cliente):

        """
        Registra un cliente después de comprobar
        que sea válido y que no esté duplicado.
        """

        if not isinstance(cliente, Cliente):

            raise TypeError(
                "Se esperaba un objeto Cliente."
            )

        # Verifica si el identificador ya existe.
        if any(
            x.identificador == cliente.identificador
            for x in self.clientes
        ):

            raise ClienteDuplicadoError(
                f"Cliente {cliente.identificador} duplicado."
            )

        # Agrega el cliente a la lista.
        self.clientes.append(cliente)

        # Registra el evento.
        logger.info(
            "Cliente registrado: %s",
            cliente.identificador
        )

        return (
            f"Cliente {cliente.identificador} registrado."
        )

    # --------------------------------------------------------
    # AGREGAR SERVICIOS
    # --------------------------------------------------------

    def agregar_servicio(self, servicio):

        """
        Agrega un servicio a la lista después
        de comprobar su tipo y código.
        """

        if not isinstance(servicio, Servicio):

            raise TypeError(
                "Se esperaba un objeto Servicio."
            )

        # Evita registrar códigos repetidos.
        if any(
            x.codigo == servicio.codigo
            for x in self.servicios
        ):

            raise ServicioDuplicadoError(
                f"Servicio {servicio.codigo} duplicado."
            )

        # Se almacena el servicio.
        self.servicios.append(servicio)

        logger.info(
            "Servicio agregado: %s",
            servicio.codigo
        )

        return (
            f"Servicio {servicio.codigo} agregado."
        )

    # --------------------------------------------------------
    # CREAR RESERVAS
    # --------------------------------------------------------

    def crear_reserva(self, reserva):

        """
        Registra una reserva verificando que
        el cliente y el servicio estén registrados.
        """

        if not isinstance(reserva, Reserva):

            raise TypeError(
                "Se esperaba un objeto Reserva."
            )

        # Verifica que no exista una reserva duplicada.
        if any(
            x.identificador == reserva.identificador
            for x in self.reservas
        ):

            raise ReservaDuplicadaError(
                f"Reserva {reserva.identificador} duplicada."
            )

        # Comprueba que el cliente esté registrado.
        if not any(
            x is reserva.cliente
            for x in self.clientes
        ):

            raise RecursoNoEncontradoError(
                "El cliente no está registrado."
            )

        # Comprueba que el servicio esté registrado.
        if not any(
            x is reserva.servicio
            for x in self.servicios
        ):

            raise RecursoNoEncontradoError(
                "El servicio no está registrado."
            )

        # Almacena la reserva en la lista.
        self.reservas.append(reserva)

        logger.info(
            "Reserva creada: %s",
            reserva.identificador
        )

        return (
            f"Reserva {reserva.identificador} creada."
        )

    # --------------------------------------------------------
    # BUSCAR CLIENTES
    # --------------------------------------------------------

    def buscar_cliente(self, identificador):

        """
        Busca un cliente mediante su identificador.
        Si no existe, genera una excepción.
        """

        for cliente in self.clientes:

            if cliente.identificador == identificador:

                return cliente

        raise RecursoNoEncontradoError(
            f"No existe el cliente {identificador}."
        )

    # --------------------------------------------------------
    # GENERAR RESUMEN GENERAL
    # --------------------------------------------------------

    def resumen(self):

        """
        Devuelve la cantidad de clientes,
        servicios y reservas almacenados.
        """

        return (
            f"Clientes: {len(self.clientes)} | "
            f"Servicios: {len(self.servicios)} | "
            f"Reservas: {len(self.reservas)}"
        )

# ============================================================
# SOFTWARE FJ
# Archivo: reservas.py
# Administración de reservas y control de estados
# ============================================================

# Importación de herramientas para crear enumeraciones.
from enum import Enum

# Importación de las clases necesarias.
from sistema.entidades import Entidad, Cliente
from sistema.servicios import Servicio, AlquilerEquipos

# Importación de excepciones personalizadas.
from sistema.excepciones import (
    DatosInvalidosError,
    ReservaInvalidaError,
    OperacionNoPermitidaError
)

# Importación del sistema de registro de eventos.
from sistema.logger import logger


# ------------------------------------------------------------
# ENUMERACIÓN DE ESTADOS DE LAS RESERVAS
# ------------------------------------------------------------

class EstadoReserva(Enum):

    """
    Define los posibles estados de una reserva.
    """

    PENDIENTE = "Pendiente"

    CONFIRMADA = "Confirmada"

    CANCELADA = "Cancelada"

    PROCESADA = "Procesada"


# ------------------------------------------------------------
# CLASE RESERVA
# ------------------------------------------------------------

class Reserva(Entidad):

    """
    Representa una reserva realizada por un cliente
    para utilizar uno de los servicios de Software FJ.
    """

    def __init__(
        self,
        identificador,
        cliente,
        servicio,
        duracion,
        parametros=None
    ):

        # Inicialización de la clase padre.
        super().__init__(identificador)

        # Verificación del tipo de cliente.
        if not isinstance(cliente, Cliente):

            raise ReservaInvalidaError(
                "La reserva requiere un cliente válido."
            )

        # Verificación del tipo de servicio.
        if not isinstance(servicio, Servicio):

            raise ReservaInvalidaError(
                "La reserva requiere un servicio válido."
            )

        # Validación de la duración.
        if (
            not isinstance(duracion, (int, float))
            or isinstance(duracion, bool)
            or duracion <= 0
        ):

            raise DatosInvalidosError(
                "La duración debe ser positiva."
            )

        # Asociación entre cliente y servicio.
        self.cliente = cliente
        self.servicio = servicio

        self.duracion = duracion

        # Parámetros particulares del servicio.
        self.parametros = parametros or {}

        # Toda reserva comienza en estado pendiente.
        self.estado = EstadoReserva.PENDIENTE

        # El costo se calcula cuando se confirma.
        self.costo = None

        # Variable que controla si se apartó inventario.
        self._inventario_apartado = False

    # --------------------------------------------------------
    # MÉTODO PARA CONFIRMAR UNA RESERVA
    # --------------------------------------------------------

    def confirmar(self):

        """
        Confirma una reserva si sus datos son correctos
        y el servicio tiene disponibilidad.
        """

        # Solo se pueden confirmar reservas pendientes.
        if self.estado is not EstadoReserva.PENDIENTE:

            raise OperacionNoPermitidaError(
                "Solo se confirma una reserva pendiente."
            )

        # Se verifica la disponibilidad del servicio.
        self.servicio.comprobar_disponibilidad()

        # Se calcula el costo utilizando el método
        # correspondiente al tipo de servicio.
        costo = self.servicio.calcular_costo(
            self.duracion,
            **self.parametros
        )

        # Si se trata de alquiler de equipos,
        # se descuenta la cantidad del inventario.
        if isinstance(self.servicio, AlquilerEquipos):

            self.servicio.reservar_inventario(
                self.parametros["cantidad"]
            )

            self._inventario_apartado = True

        # Se almacena el costo calculado.
        self.costo = costo

        # Se actualiza el estado de la reserva.
        self.estado = EstadoReserva.CONFIRMADA

        # Se registra el evento en el archivo de logs.
        logger.info(
            "Reserva %s confirmada por %.2f",
            self.identificador,
            costo
        )

        return costo

    # --------------------------------------------------------
    # MÉTODO PARA CANCELAR UNA RESERVA
    # --------------------------------------------------------

    def cancelar(self):

        """
        Permite cancelar una reserva pendiente
        o previamente confirmada.
        """

        if self.estado not in (
            EstadoReserva.PENDIENTE,
            EstadoReserva.CONFIRMADA
        ):

            raise OperacionNoPermitidaError(
                "No se puede cancelar en el estado actual."
            )

        # Si se había reservado inventario,
        # se devuelven las unidades disponibles.
        if (
            self._inventario_apartado
            and isinstance(self.servicio, AlquilerEquipos)
        ):

            self.servicio.liberar_inventario(
                self.parametros["cantidad"]
            )

            self._inventario_apartado = False

        # Se cambia el estado de la reserva.
        self.estado = EstadoReserva.CANCELADA

        # Registro de la cancelación.
        logger.info(
            "Reserva %s cancelada",
            self.identificador
        )

        return f"Reserva {self.identificador} cancelada."

    # --------------------------------------------------------
    # MÉTODO PARA PROCESAR UNA RESERVA
    # --------------------------------------------------------

    def procesar(self):

        """
        Procesa una reserva previamente confirmada.
        """

        # Verifica que la reserva esté confirmada.
        if self.estado is not EstadoReserva.CONFIRMADA:

            raise OperacionNoPermitidaError(
                "Solo se procesan reservas confirmadas."
            )

        # Se actualiza el estado.
        self.estado = EstadoReserva.PROCESADA

        # Registro del procesamiento.
        logger.info(
            "Reserva %s procesada",
            self.identificador
        )

        return (
            f"Reserva {self.identificador} procesada. "
            f"Total: ${self.costo:,.2f}"
        )

    # --------------------------------------------------------
    # MOSTRAR INFORMACIÓN DE LA RESERVA
    # --------------------------------------------------------

    def mostrar_informacion(self):

        """
        Devuelve los datos principales de la reserva.
        """

        return (
            f"{self.identificador} | "
            f"{self.cliente.nombre} | "
            f"{self.servicio.nombre} | "
            f"{self.estado.value}"
        )

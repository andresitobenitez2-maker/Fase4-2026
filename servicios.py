# ============================================================
# SOFTWARE FJ
# Archivo: servicios.py
# Herencia, abstracción y polimorfismo
# ============================================================

from abc import ABC, abstractmethod

# Importación de excepciones personalizadas.
from sistema.excepciones import (
    DatosInvalidosError,
    ServicioNoDisponibleError
)


# ------------------------------------------------------------
# CLASE ABSTRACTA SERVICIO
# ------------------------------------------------------------

class Servicio(ABC):

    """
    Clase base abstracta para todos los servicios
    ofrecidos por Software FJ.
    """

    def __init__(self, codigo, nombre, tarifa):

        # Validación del código del servicio.
        if not isinstance(codigo, str) or not codigo.strip():

            raise DatosInvalidosError(
                "Código obligatorio."
            )

        # Validación de la tarifa.
        if (
            isinstance(tarifa, bool)
            or not isinstance(tarifa, (int, float))
            or tarifa <= 0
        ):

            raise DatosInvalidosError(
                "La tarifa debe ser positiva."
            )

        self.codigo = codigo.strip()
        self.nombre = nombre
        self.tarifa_base = float(tarifa)

        # Indica si el servicio se encuentra disponible.
        self.disponible = True

    # --------------------------------------------------------
    # MÉTODOS ABSTRACTOS
    # --------------------------------------------------------

    @abstractmethod
    def validar_parametros(self, **kwargs):

        """Cada servicio valida sus propios parámetros."""

        pass

    @abstractmethod
    def calcular_costo(self, duracion, **kwargs):

        """Cada servicio implementa su propio cálculo."""

        pass

    @abstractmethod
    def describir(self):

        """Devuelve la descripción del servicio."""

        pass

    # --------------------------------------------------------
    # VALIDACIÓN DE DISPONIBILIDAD
    # --------------------------------------------------------

    def comprobar_disponibilidad(self):

        if not self.disponible:

            raise ServicioNoDisponibleError(
                f"{self.nombre} no está disponible."
            )

    # --------------------------------------------------------
    # CÁLCULO CON IMPUESTO Y DESCUENTO
    # --------------------------------------------------------

    def calcular_con_impuesto(
        self,
        duracion,
        impuesto=0.19,
        descuento=0,
        **kwargs
    ):

        """
        Calcula el costo final aplicando descuento
        e impuesto sobre el valor resultante.
        """

        if not 0 <= impuesto <= 1 or not 0 <= descuento <= 1:

            raise DatosInvalidosError(
                "Impuesto y descuento deben estar entre 0 y 1."
            )

        # Se obtiene el costo base mediante polimorfismo.
        base = self.calcular_costo(duracion, **kwargs)

        # Primero se aplica el descuento y después el impuesto.
        return round(
            base * (1 - descuento) * (1 + impuesto),
            2
        )

    # --------------------------------------------------------
    # CÁLCULO CON DESCUENTO
    # --------------------------------------------------------

    def calcular_con_descuento(
        self,
        duracion,
        descuento=0,
        **kwargs
    ):

        """Calcula el costo aplicando solamente descuento."""

        if not 0 <= descuento <= 1:

            raise DatosInvalidosError(
                "Descuento fuera de rango."
            )

        return round(
            self.calcular_costo(duracion, **kwargs) * (1 - descuento),
            2
        )


# ============================================================
# SERVICIO 1: RESERVA DE SALAS
# ============================================================

class ReservaSala(Servicio):

    """
    Servicio para alquilar salas por horas.
    """

    def __init__(self, codigo, tarifa_hora, capacidad):

        # Inicialización de la clase padre.
        super().__init__(
            codigo,
            "Reserva de sala",
            tarifa_hora
        )

        # Validación de la capacidad.
        if (
            not isinstance(capacidad, int)
            or isinstance(capacidad, bool)
            or capacidad <= 0
        ):

            raise DatosInvalidosError(
                "Capacidad inválida."
            )

        self.capacidad = capacidad

    # --------------------------------------------------------
    # VALIDACIÓN DE PARÁMETROS
    # --------------------------------------------------------

    def validar_parametros(self, **kwargs):

        personas = kwargs.get("personas")

        if (
            not isinstance(personas, int)
            or isinstance(personas, bool)
            or personas <= 0
        ):

            raise DatosInvalidosError(
                "Debe indicar una cantidad positiva de personas."
            )

        if personas > self.capacidad:

            raise ServicioNoDisponibleError(
                "La cantidad de personas supera la capacidad."
            )

        return True

    # --------------------------------------------------------
    # CÁLCULO DEL COSTO
    # --------------------------------------------------------

    def calcular_costo(self, duracion, **kwargs):

        self.validar_parametros(**kwargs)

        if (
            not isinstance(duracion, (int, float))
            or isinstance(duracion, bool)
            or duracion <= 0
        ):

            raise DatosInvalidosError(
                "Duración inválida."
            )

        return round(
            self.tarifa_base * duracion,
            2
        )

    # --------------------------------------------------------
    # DESCRIPCIÓN DEL SERVICIO
    # --------------------------------------------------------

    def describir(self):

        return (
            f"Sala: ${self.tarifa_base:,.0f}/hora; "
            f"capacidad {self.capacidad} personas."
        )


# ============================================================
# SERVICIO 2: ALQUILER DE EQUIPOS
# ============================================================

class AlquilerEquipos(Servicio):

    """
    Servicio para alquilar equipos por día.
    Controla las unidades disponibles en inventario.
    """

    def __init__(self, codigo, tarifa_dia, inventario):

        super().__init__(
            codigo,
            "Alquiler de equipos",
            tarifa_dia
        )

        # Validación del inventario inicial.
        if (
            not isinstance(inventario, int)
            or isinstance(inventario, bool)
            or inventario < 0
        ):

            raise DatosInvalidosError(
                "Inventario inválido."
            )

        self.inventario_total = inventario
        self.inventario_disponible = inventario

    # --------------------------------------------------------
    # VALIDACIÓN DE CANTIDAD DE EQUIPOS
    # --------------------------------------------------------

    def validar_parametros(self, **kwargs):

        cantidad = kwargs.get("cantidad")

        if (
            not isinstance(cantidad, int)
            or isinstance(cantidad, bool)
            or cantidad <= 0
        ):

            raise DatosInvalidosError(
                "Debe indicar una cantidad positiva de equipos."
            )

        if cantidad > self.inventario_disponible:

            raise ServicioNoDisponibleError(
                "Inventario insuficiente."
            )

        return True

    # --------------------------------------------------------
    # CÁLCULO DEL COSTO
    # --------------------------------------------------------

    def calcular_costo(self, duracion, **kwargs):

        self.validar_parametros(**kwargs)

        if (
            not isinstance(duracion, (int, float))
            or isinstance(duracion, bool)
            or duracion <= 0
        ):

            raise DatosInvalidosError(
                "Duración inválida."
            )

        cantidad = kwargs["cantidad"]

        return round(
            self.tarifa_base * duracion * cantidad,
            2
        )

    # --------------------------------------------------------
    # DESCONTAR INVENTARIO
    # --------------------------------------------------------

    def reservar_inventario(self, cantidad):

        self.validar_parametros(cantidad=cantidad)

        self.inventario_disponible -= cantidad

    # --------------------------------------------------------
    # DEVOLVER INVENTARIO
    # --------------------------------------------------------

    def liberar_inventario(self, cantidad):

        self.inventario_disponible = min(
            self.inventario_total,
            self.inventario_disponible + cantidad
        )

    # --------------------------------------------------------
    # DESCRIPCIÓN DEL SERVICIO
    # --------------------------------------------------------

    def describir(self):

        return (
            f"Equipos: ${self.tarifa_base:,.0f}/día; "
            f"disponibles {self.inventario_disponible}."
        )


# ============================================================
# SERVICIO 3: ASESORÍA ESPECIALIZADA
# ============================================================

class AsesoriaEspecializada(Servicio):

    """
    Servicio de asesoría profesional.
    El costo depende del nivel de complejidad.
    """

    # Multiplicadores según el nivel de asesoría.
    MULTIPLICADORES = {

        "basico": 1.0,
        "intermedio": 1.35,
        "avanzado": 1.75

    }

    def __init__(self, codigo, tarifa_hora):

        super().__init__(
            codigo,
            "Asesoría especializada",
            tarifa_hora
        )

    # --------------------------------------------------------
    # VALIDACIÓN DEL NIVEL DE ASESORÍA
    # --------------------------------------------------------

    def validar_parametros(self, **kwargs):

        nivel = kwargs.get("nivel")

        if (
            not isinstance(nivel, str)
            or nivel.strip().lower() not in self.MULTIPLICADORES
        ):

            raise DatosInvalidosError(
                "Nivel inválido: use básico, intermedio o avanzado."
            )

        return True

    # --------------------------------------------------------
    # CÁLCULO DEL COSTO
    # --------------------------------------------------------

    def calcular_costo(self, duracion, **kwargs):

        self.validar_parametros(**kwargs)

        if (
            not isinstance(duracion, (int, float))
            or isinstance(duracion, bool)
            or duracion <= 0
        ):

            raise DatosInvalidosError(
                "Duración inválida."
            )

        nivel = kwargs["nivel"].strip().lower()

        multiplicador = self.MULTIPLICADORES[nivel]

        return round(
            self.tarifa_base * duracion * multiplicador,
            2
        )

    # --------------------------------------------------------
    # DESCRIPCIÓN DEL SERVICIO
    # --------------------------------------------------------

    def describir(self):

        return (
            "Asesoría por hora con niveles "
            "básico, intermedio y avanzado."
        )

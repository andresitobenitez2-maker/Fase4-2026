# ============================================================
# SOFTWARE FJ
# Archivo: excepciones.py
# Definición de excepciones personalizadas
# ============================================================


# ------------------------------------------------------------
# EXCEPCIÓN PRINCIPAL DEL SISTEMA
# ------------------------------------------------------------

class ErrorSistema(Exception):

    """
    Clase base para todas las excepciones
    personalizadas de Software FJ.
    """

    pass


# ------------------------------------------------------------
# ERROR POR DATOS INCORRECTOS
# ------------------------------------------------------------

class DatosInvalidosError(ErrorSistema):

    """
    Se genera cuando un dato no cumple
    con las validaciones establecidas.
    """

    pass


# ------------------------------------------------------------
# ERROR POR CLIENTES DUPLICADOS
# ------------------------------------------------------------

class ClienteDuplicadoError(ErrorSistema):

    """
    Se genera cuando se intenta registrar
    un cliente que ya existe.
    """

    pass


# ------------------------------------------------------------
# ERROR POR SERVICIOS DUPLICADOS
# ------------------------------------------------------------

class ServicioDuplicadoError(ErrorSistema):

    """
    Se genera cuando se intenta agregar
    un servicio con un código existente.
    """

    pass


# ------------------------------------------------------------
# ERROR POR RESERVAS DUPLICADAS
# ------------------------------------------------------------

class ReservaDuplicadaError(ErrorSistema):

    """
    Se genera cuando se intenta crear
    una reserva con un identificador repetido.
    """

    pass


# ------------------------------------------------------------
# ERROR POR SERVICIO NO DISPONIBLE
# ------------------------------------------------------------

class ServicioNoDisponibleError(ErrorSistema):

    """
    Se genera cuando el servicio solicitado
    no tiene disponibilidad suficiente.
    """

    pass


# ------------------------------------------------------------
# ERROR POR RESERVA INCORRECTA
# ------------------------------------------------------------

class ReservaInvalidaError(ErrorSistema):

    """
    Se genera cuando una reserva contiene
    información o asociaciones incorrectas.
    """

    pass


# ------------------------------------------------------------
# ERROR POR OPERACIÓN NO PERMITIDA
# ------------------------------------------------------------

class OperacionNoPermitidaError(ErrorSistema):

    """
    Se genera cuando se intenta realizar
    una operación que no corresponde al
    estado actual de la reserva.
    """

    pass


# ------------------------------------------------------------
# ERROR POR RECURSO NO ENCONTRADO
# ------------------------------------------------------------

class RecursoNoEncontradoError(ErrorSistema):

    """
    Se genera cuando no se encuentra
    un cliente, servicio o reserva solicitado.
    """

    pass

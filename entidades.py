# ============================================================
# SOFTWARE FJ
# Archivo: entidades.py
# Abstracción y encapsulamiento de entidades
# ============================================================

# Importación de herramientas para crear clases abstractas.
from abc import ABC, abstractmethod

# Expresiones regulares para validar correos electrónicos.
import re

# Importación de la excepción para datos incorrectos.
from sistema.excepciones import DatosInvalidosError


# ------------------------------------------------------------
# CLASE ABSTRACTA ENTIDAD
# ------------------------------------------------------------

class Entidad(ABC):

    """
    Clase abstracta que representa una entidad general
    dentro del sistema Software FJ.
    """

    def __init__(self, identificador):

        # Validación del identificador.
        if not isinstance(identificador, str) or not identificador.strip():

            raise DatosInvalidosError(
                "El identificador es obligatorio."
            )

        # Atributo protegido: se utiliza internamente
        # y puede heredarse por las clases derivadas.
        self._identificador = identificador.strip()

    # --------------------------------------------------------
    # PROPIEDAD PARA CONSULTAR EL IDENTIFICADOR
    # --------------------------------------------------------

    @property
    def identificador(self):

        return self._identificador

    # --------------------------------------------------------
    # MÉTODO ABSTRACTO
    # --------------------------------------------------------

    @abstractmethod
    def mostrar_informacion(self):

        """
        Obliga a las clases derivadas a implementar
        su propia forma de mostrar información.
        """

        pass


# ------------------------------------------------------------
# CLASE CLIENTE
# ------------------------------------------------------------

class Cliente(Entidad):

    """
    Representa a los clientes que contratan servicios
    ofrecidos por Software FJ.
    """

    def __init__(self, identificador, nombre, correo, telefono):

        # Se inicializa la clase padre Entidad.
        super().__init__(identificador)

        # Se asignan los datos utilizando propiedades.
        # Esto permite ejecutar las validaciones.
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    # --------------------------------------------------------
    # VALIDACIÓN Y ENCAPSULAMIENTO DEL NOMBRE
    # --------------------------------------------------------

    @property
    def nombre(self):

        return self.__nombre

    @nombre.setter
    def nombre(self, valor):

        if not isinstance(valor, str) or len(valor.strip()) < 3:

            raise DatosInvalidosError(
                "El nombre debe tener al menos 3 caracteres."
            )

        self.__nombre = valor.strip()

    # --------------------------------------------------------
    # VALIDACIÓN Y ENCAPSULAMIENTO DEL CORREO
    # --------------------------------------------------------

    @property
    def correo(self):

        return self.__correo

    @correo.setter
    def correo(self, valor):

        if not isinstance(valor, str):

            raise DatosInvalidosError(
                "El correo debe ser texto."
            )

        valor = valor.strip().lower()

        # Verifica que el correo tenga una estructura válida.
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", valor):

            raise DatosInvalidosError(
                "El correo no tiene un formato válido."
            )

        self.__correo = valor

    # --------------------------------------------------------
    # VALIDACIÓN Y ENCAPSULAMIENTO DEL TELÉFONO
    # --------------------------------------------------------

    @property
    def telefono(self):

        return self.__telefono

    @telefono.setter
    def telefono(self, valor):

        if not isinstance(valor, str):

            raise DatosInvalidosError(
                "El teléfono debe ser texto."
            )

        # Se eliminan espacios y guiones.
        limpio = valor.strip().replace(" ", "").replace("-", "")

        # Se permite el símbolo + para números internacionales.
        digitos = limpio[1:] if limpio.startswith("+") else limpio

        # Se verifica que solamente contenga números
        # y que tenga una longitud permitida.
        if not digitos.isdigit() or not 7 <= len(digitos) <= 15:

            raise DatosInvalidosError(
                "El teléfono debe tener entre 7 y 15 dígitos."
            )

        self.__telefono = limpio

    # --------------------------------------------------------
    # IMPLEMENTACIÓN DEL MÉTODO ABSTRACTO
    # --------------------------------------------------------

    def mostrar_informacion(self):

        """
        Devuelve la información del cliente
        en un formato organizado.
        """

        return (
            f"{self.identificador} | "
            f"{self.nombre} | "
            f"{self.correo} | "
            f"{self.telefono}"
        )

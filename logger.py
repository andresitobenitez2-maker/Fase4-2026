# ============================================================
# SOFTWARE FJ
# Archivo: logger.py
# Configuración del registro de eventos y errores
# ============================================================

# Importación de la biblioteca de registro de Python.
import logging

# Permite trabajar con rutas y carpetas del sistema.
from pathlib import Path


# ------------------------------------------------------------
# CONFIGURACIÓN DE LA CARPETA DE LOGS
# ------------------------------------------------------------

# Se obtiene la ruta de la carpeta principal del proyecto.
carpeta = Path(__file__).resolve().parent.parent / "logs"

# Si la carpeta no existe, se crea automáticamente.
carpeta.mkdir(
    parents=True,
    exist_ok=True
)


# ------------------------------------------------------------
# CONFIGURACIÓN DEL ARCHIVO DE REGISTRO
# ------------------------------------------------------------

# Nombre y ubicación del archivo de logs.
archivo = carpeta / "software_fj.log"


# ------------------------------------------------------------
# CREACIÓN DEL LOGGER PRINCIPAL
# ------------------------------------------------------------

# Se crea un registrador identificado como SoftwareFJ.
logger = logging.getLogger("SoftwareFJ")

# Se establece el nivel mínimo de registro.
logger.setLevel(logging.INFO)


# ------------------------------------------------------------
# CONFIGURACIÓN DE LOS FORMATOS Y DESTINOS
# ------------------------------------------------------------

# Evita agregar manejadores repetidos si el módulo
# se importa varias veces.
if not logger.handlers:

    # Define el formato de los mensajes.
    formato = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    # --------------------------------------------------------
    # REGISTRO EN ARCHIVO
    # --------------------------------------------------------

    # Crea un manejador que escribe los eventos en el archivo.
    fh = logging.FileHandler(
        archivo,
        encoding="utf-8"
    )

    fh.setFormatter(formato)

    # --------------------------------------------------------
    # REGISTRO EN CONSOLA
    # --------------------------------------------------------

    # Crea un manejador para mostrar advertencias y errores.
    sh = logging.StreamHandler()

    sh.setLevel(logging.WARNING)

    sh.setFormatter(formato)

    # --------------------------------------------------------
    # ASOCIACIÓN DE LOS MANEJADORES
    # --------------------------------------------------------

    # El logger utilizará ambos destinos.
    logger.addHandler(fh)

    logger.addHandler(sh)

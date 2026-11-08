# ============================================================
# SOFTWARE FJ
# JHOJAN ANDRES CHIA BENITEZ 
# CODIGO: 1052378611
# CURSO: 213023_238
# Archivo: main.py
# Punto de entrada principal de la aplicación
# ============================================================

# Importación de la interfaz gráfica.
from gui import iniciar_gui

# Importación del sistema de registro de eventos.
from sistema.logger import logger


# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================

def main():

    """
    Función principal encargada de iniciar
    el sistema integral de Software FJ.
    """

    try:

        # Registra el inicio de la aplicación.
        logger.info(
            "Iniciando el sistema Software FJ."
        )

        print("======================================")
        print("       SISTEMA SOFTWARE FJ")
        print("======================================")
        print("Iniciando interfaz gráfica...")
        
        # Inicia la ventana principal de Tkinter.
        iniciar_gui()

    except KeyboardInterrupt:

        # Controla una interrupción manual del programa.
        logger.warning(
            "Ejecución interrumpida por el usuario."
        )

        print("\nEjecución interrumpida por el usuario.")

    except Exception as error:

        # Registra cualquier error inesperado.
        logger.exception(
            "Error crítico durante el inicio de Software FJ."
        )

        print("\nNo fue posible iniciar el sistema.")
        print("Detalle del error:", error)

    finally:

        # Este bloque se ejecuta independientemente
        # de si la aplicación termina correctamente o falla.
        logger.info(
            "Finalización del proceso principal de Software FJ."
        )

        print("\n======================================")
        print("       FIN DEL PROCESO SOFTWARE FJ")
        print("======================================")


# ============================================================
# PUNTO DE EJECUCIÓN DEL PROGRAMA
# ============================================================

if __name__ == "__main__":

    main()


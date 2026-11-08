# ============================================================
# SOFTWARE FJ
# Sistema Integral de Gestión de Clientes, Servicios y Reservas
# Archivo principal: main.py
# ============================================================

# Importación de las clases y módulos necesarios.
from sistema.entidades import Cliente

from sistema.servicios import (
    ReservaSala,
    AlquilerEquipos,
    AsesoriaEspecializada
)

from sistema.reservas import Reserva
from sistema.gestor import GestorSoftwareFJ
from sistema.excepciones import ErrorSistema
from sistema.logger import logger


# ------------------------------------------------------------
# FUNCIÓN PARA EJECUTAR OPERACIONES DE FORMA SEGURA
# ------------------------------------------------------------

def ejecutar(numero, descripcion, accion):

    print(f"\nOPERACIÓN {numero}: {descripcion}")

    try:
        # Ejecuta la operación recibida como parámetro.
        resultado = accion()

    except ErrorSistema as error:
        # Captura errores personalizados del sistema.
        logger.exception(
            "Error controlado en operación %s", numero
        )

        print(f"[ERROR CONTROLADO] {error}")

    except Exception as error:
        # Captura cualquier error inesperado.
        logger.exception(
            "Error inesperado en operación %s", numero
        )

        try:
            # Encadenamiento de excepciones:
            # conserva el error original como causa.
            raise ErrorSistema(
                "Error inesperado durante la operación."
            ) from error

        except ErrorSistema as encadenada:

            logger.exception("Excepción encadenada")

            print(f"[ERROR CONTROLADO] {encadenada}")

    else:
        # Se ejecuta únicamente cuando no ocurre ningún error.
        print(f"[OK] {resultado}")

    finally:
        # Se ejecuta siempre, exista o no una excepción.
        print("Fin de operación; el sistema continúa.")


# ------------------------------------------------------------
# FUNCIÓN PRINCIPAL DEL PROGRAMA
# ------------------------------------------------------------

def main():

    print("=" * 65)
    print("SOFTWARE FJ - GESTIÓN DE CLIENTES, SERVICIOS Y RESERVAS")
    print("=" * 65)

    # Se crea el administrador general del sistema.
    gestor = GestorSoftwareFJ()

    # --------------------------------------------------------
    # 1. REGISTRO DE CLIENTES
    # --------------------------------------------------------

    c1 = Cliente(
        "C001",
        "Andrés Benítez",
        "andres@email.com",
        "3001234567"
    )

    c2 = Cliente(
        "C002",
        "Laura Gómez",
        "laura@email.com",
        "3107654321"
    )

    ejecutar(
        1,
        "Registrar primer cliente",
        lambda: gestor.registrar_cliente(c1)
    )

    ejecutar(
        2,
        "Registrar segundo cliente",
        lambda: gestor.registrar_cliente(c2)
    )

    # Prueba de validación de correo electrónico.
    ejecutar(
        3,
        "Correo inválido",
        lambda: Cliente(
            "C003",
            "Carlos Ruiz",
            "correo_invalido",
            "3111234567"
        )
    )

    # Prueba de registro de un cliente duplicado.
    ejecutar(
        4,
        "Cliente duplicado",
        lambda: gestor.registrar_cliente(c1)
    )

    # --------------------------------------------------------
    # 2. CREACIÓN DE SERVICIOS
    # --------------------------------------------------------

    sala = ReservaSala(
        "S001",
        50000,
        20
    )

    equipos = AlquilerEquipos(
        "E001",
        30000,
        10
    )

    asesoria = AsesoriaEspecializada(
        "A001",
        80000
    )

    ejecutar(
        5,
        "Agregar sala",
        lambda: gestor.agregar_servicio(sala)
    )

    ejecutar(
        6,
        "Agregar equipos",
        lambda: gestor.agregar_servicio(equipos)
    )

    ejecutar(
        7,
        "Agregar asesoría",
        lambda: gestor.agregar_servicio(asesoria)
    )

    # Prueba de una tarifa negativa.
    ejecutar(
        8,
        "Tarifa negativa",
        lambda: ReservaSala("S002", -1000, 12)
    )

    # --------------------------------------------------------
    # 3. CREACIÓN DE RESERVAS
    # --------------------------------------------------------

    r1 = Reserva(
        "R001",
        c1,
        sala,
        3,
        {"personas": 12}
    )

    r2 = Reserva(
        "R002",
        c2,
        equipos,
        2,
        {"cantidad": 3}
    )

    r3 = Reserva(
        "R003",
        c1,
        sala,
        2,
        {"personas": 30}
    )

    r4 = Reserva(
        "R004",
        c2,
        asesoria,
        2,
        {"nivel": "avanzado"}
    )

    r5 = Reserva(
        "R005",
        c1,
        equipos,
        1,
        {"cantidad": 50}
    )

    # Función auxiliar para crear y confirmar una reserva.
    def crear_confirmar(reserva):

        gestor.crear_reserva(reserva)

        return reserva.confirmar()

    # --------------------------------------------------------
    # 4. PRUEBAS DE CONFIRMACIÓN DE RESERVAS
    # --------------------------------------------------------

    ejecutar(
        9,
        "Confirmar reserva de sala",
        lambda: crear_confirmar(r1)
    )

    ejecutar(
        10,
        "Confirmar alquiler de equipos",
        lambda: crear_confirmar(r2)
    )

    ejecutar(
        11,
        "Sala supera capacidad",
        lambda: crear_confirmar(r3)
    )

    ejecutar(
        12,
        "Asesoría avanzada",
        lambda: crear_confirmar(r4)
    )

    ejecutar(
        13,
        "Inventario insuficiente",
        lambda: crear_confirmar(r5)
    )

    # --------------------------------------------------------
    # 5. PROCESAMIENTO Y CANCELACIÓN
    # --------------------------------------------------------

    ejecutar(
        14,
        "Procesar reserva confirmada",
        lambda: r1.procesar()
    )

    ejecutar(
        15,
        "Procesar reserva pendiente",
        lambda: r3.procesar()
    )

    ejecutar(
        16,
        "Cancelar reserva pendiente",
        lambda: r3.cancelar()
    )

    # --------------------------------------------------------
    # 6. PRUEBAS DE VALIDACIONES Y BÚSQUEDAS
    # --------------------------------------------------------

    ejecutar(
        17,
        "Parámetro personas faltante",
        lambda: sala.validar_parametros()
    )

    ejecutar(
        18,
        "Buscar cliente inexistente",
        lambda: gestor.buscar_cliente("C999")
    )

    # --------------------------------------------------------
    # 7. PRUEBA DE CÁLCULO DE COSTOS
    # --------------------------------------------------------

    ejecutar(
        19,
        "Calcular asesoría con impuesto y descuento",

        lambda: asesoria.calcular_con_impuesto(
            2,
            nivel="intermedio",
            descuento=0.10
        )
    )

    # --------------------------------------------------------
    # 8. PRUEBA DE ENCADENAMIENTO DE EXCEPCIONES
    # --------------------------------------------------------

    ejecutar(
        20,
        "Demostrar raise from",
        lambda: 10 / 0
    )

    # --------------------------------------------------------
    # 9. RESUMEN FINAL
    # --------------------------------------------------------

    print("\nRESUMEN FINAL")

    print(gestor.resumen())

    print("\nRevise logs/software_fj.log")


# ------------------------------------------------------------
# PUNTO DE INICIO DE LA APLICACIÓN
# ------------------------------------------------------------

if __name__ == "__main__":

    main()

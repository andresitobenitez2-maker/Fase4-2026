from sistema.entidades import Cliente
from sistema.servicios import (
    ReservaSala,
    AlquilerEquipos,
    AsesoriaEspecializada
)
from sistema.reservas import Reserva
from sistema.gestor import GestorSoftwareFJ
from sistema.excepciones import ErrorSistema, DatosInvalidosError
from sistema.logger import logger


def ejecutar_operacion(numero, descripcion, funcion):
    """
    Ejecuta una operación y controla los errores
    para evitar que el programa se detenga.
    """
    print(f"\nOPERACIÓN {numero}: {descripcion}")

    try:
        resultado = funcion()

    except ErrorSistema as error:
        logger.exception(
            "Error controlado en operación %s: %s",
            numero,
            error
        )
        print(f"[ERROR CONTROLADO] {error}")

    except Exception as error:
        logger.exception(
            "Error inesperado en operación %s: %s",
            numero,
            error
        )

        try:
            raise ErrorSistema(
                "Se produjo un error inesperado durante la operación."
            ) from error

        except ErrorSistema as encadenada:
            logger.exception("Excepción encadenada")
            print(f"[ERROR INESPERADO CONTROLADO] {encadenada}")

    else:
        print(f"[OK] {resultado}")

    finally:
        print("Fin de la operación; el sistema continúa.")


def main():

    print("=" * 65)
    print(" SOFTWARE FJ - GESTIÓN DE CLIENTES, SERVICIOS Y RESERVAS")
    print("=" * 65)

    gestor = GestorSoftwareFJ()

    # OPERACIÓN 1: Registro correcto de cliente
    cliente1 = Cliente(
        "C001",
        "Andrés Benítez",
        "andres@email.com",
        "3001234567"
    )

    ejecutar_operacion(
        1,
        "Registrar cliente válido",
        lambda: (
            gestor.registrar_cliente(cliente1),
            cliente1.mostrar_informacion()
        )[1]
    )

    # OPERACIÓN 2: Registro de segundo cliente
    cliente2 = Cliente(
        "C002",
        "Laura Gómez",
        "laura@email.com",
        "3107654321"
    )

    ejecutar_operacion(
        2,
        "Registrar segundo cliente",
        lambda: (
            gestor.registrar_cliente(cliente2),
            cliente2.mostrar_informacion()
        )[1]
    )

    # OPERACIÓN 3: Cliente con correo inválido
    def cliente_invalido():
        cliente = Cliente(
            "C003",
            "Carlos Ruiz",
            "correo_invalido",
            "3111234567"
        )

        gestor.registrar_cliente(cliente)
        return cliente.mostrar_informacion()

    ejecutar_operacion(
        3,
        "Intentar registrar cliente con correo inválido",
        cliente_invalido
    )

    # OPERACIÓN 4: Cliente duplicado
    ejecutar_operacion(
        4,
        "Intentar registrar nuevamente el cliente C001",
        lambda: gestor.registrar_cliente(cliente1)
    )

    # OPERACIÓN 5: Crear servicio de salas
    sala = ReservaSala("S001", 50000, 20)

    ejecutar_operacion(
        5,
        "Crear servicio de reserva de sala",
        lambda: (
            gestor.agregar_servicio(sala),
            sala.describir()
        )[1]
    )

    # OPERACIÓN 6: Crear servicio de equipos
    equipos = AlquilerEquipos("E001", 30000, 10)

    ejecutar_operacion(
        6,
        "Crear servicio de alquiler de equipos",
        lambda: (
            gestor.agregar_servicio(equipos),
            equipos.describir()
        )[1]
    )

    # OPERACIÓN 7: Crear servicio de asesorías
    asesoria = AsesoriaEspecializada("A001", 80000)

    ejecutar_operacion(
        7,
        "Crear servicio de asesoría especializada",
        lambda: (
            gestor.agregar_servicio(asesoria),
            asesoria.describir()
        )[1]
    )

    # OPERACIÓN 8: Crear servicio con tarifa negativa
    ejecutar_operacion(
        8,
        "Intentar crear servicio con tarifa negativa",
        lambda: ReservaSala("S002", -1000, 12)
    )

    # OPERACIÓN 9: Reserva correcta de sala
    reserva1 = Reserva(
        "R001",
        cliente1,
        sala,
        3,
        {"personas": 12}
    )

    def confirmar_reserva1():
        gestor.crear_reserva(reserva1)
        reserva1.confirmar()

        return (
            f"{reserva1.mostrar_informacion()} | "
            f"Total con impuesto: "
            f"${sala.calcular_con_impuesto(3):,.2f}"
        )

    ejecutar_operacion(
        9,
        "Crear y confirmar reserva de sala",
        confirmar_reserva1
    )

    # OPERACIÓN 10: Reserva correcta de equipos
    reserva2 = Reserva(
        "R002",
        cliente2,
        equipos,
        2,
        {"cantidad": 3}
    )

    def confirmar_reserva2():
        gestor.crear_reserva(reserva2)

        return (
            f"{reserva2.confirmar():,.2f} - "
            f"{reserva2.mostrar_informacion()}"
        )

    ejecutar_operacion(
        10,
        "Crear y confirmar alquiler de equipos",
        confirmar_reserva2
    )

    # OPERACIÓN 11: Exceso de capacidad de sala
    reserva3 = Reserva(
        "R003",
        cliente1,
        sala,
        2,
        {"personas": 30}
    )

    def confirmar_reserva3():
        gestor.crear_reserva(reserva3)
        return reserva3.confirmar()

    ejecutar_operacion(
        11,
        "Intentar reservar sala con exceso de personas",
        confirmar_reserva3
    )

    # OPERACIÓN 12: Asesoría avanzada
    reserva4 = Reserva(
        "R004",
        cliente2,
        asesoria,
        2,
        {"nivel": "avanzado"}
    )

    def confirmar_reserva4():
        gestor.crear_reserva(reserva4)

        return (
            f"Costo: ${reserva4.confirmar():,.2f}"
        )

    ejecutar_operacion(
        12,
        "Confirmar asesoría especializada avanzada",
        confirmar_reserva4
    )

    # OPERACIÓN 13: Inventario insuficiente
    reserva5 = Reserva(
        "R005",
        cliente1,
        equipos,
        1,
        {"cantidad": 50}
    )

    def confirmar_reserva5():
        gestor.crear_reserva(reserva5)
        return reserva5.confirmar()

    ejecutar_operacion(
        13,
        "Intentar alquilar equipos sin inventario suficiente",
        confirmar_reserva5
    )

    # OPERACIÓN 14: Procesar reserva confirmada
    ejecutar_operacion(
        14,
        "Procesar reserva R001",
        lambda: (
            reserva1.procesar(),
            reserva1.mostrar_informacion()
        )[1]
    )

    # OPERACIÓN 15: Procesar reserva no confirmada
    ejecutar_operacion(
        15,
        "Intentar procesar reserva R003 no confirmada",
        lambda: reserva3.procesar()
    )

    # OPERACIÓN 16: Cancelar reserva pendiente
    ejecutar_operacion(
        16,
        "Cancelar reserva R003",
        lambda: (
            reserva3.cancelar(),
            reserva3.estado.value
        )[1]
    )

    # OPERACIÓN 17: Parámetro obligatorio faltante
    ejecutar_operacion(
        17,
        "Validar reserva sin parámetro de personas",
        lambda: sala.validar_parametros()
    )

    # OPERACIÓN 18: Buscar cliente inexistente
    ejecutar_operacion(
        18,
        "Buscar cliente inexistente",
        lambda: gestor.buscar_cliente("C999")
    )

    # OPERACIÓN 19: Demostración try/except/else/finally
    print(
        "\nOPERACIÓN 19: "
        "Demostración de try/except/else/finally"
    )

    try:
        total = asesoria.calcular_costo(
            1,
            nivel="intermedio"
        )

    except DatosInvalidosError as error:
        logger.exception(
            "Error en cálculo demostrativo: %s",
            error
        )
        print(error)

    else:
        print(
            f"Cálculo correcto de asesoría intermedia: "
            f"${total:,.2f}"
        )

    finally:
        print("Bloque finally ejecutado.")

    # RESUMEN FINAL
    print("\n" + "=" * 65)
    print("RESUMEN FINAL")
    print(gestor.resumen())

    print(
        "Las operaciones finalizaron. "
        "Revise logs/software_fj.log"
    )

    print("=" * 65)


if __name__ == "__main__":
    main()

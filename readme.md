# Fase-4_Programacion
Fase 4 - Componente práctico - Prácticas simuladas

Sistema de Gestión de Reservas - Software FJ
Este proyecto es una aplicación de escritorio desarrollada en Python utilizando la librería Tkinter. El sistema permite gestionar clientes y servicios (Salas, Equipos y Asesorías) aplicando los pilares de la Programación Orientada a Objetos (POO).

# Estructura del Proyecto
El sistema está dividido en los siguientes módulos:

main.py: Punto de entrada que ejecuta pruebas automáticas y lanza la interfaz.

gui.py: Gestión de la interfaz gráfica y eventos de usuario.

cliente.py: Lógica para el registro y búsqueda de clientes.

servicio.py: Definición de servicios (Clase abstracta, Herencia y Polimorfismo).

reserva.py: Vinculación entre clientes y servicios.

errores.py: Excepciones personalizadas para el control de fallos.

logs.py: Registro de eventos y errores en el archivo sistema.log

# Características Principales
Validación de Datos: El sistema evita errores cuando los campos de horas o días se dejan vacíos.

Pruebas Automatizadas: Al iniciar, el sistema ejecuta 10 operaciones en consola para verificar la lógica de negocio.

Persistencia de Logs: Todas las acciones importantes se guardan con fecha y hora en un archivo de texto.

POO Avanzada: Uso de Clases Abstractas, Herencia```bash
python main.py

# Requisitos
Python 3.x

Librería estándar tkinter

# Instrucciones de Uso
Asegúrate de tener todos los Funcionalidades Principales

Registro de Clientes: Validación de datos (cédula numérica, correo con @).

Gest archivos .py en la misma carpeta.

Ejecuta el comando: main.py.

Observa enión de Sesiones: Login y Logout para manejar reservas por usuario.

Cálculo Automático: Los precios se calculan según las horas o días ingres la consola los resultados de las 10 pruebas automáticas.

Usa la ventana de la aplicación para registrar un cliente, iniciar sesión y crear reservasados.

Validación de Entradas: El sistema evita errores si se dejan campos vacíos o se ingresan datos inválidos.

# Autores
JHOJAN ANDRES CHIA BENITEZ
YURLEY CAROLINA HERNANDEZ MOLINA
# Institución
UNIVERSIDAD NACIONAL ABIERTA Y A DISNACIA (UNAD)

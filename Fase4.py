"""
=============================================================================
 Universidad Nacional Abierta y a Distancia - UNAD
 Escuela de Ciencias Básicas, Tecnología e Ingeniería - ECBTI
 Programa: Ingeniería electronica
 Curso: Programación (Código: 213023)
 Grupo / Período: 2204
 Actividad: Fase 4 - Componente práctico - Prácticas simuladas
 Ejercicio: Sistema Integral de Gestión de Clientes, Servicios y Reservas (Software FJ)
 Estudiante: Juan de la Cruz Durango Uribe y Jakeline Alzate Gómez
=============================================================================
"""

# ==========================================================
# IMPORTACIÓN DE LIBRERÍAS
# ==========================================================

import logging
import re
from abc import ABC, abstractmethod
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

# ==========================================================
# CONFIGURACIÓN DEL SISTEMA DE REGISTRO DE EVENTOS (LOGS)
# ==========================================================

# Se configura un archivo para almacenar los eventos y errores que ocurran durante la ejecución del programa.

logging.basicConfig(
    filename='app_errors.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ==========================================
# 1. EXCEPCIONES PERSONALIZADAS Y ENCADENAMIENTO
# ==========================================

# Clase base para centralizar las excepciones propias del sistema.
# HERENCIA: hereda de Exception, que es la clase general de errores

class SoftwareFJException(Exception):
    """Excepción base para el sistema de Software FJ."""
    pass

# HERENCIA: cada excepción especializada hereda de SoftwareFJException.
# Esto permite identificar y controlar diferentes tipos de errores
# relacionados con los clientes, servicios y reservas.

class ErrorClienteInvalido(SoftwareFJException):
    """Se utiliza cuando los datos de un cliente no son válidos."""
    pass

class ErrorServicioInvalido(SoftwareFJException):
    """Se utiliza cuando los datos o parámetros de un servicio son incorrectos."""
    pass

class ErrorReservaInvalido(SoftwareFJException):
    """Se utiliza cuando ocurre un problema durante la gestión de una reserva."""
    pass

# ==========================================
# 2. CLASES ABSTRACTAS Y ENTIDADES
# ==========================================

# ABSTRACCIÓN:
# EntidadBase define las características y comportamientos generales que deben compartir las entidades principales del sistema.
# Al ser una clase abstracta, no está diseñada para crear objetos directamente, sino para servir como base de otras clases.

class EntidadBase(ABC):
    def __init__(self, identificador: str):
        # Se almacena el identificador de la entidad.
        # El guion bajo indica que es un atributo protegido por convención.
        self._identificador = identificador

    # ENCAPSULAMIENTO:
    # La propiedad permite consultar el identificador mediante un método de acceso, sin tener que acceder directamente al atributo interno.
    @property
    def identificador(self):
        return self._identificador

    # ABSTRACCIÓN:
    # Este método abstracto establece que las clases derivadas deben implementar su propia forma de mostrar la información.
    @abstractmethod
    def obtener_detalle(self) -> str:
        pass

# HERENCIA:
# Cliente hereda de EntidadBase y reutiliza su identificador y la estructura general definida para las entidades del sistema.

class Cliente(EntidadBase):
    def __init__(self, identificador: str, nombre: str, email: str, telefono: str):
        # Se llama al constructor de la clase padre para inicializar el identificador heredado.
        super().__init__(identificador)

        # Se asignan los datos mediante propiedades. Esto permite que las validaciones se ejecuten automáticamente.
        self.nombre = nombre
        self.email = email
        self.telefono = telefono

    # ENCAPSULAMIENTO:
    # @property permite consultar el nombre sin acceder directamente al atributo privado __nombre.
    @property
    def nombre(self):
        return self.__nombre

    # El setter controla la modificación del nombre y evita almacenar valores vacíos o nombres con menos de tres caracteres.
    @nombre.setter
    def nombre(self, valor):
        if not valor or len(valor.strip()) < 3:
            raise ErrorClienteInvalido("Client name is invalid (minimum 3 characters required).")
        self.__nombre = valor.strip()

    # ENCAPSULAMIENTO:
    # Se define una propiedad para consultar el correo electrónico.
    @property
    def email(self):
        return self.__email

    # Se valida el formato del correo antes de almacenarlo.
    @email.setter
    def email(self, valor):
        patron_email = r"^[\w\.-]+@[\w\.-]+\.\w+$"
     
        if not re.match(patron_email, valor):
            raise ErrorClienteInvalido("Email address format is strictly invalid.")
        self.__email = valor.strip()

    # ENCAPSULAMIENTO:
    # Propiedad para consultar el número telefónico.
    @property
    def telefono(self):
        return self.__telefono

    # Se verifica que el teléfono contenga únicamente números y tenga una longitud entre 7 y 15 dígitos.
    @telefono.setter
    def telefono(self, valor):
        if not valor.isdigit() or not (7 <= len(valor) <= 15):
            raise ErrorClienteInvalido("Phone number must contain only digits (7 to 15 characters).")
        self.__telefono = valor.strip()

    # POLIMORFISMO:
    # Se implementa el método abstracto heredado de EntidadBase. Esta versión muestra la información específica de un cliente.
    def obtener_detalle(self) -> str:
        return f"Customer [ID: {self._identificador}, Name: {self.__nombre}, Email: {self.__email}]"

# ==========================================================
# CLASE ABSTRACTA SERVICIO                         
# ==========================================================

# ABSTRACCIÓN Y HERENCIA MÚLTIPLE:
# Servicio hereda de EntidadBase y ABC.
# Define las características comunes de los servicios del sistema y establece los métodos que deben implementar sus clases derivadas.
class Servicio(EntidadBase, ABC):
    def __init__(self, identificador: str, descripcion: str, costo_base: float):

        # HERENCIA:
        # Se utiliza super() para inicializar el identificador heredado de EntidadBase.
        super().__init__(identificador)
        self.descripcion = descripcion
        self.costo_base = costo_base

    # ENCAPSULAMIENTO:
    # La propiedad permite consultar el costo base sin acceder directamente al atributo interno __costo_base.
    @property
    def costo_base(self):
        return self.__costo_base

    # Se valida que el costo base sea numérico y positivo antes de almacenarlo.
    @costo_base.setter
    def costo_base(self, valor):
        if not isinstance(valor, (int, float)) or valor <= 0:
            raise ErrorServicioInvalido("Base cost must be a positive number greater than zero.")
        self.__costo_base = float(valor)

    # ABSTRACCIÓN:
    # Este método obliga a las clases derivadas a implementar su propia fórmula para calcular el costo del servicio.
    @abstractmethod
    def calcular_costo(self) -> float:
        pass

    # ABSTRACCIÓN:
    # Cada tipo de servicio debe definir las validaciones específicas que necesita para funcionar correctamente.
    @abstractmethod
    def validar_parametros(self) -> bool:
        pass


# ==========================================
# 3. SERVICIOS ESPECIALIZADOS (Polimorfismo)
# ==========================================

# HERENCIA:
# ReservaSala hereda los atributos y métodos de Servicio.
# Representa el servicio de reserva de salas de reuniones.
class ReservaSala(Servicio):
    def __init__(self, identificador: str, descripcion: str, costo_base: float, capacidad: int):
     
        # Se inicializan los atributos heredados de Servicio.
        super().__init__(identificador, descripcion, costo_base)
        # Atributo propio de las reservas de salas.
        self.capacidad = capacidad

    # VALIDACIÓN:
    # Comprueba que la capacidad de la sala sea mayor que cero.
    def validar_parametros(self) -> bool:
        if self.capacidad <= 0:
            raise ErrorServicioInvalido("Room capacity must be greater than zero.")
        return True

    # POLIMORFISMO:
    # Se implementa calcular_costo() con una fórmula propia para las reservas de salas, aplicando descuento e impuesto.
    def calcular_costo(self, descuento: float = 0.0, impuesto: float = 1.19) -> float:
        self.validar_parametros()
        costo_con_descuento = self.costo_base * (1 - descuento)
        return round(costo_con_descuento * impuesto, 2)

    # POLIMORFISMO:
    # Implementa obtener_detalle() mostrando información específica de una reserva de sala.
    def obtener_detalle(self) -> str:
        return f"Room Reservation: {self.descripcion} (Capacity: {self.capacidad} people)"

# HERENCIA: 
# AlquilerEquipo hereda de Servicio y representa el alquiler de equipos tecnológicos por una cantidad determinada de días.
class AlquilerEquipo(Servicio):
    def __init__(self, identificador: str, descripcion: str, costo_base: float, dias: int):

        # Se inicializan los atributos heredados.
        super().__init__(identificador, descripcion, costo_base)
        # Atributo propio que indica la duración del alquiler.
        self.dias = dias

    # VALIDACIÓN:
    # Comprueba que la cantidad de días de alquiler sea positiva.
    def validar_parametros(self) -> bool:
        if self.dias <= 0:
            raise ErrorServicioInvalido("Rental days must be greater than zero.")
        return True

    # POLIMORFISMO:
    # Implementa el cálculo del costo para el alquiler de equipos.
    # Multiplica el costo diario por los días de alquiler y suma el valor adicional del seguro, si se proporciona.
    def calcular_costo(self, seguro: float = 0.0) -> float:
        self.validar_parametros()
        return round((self.costo_base * self.dias) + seguro, 2)

    # POLIMORFISMO:
    # Muestra los detalles particulares del alquiler de equipos.
    def obtener_detalle(self) -> str:
        return f"Equipment Rental: {self.descripcion} (Days: {self.dias})"

# HERENCIA: 
# AsesoriaEspecializada hereda de Servicio y representa los servicios de asesoría técnica especializada.
class AsesoriaEspecializada(Servicio):
    def __init__(self, identificador: str, descripcion: str, costo_base: float, horas: int):

        # Se inicializan los atributos heredados.
        super().__init__(identificador, descripcion, costo_base)
        # Atributo propio que indica la duración de la asesoría.
        self.horas = horas

    # VALIDACIÓN:
    # Comprueba que la cantidad de horas de asesoría sea positiva.
    def validar_parametros(self) -> bool:
        if self.horas <= 0:
            raise ErrorServicioInvalido("Consulting hours must be greater than zero.")
        return True

    # POLIMORFISMO:
    # Implementa una fórmula propia para calcular el costo de la asesoría, según las horas contratadas y el bono especial.
    def calcular_costo(self, bono_especial: float = 0.0) -> float:
        self.validar_parametros()
        return round((self.costo_base * self.horas) + bono_especial, 2)

    # POLIMORFISMO:
    # Muestra la información específica de una asesoría especializada.
    def obtener_detalle(self) -> str:
        return f"Specialized Consulting: {self.descripcion} (Hours: {self.horas})"


# ==========================================
# 4. CLASE RESERVA Y GESTIÓN DE EXCEPCIONES
# ==========================================
class Reserva:
    # ABSTRACCIÓN:
    # Esta clase representa una reserva del sistema y reúne la información y las operaciones necesarias para gestionarla.
 
    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio):
        self.id_reserva = id_reserva
        self.cliente = cliente
        self.servicio = servicio
        self.estado = "Pending"

    # ASOCIACIÓN ENTRE OBJETOS:
    # La reserva se relaciona con objetos de las clases Cliente y Servicio, permitiendo acceder a su información.
    def confirmar(self) -> str:
        # MÉTODO PARA CONFIRMAR UNA RESERVA.
        try:
            if self.estado == "Confirmed":
               # Se genera una excepción personalizada si la reserva ya había sido confirmada anteriormente.
                raise ErrorReservaInvalido("Reservation has already been confirmed previously.")
            self.estado = "Confirmed"

            # LOGGING:
            # Registra que la operación se realizó correctamente.
            logging.info(f"Reservation {self.id_reserva} confirmed successfully.")
            return f"[SUCCESS] Reservation {self.id_reserva} confirmed for {self.cliente.nombre}."
        except ErrorReservaInvalido as e:

            # LOGGING:
            # Registra el error ocurrido durante la confirmación.
            logging.error(f"Error confirming reservation {self.id_reserva}: {e}")
         
            # ENCADENAMIENTO DE EXCEPCIONES:
            # 'raise ... from e' genera una nueva excepción y conserva la excepción original como causa del problema.
            raise ErrorReservaInvalido(f"Failed to confirm reservation {self.id_reserva}") from e

    def cancelar(self) -> str:
        # MÉTODO PARA CANCELAR UNA RESERVA.
        try:
            if self.estado == "Cancelled":
                # Evita cancelar una reserva que ya está cancelada.
                raise ErrorReservaInvalido("Reservation is already cancelled.")
             
            self.estado = "Cancelled"
         
            # LOGGING: registra la cancelación exitosa.
            logging.info(f"Reservation {self.id_reserva} cancelled successfully.")
            return f"[INFO] Reservation {self.id_reserva} has been cancelled."
         
        except Exception as e:

            # Captura y registra cualquier excepción que ocurra durante el proceso de cancelación.
            logging.error(f"Critical error cancelling reservation {self.id_reserva}: {e}")

            # ENCADENAMIENTO DE EXCEPCIONES:
            # Conserva el error original como causa de la nueva excepción.
            raise ErrorReservaInvalido(f"Critical cancellation failure for ID {self.id_reserva}") from e

    def procesar(self) -> str:
        # MÉTODO PARA PROCESAR UNA RESERVA.
        try:
            if self.estado != "Confirmed":
                # Solo se permite procesar reservas confirmadas.
                raise ErrorReservaInvalido("Only confirmed reservations can be processed.")
            self.estado = "Processed"

            # LOGGING: registra que la reserva fue procesada.
            logging.info(f"Reservation {self.id_reserva} processed successfully.")
            return f"[PROCESS] Reservation {self.id_reserva} is now fully processed."
         
        except Exception as e:
            # Registra cualquier error ocurrido durante el procesamiento.
            logging.error(f"Error processing reservation {self.id_reserva}: {e}")

            # ENCADENAMIENTO DE EXCEPCIONES:
            # Permite conocer el error original que provocó el fallo.
            raise ErrorReservaInvalido(f"Processing error on reservation {self.id_reserva}") from e


# ==========================================
# 5. INTERFAZ GRÁFICA DE USUARIO (TKINTER)
# ==========================================
class AppSoftwareFJ:

    # ABSTRACCIÓN Y ENCAPSULAMIENTO:
    # Esta clase reúne los elementos de la interfaz gráfica y las operaciones que permiten interactuar con el sistema.
    # Oculta los detalles de construcción de las ventanas mediante métodos específicos para cada sección de la aplicación.
 
    def __init__(self, root):
        # Configuración inicial de la ventana principal.
        self.root = root
        self.root.title("Software FJ - Integrated Management System (UNAD Phase 4)")
        self.root.geometry("820x620")
        self.root.config(bg="#f4f6f9")

        style = ttk.Style()
        style.theme_use("clam")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.frame_simulacion = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_simulacion, text=" Operations Simulation ")
        self.crear_pestana_simulacion()

        self.frame_interactivo = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_interactivo, text=" Interactive Customer Registration ")
        self.crear_pestana_interactiva()

    def crear_pestana_simulacion(self):
        # INTERFAZ GRÁFICA:
        # Construye la pestaña donde el usuario puede ejecutar las diez operaciones de prueba del sistema.
        titulo = tk.Label(self.frame_simulacion, text="Automated 10-Operation Simulation (Software FJ)", font=("Arial", 12, "bold"), fg="#003865")
        titulo.pack(pady=10)

        btn_ejecutar = tk.Button(self.frame_simulacion, text="Run Full Simulation", bg="#003865", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5, command=self.ejecutar_simulacion_gui)
        btn_ejecutar.pack(pady=5)

        self.texto_consola = scrolledtext.ScrolledText(self.frame_simulacion, width=90, height=25, bg="#1e1e1e", fg="#00ff00", font=("Consolas", 9))
        self.texto_consola.pack(padx=10, pady=10, fill="both", expand=True)

    def ejecutar_simulacion_gui(self):
        # SIMULACIÓN AUTOMÁTICA:
        # Ejecuta diez operaciones que permiten comprobar el funcionamiento de las clases, las validaciones y las excepciones personalizadas del sistema.
        self.texto_consola.delete(1.0, tk.END)
        self.texto_consola.insert(tk.END, "=== STARTING 10-OPERATION SIMULATION ===\n\n")
        
        operaciones_totales = 10
        for i in range(1, operaciones_totales + 1):
            self.texto_consola.insert(tk.END, f"--- Operation #{i} ---\n")
            try:
                if i == 1:
                    c1 = Cliente("C001", "Ana María Pérez", "ana.perez@email.com", "3104567890")
                    s1 = ReservaSala("S001", "North Executive Room", 150000.0, 10)
                    res1 = Reserva("R001", c1, s1)
                    msg = res1.confirmar()
                    self.texto_consola.insert(tk.END, f"{msg}\n")
                    
                    # Se procesa la reserva después de confirmar su estado.
                    # Esto permite comprobar que el método procesar() funciona correctamente cuando la reserva está confirmada.
                    msg_proceso = res1.procesar()
                    self.texto_consola.insert(tk.END, f"{msg_proceso}\n")
                    
                    self.texto_consola.insert(tk.END, f"Total cost with taxes: ${s1.calcular_costo(descuento=0.1)}\n")

                elif i == 2:
                    self.texto_consola.insert(tk.END, "Attempting to register customer with invalid email...\n")
                    Cliente("C002", "Carlos Ruiz", "invalid-email.com", "3201234567")

                elif i == 3:
                    c3 = Cliente("C003", "Lucía Gómez", "lucia.gomez@email.com", "3009876543")
                    s3 = AlquilerEquipo("S002", "HP Server Rack", 80000.0, 5)
                    res3 = Reserva("R002", c3, s3)
                    msg = res3.confirmar()
                    self.texto_consola.insert(tk.END, f"{msg}\nRental cost: ${s3.calcular_costo(seguro=25000.0)}\n")

                elif i == 4:
                    self.texto_consola.insert(tk.END, "Attempting to create service with negative cost...\n")
                    AlquilerEquipo("S003", "Cisco Switch", -500.0, 2)

                elif i == 5:
                    c5 = Cliente("C004", "Andrés Felipe Marín", "andres.marin@email.com", "3112223344")
                    s5 = AsesoriaEspecializada("S003", "AWS Cloud Architecture", 120000.0, 4)
                    res5 = Reserva("R003", c5, s5)
                    msg = res5.confirmar()
                    self.texto_consola.insert(tk.END, f"{msg}\nConsulting cost: ${s5.calcular_costo(bono_especial=50000.0)}\n")

                elif i == 6:
                    self.texto_consola.insert(tk.END, "Attempting to register customer with invalid phone number...\n")
                    Cliente("C005", "Sofía Castro", "sofia@email.com", "ABC12345")

                elif i == 7:
                    # Corrección Operación 7: Doble confirmación forzosa que dispara excepción controlada
                    c7 = Cliente("C006", "Jorge Higuita", "jorge@email.com", "3123334455")
                    s7 = ReservaSala("S004", "Creative Room", 100000.0, 6)
                    res7 = Reserva("R004", c7, s7)
                    self.texto_consola.insert(tk.END, f"{res7.confirmar()}\n")
                    self.texto_consola.insert(tk.END, "Attempting double confirmation (should trigger exception):\n")
                    res7.confirmar() # Dispara excepción porque ya estaba confirmada

                elif i == 8:
                    self.texto_consola.insert(tk.END, "Creating room with zero capacity...\n")
                    reserva_falsa = ReservaSala("S005", "Auditorium Room", 200000.0, 0)
                    reserva_falsa.validar_parametros()

                elif i == 9:
                    c9 = Cliente("C007", "Mariana Ríos", "mariana@email.com", "3156667788")
                    s9 = AlquilerEquipo("S006", "Laser Projector", 50000.0, 1)
                    res9 = Reserva("R005", c9, s9)
                    msg_cancel = res9.cancelar()
                    self.texto_consola.insert(tk.END, f"{msg_cancel}\n")

                elif i == 10:
                    self.texto_consola.insert(tk.END, "Registering customer with a very short name...\n")
                    Cliente("C008", "Al", "al@email.com", "3189990000")

            except (SoftwareFJException, ValueError, TypeError) as ex:
                # REGISTRO DE ERRORES:
                # Guarda el tipo de excepción y el mensaje generado durante la operación que presentó el problema.
                logging.warning(f"Exception caught in operation #{i}: {type(ex).__name__} - {ex}")
            
                self.texto_consola.insert(tk.END, f"[CONTROLLED EXCEPTION CAUGHT] Failed safely -> {ex}\n")
            
                # ENCADENAMIENTO DE EXCEPCIONES:
                # __cause__ permite consultar la excepción original cuando se ha utilizado la instrucción raise ... from ...
                if ex.__cause__ is not None:
                    self.texto_consola.insert(tk.END, f"[ORIGINAL CAUSE] {type(ex.__cause__).__name__}: {ex.__cause__}\n")
            else:
                self.texto_consola.insert(tk.END, f"[STATUS] Operation #{i} completed successfully.\n")
            finally:
                self.texto_consola.insert(tk.END, f"--- End of Operation #{i} cycle ---\n\n")

        self.texto_consola.insert(tk.END, "=== SIMULATION COMPLETED. CHECK 'app_errors.log' ===\n")

    def crear_pestana_interactiva(self):
        # INTERFAZ INTERACTIVA:
        # Construye un formulario para ingresar los datos de un cliente y comprobar sus validaciones desde la interfaz.
        lbl_info = tk.Label(self.frame_interactivo, text="Customer Data Validation Test", font=("Arial", 12, "bold"), fg="#003865")
        lbl_info.pack(pady=15)

        form_frame = tk.Frame(self.frame_interactivo, bg="#f4f6f9")
        form_frame.pack(pady=5)

        tk.Label(form_frame, text="Customer ID:", font=("Arial", 10), bg="#f4f6f9").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        self.ent_id = tk.Entry(form_frame, width=35)
        self.ent_id.grid(row=0, column=1, pady=5, padx=5)

        tk.Label(form_frame, text="Full Name:", font=("Arial", 10), bg="#f4f6f9").grid(row=1, column=0, sticky="w", pady=5, padx=5)
        self.ent_nombre = tk.Entry(form_frame, width=35)
        self.ent_nombre.grid(row=1, column=1, pady=5, padx=5)

        tk.Label(form_frame, text="Email Address:", font=("Arial", 10), bg="#f4f6f9").grid(row=2, column=0, sticky="w", pady=5, padx=5)
        self.ent_email = tk.Entry(form_frame, width=35)
        self.ent_email.grid(row=2, column=1, pady=5, padx=5)

        tk.Label(form_frame, text="Phone (digits only):", font=("Arial", 10), bg="#f4f6f9").grid(row=3, column=0, sticky="w", pady=5, padx=5)
        self.ent_tel = tk.Entry(form_frame, width=35)
        self.ent_tel.grid(row=3, column=1, pady=5, padx=5)

        btn_validar = tk.Button(self.frame_interactivo, text="Register & Validate Customer", bg="#28a745", fg="white", font=("Arial", 10, "bold"), padx=10, pady=5, command=self.validar_cliente_interactivo)
        btn_validar.pack(pady=20)

    def validar_cliente_interactivo(self):
        # VALIDACIÓN Y MANEJO DE EXCEPCIONES:
        # Obtiene los datos ingresados por el usuario e intenta crear un objeto Cliente. Si los datos no cumplen las condiciones establecidas, muestra el error correspondiente.
        try:
            cli = Cliente(
                self.ent_id.get(),
                self.ent_nombre.get(),
                self.ent_email.get(),
                self.ent_tel.get()
            )
            messagebox.showinfo("Success", f"Customer registered successfully:\n{cli.obtener_detalle()}")
        except SoftwareFJException as e:
            logging.warning(f"Interactive validation error: {e}")
            messagebox.showerror("Validation Error (Exception)", str(e))
        except Exception as ex:
            messagebox.showerror("Unexpected Error", str(ex))


if __name__ == "__main__":
    root = tk.Tk()
    app = AppSoftwareFJ(root)
    root.mainloop()

# ==========================================
# 6. PUNTO DE ENTRADA DEL PROGRAMA
# ==========================================

if __name__ == "__main__":
    # Crea la ventana principal de Tkinter.
    root = tk.Tk()

    # Instancia la aplicación y construye sus componentes gráficos.
    app = AppSoftwareFJ(root)

    # Mantiene activa la interfaz y espera las acciones del usuario.
    root.mainloop()

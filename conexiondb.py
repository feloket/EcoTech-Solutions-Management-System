"""Módulo conexion a la base de datos"""
import mysql.connector
from mysql.connector import Error


class Database:
    """Clase para manejar la conexión a la base de datos"""

    def __init__(self):
        self.__host = "localhost"
        self.__port = 3308
        self.__user = "root"
        self.__password = ""
        self.__database = "Ecotech_solutions_DB"
        self.__connection = None

    def conectar(self):
        """Establecer conexión con la base de datos"""
        try:
            if self.__connection is None or not self.__connection.is_connected():
                self.__connection = mysql.connector.connect(
                    host=self.__host,
                    port=self.__port,
                    user=self.__user,
                    password=self.__password,
                    database=self.__database
                )

            if self.__connection.is_connected():
                return self.__connection
        except Error as e:
            if "Unknown database" in str(e):
                print(
                    f"Base de datos '{self.__database}' no existe. Creando...")
                self._crear_base_datos()
                return self.conectar()
            else:
                raise Exception(f"Error de conexión: {e}")

    def _crear_base_datos(self):
        """Crear la base de datos si no existe"""
        try:
            temp_connection = mysql.connector.connect(
                host=self.__host,
                port=self.__port,
                user=self.__user,
                password=self.__password
            )
            cursor = temp_connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.__database}")
            cursor.close()
            temp_connection.close()
            print(f"Base de datos '{self.__database}' creada exitosamente.")
        except Error as e:
            raise Exception(f"Error al crear la base de datos: {e}")

    def create_tables(self):
        """Crea el esquema de la base de datos"""
        if self.__connection and self.__connection.is_connected():
            try:
                cursor = self.__connection.cursor()

                # Tabla Empleados
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Empleados (
                        id_empleado INT AUTO_INCREMENT PRIMARY KEY,
                        nombre VARCHAR(100) NOT NULL,
                        direccion BLOB NOT NULL,
                        telefono BLOB NOT NULL,
                        email BLOB NOT NULL,
                        fecha_contratacion DATE DEFAULT (CURRENT_DATE),
                        salario DECIMAL(10,2) NOT NULL
                    );
                """)
                self.__connection.commit()
                print("Tabla 'Empleados' creada (o ya existía).")

                # Tabla Proyectos
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Proyectos (
                        id_proyecto INT AUTO_INCREMENT PRIMARY KEY,
                        nombre VARCHAR(100) NOT NULL,
                        descripcion TEXT,
                        fecha_inicio DATE,
                        fecha_termino DATE
                    );
                """)
                self.__connection.commit()
                print("Tabla 'Proyectos' creada (o ya existía).")

                # Tabla Usuario
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Usuario (
                        id_usuario INT AUTO_INCREMENT PRIMARY KEY,
                        nombre_usuario VARCHAR(100) NOT NULL UNIQUE,
                        password_hash VARCHAR(255) NOT NULL,
                        rol VARCHAR(50),
                        id_empleado INT UNIQUE,
                        FOREIGN KEY (id_empleado) REFERENCES Empleados(id_empleado) 
                            ON DELETE CASCADE
                    );
                """)
                self.__connection.commit()
                print("Tabla 'Usuario' creada (o ya existía).")

                # Tabla Departamentos
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Departamentos (
                        id_departamento INT AUTO_INCREMENT PRIMARY KEY,
                        nombre VARCHAR(100) NOT NULL,
                        gerente VARCHAR(100),
                        id_empleado INT,
                        id_proyecto INT,
                        FOREIGN KEY (id_empleado) REFERENCES Empleados(id_empleado) 
                            ON DELETE CASCADE,
                        FOREIGN KEY (id_proyecto) REFERENCES Proyectos(id_proyecto) 
                            ON DELETE CASCADE
                    );
                """)
                self.__connection.commit()
                print("Tabla 'Departamentos' creada (o ya existía).")

                # Tabla RegistroDeTiempo
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS RegistrodeTiempo (
                        id_registro INT AUTO_INCREMENT PRIMARY KEY,
                        fecha DATE NOT NULL,
                        horas INT NOT NULL,
                        descripcion TEXT,
                        id_empleado INT NOT NULL,
                        id_proyecto INT NOT NULL,
                        FOREIGN KEY (id_empleado) REFERENCES Empleados(id_empleado)
                            ON DELETE CASCADE,
                        FOREIGN KEY (id_proyecto) REFERENCES Proyectos(id_proyecto)
                            ON DELETE CASCADE
                    );
                """)
                self.__connection.commit()
                print("Tabla 'RegistrodeTiempo' creada (o ya existía).")

                #  TABLA Indicadores Economicos
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS IndicadoresEconomicos (
                        id_indicador INT AUTO_INCREMENT PRIMARY KEY,
                        nombre_indicador VARCHAR(50) NOT NULL,
                        fecha_valor DATE NOT NULL,
                        valor DECIMAL(15,4) NOT NULL,
                        fecha_consulta DATETIME NOT NULL,
                        usuario_consulta VARCHAR(100),
                        sitio_proveedor VARCHAR(255),
                        id_usuario INT,
                        FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
                            ON DELETE SET NULL
                    );
                """)
                self.__connection.commit()
                print("Tabla 'IndicadoresEconomicos' creada (o ya existía).")

            except Error as e:
                print(f"Error creando tablas: {e}")
                raise
            finally:
                if cursor:
                    cursor.close()
        else:
            raise Exception("No hay conexión activa a la base de datos")

    def desconectar(self):
        """Cierra la conexión"""
        if self.__connection and self.__connection.is_connected():
            self.__connection.close()
            self.__connection = None

    def __del__(self):
        """Destructor para asegurar que la conexión se cierre"""
        self.desconectar()

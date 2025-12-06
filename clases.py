"""Constructor de clases con seguridad"""
import bcrypt  # Para hash de contraseñas con sal
from mysql.connector import Error
from datetime import date, datetime
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

# Clave AES de 16 bytes

AES_KEY = b'Mi_Clave_AES_128'


def _aes_encrypt_ecb(plaintext: str) -> bytes:
    """Cifra texto con AES-128-ECB + PKCS7."""
    if plaintext is None:
        return None
    data = plaintext.encode("utf-8")
    padder = padding.PKCS7(128).padder()
    padded = padder.update(data) + padder.finalize()

    cipher = Cipher(algorithms.AES(AES_KEY), modes.ECB())
    encryptor = cipher.encryptor()
    ct = encryptor.update(padded) + encryptor.finalize()
    return ct


def _aes_decrypt_ecb(blob: bytes) -> str:
    """Descifra dato AES-128-ECB + PKCS7"""
    if not blob:
        return ""
    try:
        cipher = Cipher(algorithms.AES(AES_KEY), modes.ECB())
        decryptor = cipher.decryptor()
        padded = decryptor.update(blob) + decryptor.finalize()

        unpadder = padding.PKCS7(128).unpadder()
        data = unpadder.update(padded) + unpadder.finalize()
        return data.decode("utf-8")
    except Exception as e:
        print(f"Error descifrando datos: {e}")
        return ""


class Empleados:
    """Clase para gestionar empleados con datos cifrados"""

    def __init__(self, db, id_empleado=None, nombre="", direccion="",
                 telefono="", email="", fecha_contratacion=None, salario=0.0):
        self.db = db
        self.id_empleado = id_empleado
        self.nombre = nombre
        self._direccion_cifrada = None
        self._telefono_cifrado = None
        self._email_cifrada = None

        if direccion:
            self.direccion = direccion
        if telefono:
            self.telefono = telefono
        if email:
            self.email = email

        self.fecha_contratacion = fecha_contratacion or date.today()
        self.salario = salario

    def __str__(self):
        return (f"ID: {self.id_empleado}, Nombre: {self.nombre}, "
                f"Dirección: {self.direccion}, Teléfono: {self.telefono}, "
                f"Email: {self.email}, "
                f"Fecha Contratación: {self.fecha_contratacion}, "
                f"Salario: ${self.salario:,.2f}")

    # ==================== Propiedades ======================

    @property
    def direccion(self) -> str:
        """Devuelve la dirección descifrada."""
        return _aes_decrypt_ecb(self._direccion_cifrada)

    @direccion.setter
    def direccion(self, valor: str):
        """Cifra y almacena la dirección."""
        self._direccion_cifrada = _aes_encrypt_ecb(valor)

    @property
    def telefono(self) -> str:
        """Devuelve el teléfono descifrado."""
        return _aes_decrypt_ecb(self._telefono_cifrado)

    @telefono.setter
    def telefono(self, valor: str):
        """Cifra y almacena el teléfono."""
        self._telefono_cifrado = _aes_encrypt_ecb(str(valor))

    @property
    def email(self) -> str:
        """Devuelve el email descifrado."""
        return _aes_decrypt_ecb(self._email_cifrada)

    @email.setter
    def email(self, valor: str):
        """Cifra y almacena el email."""
        self._email_cifrada = _aes_encrypt_ecb(valor)

    # ======================= CRUD =========================

    def registrar_empleado(self):
        """Insertar empleado en la base de datos."""
        sql = """
            INSERT INTO Empleados (nombre, direccion, telefono, email, 
                                   fecha_contratacion, salario)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (
            self.nombre,
            self._direccion_cifrada,
            self._telefono_cifrado,
            self._email_cifrada,
            self.fecha_contratacion,
            self.salario
        )

        try:
            connection = self.db.conectar()
            cursor = connection.cursor()
            cursor.execute(sql, values)
            connection.commit()
            self.id_empleado = cursor.lastrowid
            print(
                f"Empleado '{self.nombre}' registrado con ID: {self.id_empleado}")
            return self.id_empleado
        except Error as e:
            connection.rollback()
            print(f"Error al registrar empleado: {e}")
            return None
        finally:
            cursor.close()

    def actualizar_empleado(self):
        """Actualizar datos del empleado."""
        sql = """
            UPDATE Empleados 
            SET nombre=%s, direccion=%s, telefono=%s, email=%s, salario=%s
            WHERE id_empleado=%s
        """
        values = (
            self.nombre,
            self._direccion_cifrada,
            self._telefono_cifrado,
            self._email_cifrada,
            self.salario,
            self.id_empleado
        )

        try:
            connection = self.db.conectar()
            cursor = connection.cursor()
            cursor.execute(sql, values)
            connection.commit()
            print(
                f"Empleado ID {self.id_empleado} actualizado correctamente")
            return True
        except Error as e:
            connection.rollback()
            print(f"Error al actualizar empleado: {e}")
            return False
        finally:
            cursor.close()

    @staticmethod
    def listar_empleados(db):
        """Lista todos los empleados."""
        try:
            connection = db.conectar()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Empleados")
            resultados = cursor.fetchall()

            empleados = []
            for row in resultados:
                emp = Empleados(
                    db, id_empleado=row['id_empleado'], nombre=row['nombre'])
                emp._direccion_cifrada = row['direccion']
                emp._telefono_cifrado = row['telefono']
                emp._email_cifrada = row['email']
                emp.fecha_contratacion = row['fecha_contratacion']
                emp.salario = row['salario']
                empleados.append(emp)

            return empleados
        except Error as e:
            print(f"Error al listar empleados: {e}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def buscar_por_id(db, id_empleado):
        """Buscar empleado por ID."""
        try:
            connection = db.conectar()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM Empleados WHERE id_empleado = %s", (id_empleado,))
            row = cursor.fetchone()

            if row:
                emp = Empleados(
                    db, id_empleado=row['id_empleado'], nombre=row['nombre'])
                emp._direccion_cifrada = row['direccion']
                emp._telefono_cifrado = row['telefono']
                emp._email_cifrada = row['email']
                emp.fecha_contratacion = row['fecha_contratacion']
                emp.salario = row['salario']
                return emp
            return None
        except Error as e:
            print(f"Error al buscar empleado: {e}")
            return None
        finally:
            cursor.close()

    @staticmethod
    def eliminar_empleado(db, id_empleado):
        """Eliminar empleado."""
        try:
            connection = db.conectar()
            cursor = connection.cursor()
            cursor.execute(
                "DELETE FROM Empleados WHERE id_empleado = %s", (id_empleado,))
            connection.commit()
            print(f"Empleado ID {id_empleado} eliminado")
            return True
        except Error as e:
            print(f"Error al eliminar empleado: {e}")
            return False
        finally:
            cursor.close()


class Usuario:
    """
    Clase para gestionar usuarios del sistema con autenticación bcrypt.
    """

    def __init__(self, db, id_usuario=None, nombre_usuario="", password="",
                 rol="", id_empleado=None):
        self.db = db
        self.id_usuario = id_usuario
        self.nombre_usuario = nombre_usuario
        self.password = password  # Se guarda temporalmente para autenticación
        self.__password_hash = None
        self.rol = rol
        self.id_empleado = id_empleado

    def __str__(self):
        return f"ID: {self.id_usuario}, Usuario: {self.nombre_usuario}, Rol: {self.rol}"

    @staticmethod
    def _hash_password(password):
        """Genera hash bcrypt de la contraseña con sal automática."""
        # Genera sal y hashea
        # rounds=12 significa 2^12 = 4096
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')  # Convertir a string para almacenar

    def autenticar(self):
        """Autentica usuario usando bcrypt"""
        try:
            connection = self.db.conectar()
            cursor = connection.cursor(dictionary=True)

            # Buscar usuario
            cursor.execute(
                "SELECT * FROM Usuario WHERE nombre_usuario = %s",
                (self.nombre_usuario,)
            )
            resultado = cursor.fetchone()

            if resultado:
                # Verificar contraseña con bcrypt
                stored_hash = resultado['password_hash'].encode('utf-8')
                if bcrypt.checkpw(self.password.encode('utf-8'), stored_hash):
                    self.id_usuario = resultado['id_usuario']
                    self.rol = resultado['rol']
                    self.id_empleado = resultado['id_empleado']
                    print(f"Bienvenido {self.nombre_usuario} ({self.rol})")
                    return True
                else:
                    print("Usuario o contraseña incorrectos")
                    return False
            else:
                print("Usuario o contraseña incorrectos")
                return False
        except Error as e:
            print(f"Error en autenticación: {e}")
            return False
        finally:
            cursor.close()

    def autorizar(self, rol_requerido):
        """Verifica si el usuario tiene el rol necesario."""
        return self.rol == rol_requerido or self.rol == "admin"

    def registrar_usuario(self):
        """Registra nuevo usuario con contraseña hasheada."""
        # Hashear contraseña antes de guardar
        password_hash = self._hash_password(self.password)

        sql = """
            INSERT INTO Usuario (nombre_usuario, password_hash, rol, id_empleado)
            VALUES (%s, %s, %s, %s)
        """
        values = (self.nombre_usuario, password_hash,
                  self.rol, self.id_empleado)

        try:
            connection = self.db.conectar()
            cursor = connection.cursor()
            cursor.execute(sql, values)
            connection.commit()
            self.id_usuario = cursor.lastrowid
            print(
                f"Usuario '{self.nombre_usuario}' registrado con ID: {self.id_usuario}")
            print("Contraseña hasheada")
            return self.id_usuario
        except Error as e:
            connection.rollback()
            print(f"Error al registrar usuario: {e}")
            return None
        finally:
            cursor.close()

    @staticmethod
    def listar_usuarios(db):
        """Lista todos los usuarios (sin mostrar hashes)."""
        try:
            connection = db.conectar()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                "SELECT id_usuario, nombre_usuario, rol, id_empleado FROM Usuario")
            return cursor.fetchall()
        except Error as e:
            print(f"Error al listar usuarios: {e}")
            return []
        finally:
            cursor.close()


class Departamento:
    """Clase para gestionar departamentos."""

    def __init__(self, db, id_departamento=None, nombre="", gerente="",
                 id_empleado=None, id_proyecto=None):
        self.db = db
        self.id_departamento = id_departamento
        self.nombre = nombre
        self.gerente = gerente
        self.id_empleado = id_empleado
        self.id_proyecto = id_proyecto

    def __str__(self):
        return f"ID: {self.id_departamento}, Nombre: {self.nombre}, Gerente: {self.gerente}"

    def crear_departamento(self):
        """Crear departamento en la BD."""
        sql = """
            INSERT INTO Departamentos (nombre, gerente, id_empleado, id_proyecto) 
            VALUES (%s, %s, %s, %s)
        """
        values = (self.nombre, self.gerente,
                  self.id_empleado, self.id_proyecto)

        try:
            connection = self.db.conectar()
            cursor = connection.cursor()
            cursor.execute(sql, values)
            connection.commit()
            self.id_departamento = cursor.lastrowid
            print(
                f"Departamento '{self.nombre}' creado con ID: {self.id_departamento}")
            return self.id_departamento
        except Error as e:
            connection.rollback()
            print(f"Error al crear departamento: {e}")
            return None
        finally:
            cursor.close()

    def actualizar_departamento(self):
        """Actualizar departamento."""
        sql = """
            UPDATE Departamentos 
            SET nombre=%s, gerente=%s, id_empleado=%s, id_proyecto=%s
            WHERE id_departamento=%s
        """
        values = (self.nombre, self.gerente, self.id_empleado,
                  self.id_proyecto, self.id_departamento)

        try:
            connection = self.db.conectar()
            cursor = connection.cursor()
            cursor.execute(sql, values)
            connection.commit()
            print(f"Departamento ID {self.id_departamento} actualizado")
            return True
        except Error as e:
            connection.rollback()
            print(f"Error al actualizar departamento: {e}")
            return False
        finally:
            cursor.close()

    @staticmethod
    def listar_departamentos(db):
        """Listar todos los departamentos."""
        try:
            connection = db.conectar()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Departamentos")
            return cursor.fetchall()
        except Error as e:
            print(f"Error al listar departamentos: {e}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def buscar_por_id(db, id_departamento):
        """Buscar departamento por ID."""
        try:
            connection = db.conectar()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM Departamentos WHERE id_departamento = %s",
                (id_departamento,))
            row = cursor.fetchone()

            if row:
                return Departamento(
                    db,
                    id_departamento=row['id_departamento'],
                    nombre=row['nombre'],
                    gerente=row['gerente'],
                    id_empleado=row['id_empleado'],
                    id_proyecto=row['id_proyecto']
                )
            return None
        except Error as e:
            print(f"Error al buscar departamento: {e}")
            return None
        finally:
            cursor.close()

    @staticmethod
    def eliminar_departamento(db, id_departamento):
        """Eliminar departamento."""
        try:
            connection = db.conectar()
            cursor = connection.cursor()
            cursor.execute(
                "DELETE FROM Departamentos WHERE id_departamento = %s",
                (id_departamento,))
            connection.commit()
            print(f"Departamento ID {id_departamento} eliminado")
            return True
        except Error as e:
            print(f"Error al eliminar departamento: {e}")
            return False
        finally:
            cursor.close()


class Proyecto:
    """Clase para gestionar proyectos."""

    def __init__(self, db, id_proyecto=None, nombre="", descripcion="",
                 fecha_inicio=None, fecha_termino=None):
        self.db = db
        self.id_proyecto = id_proyecto
        self.nombre = nombre
        self.descripcion = descripcion
        self.fecha_inicio = fecha_inicio or date.today()
        self.fecha_termino = fecha_termino

    def __str__(self):
        return (f"ID: {self.id_proyecto}, Nombre: {self.nombre}, "
                f"Inicio: {self.fecha_inicio}, Término: {self.fecha_termino}")

    def crear_proyecto(self):
        """Crear proyecto en la BD."""
        sql = """
            INSERT INTO Proyectos (nombre, descripcion, fecha_inicio, fecha_termino) 
            VALUES (%s, %s, %s, %s)
        """
        values = (self.nombre, self.descripcion,
                  self.fecha_inicio, self.fecha_termino)

        try:
            connection = self.db.conectar()
            cursor = connection.cursor()
            cursor.execute(sql, values)
            connection.commit()
            self.id_proyecto = cursor.lastrowid
            print(
                f"Proyecto '{self.nombre}' creado con ID: {self.id_proyecto}")
            return self.id_proyecto
        except Error as e:
            connection.rollback()
            print(f"Error al crear proyecto: {e}")
            return None
        finally:
            cursor.close()

    def editar_proyecto(self):
        """Actualizar proyecto."""
        sql = """
            UPDATE Proyectos 
            SET nombre=%s, descripcion=%s, fecha_inicio=%s, fecha_termino=%s
            WHERE id_proyecto=%s
        """
        values = (self.nombre, self.descripcion, self.fecha_inicio,
                  self.fecha_termino, self.id_proyecto)

        try:
            connection = self.db.conectar()
            cursor = connection.cursor()
            cursor.execute(sql, values)
            connection.commit()
            print(f"Proyecto ID {self.id_proyecto} actualizado")
            return True
        except Error as e:
            connection.rollback()
            print(f"Error al actualizar proyecto: {e}")
            return False
        finally:
            cursor.close()

    @staticmethod
    def listar_proyectos(db):
        """Listar todos los proyectos."""
        try:
            connection = db.conectar()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM Proyectos")
            return cursor.fetchall()
        except Error as e:
            print(f"Error al listar proyectos: {e}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def eliminar_proyecto(db, id_proyecto):
        """Eliminar proyecto."""
        try:
            connection = db.conectar()
            cursor = connection.cursor()
            cursor.execute(
                "DELETE FROM Proyectos WHERE id_proyecto = %s", (id_proyecto,))
            connection.commit()
            print(f"Proyecto ID {id_proyecto} eliminado")
            return True
        except Error as e:
            print(f"Error al eliminar proyecto: {e}")
            return False
        finally:
            cursor.close()


class RegistroDeTiempo:
    """Clase para gestionar registros de tiempo."""

    def __init__(self, db, id_registro=None, fecha=None, horas=0,
                 descripcion="", id_empleado=None, id_proyecto=None):
        self.db = db
        self.id_registro = id_registro
        self.fecha = fecha or date.today()
        self.horas = horas
        self.descripcion = descripcion
        self.id_empleado = id_empleado
        self.id_proyecto = id_proyecto

    def __str__(self):
        return (f"ID: {self.id_registro}, Fecha: {self.fecha}, Horas: {self.horas}, "
                f"Empleado: {self.id_empleado}, Proyecto: {self.id_proyecto}")

    def registrar_tiempo(self):
        """Registrar tiempo trabajado."""
        sql = """
            INSERT INTO RegistrodeTiempo (fecha, horas, descripcion, id_empleado, id_proyecto)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (self.fecha, self.horas, self.descripcion,
                  self.id_empleado, self.id_proyecto)

        try:
            connection = self.db.conectar()
            cursor = connection.cursor()
            cursor.execute(sql, values)
            connection.commit()
            self.id_registro = cursor.lastrowid
            print(f"Registro de tiempo creado con ID: {self.id_registro}")
            return self.id_registro
        except Error as e:
            connection.rollback()
            print(f"Error al registrar tiempo: {e}")
            return None
        finally:
            cursor.close()

    @staticmethod
    def listar_registros(db):
        """Listar todos los registros de tiempo."""
        try:
            connection = db.conectar()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM RegistrodeTiempo")
            return cursor.fetchall()
        except Error as e:
            print(f"Error al listar registros: {e}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def consultar_registro(db, id_empleado=None, id_proyecto=None):
        """Consultar registros por empleado o proyecto."""
        try:
            connection = db.conectar()
            cursor = connection.cursor(dictionary=True)

            if id_empleado:
                cursor.execute(
                    "SELECT * FROM RegistrodeTiempo WHERE id_empleado = %s",
                    (id_empleado,))
            elif id_proyecto:
                cursor.execute(
                    "SELECT * FROM RegistrodeTiempo WHERE id_proyecto = %s",
                    (id_proyecto,))
            else:
                cursor.execute("SELECT * FROM RegistrodeTiempo")

            return cursor.fetchall()
        except Error as e:
            print(f"Error al consultar registros: {e}")
            return []
        finally:
            cursor.close()

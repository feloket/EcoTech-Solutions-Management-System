"""Módulo para consulta y almacenamiento de indicadores económicos"""
import requests
from datetime import datetime, date
from mysql.connector import Error


class IndicadorEconomico:
    """Clase para gestionar indicadores económicos desde API externa"""
    INDICADORES = {
        "1": {"codigo": "uf", "nombre": "Unidad de Fomento (UF)"},
        "2": {"codigo": "ivp", "nombre": "Índice de Valor Promedio (IVP)"},
        "3": {"codigo": "ipc", "nombre": "Índice de Precio al Consumidor (IPC)"},
        "4": {"codigo": "utm", "nombre": "Unidad Tributaria Mensual (UTM)"},
        "5": {"codigo": "dolar", "nombre": "Dólar Observado"},
        "6": {"codigo": "euro", "nombre": "Euro"}
    }

    API_BASE_URL = "https://mindicador.cl/api"

    def __init__(self, db, api_key=None):
        self.db = db
        self.sitio_proveedor = "https://mindicador.cl"

        self.api_key = api_key
        self.headers = {
            'User-Agent': 'EcoTech-Solutions/1.0',
            'Accept': 'application/json'
        }
        if self.api_key:
            self.headers['Authorization'] = f'Bearer {self.api_key}'

    @classmethod
    def mostrar_indicadores(cls):
        """Muestra el listado de indicadores disponibles"""
        print("\n INDICADORES ECONÓMICOS DISPONIBLES ")
        for key, value in cls.INDICADORES.items():
            print(f"{key}. {value['nombre']}")
        print("=" * 50)

    def consultar_indicador_fecha(self, codigo_indicador, fecha):
        """Consulta el valor de un indicador en una fecha específica"""
        try:
            # Formato de la API: /api/{indicador}/{dd-mm-yyyy}
            fecha_str = fecha.strftime("%d-%m-%Y")
            url = f"{self.API_BASE_URL}/{codigo_indicador}/{fecha_str}"

            print(f"\n🔍 Consultando: {url}")

            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()

            data = response.json()

            # La API devuelve un objeto con una serie, que es una lista
            if 'serie' in data and len(data['serie']) > 0:
                valor_dato = data['serie'][0]
                return {
                    'nombre': data.get('nombre', codigo_indicador.upper()),
                    'codigo': data.get('codigo', codigo_indicador),
                    'fecha': valor_dato.get('fecha', ''),
                    'valor': valor_dato.get('valor', 0),
                    'unidad_medida': data.get('unidad_medida', '')
                }
            else:
                print(
                    f"No se encontraron datos para {codigo_indicador} en {fecha_str}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"Error al consultar API: {e}")
            return None
        except Exception as e:
            print(f"Error inesperado: {e}")
            return None

    def consultar_indicador_periodo(self, codigo_indicador, fecha_inicio, fecha_fin):
        """Consulta valores de un indicador en un periodo"""
        try:
            # Obtener año para consulta
            url = f"{self.API_BASE_URL}/{codigo_indicador}"

            print(f"\nConsultando periodo: {url}")

            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()

            data = response.json()

            resultados = []

            if 'serie' in data:
                for valor_dato in data['serie']:
                    fecha_valor_str = valor_dato.get('fecha', '')
                    fecha_valor = datetime.fromisoformat(
                        fecha_valor_str.replace('Z', '+00:00')
                    ).date()

                    # Filtrar por rango de fechas
                    if fecha_inicio <= fecha_valor <= fecha_fin:
                        resultados.append({
                            'nombre': data.get('nombre', codigo_indicador.upper()),
                            'codigo': data.get('codigo', codigo_indicador),
                            'fecha': fecha_valor_str,
                            'valor': valor_dato.get('valor', 0),
                            'unidad_medida': data.get('unidad_medida', '')
                        })

                # Ordenar por fecha
                resultados.sort(key=lambda x: x['fecha'])

            return resultados

        except requests.exceptions.RequestException as e:
            print(f"Error al consultar API: {e}")
            return []
        except Exception as e:
            print(f"Error inesperado: {e}")
            return []

    def registrar_indicador(self, nombre_indicador, fecha_valor, valor, usuario_consulta, id_usuario=None):
        """Registra un indicador económico en la base de datos"""
        sql = """
            INSERT INTO IndicadoresEconomicos 
            (nombre_indicador, fecha_valor, valor, fecha_consulta, usuario_consulta, sitio_proveedor, id_usuario)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        if isinstance(fecha_valor, str):
            try:
                fecha_valor = datetime.fromisoformat(
                    fecha_valor.replace('Z', '+00:00')
                ).date()
            except:
                fecha_valor = date.today()

        fecha_consulta = datetime.now()

        values = (
            nombre_indicador,
            fecha_valor,
            valor,
            fecha_consulta,
            usuario_consulta,
            self.sitio_proveedor,
            id_usuario
        )

        try:
            connection = self.db.conectar()
            cursor = connection.cursor()
            cursor.execute(sql, values)
            connection.commit()
            id_registro = cursor.lastrowid
            print(
                f"Indicador '{nombre_indicador}' registrado con ID: {id_registro}")
            return id_registro
        except Error as e:
            connection.rollback()
            print(f"Error al registrar indicador: {e}")
            return None
        finally:
            cursor.close()

    @staticmethod
    def listar_registros(db, limite=50):
        """Lista los últimos registros de indicadores"""
        try:
            connection = db.conectar()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT * FROM IndicadoresEconomicos 
                ORDER BY fecha_consulta DESC 
                LIMIT %s
            """, (limite,))
            return cursor.fetchall()
        except Error as e:
            print(f"Error al listar indicadores: {e}")
            return []
        finally:
            cursor.close()

    @staticmethod
    def consultar_por_indicador(db, nombre_indicador):
        """Consulta registros de un indicador específico"""
        try:
            connection = db.conectar()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT * FROM IndicadoresEconomicos 
                WHERE nombre_indicador LIKE %s
                ORDER BY fecha_valor DESC
            """, (f"%{nombre_indicador}%",))
            return cursor.fetchall()
        except Error as e:
            print(f"Error al consultar indicador: {e}")
            return []
        finally:
            cursor.close()

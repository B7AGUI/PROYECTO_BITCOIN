import os
import psycopg2
import requests
from datetime import datetime, timedelta
from abc import ABC, abstractmethod
from dotenv import load_dotenv

load_dotenv()

# 1. LA INTERFAZ (Ahora genérica para cualquier Crypto)
class ProveedorCrypto(ABC):
    @abstractmethod
    def obtener_precios(self, monedas):
        pass

    @abstractmethod
    def obtener_historial(self, moneda_id, limite=5):
        pass

# 2. EL OBJETO REAL (Conexión por lotes a la API)
class APICryptoReal(ProveedorCrypto):
    def obtener_precios(self, monedas):
        try:
            ids = ",".join(monedas)
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            respuesta = requests.get(url, headers=headers)
            datos = respuesta.json()
            
            return {m: float(datos[m]['usd']) for m in monedas if m in datos}
        except Exception:
            return None

    # ---> NUEVO: La API real no gestiona nuestro caché, así que retorna vacío para cumplir la interfaz
    def obtener_historial(self, moneda_id, limite=5):
        return []

# 3. EL PROXY (Caché inteligente por moneda)
class ProxyCrypto(ProveedorCrypto):
    def __init__(self):
        self.api_real = APICryptoReal()
        try:
            self.conn = psycopg2.connect(
                host=os.getenv("DB_HOST"),
                database=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD")
            )
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(f"Error de conexión: {e}")

    def obtener_precios(self, monedas):
        precios_finales = {}
        monedas_a_consultar_api = []

        for moneda in monedas:
            self.cursor.execute(
                "SELECT precio, fecha FROM historial_bitcoin WHERE moneda_id = %s ORDER BY fecha DESC LIMIT 1;", 
                (moneda,)
            )
            resultado = self.cursor.fetchone()

            if resultado and (datetime.now() - resultado[1]) < timedelta(minutes=5):
                precios_finales[moneda] = float(resultado[0])
            else:
                monedas_a_consultar_api.append(moneda)

        if monedas_a_consultar_api:
            nuevos_datos = self.api_real.obtener_precios(monedas_a_consultar_api)
            if nuevos_datos:
                fecha_actual = datetime.now()
                for m, p in nuevos_datos.items():
                    precios_finales[m] = p
                    self.cursor.execute(
                        "INSERT INTO historial_bitcoin (moneda_id, precio, fecha) VALUES (%s, %s, %s);",
                        (m, p, fecha_actual)
                    )
                self.conn.commit()

        return precios_finales

    def obtener_historial(self, moneda_id, limite=5):
        try:
            self.cursor.execute(
                "SELECT precio, fecha FROM historial_bitcoin WHERE moneda_id = %s ORDER BY fecha DESC LIMIT %s;", 
                (moneda_id, limite)
            )
            return self.cursor.fetchall()
        except Exception as e:
            return []

    def cerrar_conexion(self):
        if self.cursor: self.cursor.close()
        if self.conn: self.conn.close()           

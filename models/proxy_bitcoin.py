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

# 2. EL OBJETO REAL (Conexión por lotes a la API)
class APICryptoReal(ProveedorCrypto):
    def obtener_precios(self, monedas):
        try:
            # Convertimos la lista ['bitcoin', 'ethereum'] en "bitcoin,ethereum"
            ids = ",".join(monedas)
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            respuesta = requests.get(url, headers=headers)
            datos = respuesta.json()
            
            # Retornamos un diccionario limpio: {'bitcoin': 63000.0, 'ethereum': 3000.0, ...}
            return {m: float(datos[m]['usd']) for m in monedas if m in datos}
        except Exception:
            return None

# 3. EL PROXY (Caché inteligente por moneda y sin "prints" molestos)
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
            # A) Buscamos en BD el último precio de ESTA moneda específica
            self.cursor.execute(
                "SELECT precio, fecha FROM historial_bitcoin WHERE moneda_id = %s ORDER BY fecha DESC LIMIT 1;", 
                (moneda,)
            )
            resultado = self.cursor.fetchone()

            # B) Verificamos si el dato existe y es menor a 5 minutos
            if resultado and (datetime.now() - resultado[1]) < timedelta(minutes=5):
                precios_finales[moneda] = float(resultado[0])
            else:
                monedas_a_consultar_api.append(moneda)

        # C) Si hay monedas caducadas o nuevas, vamos a la API una sola vez
        if monedas_a_consultar_api:
            nuevos_datos = self.api_real.obtener_precios(monedas_a_consultar_api)
            if nuevos_datos:
                fecha_actual = datetime.now()
                for m, p in nuevos_datos.items():
                    precios_finales[m] = p
                    # Guardamos en la BD con su ID correspondiente
                    self.cursor.execute(
                        "INSERT INTO historial_bitcoin (moneda_id, precio, fecha) VALUES (%s, %s, %s);",
                        (m, p, fecha_actual)
                    )
                self.conn.commit()

        return precios_finales

    def cerrar_conexion(self):
        if self.cursor: self.cursor.close()
        if self.conn: self.conn.close()   

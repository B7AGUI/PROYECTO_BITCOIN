import psycopg2
import requests
from datetime import datetime, timedelta
from abc import ABC, abstractmethod

# 1. LA INTERFAZ
class ProveedorBitcoin(ABC):
    @abstractmethod
    def obtener_precio(self):
        pass

# 2. EL OBJETO REAL (Conexión real a internet)
class APIBitcoinReal(ProveedorBitcoin):
    def obtener_precio(self):
        print("[API Real] Conectando a CoinGecko para descargar el precio en vivo...")
        try:
            url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
            respuesta = requests.get(url)
            datos = respuesta.json()
            precio_actual = datos['bitcoin']['usd']
            print(f"[API Real] ¡Éxito! Precio descargado: ${precio_actual}")
            return float(precio_actual)
        except Exception as e:
            print(f"[Error de Red] Falló la conexión a internet: {e}")
            return None

# 3. EL PROXY (El Cerebro con Caché Inteligente)
class ProxyBitcoin(ProveedorBitcoin):
    def __init__(self):
        self.api_real = APIBitcoinReal()
        
        try:
            self.conn = psycopg2.connect(
                host="localhost",
                database="tu_base_de_datos", 
                user="postgres",
                password="tu_password" # <--- CAMBIA ESTO
            )
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(f"[Error CRÍTICO] No se pudo conectar a la BD: {e}")

    def obtener_precio(self):
        print("\n[Proxy] Interceptando la petición del usuario...")
        
        try:
            # A) Buscamos el último precio Y su fecha exacta
            consulta_select = "SELECT precio, fecha FROM historial_bitcoin ORDER BY fecha DESC LIMIT 1;"
            self.cursor.execute(consulta_select)
            resultado = self.cursor.fetchone()

            # B) Lógica de Tiempo de Vida (TTL - 5 minutos)
            if resultado:
                precio_bd = resultado[0]
                fecha_bd = resultado[1]
                
                tiempo_transcurrido = datetime.now() - fecha_bd
                
                if tiempo_transcurrido < timedelta(minutes=5):
                    segundos_edad = tiempo_transcurrido.seconds
                    print(f"[Proxy] Dato fresco ({segundos_edad} seg de antigüedad). Usando Caché: ${precio_bd}")
                    return precio_bd
                else:
                    print("[Proxy] El dato en BD ya caducó (tiene más de 5 min). Necesitamos actualizar...")

            # C) Si no hay datos, o ya caducaron, vamos a la API Real
            print("[Proxy] Delegando tarea a la API Real...")
            precio_nuevo = self.api_real.obtener_precio()

            # D) Guardamos el nuevo registro fresquito en la base de datos
            if precio_nuevo:
                consulta_insert = "INSERT INTO historial_bitcoin (precio, fecha) VALUES (%s, %s);"
                fecha_actual = datetime.now()
                self.cursor.execute(consulta_insert, (precio_nuevo, fecha_actual))
                self.conn.commit()
                print("[Proxy] Nuevo precio guardado en PostgreSQL para futuras consultas.")

            return precio_nuevo

        except Exception as e:
            print(f"[Error en consulta] {e}")
            return None

    def cerrar_conexion(self):
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()

# 4. PRUEBA DE FUEGO FINAL
if __name__ == "__main__":
    mi_proxy = ProxyBitcoin()
    
    print("\n--- INTENTO 1: Buscando el precio real ---")
    mi_proxy.obtener_precio()
    
    print("\n--- INTENTO 2: Consultando inmediatamente después ---")
    mi_proxy.obtener_precio()
    
    mi_proxy.cerrar_conexion()   

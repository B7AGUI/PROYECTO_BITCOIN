# actualizador.py
from controller.crypto_controller import CryptoController

def recoleccion_nocturna():
    # Instanciamos el controlador
    controlador = CryptoController()
    
    # Esto fuerza al Proxy a revisar la BD y la API, guardando los datos nuevos
    controlador.obtener_precios_actualizados()

if __name__ == "__main__":
    recoleccion_nocturna()

# controllers/crypto_controller.py

from models.proxy_bitcoin import ProxyCrypto 

class CryptoController:
    def __init__(self):
        # Conectamos con el modelo real
        self.proxy = ProxyCrypto()
        
        # Las 7 monedas de tu captura
        self.monedas_activas = [
            "bitcoin", 
            "ethereum", 
            "binancecoin", 
            "ripple", 
            "chainlink", 
            "litecoin", 
            "tether"
        ]

    def obtener_precios_actualizados(self):
        """
        Pide los datos al Proxy pasándole la lista de monedas
        y retorna el diccionario con los precios limpios.
        """
        return self.proxy.obtener_precios(self.monedas_activas)

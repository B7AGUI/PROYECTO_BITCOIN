from models.proxy_bitcoin import ProxyCrypto

class CryptoController:
    def __init__(self):
        self.proxy = ProxyCrypto()
        
        self.monedas_activas = [
            "bitcoin", "ethereum", "binancecoin", "ripple", 
            "chainlink", "litecoin", "tether"
        ]

    def obtener_precios_actualizados(self):
        return self.proxy.obtener_precios(self.monedas_activas)

    def obtener_historial_moneda(self, moneda_id):
        return self.proxy.obtener_historial(moneda_id, limite=2000)

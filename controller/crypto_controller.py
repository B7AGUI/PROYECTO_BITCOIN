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

    # ---> ESTO ES LO NUEVO QUE ESTAMOS AGREGANDO <---
    def obtener_historial_moneda(self, moneda_id):
        """Pide al proxy los últimos 5 registros de una moneda"""
        return self.proxy.obtener_historial(moneda_id, limite=5)

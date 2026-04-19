from flask import Flask, render_template
from controller.crypto_controller import CryptoController

app = Flask(__name__)
controlador = CryptoController()

diccionario_logos = {
    "bitcoin": "https://upload.wikimedia.org/wikipedia/commons/4/46/Bitcoin.svg",
    "ethereum": "https://upload.wikimedia.org/wikipedia/commons/0/05/Ethereum_logo_2014.svg",
    "binancecoin": "https://upload.wikimedia.org/wikipedia/commons/f/fc/Binance-coin-bnb-logo.png",
    "ripple": "https://upload.wikimedia.org/wikipedia/commons/8/88/Ripple_logo.svg",
    "chainlink": "https://upload.wikimedia.org/wikipedia/commons/1/15/Chainlink_Logo_Blue.svg",
    "litecoin": "https://upload.wikimedia.org/wikipedia/commons/f/f8/LTC-400.png",
    "tether": "https://www.shutterstock.com/image-illustration/usdt-logo-coin-tether-260nw-2653907905.jpg"
}
@app.route('/')
def inicio():
    datos_actualizados = controlador.obtener_precios_actualizados() 
    # Le mandamos también el diccionario de logos a la plantilla
    return render_template('index.html', criptos=datos_actualizados, logos=diccionario_logos)

@app.route('/historial/<moneda_id>')
def historial(moneda_id):
    datos_historial = controlador.obtener_historial_moneda(moneda_id)
    return render_template('historial.html', moneda=moneda_id, historial=datos_historial)

if __name__ == '__main__':
    app.run(debug=True, port=5000)   

 # main.py
import os
from controller.crypto_controller import CryptoController

# Códigos ANSI para el estilo neón/cyberpunk en terminal
NEON_YELLOW = '\033[38;5;226m'
NEON_CYAN = '\033[38;5;51m'
DARK_GREY = '\033[38;5;239m'
RESET = '\033[0m'
BOLD = '\033[1m'

def limpiar_pantalla():
    """Limpia la consola para que no se amontone el texto"""
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_interfaz(datos_criptos):
    """Renderiza el dashboard en la terminal"""
    limpiar_pantalla()
    
    # Encabezado
    print(f"{NEON_YELLOW}{BOLD}╔════════════════════════════════════════════╗{RESET}")
    print(f"{NEON_YELLOW}{BOLD}║         MERCADO CRYPTO EN VIVO             ║{RESET}")
    print(f"{NEON_YELLOW}{BOLD}╚════════════════════════════════════════════╝{RESET}")
    print(f"{DARK_GREY}ACTIVO\t\t\tVALOR (USD){RESET}")
    print(f"{DARK_GREY}----------------------------------------------{RESET}")
    
    # Si por alguna razón la BD o la API fallan y regresa vacío
    if not datos_criptos:
        print(f"{NEON_YELLOW}>> No se pudieron obtener los datos.{RESET}")
    else:
        # Imprimimos cada moneda con su precio formateado
        for moneda, precio in datos_criptos.items():
            nombre_formateado = f"[{moneda.upper()}]"
            print(f"{NEON_CYAN}{nombre_formateado:<20}{RESET}\t${precio:,.4f}")
            
    print(f"{DARK_GREY}----------------------------------------------{RESET}")
    print(f"{NEON_YELLOW}[ENTER]{RESET} Actualizar  |  {NEON_YELLOW}[Q]{RESET} Desconectar")

def ejecutar_aplicacion():
    # Instanciamos el controlador una sola vez al iniciar
    controlador = CryptoController()
    
    while True:
        # Obtenemos el diccionario con los precios desde el controlador
        datos_actualizados = controlador.obtener_precios_actualizados() 
        
        # Dibujamos la interfaz
        mostrar_interfaz(datos_actualizados)
        
        # Esperamos la instrucción del usuario
        accion = input("").strip().lower()
        if accion == 'q':
            print(f"{NEON_YELLOW}Desconectando del servidor...{RESET}")
            break

if __name__ == "__main__":
    ejecutar_aplicacion()   

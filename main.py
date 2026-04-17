import os
from controller.crypto_controller import CryptoController

# Códigos ANSI para el estilo neón/cyberpunk
NEON_YELLOW = '\033[38;5;226m'
NEON_CYAN = '\033[38;5;51m'
DARK_GREY = '\033[38;5;239m'
RESET = '\033[0m'
BOLD = '\033[1m'

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_interfaz(datos_criptos):
    limpiar_pantalla()
    print(f"{NEON_YELLOW}{BOLD}╔════════════════════════════════════════════╗{RESET}")
    print(f"{NEON_YELLOW}{BOLD}║         MERCADO CRYPTO EN VIVO             ║{RESET}")
    print(f"{NEON_YELLOW}{BOLD}╚════════════════════════════════════════════╝{RESET}")
    print(f"{DARK_GREY}ACTIVO\t\t\tVALOR (USD){RESET}")
    print(f"{DARK_GREY}----------------------------------------------{RESET}")
    
    if not datos_criptos:
        print(f"{NEON_YELLOW}>> No se pudieron obtener los datos.{RESET}")
    else:
        for moneda, precio in datos_criptos.items():
            nombre_formateado = f"[{moneda.upper()}]"
            print(f"{NEON_CYAN}{nombre_formateado:<20}{RESET}\t${precio:,.4f}")
            
    print(f"{DARK_GREY}----------------------------------------------{RESET}")

def mostrar_historial(moneda, datos_historial):
    """Renderiza la tabla del historial en la terminal"""
    limpiar_pantalla()
    print(f"{NEON_YELLOW}{BOLD}╔════════════════════════════════════════════╗{RESET}")
    print(f"{NEON_YELLOW}{BOLD}║         HISTORIAL: {moneda.upper():<23} ║{RESET}")
    print(f"{NEON_YELLOW}{BOLD}╚════════════════════════════════════════════╝{RESET}")
    print(f"{DARK_GREY}FECHA Y HORA\t\t\tVALOR (USD){RESET}")
    print(f"{DARK_GREY}----------------------------------------------{RESET}")
    
    if not datos_historial:
        print(f"{NEON_CYAN}>> Aún no hay suficientes datos registrados.{RESET}")
    else:
        for precio, fecha in datos_historial:
            fecha_str = fecha.strftime("%Y-%m-%d %H:%M:%S")
            print(f"{NEON_CYAN}{fecha_str}{RESET}\t\t${precio:,.4f}")
            
    print(f"{DARK_GREY}----------------------------------------------{RESET}")
    input(f"{NEON_YELLOW}[ENTER]{RESET} Volver al dashboard principal...")

def ejecutar_aplicacion():
    controlador = CryptoController()
    
    while True:
        # 1. Cargamos y mostramos el dashboard principal
        datos_actualizados = controlador.obtener_precios_actualizados() 
        mostrar_interfaz(datos_actualizados)
        
        # 2. Mostramos el menú con la nueva opción
        print(f"{NEON_YELLOW}[ENTER]{RESET} Actualizar  |  {NEON_YELLOW}[H]{RESET} Historial  |  {NEON_YELLOW}[Q]{RESET} Salir")
        
        accion = input(">> ").strip().lower()
        
        # 3. Lógica de las opciones
        if accion == 'q':
            print(f"{NEON_YELLOW}Desconectando del servidor...{RESET}")
            break
        elif accion == 'h':
            print(f"\n{NEON_CYAN}Escribe la moneda (ej. bitcoin, ethereum):{RESET}")
            moneda_elegida = input(">> ").strip().lower()
            
            if moneda_elegida in controlador.monedas_activas:
                # Si la moneda existe, pedimos el historial y lo mostramos
                historial = controlador.obtener_historial_moneda(moneda_elegida)
                mostrar_historial(moneda_elegida, historial)
            else:
                print(f"{NEON_YELLOW}Moneda no reconocida. Presiona ENTER para continuar.{RESET}")
                input("")

if __name__ == "__main__":
    ejecutar_aplicacion()    

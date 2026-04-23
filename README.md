# 🌐 Mercado Crypto en Vivo ( NEONCHAIN )

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python&logoColor=yellow)
![Flask](https://img.shields.io/badge/Flask-Backend-black?style=for-the-badge&logo=flask)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue?style=for-the-badge&logo=postgresql)
![Chart.js](https://img.shields.io/badge/Chart.js-Gráficas-FF6384?style=for-the-badge&logo=chartdotjs)

Un sistema de backend para la recolección, almacenamiento y visualización de fluctuaciones de criptomonedas. 

A diferencia de un simple consumidor web de APIs, este proyecto implementa un motor de persistencia propio y un caché inteligente de tipo "Lazy Loading" para garantizar la soberanía de los datos, optimizar recursos y evitar bloqueos por *Rate Limiting*.

## Características Principales

* **Arquitectura MVC:** Separación estricta entre la lógica de negocio (Modelos), el control de flujo (Controladores) y la renderización web (Vistas).
* **Patrón de Diseño Proxy (On-Demand Fetching):** Sistema de caché inteligente que intercepta las peticiones de los usuarios. Solo consulta la API externa si la información almacenada tiene más de 5 minutos de antigüedad, insertando el nuevo registro en la base de datos automáticamente.
* **Persistencia de Datos:** Uso de PostgreSQL para mantener un registro histórico propio de las fluctuaciones de precios, permitiendo auditorías y análisis sin depender de endpoints externos premium.
* **Gráficas Dinámicas:** Renderizado de la volatilidad histórica utilizando Chart.js, alimentado directamente desde el backend.
* **Estética Cyberpunk:** Interfaz de usuario (UI) responsiva con paleta de colores oscura, acentos en amarillo ocre y detalles de iluminación neón.

##  Arquitectura del Sistema

El proyecto funciona mediante la integración de dos servidores locales que manejan el ciclo de vida de los datos:

1. **Servidor Web (Aplicación - Flask):** - Escucha en el puerto 5000 y opera bajo el patrón MVC.
   - Gestiona la lógica de evaluación de tiempo (Proxy) para decidir si lee del disco duro o realiza una petición HTTP a CoinGecko.

2. **Servidor de Base de Datos (PostgreSQL):**
   - Actúa como el motor de persistencia principal.
   - Registra cada punto de datos histórico generado por los usuarios al interactuar con la plataforma, construyendo una bitácora de precios a lo largo del tiempo.

##  Flujo de Datos (Data Pipeline)

1. `Usuario` ➔ Recarga o ingresa al Dashboard desde el navegador.
2. `Controlador (Proxy)` ➔ Revisa la base de datos: ¿El último registro tiene más de 5 min?
   - **NO:** Devuelve los datos locales instantáneamente (Caché).
   - **SÍ:** Llama a la API de `CoinGecko` ➔ Devuelve JSON ➔ Hace un `INSERT` en `PostgreSQL`.
3. `Flask` ➔ Construye el HTML inyectando los datos.
4. `Chart.js` ➔ Transforma el historial en una gráfica interactiva de líneas.



## Instrucciones de Instalación

1. Requisitos Previos
Asegúrate de tener instalados los siguientes componentes en tu sistema:
Python 3.8+
PostgreSQL (Servidor activo y corriendo)
2. Configuración de la Base de Datos
Antes de arrancar la aplicación de Flask, es indispensable preparar el almacenamiento persistente para nuestro caché (Proxy).
Abre tu terminal de PostgreSQL (o pgAdmin):
Crea una base de datos para el proyecto con el nombre de Crypto_Monitor
Crea la tabla necesaria para el historial. Asegúrate de respetar este esquema exacto, ya que el Patrón Proxy depende de él:
SQL
CREATE TABLE historial_bitcoin (
    id SERIAL PRIMARY KEY,
    moneda_id VARCHAR(50) NOT NULL,
    precio NUMERIC(15, 6) NOT NULL,
    fecha TIMESTAMP NOT NULL
);
3. Configuración del Entorno Python
Vamos a aislar las dependencias del proyecto utilizando un entorno virtual. En tu terminal de Linux, posicionado en la carpeta models del proyecto, ejecuta:
Crear el entorno virtual: en la carpeta models con python3 -m venv venv
Activar el entorno virtual: source venv/bin/activate
Instalar las dependencias: Ejecuta: pip install -r requirements.txt
(En caso de algún fallo, puedes instalarlas manualmente con: pip install flask psycopg2-binary requests python-dotenv)
4. Variables de Entorno (.env)
El sistema utiliza la librería dotenv para proteger las credenciales. En la raíz de tu proyecto (donde está tu app.py), crea un archivo llamado exactamente .env y coloca tus credenciales reales:
Fragmento de código
DB_HOST=localhost
DB_NAME=cripto_db
DB_USER=tu_usuario_postgres
DB_PASSWORD=tu_contraseña_secreta

5. Ejecución del Servidor Flask
Con la base de datos lista, el entorno activado y las variables configuradas, es hora de encender el Controlador.
Ejecuta el archivo principal: python3 app.py
El terminal te indicará que el servidor está corriendo en modo desarrollo.
Abre tu navegador web de preferencia y dirígete a: http://127.0.0.1:5000
Notas del Sistema:
La primera vez que el tablero cargue, la aplicación hará peticiones reales a la API de CoinGecko.
Las consultas posteriores (dentro del primer minuto) se servirán ultra-rápido desde PostgreSQL gracias a la implementación del Patrón Proxy.
Al hacer clic en "Ver Historial", la vista generará una gráfica procesando los datos almacenados localmente.

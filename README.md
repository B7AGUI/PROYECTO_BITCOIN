# 🌐 Mercado Crypto en Vivo - Dashboard Cyberpunk

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python&logoColor=yellow)
![Flask](https://img.shields.io/badge/Flask-Backend-black?style=for-the-badge&logo=flask)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue?style=for-the-badge&logo=postgresql)
![Chart.js](https://img.shields.io/badge/Chart.js-Gráficas-FF6384?style=for-the-badge&logo=chartdotjs)

Un sistema de backend robusto para la recolección, almacenamiento y visualización de fluctuaciones de criptomonedas. 

A diferencia de un simple consumidor web de APIs, este proyecto implementa un motor de persistencia propio y un caché inteligente de tipo "Lazy Loading" para garantizar la soberanía de los datos, optimizar recursos y evitar bloqueos por *Rate Limiting*.

## ✨ Características Principales

* **Arquitectura MVC:** Separación estricta entre la lógica de negocio (Modelos), el control de flujo (Controladores) y la renderización web (Vistas).
* **Patrón de Diseño Proxy (On-Demand Fetching):** Sistema de caché inteligente que intercepta las peticiones de los usuarios. Solo consulta la API externa si la información almacenada tiene más de 5 minutos de antigüedad, insertando el nuevo registro en la base de datos automáticamente.
* **Persistencia de Datos:** Uso de PostgreSQL para mantener un registro histórico propio de las fluctuaciones de precios, permitiendo auditorías y análisis sin depender de endpoints externos premium.
* **Gráficas Dinámicas:** Renderizado de la volatilidad histórica utilizando Chart.js, alimentado directamente desde el backend.
* **Estética Cyberpunk:** Interfaz de usuario (UI) responsiva con paleta de colores oscura, acentos en amarillo ocre y detalles de iluminación neón.

## 🏗️ Arquitectura del Sistema

El proyecto funciona mediante la integración de dos servidores locales que manejan el ciclo de vida de los datos:

1. **Servidor Web (Aplicación - Flask):** - Escucha en el puerto 5000 y opera bajo el patrón MVC.
   - Gestiona la lógica de evaluación de tiempo (Proxy) para decidir si lee del disco duro o realiza una petición HTTP a CoinGecko.

2. **Servidor de Base de Datos (PostgreSQL):**
   - Actúa como el motor de persistencia principal.
   - Registra cada punto de datos histórico generado por los usuarios al interactuar con la plataforma, construyendo una bitácora de precios a lo largo del tiempo.

## ⚙️ Flujo de Datos (Data Pipeline)

1. `Usuario` ➔ Recarga o ingresa al Dashboard desde el navegador.
2. `Controlador (Proxy)` ➔ Revisa la base de datos: ¿El último registro tiene más de 5 min?
   - **NO:** Devuelve los datos locales instantáneamente (Caché).
   - **SÍ:** Llama a la API de `CoinGecko` ➔ Devuelve JSON ➔ Hace un `INSERT` en `PostgreSQL`.
3. `Flask` ➔ Construye el HTML inyectando los datos.
4. `Chart.js` ➔ Transforma el historial en una gráfica interactiva de líneas.

# 🌐 Mercado Crypto en Vivo - Dashboard Cyberpunk

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python&logoColor=yellow)
![Flask](https://img.shields.io/badge/Flask-Backend-black?style=for-the-badge&logo=flask)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue?style=for-the-badge&logo=postgresql)
![Chart.js](https://img.shields.io/badge/Chart.js-Gráficas-FF6384?style=for-the-badge&logo=chartdotjs)

Un sistema de ingeniería de datos robusto para la recolección, almacenamiento y visualización de fluctuaciones de criptomonedas en tiempo real. 

A diferencia de un simple consumidor web de APIs, este proyecto implementa un motor de persistencia propio y una arquitectura de software limpia para garantizar la soberanía de los datos, optimizar recursos y evitar bloqueos por *Rate Limiting*.

## ✨ Características Principales

* **Arquitectura MVC:** Separación estricta entre la lógica de negocio (Modelos), el control de flujo (Controladores) y la renderización web (Vistas).
* **Patrón de Diseño Proxy:** Sistema de caché inteligente que intercepta las peticiones y restringe el consumo de la API externa a ventanas de 5 minutos, protegiendo la red.
* **Motor de Ingesta Autónomo:** Script recolector (`actualizador.py`) operado de forma invisible a nivel de sistema operativo mediante tareas programadas (Linux Cron).
* **Gráficas Dinámicas:** Renderizado de la volatilidad histórica utilizando Chart.js, alimentado directamente desde la base de datos local.
* **Estética Cyberpunk:** Interfaz de usuario (UI) responsiva con paleta de colores oscura, acentos en amarillo ocre y detalles de iluminación neón.

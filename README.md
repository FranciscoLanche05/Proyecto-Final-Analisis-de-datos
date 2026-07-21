# 📊 Proyecto Final: Análisis y Arquitectura de Datos Multi-Motor

Este repositorio contiene la arquitectura de datos, scripts de ingeniería (ETL) y análisis visual correspondiente al proyecto final de Análisis de Datos. El enfoque principal es la integración de múltiples fuentes de datos dispersas hacia entornos unificados y motores de bases de datos relacionales y no relacionales.

---

## 👥 Integrantes del Proyecto
* **Francisco Lanche**
* **Joel Acosta**

---

## 🚀 Resumen del Proyecto

El objetivo del proyecto es demostrar la capacidad de extraer, transformar, consolidar y visualizar datos provenientes de múltiples orígenes (Olimpiadas, Clima Mundial, Economía, Demografía y Twitter). 

Iniciamos con más de **90 datasets** heterogéneos (Archivos .csv, .json, .db) y desarrollamos un pipeline automatizado para reducir la redundancia, mejorar la calidad de los datos y consolidarlos en **20 datasets estructurados**. Posteriormente, estos datos alimentaron un flujo en **KNIME** y un Dashboard interactivo en **PowerBI**.

---

## 🛠️ Arquitectura y Flujo de Trabajo (Workflow)

El desarrollo se dividió en las siguientes fases clave:

### 1. Consolidación y Limpieza (Python / Pandas)
* Creación del script scriptConsolidacion.py para leer los +90 archivos crudos.
* Uso de técnicas de NLP básico para limpiar caracteres especiales y ruido, especialmente en los datos extraídos de Twitter.
* Cruce y unificación de columnas para dar como resultado **20 archivos maestros** (en la carpeta datasets_consolidados).

### 2. Poblamiento de Bases de Datos (Ingeniería de Datos)
* Se desarrolló el script poblar_motores_datos.py que toma los 20 datasets consolidados y los distribuye de manera equitativa entre **4 motores de bases de datos distintos**:
  * **MySQL** (Datos relacionales y estructurados)
  * **PostgreSQL** (Datos tabulares de alto volumen)
  * **MongoDB** (Datos semi-estructurados y colecciones JSON)
  * **Redis** (Almacenamiento clave-valor rápido)

### 3. Procesamiento Visual ETL (KNIME)
* Se construyó un flujo de trabajo (KNIME_PROYECTO_ANALISIS4.knwf) donde se configuran conectores hacia los motores de bases de datos y archivos locales.
* Dentro de los metanodos de KNIME, se ejecutaron procesos de limpieza profunda: *String to Number*, filtros de valores nulos (*Missing Values*), agrupaciones y contadores (*Value Counters*).
* Exportación final hacia un motor central unificado (Microsoft SQL Server).

### 4. Visualización e Inteligencia de Negocios (Power BI)
* Se conectó la fuente de datos refinada al reporte ProyectoAnalisisDatos.pbix.
* Generación de KPIs y gráficos interactivos para entender las tendencias climáticas, resultados olímpicos y crecimiento demográfico de los países.

---

## 📂 Estructura del Repositorio

* /scripts/: Contiene la lógica en Python para consolidar datos (scriptConsolidacion.py) y poblar las bases de datos (poblar_motores_datos.py).
* /documentacion/ y headers.md: Diccionarios de datos y referencia de las columnas disponibles en cada archivo resultante.
* /workflow/: Contiene el flujo exportado de KNIME (.knwf).
* /PowerBi/: Contiene el Dashboard final del proyecto.
* /Videos/: Enlaces a las demostraciones del funcionamiento del sistema.

---
"*Desarrollado para la materia de Análisis de Datos.*"

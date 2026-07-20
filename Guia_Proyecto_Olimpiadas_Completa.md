# 🏅 Proyecto Final de Análisis de Datos: Olimpiadas
**Materia:** Análisis de Datos (EPN) | **Período:** 2026-A

---

## ✅ FASE 1: Lo que hemos realizado (Inventario de Datos)
*Se ha logrado generar, extraer y estructurar una base de aproximadamente 5.5 millones de registros, cumpliendo con los requisitos de fuentes reales y simuladas.*

### 1. Datos Reales y Verificables (~2.5 Millones)
- **Kaggle (Histórico y Eventos):** Archivos `athletes.csv`, `nocs.csv`, `medallists.csv` con el histórico de participantes de verano e invierno (1896-2024).
- **Noticias Globales (GDELT):** Extracción automatizada vía Google BigQuery sobre la percepción y el sentimiento mundial de los Juegos Olímpicos.
- **Redes Sociales (Kaggle Twitter/Reddit):** Volumen masivo desestructurado para aplicar análisis de sentimiento público.
- **Medallero Oficial (Web Scraping):** Extracción estructurada y automatizada mediante Python (BeautifulSoup/Regex) directamente desde Wikipedia.

### 2. Datos Climáticos (1984 - 2024)
- **API Open-Meteo:** Extracción masiva y paginada (chunking) del clima por hora de las últimas 10 ciudades sede.
- **Distribución de formatos de ingesta:**
  - **JSON:** Ciudades europeas (preparado para MongoDB).
  - **CSV:** Ciudades americanas (preparado para motores NoSQL como Cassandra o Neo4j).
  - **SQLite/MySQL:** Ciudades de Asia y Oceanía (inserción directa a base de datos relacional mediante SQLAlchemy).

### 3. Datos Generados/Simulados con Inconsistencias (~2 Millones)
- **Economía - Venta de Entradas (CSV):** Precios y categorías (con valores nulos y precios negativos inyectados para forzar el uso de filtros).
- **IoT - Telemetría Biométrica (JSON):** Ritmo cardíaco y saturación de oxígeno de atletas (con strings corruptos en columnas numéricas y outliers).
- **Movilidad Urbana (Parquet):** Big Data de tráfico de pasajeros en estaciones (con errores de capitalización y registros huérfanos).

---

## 🚀 FASE 2: Lo que vamos a hacer (Guía y Roles)

### Rol A: Arquitectura, Análisis Avanzado y Power BI
**Tecnologías:** Python, Jupyter, MySQL, MongoDB, SQL Server, Power BI.
*   **Despliegue de Bases de Datos:** Levantar localmente los motores y cargar los archivos en sus respectivos entornos. Crear la base de datos `Olimpiadas_DWH` en SQL Server.
*   **Análisis NLP y EDA:** Utilizar un Jupyter Notebook para aplicar bibliotecas (como VADER o TextBlob) al texto de GDELT/Twitter y guardar el sentimiento. Crear 3 a 4 gráficos exploratorios obligatorios.
*   **Dashboards Inteligentes:** Conectar Power BI a SQL Server utilizando un Modelo en Estrella. Desarrollar 4 páginas de análisis (Resumen, Exploración, Detalle y Recomendaciones).
*   **Medidas DAX:** Construir al menos 8 medidas DAX fuertes (KPIs, variaciones de crecimiento, rankings e índices propios como un "Índice de Eficiencia").

### Rol B: Orquestación del ETL en KNIME
**Tecnologías:** KNIME Analytics Platform.
*   **Lectura de Fuentes Diversas:** Conectar nodos específicos (`MongoDB Reader`, `DB Reader`, `CSV Reader`, `Parquet Reader`) para integrar todos los datos aislados.
*   **Auditoría de Calidad:** Configurar un reporte de calidad inicial que cuente exactamente los nulos y duplicados que se inyectaron en el código Python.
*   **Limpieza de Datos:** Aplicar nodos como `Row Filter` (remover anomalías), `Missing Value` (imputaciones de O2 o precios) y `String Manipulation` (corregir mayúsculas/minúsculas).
*   **Modelado Relacional:** Hacer Joins de las tablas dimensionales (Atletas, Eventos, Sedes) con las tablas de hechos (Clima, Entradas, Telemetría).
*   **Exportación al Data Warehouse:** Utilizar un `DB Writer` para despachar la tabla matriz definitiva y limpia hacia SQL Server.

---

## 📦 FASE 3: Entregables y Defensa (Trabajo en Equipo)
- **Repositorio Git:** Organización en carpetas, archivos `.py`, `.ipynb`, `.knwf` (KNIME), `README.md`, y el `requirements.txt`.
- **Informe Técnico (Formato IEEE):** Documento a doble columna que consolide la arquitectura, reglas de calidad de datos, y justificación de conclusiones.
- **Videos Explicativos:**
  - **Video 1 (Rol B - 4 a 6 min):** Defensa del proceso ETL, transformación de nodos y manejo de calidad de datos en KNIME.
  - **Video 2 (Rol A - 4 a 6 min):** Defensa de la toma de decisiones, explicación del Modelo de Datos en Power BI y las funciones DAX creadas.

---
---

# 📄 ANEXO: DOCUMENTO OFICIAL DEL PROYECTO (RÚBRICA Y REQUISITOS)

## 1. Objetivo general
Diseñar, implementar y defender una solución integral de análisis de datos que combine Python, KNIME y Power BI para extraer, limpiar, transformar, integrar, modelar, analizar y visualizar información proveniente de múltiples fuentes, generando conclusiones útiles para la toma de decisiones.

## 2. Nivel de dificultad actualizado
Este proyecto mantiene la estructura del proyecto 2025-A, pero eleva moderadamente el nivel técnico mediante automatización, validación de calidad de datos, modelado analítico reproducible, integración KNIME-Python y dashboards con indicadores accionables.

## 3. Herramientas obligatorias
| Herramienta | Uso mínimo obligatorio | Evidencia esperada | Peso técnico sugerido |
| :--- | :--- | :--- | :--- |
| **Python** | Extracción, limpieza avanzada, validación, análisis exploratorio y/o modelado básico. | Notebooks .ipynb, scripts .py, requirements.txt y datasets procesados. | 35% |
| **KNIME** | Workflow ETL completo con lectura, limpieza, combinación, transformación y exportación. | Archivo .knwf o capturas del workflow, nodos documentados y ejecución reproducible. | 30% |
| **Power BI** | Modelo de datos, medidas DAX, visualizaciones, segmentadores y narrativa ejecutiva. | Archivo .pbix, capturas del dashboard y explicación de decisiones. | 35% |

## 4. Caso de estudio
Cada grupo seleccionará un problema real de análisis de datos. El proyecto debe integrar al menos 6 fuentes de datos relacionadas con una temática principal (En nuestro caso: **Deportes, rendimiento, asistencia, resultados o comportamiento de aficionados - Olimpiadas**).

## 5. Requisitos técnicos mínimos
1. Usar al menos 6 fuentes de datos. Mínimo 3 deben ser reales y verificables; las demás pueden ser complementarias, generadas o enriquecidas.
2. Integrar datos estructurados y semiestructurados: CSV/Excel, JSON/API, base de datos SQL o archivo plano exportado.
3. Trabajar con al menos 2'500.000 registros acumulados. Para nota máxima se recomienda superar 2'000.000 de registros.
4. Crear un proceso ETL reproducible en KNIME que incluya limpieza, normalización, unión de tablas y exportación final.
5. Crear al menos un notebook o script en Python para EDA, limpieza avanzada, validación de calidad o modelado analítico.
6. Construir un modelo en estrella o modelo tabular en Power BI con tabla de hechos, dimensiones y relaciones correctamente definidas.
7. Implementar mínimo 8 medidas DAX, incluyendo indicadores de tendencia, ranking, variación porcentual y KPI principal.
8. Aplicar análisis de sentimiento si el caso contiene texto; si no contiene texto, aplicar una técnica alternativa: clustering, scoring, predicción simple, detección de anomalías o segmentación.
9. Documentar el diccionario de datos y las reglas de transformación aplicadas.
10. Publicar el proyecto en GitHub con estructura organizada y README técnico.

## 6. Requisitos de calidad de datos
* Identificar valores nulos, duplicados, inconsistencias, outliers y formatos incorrectos.
* Crear una tabla o reporte de calidad antes y después de la limpieza.
* Definir reglas de limpieza justificadas: eliminación, imputación, estandarización, conversión de tipos y tratamiento de outliers.
* Validar que las llaves, relaciones y agregaciones sean coherentes antes de construir el dashboard.
* Incluir al menos 5 pruebas de validación: conteo de registros, rangos válidos, unicidad, integridad referencial y consistencia de fechas.

## 7. Arquitectura esperada
La arquitectura debe evidenciar el flujo completo de datos: fuentes -> extracción -> staging -> limpieza -> integración -> modelo analítico -> visualización -> conclusiones.
* **Capa de fuentes:** archivos CSV/Excel, APIs, JSON, bases SQL, web scraping permitido solo si respeta términos de uso.
* **Capa de procesamiento:** KNIME como flujo principal y Python como soporte analítico/automatización.
* **Capa de almacenamiento:** carpeta data/raw, data/processed y, opcionalmente, SQLite/PostgreSQL/MYSQL.
* **Capa de visualización:** Power BI con modelo relacional, medidas DAX y dashboards explicativos.
* **Capa de documentación:** informe IEEE, README, diccionario de datos, capturas y videos.

## 8. Dashboards y preguntas de análisis
El dashboard debe responder al menos 12 preguntas o casos de análisis. No basta con mostrar gráficos: cada visualización debe apoyar una conclusión o recomendación.
* Mínimo 4 páginas de dashboard: resumen ejecutivo, exploración, análisis detallado y conclusiones/recomendaciones.
* Mínimo 10 visualizaciones útiles y no repetitivas.
* Mínimo 4 segmentadores relevantes: fecha, ubicación, categoría, fuente, grupo, producto, evento u otro.
* Mínimo 3 KPIs principales con interpretación.
* Cada página debe incluir una breve narrativa: qué se observa, por qué importa y qué decisión permite tomar.

## 9. Entregables
| Entregable | Contenido mínimo | Porcentaje |
| :--- | :--- | :--- |
| **Informe IEEE doble columna** | Caso de estudio, objetivos, arquitectura, fuentes, ETL, calidad de datos, análisis, visualizaciones, resultados, conclusiones, recomendaciones, problemas encontrados y link GitHub. | 25% |
| **Proyecto técnico en GitHub** | Scripts Python, notebook, workflow KNIME, archivo Power BI, datasets de muestra o instrucciones de descarga, README, requirements.txt y estructura de carpetas. | 25% |
| **Dashboard Power BI** | Modelo de datos, medidas DAX, páginas de dashboard, KPIs, filtros, narrativa y conclusiones accionables. | 20% |
| **Videos explicativos** | Video 1: proceso de datos y ETL. Video 2: análisis del dashboard y conclusiones. Cada video de 4 a 6 minutos. | 15% |
| **Defensa individual** | Presentación técnica de 15 a 20 minutos por grupo. Preguntas individuales sobre código, KNIME, Power BI, datos y decisiones tomadas. | 15% |

## 10. Herramientas Obligatorias
* Debe utilizar, en su arquitectura, al menos 2 bases de datos SQL y 2 NoSQL.
* Python, Knime para el proceso de etl.
* Power BI para las visualizaciones.

## 11. Rúbrica resumida (Criterios de "Excelente")
* **Integración de datos:** 10+ fuentes, flujo reproducible, datos reales y bien documentados.
* **Python:** EDA, limpieza, validación y análisis/modelado bien explicado.
* **KNIME:** Workflow completo, ordenado, comentado y exportable.
* **Power BI:** Modelo correcto, DAX sólido, narrativa y decisiones claras.
* **Conclusiones:** Basadas en evidencia, accionables y conectadas al caso.

*Ejemplo de distribución de fuentes para nota máxima:*
* APIS REST: 4
* Open Data: 3
* Web Scraping: 1
* Dataset (Kaggle, UCI, etc.): 2

## 12. Criterios de defensa individual
* Cada estudiante debe explicar su aporte específico y demostrar que comprende el flujo completo.
* El docente podrá solicitar la ejecución de un script, notebook, workflow KNIME o explicación de una medida DAX.
* Se evaluará la coherencia entre informe, repositorio, dashboard y exposición.

## 13. Recomendaciones para subir el nivel sin volverlo excesivo
* Agregar una métrica compuesta o índice propio del grupo.
* Comparar resultados por ciudad, fecha, categoría o segmento.
* Incluir una página de "calidad de datos" en Power BI.
* Usar Python para automatizar una parte repetitiva del proceso.
* Crear un pequeño modelo predictivo o de segmentación solo si aporta al caso de estudio.
* Mantener el enfoque en decisiones: qué problema se detectó y qué acción se recomienda.
* *Nota: la innovación, automatización, buena documentación y defensa técnica individual serán consideradas como plus para la nota final.*

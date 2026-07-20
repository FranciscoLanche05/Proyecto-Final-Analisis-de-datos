import pandas as pd
import numpy as np
import os
from datetime import timedelta

print("Iniciando motor de generación y corrupción de datos...")

# Crear carpeta principal
carpeta_salida = r"datasets\datos_simulados"
os.makedirs(carpeta_salida, exist_ok=True)

# Fijar semilla para reproducibilidad
np.random.seed(42)
num_registros = 1000000

# ==========================================
# 1. ECONOMÍA: VENTA DE ENTRADAS (CSV - Estructurado)
# ==========================================
print("\nGenerando 1M de registros de Venta de Entradas (CSV)...")
fechas_base = pd.to_datetime('2024-07-01') + pd.to_timedelta(np.random.randint(0, 45, num_registros), unit='D')

df_tickets = pd.DataFrame({
    'ID_Ticket': np.arange(1, num_registros + 1),
    'Fecha_Compra': fechas_base,
    'ID_Evento': np.random.randint(100, 500, num_registros),
    'Precio_USD': np.round(np.random.uniform(50, 500, num_registros), 2),
    'Categoria': np.random.choice(['General', 'VIP', 'Prensa'], num_registros)
})

# 💥 INYECTANDO "SUCIEDAD" (Aprox 50% afectado)
print(" -> Inyectando errores de calidad en Entradas...")
# 1. Nulos (Missing values)
df_tickets.loc[np.random.choice(num_registros, 50000, replace=False), 'Precio_USD'] = np.nan
# 2. Outliers (Precios negativos imposibles)
df_tickets.loc[np.random.choice(num_registros, 20000, replace=False), 'Precio_USD'] = -150.00
# 3. Inconsistencias de texto
df_tickets.loc[np.random.choice(num_registros, 30000, replace=False), 'Categoria'] = 'v.i.p'
df_tickets.loc[np.random.choice(num_registros, 30000, replace=False), 'Categoria'] = 'GENERAL '
# 4. Duplicados intencionales (Copiar 10,000 filas al final)
df_tickets = pd.concat([df_tickets, df_tickets.sample(10000)])

# Guardar en 2 Chunks para evitar archivos pesados (>50MB)
df_tickets.iloc[:500000].to_csv(os.path.join(carpeta_salida, "tickets_parte1.csv"), index=False)
df_tickets.iloc[500000:].to_csv(os.path.join(carpeta_salida, "tickets_parte2.csv"), index=False)
print(" -> Guardado en 2 archivos CSV.")


# ==========================================
# 2. IOT: TELEMETRÍA BIOMÉTRICA (JSON - Semiestructurado)
# ==========================================
print("\nGenerando 1M de registros de Telemetría (JSON)...")
df_bio = pd.DataFrame({
    'ID_Lectura': np.arange(1, num_registros + 1),
    'ID_Atleta': np.random.randint(1000, 5000, num_registros),
    'BPM': np.round(np.random.normal(140, 15, num_registros)),
    'Saturacion_O2': np.random.uniform(92, 100, num_registros)
})

# 💥 INYECTANDO "SUCIEDAD"
print(" -> Inyectando errores de calidad en Telemetría...")
# 1. Outliers Biológicos (BPM de 800 es un error de sensor)
df_bio.loc[np.random.choice(num_registros, 40000, replace=False), 'BPM'] = 850
# 2. Tipos de datos incorrectos (Strings en columnas numéricas)
df_bio['BPM'] = df_bio['BPM'].astype(object)
df_bio.loc[np.random.choice(num_registros, 10000, replace=False), 'BPM'] = "Error_Sensor"
# 3. Nulos estructurales
df_bio.loc[np.random.choice(num_registros, 60000, replace=False), 'Saturacion_O2'] = np.nan

# Guardar en 4 Chunks JSON (El JSON ocupa mucho espacio en disco)
chunk_size = 250000
for i in range(4):
    inicio = i * chunk_size
    fin = (i + 1) * chunk_size
    ruta_json = os.path.join(carpeta_salida, f"biometria_chunk_{i+1}.json")
    df_bio.iloc[inicio:fin].to_json(ruta_json, orient='records')
print(" -> Guardado en 4 archivos JSON.")


# ==========================================
# 3. MOVILIDAD: TRANSPORTE PÚBLICO (Parquet - Big Data)
# ==========================================
print("\nGenerando 1M de registros de Movilidad Urbana (Parquet)...")
ciudades = ["Paris", "Marsella", "Lyon", "Niza"]
df_movilidad = pd.DataFrame({
    'ID_Viaje': np.arange(1, num_registros + 1),
    'Ciudad_Sede': np.random.choice(ciudades, num_registros),
    'Estacion': np.random.choice(['Gare du Nord', 'Estadio', 'Villa Olimpica', 'Aeropuerto'], num_registros),
    'Pasajeros_Hora': np.random.randint(500, 10000, num_registros)
})

# 💥 INYECTANDO "SUCIEDAD"
print(" -> Inyectando errores de calidad en Movilidad...")
# 1. Inconsistencias de capitalización (Requiere limpieza String Manipulation en KNIME)
df_movilidad.loc[np.random.choice(num_registros, 40000, replace=False), 'Ciudad_Sede'] = 'paRis'
df_movilidad.loc[np.random.choice(num_registros, 40000, replace=False), 'Ciudad_Sede'] = 'LYON'
# 2. Registros huérfanos (Estaciones que no existen en el catálogo)
df_movilidad.loc[np.random.choice(num_registros, 15000, replace=False), 'Estacion'] = 'Estacion_Desconocida_99'
# 3. Nulos
df_movilidad.loc[np.random.choice(num_registros, 50000, replace=False), 'Ciudad_Sede'] = None

# Guardar en Parquet (Alta compresión, 1M de registros pesará menos de 15MB)
ruta_parquet = os.path.join(carpeta_salida, "movilidad_urbana.parquet")
df_movilidad.to_parquet(ruta_parquet, index=False)
print(f" -> Guardado en 1 archivo Parquet único (ultra comprimido).")

print("\n" + "="*50)
print("¡GENERACIÓN COMPLETA!")
print("Archivos listos con millones de registros y listos para ser limpiados en KNIME.")
print("="*50)
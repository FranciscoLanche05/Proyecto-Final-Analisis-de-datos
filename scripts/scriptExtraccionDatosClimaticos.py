import requests
import pandas as pd
import time
import os
import json
from sqlalchemy import create_engine

print("Iniciando motor de extracción multiformato con CHUNKING (Open-Meteo API)...")

# Dividimos las ciudades según el motor de base de datos destino
ciudades_mongodb = {"Paris": {"lat": 48.8566, "lon": 2.3522}, "London": {"lat": 51.5074, "lon": -0.1278}, "Athens": {"lat": 37.9838, "lon": 23.7275}}
ciudades_nosql2 = {"Rio de Janeiro": {"lat": -22.9068, "lon": -43.1729}, "Atlanta": {"lat": 33.7490, "lon": -84.3880}}
ciudades_mysql = {"Tokyo": {"lat": 35.6895, "lon": 139.6917}, "Beijing": {"lat": 39.9042, "lon": 116.4074}, "Sydney": {"lat": -33.8688, "lon": 151.2093}, "Seoul": {"lat": 37.5665, "lon": 126.9780}}

# Dividimos los 24 años en bloques de 4 años para no saturar la API
periodos = [
    ("2000-01-01", "2003-12-31"),
    ("2004-01-01", "2007-12-31"),
    ("2008-01-01", "2011-12-31"),
    ("2012-01-01", "2015-12-31"),
    ("2016-01-01", "2019-12-31"),
    ("2020-01-01", "2024-01-01")
]

carpeta_salida = r"datasets\clima_historico_distribuido"
os.makedirs(carpeta_salida, exist_ok=True)

ruta_sql = os.path.join(carpeta_salida, "clima_mysql.db")
motor_sql = create_engine(f"sqlite:///{ruta_sql}")

def extraer_clima_por_bloques(ciudad, coords):
    print(f"\nDescargando datos de {ciudad}...")
    df_ciudad_completo = []
    
    for inicio, fin in periodos:
        print(f"  -> Extrayendo bloque {inicio[:4]} a {fin[:4]}...")
        url = "https://archive-api.open-meteo.com/v1/archive"
        params = {
            "latitude": coords["lat"], "longitude": coords["lon"],
            "start_date": inicio, "end_date": fin,
            "hourly": ["temperature_2m", "relative_humidity_2m", "precipitation"],
            "timezone": "auto"
        }
        
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if 'hourly' in data and len(data['hourly']['time']) > 0:
                    df_temp = pd.DataFrame(data['hourly'])
                    df_temp['Ciudad'] = ciudad
                    df_ciudad_completo.append(df_temp)
                else:
                    print("     [!] JSON vacío devuelto por la API.")
            else:
                print(f"     [!] Error de API: {response.status_code}")
        except Exception as e:
            print(f"     [!] Excepción: {e}")
            
        time.sleep(2) # Pausa estricta de 2 segundos para respetar el límite de la API gratuita
        
    if df_ciudad_completo:
        return pd.concat(df_ciudad_completo, ignore_index=True)
    return None

total_registros = 0

# ==========================================
# 1. EXTRACCIÓN PARA MONGODB (Formato JSON)
# ==========================================
print("\n--- Procesando Grupo MongoDB (JSON) ---")
datos_mongo = []
for ciudad, coords in ciudades_mongodb.items():
    df = extraer_clima_por_bloques(ciudad, coords)
    if df is not None:
        datos_mongo.extend(df.to_dict(orient='records'))
        total_registros += len(df)

# Partir en 2 archivos para no generar un JSON demasiado pesado
mitad = len(datos_mongo) // 2

ruta_json_p1 = os.path.join(carpeta_salida, "clima_europa_mongodb_part1.json")
ruta_json_p2 = os.path.join(carpeta_salida, "clima_europa_mongodb_part2.json")

with open(ruta_json_p1, 'w', encoding='utf-8') as f:
    json.dump(datos_mongo[:mitad], f)
with open(ruta_json_p2, 'w', encoding='utf-8') as f:
    json.dump(datos_mongo[mitad:], f)

print(f"\n-> Guardado JSON masivo en 2 partes: {ruta_json_p1} y {ruta_json_p2}")

# ==========================================
# 2. EXTRACCIÓN PARA CASSANDRA/NEO4J (Formato CSV)
# ==========================================
print("\n--- Procesando Grupo NoSQL Alternativo (CSV) ---")
dfs_nosql2 = []
for ciudad, coords in ciudades_nosql2.items():
    df = extraer_clima_por_bloques(ciudad, coords)
    if df is not None:
        dfs_nosql2.append(df)
        total_registros += len(df)

if dfs_nosql2:
    ruta_csv = os.path.join(carpeta_salida, "clima_america_nosql.csv")
    pd.concat(dfs_nosql2, ignore_index=True).to_csv(ruta_csv, index=False)
    print(f"\n-> Guardado CSV masivo: {ruta_csv}")

# ==========================================
# 3. EXTRACCIÓN PARA MYSQL (Base de datos relacional directa)
# ==========================================
print("\n--- Procesando Grupo MySQL (Directo a DB Relacional) ---")
for ciudad, coords in ciudades_mysql.items():
    df = extraer_clima_por_bloques(ciudad, coords)
    if df is not None:
        df.to_sql(name='historico_clima', con=motor_sql, if_exists='append', index=False)
        total_registros += len(df)
        print(f"-> Inserción SQL exitosa de {len(df):,} filas para {ciudad}")

print("\n" + "="*50)
print(f"¡EXTRACCIÓN Y DISTRIBUCIÓN MULTIMOTOR COMPLETADA!")
print(f"Total de registros reales procesados: {total_registros:,}")
print("="*50)
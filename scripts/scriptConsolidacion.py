import os
import pandas as pd
import json
import glob
import re
import shutil

# Directorios de trabajo
DIR_BASE = "datasets"
DIR_SALIDA = "datasets_consolidados"
os.makedirs(DIR_SALIDA, exist_ok=True)

def limpiar_texto(texto):
    """
    Función para limpieza avanzada (NLP-prep).
    Elimina URLs y menciones (@) para que el análisis de sentimiento sea más preciso.
    """
    if pd.isna(texto):
        return ""
    texto = str(texto)
    # Quitar URLs
    texto = re.sub(r'http\S+|www\S+|https\S+', '', texto, flags=re.MULTILINE)
    # Quitar Menciones @
    texto = re.sub(r'\@\w+', '', texto)
    return texto.strip()

def consolidar_tweets():
    print("Consolidando y limpiando Tweets...")
    # Leer todos los archivos CSV en la carpeta tweets
    archivos = glob.glob(os.path.join(DIR_BASE, "tweets", "*.csv"))
    dfs = []
    for archivo in archivos:
        try:
            # engine='python' y on_bad_lines='skip' nos protegen de filas corruptas
            df = pd.read_csv(archivo, on_bad_lines='skip', engine='python', encoding='utf-8')
            dfs.append(df)
        except Exception as e:
            print(f"Error leyendo {archivo}: {e}")
    
    if dfs:
        df_unido = pd.concat(dfs, ignore_index=True)
        # Limpieza avanzada en la columna de texto ('text' suele ser la común en Kaggle Twitter)
        col_texto = None
        for col in ['text', 'tweet', 'content', 'Text']:
            if col in df_unido.columns:
                col_texto = col
                break
        
        if col_texto:
            print(f"  -> Aplicando limpieza de texto (Regex) en la columna '{col_texto}'")
            df_unido[col_texto] = df_unido[col_texto].apply(limpiar_texto)
            # Eliminar tweets que se quedaron vacíos después de la limpieza
            df_unido = df_unido[df_unido[col_texto] != ""]
            
        ruta_salida = os.path.join(DIR_SALIDA, "tweets_consolidados.csv")
        df_unido.to_csv(ruta_salida, index=False, encoding='utf-8')
        print(f"[OK] Tweets consolidados guardados en {ruta_salida} ({len(df_unido)} registros)")

def consolidar_resultados_paris():
    print("\nConsolidando Resultados de París 2024...")
    # Leer los ~35 archivos de resultados por deporte
    archivos = glob.glob(os.path.join(DIR_BASE, "paris 2024", "results", "*.csv"))
    dfs = []
    for archivo in archivos:
        try:
            df = pd.read_csv(archivo, encoding='utf-8')
            # Extraer el nombre del deporte del nombre del archivo y añadirlo como columna
            deporte = os.path.basename(archivo).replace(".csv", "")
            df['Deporte'] = deporte
            dfs.append(df)
        except Exception as e:
            pass
            
    if dfs:
        # Concatenar todos los deportes en una sola gran tabla
        df_unido = pd.concat(dfs, ignore_index=True)
        ruta_salida = os.path.join(DIR_SALIDA, "paris_resultados_consolidados.csv")
        df_unido.to_csv(ruta_salida, index=False, encoding='utf-8')
        print(f"[OK] Resultados París consolidados guardados en {ruta_salida} ({len(df_unido)} registros)")

def consolidar_biometria():
    print("\nConsolidando chunks de Biometría IoT...")
    # Leer los 4 archivos JSON
    archivos = glob.glob(os.path.join(DIR_BASE, "datos_simulados_limpios", "biometria_limpia.json"))
    datos_unidos = []
    for archivo in archivos:
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                data = json.load(f)
                datos_unidos.extend(data)
        except Exception as e:
            print(f"Error leyendo {archivo}: {e}")
            
    if datos_unidos:
        ruta_salida = os.path.join(DIR_SALIDA, "biometria_consolidada.json")
        with open(ruta_salida, 'w', encoding='utf-8') as f:
            json.dump(datos_unidos, f, indent=4)
        print(f"[OK] Biometría consolidada guardada en {ruta_salida} ({len(datos_unidos)} registros)")

def consolidar_movilidad():
    print("\nConsolidando Movilidad Urbana...")
    ruta = os.path.join(DIR_BASE, "datos_simulados_limpios", "movilidad_limpia.parquet")
    if os.path.exists(ruta):
        df = pd.read_parquet(ruta)
        ruta_salida = os.path.join(DIR_SALIDA, "movilidad_consolidada.csv")
        df.to_csv(ruta_salida, index=False, encoding='utf-8')
        print(f"[OK] Movilidad consolidada guardada en {ruta_salida} ({len(df)} registros)")
    else:
        print("[WARNING] No se encontró movilidad_limpia.parquet, corre primero el notebook de limpieza")

def consolidar_tickets():
    print("\nConsolidando tickets simulados...")
    archivos = glob.glob(os.path.join(DIR_BASE, "datos_simulados_limpios", "tickets_limpios.csv"))
    dfs = []
    for archivo in archivos:
        try:
            df = pd.read_csv(archivo, encoding='utf-8')
            dfs.append(df)
        except:
            pass
            
    if dfs:
        df_unido = pd.concat(dfs, ignore_index=True)
        ruta_salida = os.path.join(DIR_SALIDA, "tickets_consolidados.csv")
        df_unido.to_csv(ruta_salida, index=False, encoding='utf-8')
        print(f"[OK] Tickets consolidados guardados en {ruta_salida} ({len(df_unido)} registros)")

def copiar_archivos_restantes():
    print("\nCopiando datasets adicionales (no consolidados) para el Estudiante B...")
    archivos_a_copiar = [
        "clima_historico_distribuido/clima_america_nosql.csv",
        "clima_historico_distribuido/clima_europa_mongodb_part1.json",
        "clima_historico_distribuido/clima_europa_mongodb_part2.json",
        "clima_historico_distribuido/clima_mysql.db",
        "120 year athletes and results/athlete_events.csv",
        "120 year athletes and results/noc_regions.csv",
        "PIByDatosPoblacionales/api_rest_pib_historico.json",
        "PIByDatosPoblacionales/api_rest_poblacion_paises.json",
        "indiceDeDesarrolloHumano/HDR25_Composite_indices_complete_time_series.csv"
    ]
    
    for ruta_relativa in archivos_a_copiar:
        origen = os.path.join(DIR_BASE, ruta_relativa)
        # Extraer solo el nombre del archivo para pegarlo en la raiz de la carpeta destino
        nombre_archivo = os.path.basename(origen)
        destino = os.path.join(DIR_SALIDA, nombre_archivo)
        
        if os.path.exists(origen):
            try:
                shutil.copy2(origen, destino)
                print(f"[OK] Copiado: {nombre_archivo}")
            except Exception as e:
                print(f"Error copiando {nombre_archivo}: {e}")
        else:
            print(f"[WARNING] No se encontró el archivo: {origen}")

if __name__ == "__main__":
    print("=== INICIANDO CONSOLIDACIÓN DE DATOS (FASE 2) ===")
    consolidar_tweets()
    consolidar_resultados_paris()
    consolidar_biometria()
    consolidar_tickets()
    consolidar_movilidad()  
    copiar_archivos_restantes()
    
    print("\n=== CONSOLIDACIÓN COMPLETADA ===")
    print(f"TODOS los archivos necesarios están ahora en la carpeta: '{DIR_SALIDA}'")

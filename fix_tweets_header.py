import pandas as pd
import os

CARPETA = os.path.join("datasets", "tweets")
PART1 = os.path.join(CARPETA, "Olympics_Tokyo_tweets_part1.csv")
PART2 = os.path.join(CARPETA, "Olympics_Tokyo_tweets_part2.csv")
RECONSTRUIDO = os.path.join(CARPETA, "tokyo_tweets_reconstruido.csv")

# 1. Unir los dos archivos crudos (byte a byte) para reconstruir la fila que quedó cortada
with open(RECONSTRUIDO, "wb") as salida:
    for archivo in [PART1, PART2]:
        with open(archivo, "rb") as f:
            salida.write(f.read())

print("Archivos unidos en:", RECONSTRUIDO)

# 2. Leer el archivo reconstruido (ya con la fila completa y el header correcto)
df = pd.read_csv(RECONSTRUIDO, on_bad_lines='warn', engine='python', encoding='utf-8')
print("Filas reconstruidas:", len(df))
print("Duplicados por id:", df.duplicated(subset=['id']).sum())

# 3. Volver a partir en 2 mitades limpias, respetando filas completas y con header en ambas
mitad = len(df) // 2
df.iloc[:mitad].to_csv(PART1, index=False, encoding='utf-8')
df.iloc[mitad:].to_csv(PART2, index=False, encoding='utf-8')

# 4. Borrar el archivo temporal reconstruido
os.remove(RECONSTRUIDO)

print("Listo. part1 y part2 sobrescritos correctamente, cada uno con su header.")
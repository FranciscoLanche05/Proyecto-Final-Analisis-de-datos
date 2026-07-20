import pandas as pd
import json
import os

carpeta = os.path.join(os.path.dirname(__file__), "..", "datasets_consolidados")
salida = os.path.join(os.path.dirname(__file__), "..", "documentacion", "diccionario_datos.csv")
os.makedirs(os.path.dirname(salida), exist_ok=True)

registros = []

for archivo in os.listdir(carpeta):
    ruta = os.path.join(carpeta, archivo)
    if archivo.endswith(".csv"):
        df = pd.read_csv(ruta, nrows=5)
        nombre = archivo.replace(".csv", "")
    elif archivo.endswith(".json"):
        with open(ruta, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list) and len(data) > 0:
            df = pd.DataFrame(data[:5])
            nombre = archivo.replace(".json", "")
        else:
            continue
    else:
        continue

    for col in df.columns:
        registros.append({
            "Dataset": nombre,
            "Columna": col,
            "Tipo_Dato": str(df[col].dtype),
            "Descripcion": "",
            "Fuente": "",
            "Regla_Transformacion": ""
        })

df_dict = pd.DataFrame(registros)
df_dict.to_csv(salida, index=False)
print(f"Diccionario generado: {salida}")
print(f"Total: {len(df_dict)} columnas en {df_dict['Dataset'].nunique()} datasets")
print(df_dict.groupby("Dataset")["Columna"].count())

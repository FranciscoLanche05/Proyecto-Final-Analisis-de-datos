import pandas as pd
import os
import json

# ════════════════════════════════════════════════════════════════
#   CONFIGURACIÓN — edita según lo que tengas disponible
# ════════════════════════════════════════════════════════════════

DATASETS_FOLDER = "datasets"

# ── SQL (descomenta y llena los que uses) ────────────────────────
SQL_CONNECTIONS = [
    # SQLite  → solo ruta al archivo
    # {"type": "sqlite",    "db": "mi_base.db"},

    # SQL Server
    # {"type": "sqlserver", "server": "localhost", "database": "miDB"},

    # MySQL / MariaDB
    # {"type": "mysql",     "host": "localhost", "user": "root", "password": "", "database": "miDB"},

    # PostgreSQL
    # {"type": "postgresql","host": "localhost", "user": "postgres", "password": "", "database": "miDB"},

    # Oracle XE
    # {"type": "oracle",    "dsn": "localhost:1521/XE", "user": "tu_usuario", "password": "tu_pass"},
]

# ── NoSQL (descomenta y llena los que uses) ──────────────────────
NOSQL_CONNECTIONS = [
    # MongoDB
    # {"type": "mongodb", "uri": "mongodb://localhost:27017", "database": "miDB"},
]

# ════════════════════════════════════════════════════════════════
#   FUNCIONES DE CONEXIÓN SQL
# ════════════════════════════════════════════════════════════════

def contar_tablas_sql(config):
    tipo = config["type"]
    resultados = []
    try:
        if tipo == "sqlite":
            import sqlite3
            conn = sqlite3.connect(config["db"])
            engine = None
        elif tipo == "sqlserver":
            import pyodbc
            conn_str = f"Driver={{SQL Server}};Server={config['server']};Database={config['database']};Trusted_Connection=yes"
            conn = pyodbc.connect(conn_str)
            engine = None
        elif tipo == "mysql":
            import mysql.connector
            conn = mysql.connector.connect(
                host=config["host"], user=config["user"],
                password=config["password"], database=config["database"]
            )
            engine = None
        elif tipo == "postgresql":
            import psycopg2
            conn = psycopg2.connect(
                host=config["host"], user=config["user"],
                password=config["password"], database=config["database"]
            )
            engine = None
        elif tipo == "oracle":
            import cx_Oracle
            conn = cx_Oracle.connect(f"{config['user']}/{config['password']}@{config['dsn']}")
            engine = None
        else:
            return []

        tablas = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table'" 
                             if tipo == "sqlite" 
                             else "SELECT table_name FROM information_schema.tables WHERE table_schema = DATABASE()" 
                             if tipo == "mysql"
                             else "SELECT tablename FROM pg_tables WHERE schemaname='public'"
                             if tipo == "postgresql"
                             else "SELECT table_name FROM user_tables"
                             if tipo == "oracle"
                             else "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'",
                             conn)

        col = tablas.columns[0]
        for tabla in tablas[col]:
            conteo = pd.read_sql(f"SELECT COUNT(*) as total FROM {tabla}", conn)
            resultados.append({
                "Origen": f"[{tipo.upper()}] {config.get('database', config.get('db', ''))}",
                "Archivo/Tabla": tabla,
                "Registros": int(conteo["total"][0]),
                "Columnas": "-"
            })
        conn.close()
    except Exception as e:
        resultados.append({
            "Origen": f"[{tipo.upper()}]",
            "Archivo/Tabla": config.get("database", config.get("db", "")),
            "Registros": f"ERROR: {e}",
            "Columnas": "-"
        })
    return resultados


# ════════════════════════════════════════════════════════════════
#   FUNCIONES DE CONEXIÓN NOSQL
# ════════════════════════════════════════════════════════════════

def contar_colecciones_nosql(config):
    tipo = config["type"]
    resultados = []
    try:
        if tipo == "mongodb":
            from pymongo import MongoClient
            client = MongoClient(config["uri"])
            db = client[config["database"]]
            for coleccion in db.list_collection_names():
                total = db[coleccion].count_documents({})
                resultados.append({
                    "Origen": f"[MONGODB] {config['database']}",
                    "Archivo/Tabla": coleccion,
                    "Registros": total,
                    "Columnas": "-"
                })
            client.close()
    except Exception as e:
        resultados.append({
            "Origen": f"[{tipo.upper()}]",
            "Archivo/Tabla": config.get("database", ""),
            "Registros": f"ERROR: {e}",
            "Columnas": "-"
        })
    return resultados


# ════════════════════════════════════════════════════════════════
#   LEER ARCHIVOS LOCALES (CSV, Excel, JSON, PKL, Parquet, TSV…)
# ════════════════════════════════════════════════════════════════

def leer_archivo(ruta, ext):
    if ext == ".csv":
        return pd.read_csv(ruta, encoding="utf-8", on_bad_lines='skip', engine='python')
    elif ext in [".xlsx", ".xls"]:
        return pd.read_excel(ruta)
    elif ext == ".pkl":
        return pd.read_pickle(ruta)
    elif ext == ".json":
        with open(ruta, "r", encoding="utf-8") as f:
            data = json.load(f)
        return pd.DataFrame(data) if isinstance(data, list) else pd.json_normalize(data)
    elif ext == ".parquet":
        return pd.read_parquet(ruta)
    elif ext == ".tsv":
        return pd.read_csv(ruta, sep="\t", encoding="utf-8", on_bad_lines='skip', engine='python')
    elif ext == ".xml":
        return pd.read_xml(ruta)
    elif ext == ".feather":
        return pd.read_feather(ruta)
    elif ext == ".orc":
        return pd.read_orc(ruta)
    return None


# ════════════════════════════════════════════════════════════════
#   MAIN
# ════════════════════════════════════════════════════════════════

resultados = []

FORMATOS_SOPORTADOS = {".csv", ".xlsx", ".xls", ".pkl", ".json",
                       ".parquet", ".tsv", ".xml", ".feather", ".orc"}

# ── 1. Archivos locales ──────────────────────────────────────────
for root, dirs, files in os.walk(DATASETS_FOLDER):
    for file in files:
        ext = os.path.splitext(file)[1].lower()
        if ext not in FORMATOS_SOPORTADOS:
            continue
        ruta = os.path.join(root, file)
        carpeta = os.path.relpath(root, DATASETS_FOLDER)
        try:
            df = leer_archivo(ruta, ext)
            resultados.append({
                "Origen": carpeta,
                "Archivo/Tabla": file,
                "Registros": len(df),
                "Columnas": df.shape[1]
            })
        except Exception as e:
            resultados.append({
                "Origen": carpeta,
                "Archivo/Tabla": file,
                "Registros": f"ERROR: {e}",
                "Columnas": "-"
            })

# ── 2. Bases de datos SQL ────────────────────────────────────────
for config in SQL_CONNECTIONS:
    resultados.extend(contar_tablas_sql(config))

# ── 3. NoSQL ─────────────────────────────────────────────────────
for config in NOSQL_CONNECTIONS:
    resultados.extend(contar_colecciones_nosql(config))


# ════════════════════════════════════════════════════════════════
#   REPORTE FINAL
# ════════════════════════════════════════════════════════════════

resumen = pd.DataFrame(resultados)
pd.set_option("display.max_colwidth", 45)
pd.set_option("display.max_rows", 200)

print("\n" + "=" * 70)
print("   RESUMEN DE DATASETS")
print("=" * 70)
print(resumen.to_string(index=False))

# ── Total general ────────────────────────────────────────────────
solo_numeros = resumen[pd.to_numeric(resumen["Registros"], errors="coerce").notna()]
total = pd.to_numeric(solo_numeros["Registros"]).sum()

print("=" * 70)
print(f"  Total de datasets analizados : {len(resumen):>10,}")
print(f"  Total de registros (todos)   : {int(total):>10,}")
print("=" * 70)
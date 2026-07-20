import requests
import json
import os

# Crear la carpeta datasets si no existe
os.makedirs('datasets', exist_ok=True)

def extraer_datos_paises():
    """
    Se conecta a la API del 'Banco Mundial' para obtener la Población Total.
    Útil para crear la métrica de 'Medallas per Cápita' en Power BI.
    """
    print("📡 Obteniendo datos de población (Banco Mundial API)...")
    # Indicador SP.POP.TOTL = Población total para el año 2023.
    url = "http://api.worldbank.org/v2/country/all/indicator/SP.POP.TOTL?format=json&date=2023&per_page=15000"
    response = requests.get(url)
    
    if response.status_code == 200:
        datos = response.json()
        # La API del Banco Mundial devuelve la información en el índice 1
        registros = datos[1]
        paises_filtrados = []
        
        for reg in registros:
            if reg.get("value") is not None and reg.get("countryiso3code") != "":
                info = {
                    "codigo_iso": reg.get("countryiso3code", ""), # Este código sirve para unir con la tabla de atletas
                    "pais": reg["country"]["value"],
                    "poblacion": reg.get("value", 0)
                }
                paises_filtrados.append(info)
            
        ruta_archivo = os.path.join('datasets', 'api_rest_poblacion_paises.json')
        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            json.dump(paises_filtrados, f, ensure_ascii=False, indent=4)
        print(f"✅ Éxito: {len(paises_filtrados)} países guardados en '{ruta_archivo}'")
    else:
        print("❌ Error al conectar con API de Población")

def extraer_datos_pib():
    """
    Se conecta a la API del 'Banco Mundial' para obtener el PIB Histórico.
    Útil para analizar si el éxito olímpico depende del dinero.
    """
    print("📡 Obteniendo datos del PIB Histórico (Banco Mundial API)...")
    # Indicador NY.GDP.PCAP.CD = PIB per cápita en dólares. Años 2000 al 2023.
    url = "http://api.worldbank.org/v2/country/all/indicator/NY.GDP.PCAP.CD?format=json&date=2000:2023&per_page=15000"
    response = requests.get(url)
    
    if response.status_code == 200:
        datos = response.json()
        # La API del Banco Mundial devuelve la información en el índice 1
        registros = datos[1] 
        pib_filtrado = []
        
        for reg in registros:
            if reg.get("value") is not None and reg.get("countryiso3code") != "":
                info = {
                    "codigo_iso": reg["countryiso3code"],
                    "pais": reg["country"]["value"],
                    "anio": reg["date"],
                    "pib_per_capita_usd": round(reg["value"], 2)
                }
                pib_filtrado.append(info)
                
        ruta_archivo = os.path.join('datasets', 'api_rest_pib_historico.json')
        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            json.dump(pib_filtrado, f, ensure_ascii=False, indent=4)
        print(f"✅ Éxito: {len(pib_filtrado)} registros de PIB guardados en '{ruta_archivo}'")
    else:
        print("❌ Error al conectar con la API del Banco Mundial")

if __name__ == "__main__":
    print("--- INICIANDO EXTRACCIÓN DE NUEVAS FUENTES (APIs) ---")
    extraer_datos_paises()
    print("-" * 50)
    extraer_datos_pib()
    print("--- EXTRACCIÓN FINALIZADA ---")

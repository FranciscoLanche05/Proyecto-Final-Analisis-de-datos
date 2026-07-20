import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def scraping_wikipedia_delegaciones():
    url = "https://en.wikipedia.org/wiki/2024_Summer_Olympics"
    print(f"Iniciando web scraping en: {url}...")
    
    # El User-Agent es clave para que Wikipedia no bloquee el script
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except Exception as e:
        print(f"Error de conexión: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    delegaciones = []
    
    print("Analizando la estructura HTML con BeautifulSoup...")
    
    # Buscamos en todas las etiquetas de lista de la página web
    for li in soup.find_all('li'):
        texto = li.get_text(strip=True)
        
        # Expresión regular: Busca el patrón "Nombre País (Número)" 
        # Ejemplo: "Ecuador (40)" o "United States (592)[a]"
        match = re.search(r'^([A-Za-zÀ-ÿ\s\-\'\,]+?)\s*\((\d+)\)(?:\[.*?\])*$', texto)
        
        if match:
            pais = match.group(1).strip()
            atletas = int(match.group(2))
            
            # Filtro lógico para evitar capturar enlaces u otros textos basura
            if len(pais) < 40 and atletas <= 650:
                delegaciones.append({'NOC': pais, 'Atletas': atletas})
                
    if delegaciones:
        df = pd.DataFrame(delegaciones)
        # Wikipedia suele repetir la lista de países en la página, eliminamos duplicados
        df = df.drop_duplicates(subset='NOC').sort_values(by='Atletas', ascending=False)
        print(f"¡Éxito! Se extrajeron {len(df)} países directamente del código fuente.")
        return df
        
    print("No se encontraron los datos con el patrón especificado.")
    return None

# Ejecución
df_resultado = scraping_wikipedia_delegaciones()

if df_resultado is not None:
    print("\nPrevisualización de datos extraídos:")
    print(df_resultado.head())
    
    # Guardamos en tu estructura de carpetas exacta
    ruta_salida = r"datasets\paris 2024\delegaciones_wikipedia.csv"
    df_resultado.to_csv(ruta_salida, index=False, encoding='utf-8')
    print(f"\nDatos guardados exitosamente en: {ruta_salida}")
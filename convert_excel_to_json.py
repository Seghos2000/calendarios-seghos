import pandas as pd
import json

# Cargar el Excel
excel_file = 'm_ranking Seghos 2025_26.xlsx'
xl = pd.ExcelFile(excel_file)

# Diccionario final
ranking = {}

# Procesar cada hoja o sección
for sheet_name in xl.sheet_names:
    df = xl.parse(sheet_name)
    df = df.dropna(how='all')  # Eliminar filas vacías
    if 'Jugador' in df.columns:
        jugadores = df.to_dict(orient='records')
        ranking[sheet_name] = jugadores

# Guardar como JSON
with open('ranking.json', 'w', encoding='utf-8') as f:
    json.dump(ranking, f, ensure_ascii=False, indent=2)

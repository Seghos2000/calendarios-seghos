import pandas as pd
import json

# Cargar el Excel
excel_file = 'm_ranking Seghos 2025_26.xlsx'
df = pd.read_excel(excel_file, header=None)
df = df.where(pd.notnull(df), None)


# Diccionario final
ranking = {}
categoria_actual = None
columnas = ["Jugador", "Jugados", "Ganados", "Perdidos", "Jue. favor", "Jue. contra", "% victorias"]
bloque = []

for _, row in df.iterrows():
    fila = row.tolist()
    if any(isinstance(cell, str) and "División" in cell for cell in fila):
        # Guardar bloque anterior
        if categoria_actual and bloque:
            bloque_df = pd.DataFrame(bloque, columns=columnas)
            bloque_df = bloque_df.where(pd.notnull(bloque_df), None)		
            ranking[categoria_actual] = bloque_df.to_dict(orient='records')
            bloque = []
        # Nueva categoría
        categoria_actual = next(cell for cell in fila if isinstance(cell, str))
    elif fila[0] == "Jugador":
        continue  # encabezado
    elif categoria_actual and isinstance(fila[0], str):
        bloque.append(fila[:7])  # solo las primeras 7 columnas

# Guardar último bloque
if categoria_actual and bloque:
    bloque_df = pd.DataFrame(bloque, columns=columnas)
    ranking[categoria_actual] = bloque_df.to_dict(orient='records')


# Exportar a JSON
with open('ranking.json', 'w', encoding='utf-8') as f:
    json.dump(ranking, f, ensure_ascii=False, indent=2)

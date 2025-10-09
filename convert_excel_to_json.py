import pandas as pd
import json

# Ruta del archivo Excel
excel_file = 'm_ranking Seghos 2025_26.xlsx'

# Leer el archivo sin encabezados fijos
df = pd.read_excel(excel_file, header=None)

# Inicializar variables
ranking = {}
categoria_actual = None
columnas = ["Jugador", "Jugados", "Ganados", "Perdidos", "Jue. favor", "Jue. contra", "% victorias"]
bloque = []

# Recorrer cada fila
for _, row in df.iterrows():
    fila = row.tolist()

    # Detectar nueva categoría
    if any(isinstance(cell, str) and cell.strip() in [
        "División Honor Nacional",
        "Tercera Nacional",
        "División de Honor Territorial",
        "DOBLES"
    ] for cell in fila):
        # Guardar bloque anterior si tiene datos
        if categoria_actual and bloque:
            bloque_df = pd.DataFrame(bloque, columns=columnas)
            bloque_df.dropna(how='all', inplace=True)
            if not bloque_df.empty:
                bloque_df = bloque_df.where(pd.notnull(bloque_df), None)
                ranking[categoria_actual] = bloque_df.to_dict(orient='records')
            bloque = []

        # Nueva categoría
        categoria_actual = next(cell for cell in fila if isinstance(cell, str))

    # Ignorar encabezados repetidos
    elif fila[0] == "Jugador":
        continue

    # Agregar fila de datos si hay categoría activa
    elif categoria_actual and isinstance(fila[0], str):
        bloque.append(fila[:7])  # Solo las primeras 7 columnas

# Guardar el último bloque
if categoria_actual and bloque:
    bloque_df = pd.DataFrame(bloque, columns=columnas)
    bloque_df.dropna(how='all', inplace=True)
    if not bloque_df.empty:
        bloque_df = bloque_df.where(pd.notnull(bloque_df), None)
        ranking[categoria_actual] = bloque_df.to_dict(orient='records')

# Exportar a JSON
with open('ranking.json', 'w', encoding='utf-8') as f:
    json.dump(ranking, f, ensure_ascii=False, indent=2)

print("✅ ranking.json generado correctamente.")

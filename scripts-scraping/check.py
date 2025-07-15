import pandas as pd

# 1. Cargar el archivo CSV
archivo_original = 'productos_mercadona.csv'
df = pd.read_csv(archivo_original)

# 2. Verificar columna de IDs (ajusta el nombre de la columna)
columna_id = 'product_code'  # Cambia esto al nombre de tu columna de IDs

# 3. Mostrar información inicial
print(f"Registros totales: {len(df)}")
print(f"Registros duplicados: {df.duplicated(subset=[columna_id]).sum()}")

# 4. Eliminar duplicados manteniendo la primera ocurrencia
df_limpio = df.drop_duplicates(subset=[columna_id], keep='first')

# 5. Guardar resultados en nuevo archivo
archivo_limpio = 'productos_mercadona2.csv'
df_limpio.to_csv(archivo_limpio, index=False)

# 6. Mostrar resumen
print("\nResumen de limpieza:")
print(f"Registros originales: {len(df)}")
print(f"Registros únicos: {len(df_limpio)}")
print(f"Duplicados eliminados: {len(df) - len(df_limpio)}")
print(f"Archivo limpio guardado como: {archivo_limpio}")
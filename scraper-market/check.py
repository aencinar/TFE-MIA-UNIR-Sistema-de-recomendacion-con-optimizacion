import pandas as pd

archivo_original = 'productos_mercadona.csv'
df = pd.read_csv(archivo_original)

columna_id = 'product_code' 

print(f"Registros totales: {len(df)}")
print(f"Registros duplicados: {df.duplicated(subset=[columna_id]).sum()}")

df_limpio = df.drop_duplicates(subset=[columna_id], keep='first')


archivo_limpio = 'productos_mercadona2.csv'
df_limpio.to_csv(archivo_limpio, index=False)


print("\nResumen de limpieza:")
print(f"Registros originales: {len(df)}")
print(f"Registros únicos: {len(df_limpio)}")
print(f"Duplicados eliminados: {len(df) - len(df_limpio)}")
print(f"Archivo limpio guardado como: {archivo_limpio}")
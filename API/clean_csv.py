import pandas as pd
import re

def clean_product_codes(input_csv: str, output_csv: str):
    # 1. Lee todo como strings
    df = pd.read_csv(input_csv, dtype={ 'product_code': str })
    
    # 2. Extrae la parte numérica antes del primer guion
    #    Usa .str.extract para no crear columna extra
    df['product_code'] = (
        df['product_code']
          .str.strip()                  # quita espacios exteriores
          .str.extract(r'^(\d+)', expand=False)  # captura solo dígitos iniciales
    )
    
    # 3. Elimina filas sin código válido
    df = df[df['product_code'].notna()]
    
    # 4. Convierte a entero
    df['product_code'] = df['product_code'].astype(int)

    
    # 6. Guarda el CSV limpio
    df.to_csv(output_csv, index=False)
    print(f"Guardado {len(df)} filas limpias en '{output_csv}'")

if __name__ == "__main__":
    clean_product_codes(
        input_csv="./API/productos_filtrados.csv",
        output_csv="./API/productos_filtrados2.csv"
    )

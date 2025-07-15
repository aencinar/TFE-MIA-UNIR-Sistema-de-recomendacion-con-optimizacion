import csv

input_file = 'productos_mercadona.csv'
output_file = 'productos_mercadona2.csv'

with open(input_file, 'r', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    rows = list(reader)

header = rows[0]
if 'subcategory' not in header:
    header.append('subcategory')
subcategory_index = header.index('subcategory')

for i in range(1, len(rows)):
    row = rows[i]

    if len(row) < len(header):
        row += [''] * (len(header) - len(row))

    contiene_estandar = any("estandar" in str(cell).lower() for cell in row)

    if not contiene_estandar:
        row[subcategory_index] = 'estandar'


with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print("Archivo actualizado correctamente:", output_file)

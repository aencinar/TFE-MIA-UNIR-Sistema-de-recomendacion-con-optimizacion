import csv

input_file = 'productos_eroski.csv'
output_file = 'productos_eroski2.csv'

with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
    reader = list(csv.reader(infile))
    header = reader[0]

    rows = [header]

    for row in reader[1:]:
        if len(row) >= 4:
            texto_col4 = row[3].lower()
            if 'sin gluten' in texto_col4 and 'sin lactosa' not in texto_col4:
                if len(row) >= 7:
                    row[6] = 'Celiaco'
        rows.append(row)

with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile)
    writer.writerows(rows)

print(f"Archivo actualizado guardado como '{output_file}'")

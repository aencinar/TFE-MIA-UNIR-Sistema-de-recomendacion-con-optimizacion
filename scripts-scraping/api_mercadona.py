import requests
import csv
import os
import datetime

categories = {
    'Aceite': 1, 'Vinagre': 2, 'Sal': 3, 'Especias': 4, 'Salsas': 5,
    'Bebidas sin alcohol': 6, 'Bebidas con alcohol': 7, 'Aperitivos': 8, 'Arroz': 9, 'Legumbre': 10,
    'Pasta': 11, 'Dulces y pasteleria': 12, 'Comida preparada': 13, 'Cacao, café, infusiones': 14,
    'Carne': 15, 'Pescado': 16, 'Cereales': 17, 'Galletas': 18, 'Charcuteria': 19,
    'Quesos': 20, 'Congelados': 21, 'Conservas': 22, 'Caldos y sopas': 23, 'Cremas': 24,
    'Fruta': 25, 'Verduras': 26, 'Ensaladas': 27, 'Huevos': 28, 'Lacteos': 29,
    'Panaderia': 30, 'Pizzas': 31, 'Zumos': 32, 'Bicarbonato': 33, 'Sazonador': 34, 'Harina y masas':35 ,
    'Comida mexicana': 36, 'Comida oriental': 37, 'Otros':38, 'Azucar, edulcorantes, otros': 39, 
    'Mermelada, membrillo, miel, otros': 40
}

category_name = "Otros"  # 👈 Puedes cambiarlo según la categoría que estás scrapeando
category_code = categories.get(category_name, 0)

# Configuración inicial
url = "https://tienda.mercadona.es/api/categories/79/?lang=es&wh=4471"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

OUTPUT_FILE = "productos_mercadona.csv"
HEADERS = ["supermarket", "product_code", "category", "name", "price", "lastUpdate"]


def get_products():
    # Realizar la petición a la API
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()

        # Extraer productos de la estructura anidada de la API
        for category in data.get("categories", []):
            for product in category.get("products", []):
                product_info = {
                    "supermarket": "Mercadona",
                    "product_code": product.get("id"),
                    "category": category_code,  # Categoría del URL
                    "name": product.get("display_name", ""),
                    "price": product.get("price_instructions", {}).get("unit_price", 0),
                    "lastUpdate": datetime.datetime.now().timestamp()
                }
                    
                save_csv(product_info)

        print(f"Todo ok")    

    else:
        print(f"Error al obtener datos: Código {response.status_code}")


def save_csv(product):

    write_header = not os.path.exists(OUTPUT_FILE) or os.stat(OUTPUT_FILE).st_size == 0
    # Guardar en CSV
    with open(OUTPUT_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        if write_header:
            writer.writeheader()
        writer.writerow(product)


if __name__ == "__main__":
    get_products()
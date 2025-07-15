import csv
import datetime
import os
import requests
from bs4 import BeautifulSoup

# Categorías mapeadas a códigos
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

urls = [
    
]


OUTPUT_FILE = "productos_alcampo.csv"
HEADERS = ["supermarket", "product_code", "category", "name", "price", "lastUpdate", "subcategory"]

# Asumimos que el nombre de la categoría está en la URL o se lo pasamos tú manualmente
category_name = "Dulces y pasteleria"  # 👈 Puedes cambiarlo según la categoría que estás scrapeando
category_code = categories.get(category_name, 0)

def scrape_products():

    total_products = 0

    for url in urls:

        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            card_products = soup.find_all('div', class_='product-card-container')

            for card in card_products:
                title = card.find('div', class_="title-container")
                title = title.text.strip() if title else "Sin título"

                price = card.find('span', attrs={"data-test": 'fop-price'})
                price = price.text.replace("€", "").strip() if price else "Sin precio"

                href_tag = card.find('a', attrs={"data-test": "fop-product-link"})
                href = href_tag['href'] if href_tag and 'href' in href_tag.attrs else None
                product_code = href.strip("/").split("/")[-1]

                product = {
                    "supermarket": "Alcampo",
                    "product_code": product_code,
                    "category": category_code,
                    "name": title,
                    "price": price,
                    "lastUpdate": datetime.datetime.now().timestamp(),
                    "subcategory": "Sin lactosa"
                }

                save_csv(product)

                total_products +=1

                print(f"\nTotal productos guardados: {total_products}")

        else:
            print(f"[{response}] ❌ Error")


def save_csv(product):

    write_header = not os.path.exists(OUTPUT_FILE) or os.stat(OUTPUT_FILE).st_size == 0
    # Guardar en CSV
    with open(OUTPUT_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        if write_header:
            writer.writeheader()
        writer.writerow(product)


if __name__ == "__main__":
    scrape_products()
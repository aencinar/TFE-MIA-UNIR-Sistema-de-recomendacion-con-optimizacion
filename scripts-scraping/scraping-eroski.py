import csv
import datetime
import os
import re
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
    "Referer": "https://www.carrefour.es/",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

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



OUTPUT_FILE = "productos_eroski.csv"
HEADERS = ["supermarket", "product_code", "category", "name", "price", "lastUpdate", "subcategory"]

# Asumimos que el nombre de la categoría está en la URL o se lo pasamos tú manualmente
category_name = "Panaderia"  # 👈 Puedes cambiarlo según la categoría que estás scrapeando
category_code = categories.get(category_name, 0)

def init_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # O quítalo para ver el navegador
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver


def scroll_and_collect(driver, url, subcategory):
    print(f"🔍 Visitando: {url}")
    driver.get(url)
    time.sleep(2)

    # Scroll infinito
    last_height = driver.execute_script("return document.body.scrollHeight")
    scroll_attempts = 0
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            scroll_attempts += 1
            if scroll_attempts >= 2:
                break
        else:
            last_height = new_height
            scroll_attempts = 0

    time.sleep(2)

    # Extraer productos
    products = driver.find_elements(By.CLASS_NAME, "product-description")
    total = 0
    for product in products:
        try:
            title_el = product.find_element(By.CSS_SELECTOR, ".product-title a")
            name = title_el.get_attribute("innerText").strip()
            if not name:
                name = title_el.get_attribute("title") or "Sin nombre"
            href = title_el.get_attribute("href")
            match = re.search(r'/productdetail/(\d+)-', href)
            product_code = match.group(1) if match else "0000"

            try:
                price_el = product.find_element(By.CLASS_NAME, "price-offer-now")
                price = price_el.text.replace("€", "").strip()
            except NoSuchElementException:
                price = "Sin precio"

            save_csv({
                "supermarket": "Eroski",
                "product_code": product_code,
                "category": category_code,
                "name": name,
                "price": price,
                "lastUpdate": datetime.datetime.now().timestamp(),
                "subcategory": subcategory
            })

            total += 1
        except Exception as e:
            print(f"❌ Error procesando producto: {e}")
            continue

    print(f"✅ Total productos extraídos de {subcategory}: {total}")


def save_csv(product):

    write_header = not os.path.exists(OUTPUT_FILE) or os.stat(OUTPUT_FILE).st_size == 0
    # Guardar en CSV
    with open(OUTPUT_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        if write_header:
            writer.writeheader()
        writer.writerow(product)


def main():
    driver = init_driver()
    for url in urls:
        scroll_and_collect(driver, url, "Celiaco")
    driver.quit()


if __name__ == "__main__":
    main()
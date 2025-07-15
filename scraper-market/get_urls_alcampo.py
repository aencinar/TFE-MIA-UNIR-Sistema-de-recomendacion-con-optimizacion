import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.compraonline.alcampo.es"

def get_sidebar_category_urls():
    url = f"{BASE_URL}/categories/bebidas/refrescos/refresco-de-naranja/OCRefrescoNaranja?sortBy=favorite"
    
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Las categorías están en la barra lateral izquierda, suelen ser <a> con href
        sidebar_links = soup.select('#product-page ul a[href]')

        urls = [BASE_URL + a['href'] for a in sidebar_links]
        return urls

# Ejecutar
if __name__ == "__main__":
    urls = get_sidebar_category_urls()
    for u in urls:
        print(u)

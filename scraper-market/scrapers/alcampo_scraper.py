import datetime
from bs4 import BeautifulSoup
from scrapers.base_scraper import BaseScraper
from utils.http_utils import fetch_html

class AlcampoScraper(BaseScraper):
    def __init__(self):
        super().__init__(supermarket_name="Alcampo")

    def _fetch_page_data(self, url, **kwargs):
        # Add headers if Alcampo requires them (e.g. User-Agent)
        # headers = {"User-Agent": "MyFriendlyScraper/1.0"}
        # return fetch_html(url, headers=headers)
        return fetch_html(url)

    def _parse_products_from_page(self, page_content, category_name, subcategory_name=None, url=None):
        products_list = []
        soup = BeautifulSoup(page_content, 'html.parser')

        # Alcampo uses product "tiles" or "cards"
        # The class names might change, inspect HTML if no products are found
        card_products = soup.find_all('div', class_='product-card-container')
        if not card_products:
             # Fallback: Alcampo sometimes uses this structure
            card_products = soup.find_all('div', class_='product-tile-container')


        for card in card_products:
            name = "Sin título"
            product_code = None
            price = 0.0

            # Extract name
            # Common class for product name/title
            title_tag = card.find(['div', 'h3', 'h4'], class_=['productName', 'title-container', 'product-name-wrapper'])
            if title_tag:
                # Sometimes the name is in a child <a> or <span>
                name_inner_tag = title_tag.find(['a', 'span'])
                if name_inner_tag:
                    name = name_inner_tag.text.strip()
                else:
                    name = title_tag.text.strip()
            else: # More specific fallbacks if the general one fails
                title_tag = card.find('div', class_="product_name") # Another possible class
                if title_tag and title_tag.find('a'):
                    name = title_tag.find('a').text.strip()
                elif card.find('a', class_="product-link"): # Check for a link with product name
                     name = card.find('a', class_="product-link").text.strip()


            # Extract price
            # Common class/attribute for price
            price_tag = card.find('span', attrs={"data-test": 'fop-price'})
            if not price_tag: # Fallback
                price_tag = card.find('div', class_='price')
            if not price_tag: # another Fallback for other structures
                price_tag = card.find('p', class_='price')

            if price_tag:
                # Price might be split into integer and decimal parts or have currency symbols
                # This logic tries to handle common cases
                price_text = ""
                if price_tag.find('span', class_='price-offer'): # Prioritize offer price
                    price_text = price_tag.find('span', class_='price-offer').text
                elif price_tag.find('strong', class_='price'): # Common pattern
                     price_text = price_tag.find('strong', class_='price').text
                else:
                    price_text = price_tag.text # General case

                # Clean price text
                price_text = price_text.replace("€", "").replace(",", ".").replace("\n", " ").strip()
                # Handle cases like "1. 23" -> "1.23"
                price_text_parts = price_text.split()
                if len(price_text_parts) > 1 and '.' in price_text_parts[0] and price_text_parts[1].isdigit():
                    price_text = price_text_parts[0] + price_text_parts[1]
                elif len(price_text_parts) == 1:
                     price_text = price_text_parts[0]
                else: # If multiple parts and not fitting the pattern, try to join and parse
                    price_text = "".join(price_text_parts)


                try:
                    price = float(price_text)
                except ValueError:
                    # print(f"Warning: Could not parse price for '{name}' from text '{price_text_original}'. Using 0.0.")
                    price = 0.0

            # Extract product code from product URL
            href_tag = card.find('a', attrs={"data-test": "fop-product-link"}) # Primary way
            if not href_tag: # Fallback if primary not found
                href_tag = card.find('a', class_='product-item-link')
            if not href_tag: # Another fallback
                 product_link_tag = card.find(lambda tag: tag.name == 'a' and tag.has_attr('href') and '/p/' in tag['href'])
                 if product_link_tag:
                     href_tag = product_link_tag


            if href_tag and 'href' in href_tag.attrs:
                href = href_tag['href']
                # Example Alcampo URL: /productos/alimentacion/aceites-vinagres-y-salsas/aceites/aceite-de-oliva/aceite-de-oliva-virgen-extra-coosur-botella-1-l/p/790300539
                # Example 2: /p/00000633700418-patatas-fritas-lays-al-punto-de-sal-bolsa-270-g
                # Example 3 (from search): /producto/pan-bimbo-sin-corteza-450g/390003835

                href_path_parts = href.split('?')[0].strip('/').split('/')

                if len(href_path_parts) > 0:
                    last_part = href_path_parts[-1]
                    # Case 1: /p/CODE or /p/CODE-description
                    if len(href_path_parts) > 1 and href_path_parts[-2] == 'p':
                        product_code = last_part.split('-', 1)[0]
                    # Case 2: /producto/DESCRIPTION/CODE
                    elif len(href_path_parts) > 1 and href_path_parts[-2] != 'p' and href_path_parts[0] == 'producto':
                         product_code = last_part
                    # Case 3: .../OC<CODE> (often category listings, but sometimes products are just numbers)
                    elif last_part.startswith("OC") and last_part[2:].isdigit():
                         pass # This is usually a category, not a product code, skip
                    # Case 4: Simple numeric code as last part, not preceded by /p/
                    elif last_part.isdigit() and (len(href_path_parts) < 2 or href_path_parts[-2] != 'p'):
                         product_code = last_part
                    # Case 5: product code is embedded in a data attribute of the card
                    if not product_code and card.has_attr('data-product-id'):
                        product_code = card['data-product-id']
                    elif not product_code and card.has_attr('data-ean'): # EAN can also serve as a unique ID
                        product_code = card['data-ean']


            if name and product_code and name != "Sin título" and price > 0: # Added price > 0 check
                product_info = {
                    "product_code": str(product_code).strip(), # Ensure it's a string
                    "name": name,
                    "price": price,
                    # subcategory is set by BaseScraper if not set here and subcategory_name is available
                }
                products_list.append(product_info)
            # else:
                # print(f"Skipping product: Name='{name}', Code='{product_code}', Price='{price}' (URL: {url})")

        return products_list

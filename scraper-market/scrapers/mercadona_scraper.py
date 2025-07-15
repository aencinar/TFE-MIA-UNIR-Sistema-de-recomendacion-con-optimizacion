import datetime
import requests # For making API calls
import json
from scrapers.base_scraper import BaseScraper
from utils.http_utils import DEFAULT_USER_AGENT # For consistent User-Agent
from utils.csv_utils import save_products_to_csv # Added import

class MercadonaScraper(BaseScraper):
    def __init__(self):
        super().__init__(supermarket_name="Mercadona")
        self.api_base_url = "https://tienda.mercadona.es/api/categories"
        # The default_headers from BaseScraper includes "subcategory".
        # Mercadona's API provides its own hierarchy which we'll use for "subcategory".

    def _fetch_page_data(self, api_category_id, **kwargs):
        # api_category_id is the ID from mercadona_scrape_list
        api_url = f"{self.api_base_url}/{api_category_id}/?lang=es"
        # Optional: add store ID if known and necessary: &wh=STORE_ID
        # e.g., store_id = kwargs.get('store_id')
        # if store_id:
        #     api_url += f"&wh={store_id}"

        headers = {
            "User-Agent": DEFAULT_USER_AGENT
        }
        print(f"Fetching Mercadona API: {api_url}")
        try:
            response = requests.get(api_url, headers=headers, timeout=20)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            print(f"Timeout fetching Mercadona API for category {api_category_id} from {api_url}")
            return None
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error fetching Mercadona API for category {api_category_id}: {e.response.status_code} from {api_url}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Request error fetching Mercadona API for category {api_category_id} from {api_url}: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from Mercadona API for category {api_category_id} from {api_url}: {e}")
            return None

    def _parse_products_from_page(self, api_response_json, category_name_for_mapping, subcategory_name=None, url=None):
        # category_name_for_mapping is the 'name' field from mercadona_scrape_list.
        # This is used by BaseScraper to determine the category_code.
        # Mercadona API's own category names within the response will go into our 'subcategory' field.

        products_list = []
        if not api_response_json:
            print("No API response JSON to parse for Mercadona.")
            return products_list

        # The API response for a category ID contains a "categories" list.
        # These are the actual product groupings/subcategories within the fetched main category.
        for mercadona_section in api_response_json.get("categories", []):
            mercadona_subcategory_display_name = mercadona_section.get("name", "Desconocido")

            for product_data in mercadona_section.get("products", []):
                product_id = product_data.get("id")
                display_name = product_data.get("display_name", "Sin nombre")

                price_info = product_data.get("price_instructions", {})
                unit_price = price_info.get("unit_price") # This is usually a float

                if not product_id or display_name == "Sin nombre" or unit_price is None or float(unit_price) <= 0:
                    # print(f"Skipping product: ID={product_id}, Name='{display_name}', Price={unit_price}")
                    continue

                product_info = {
                    "product_code": str(product_id).strip(),
                    "name": display_name.strip(),
                    "price": float(unit_price),
                    "subcategory": mercadona_subcategory_display_name.strip(),
                    # "category_name" and "category_code" will be set by BaseScraper using category_name_for_mapping
                }
                products_list.append(product_info)

        if not products_list:
            print(f"No products parsed from API response for category '{category_name_for_mapping}'. Check API response structure if products were expected.")
        return products_list

    # Override scrape_category_urls for Mercadona's specific needs (passing category ID)
    def scrape_category_urls(self, url_infos):
        # url_infos for Mercadona: list of dicts like {"id": "79", "name": "Aceite"}
        # where 'name' is the category name WE define for mapping to our categories.json
        all_products = []
        if not self.categories_map:
            print("Critical: Category mapping file (categories.json) not loaded. Cannot proceed with Mercadona scraper.")
            return

        for cat_info in url_infos:
            api_cat_id = cat_info.get("id")
            # This 'name' is crucial: it's the category name from mercadona_scrape_list
            # that we'll use for our CSV's 'category_name' field and for mapping to 'category_code'.
            our_defined_category_name = cat_info.get("name")

            if not api_cat_id or not our_defined_category_name:
                print(f"Skipping invalid entry in mercadona_scrape_list: {cat_info}")
                continue

            print(f"Processing {self.supermarket_name}: API Category ID '{api_cat_id}' (mapped to our category: '{our_defined_category_name}')...")

            # _fetch_page_data for Mercadona expects the API category ID
            api_response_json = self._fetch_page_data(api_cat_id)

            if api_response_json:
                # _parse_products_from_page uses our_defined_category_name for context if needed,
                # but primarily for BaseScraper to use for mapping.
                products_on_page = self._parse_products_from_page(
                    api_response_json, our_defined_category_name
                )

                if products_on_page:
                    # Get our internal category_code using the mapping from our_defined_category_name
                    internal_category_code = self.categories_map.get(our_defined_category_name)

                    if internal_category_code is None:
                         print(f"Warning: Category name '{our_defined_category_name}' from mercadona_urls.py not found in categories.json. Products will have code 0.")
                         internal_category_code = 0

                    processed_products_count = 0
                    for product in products_on_page:
                        product["supermarket"] = self.supermarket_name
                        product["category_name"] = our_defined_category_name
                        product["category_code"] = internal_category_code

                        # Ensure all default headers are present
                        for header_item in self.default_headers:
                            if header_item not in product:
                                product[header_item] = None # Initialize if missing

                        # Final validation before adding
                        if not product.get("product_code") or not product.get("name") or product.get("price") is None:
                            # print(f"Skipping malformed product after processing: {product}")
                            continue

                        all_products.append(product)
                        processed_products_count +=1

                    print(f"Successfully processed and added {processed_products_count} products from API category ID {api_cat_id} as '{our_defined_category_name}'.")
                else:
                    print(f"No products parsed for API category ID {api_cat_id} (Our Category: '{our_defined_category_name}').")
            else:
                print(f"Failed to fetch or decode data for API category ID {api_cat_id}.")

        if all_products:
            # BaseScraper's output_filename is e.g. "productos_mercadona.csv"
            # csv_utils saves it into "scraper-market/data/"
            save_products_to_csv(all_products, self.output_filename, headers=self.default_headers)
            print(f"Total {len(all_products)} products for {self.supermarket_name} saved.")
        else:
            print(f"No products collected for {self.supermarket_name}.")

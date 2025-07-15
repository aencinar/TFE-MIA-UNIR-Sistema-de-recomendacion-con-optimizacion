from abc import ABC, abstractmethod
import json
import os # Added os for path manipulation
from utils.csv_utils import save_products_to_csv
from utils.http_utils import fetch_html

class BaseScraper(ABC):
    def __init__(self, supermarket_name):
        self.supermarket_name = supermarket_name
        # Output filename will be like 'productos_alcampo.csv' and will be saved in scraper-market/data/
        self.output_filename = f"productos_{supermarket_name.lower().replace(' ', '_')}.csv"
        self.categories_map = self._load_categories()
        self.default_headers = ["supermarket", "product_code", "category_code", "category_name", "name", "price", "lastUpdate", "subcategory"]

    def _load_categories(self):
        # Corrected path to be relative to the project root where main.py might be run from
        # or ensure it's an absolute path or relative to this file's location.
        # For now, assuming execution from project root or that scraper-market is in PYTHONPATH
        config_path = os.path.join(os.path.dirname(__file__), "..", "config", "categories.json")
        # If running main.py from scraper-market directory, this needs to be "config/categories.json"
        # For robustness, let's try a path relative to this file first.
        if not os.path.exists(config_path):
            # Fallback for when main.py is in scraper-market and run from there
            config_path = "config/categories.json"
            if not os.path.exists(config_path):
                 # Fallback for when main.py is in root and run from there
                config_path = "scraper-market/config/categories.json"


        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Categories file not found. Tried: {config_path} and other fallbacks.")
            return {}
        except json.JSONDecodeError:
            print(f"Error: Categories file at {config_path} is not valid JSON.")
            return {}

    @abstractmethod
    def _fetch_page_data(self, url, **kwargs):
        pass

    @abstractmethod
    def _parse_products_from_page(self, page_content, category_name, subcategory_name=None, url=None):
        pass

    def scrape_category_urls(self, url_infos):
        all_products = []
        if not self.categories_map:
            print("Cannot proceed without category mappings.")
            return

        for url_info in url_infos:
            url = url_info["url"]
            category_name = url_info["category_name"]
            subcategory_name = url_info.get("subcategory_name")

            print(f"Processing {self.supermarket_name}: Category '{category_name}' (Subcategory: '{subcategory_name or ''}') from {url}...")
            page_content = self._fetch_page_data(url)

            if page_content:
                products_on_page = self._parse_products_from_page(
                    page_content, category_name, subcategory_name, url=url
                )
                if products_on_page:
                    category_code = self.categories_map.get(category_name)
                    if category_code is None:
                        print(f"Warning: Category '{category_name}' not found in categories_map. Using default code 0.")
                        category_code = 0 # Default or error code

                    for product in products_on_page:
                        product["supermarket"] = self.supermarket_name
                        product["category_name"] = category_name
                        product["category_code"] = category_code
                        if "subcategory" not in product and subcategory_name:
                            product["subcategory"] = subcategory_name
                        # Ensure all default headers are present
                        for header_item in self.default_headers:
                            if header_item not in product:
                                product[header_item] = None

                        # Ensure product_code is present, if not, it's a critical parsing error for this item
                        if product.get("product_code") is None:
                            print(f"Warning: Product '{product.get('name', 'Unknown Name')}' from {url} is missing 'product_code'. Skipping this product.")
                            continue # Skip adding this product

                        all_products.append(product)
                    print(f"Parsed {len(products_on_page)} products from {url} (after validation).")
                else:
                    print(f"No products found or parsed from {url}.")
            else:
                print(f"Failed to fetch data from {url}.")

        if all_products:
            # Pass self.output_filename directly, csv_utils will prepend scraper-market/data/
            save_products_to_csv(all_products, self.output_filename, headers=self.default_headers)
        else:
            print(f"No products collected for {self.supermarket_name}.")

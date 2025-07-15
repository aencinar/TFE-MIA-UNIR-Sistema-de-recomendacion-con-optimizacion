import datetime
import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, WebDriverException
from scrapers.base_scraper import BaseScraper
from utils.http_utils import DEFAULT_USER_AGENT # For consistency if needed

class EroskiScraper(BaseScraper):
    def __init__(self):
        super().__init__(supermarket_name="Eroski")
        self.driver = None

    def _init_driver(self):
        if self.driver is None:
            try:
                print("Initializing Selenium WebDriver for Eroski...")
                chrome_options = ChromeOptions()
                chrome_options.add_argument(f"user-agent={DEFAULT_USER_AGENT}")
                chrome_options.add_argument("--headless")
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-dev-shm-usage")
                chrome_options.add_argument("--disable-gpu")
                chrome_options.add_argument("window-size=1920,1080")
                chrome_options.add_argument("--log-level=3") # Suppress console logs from driver

                # Ensure webdriver_manager is used correctly
                try:
                    driver_path = ChromeDriverManager().install()
                    print(f"ChromeDriver installed at: {driver_path}")
                    self.driver = webdriver.Chrome(service=ChromeService(executable_path=driver_path), options=chrome_options)
                except Exception as e: # Catch specific webdriver_manager errors if possible
                    print(f"Error during ChromeDriverManager().install(): {e}")
                    print("Attempting to use system ChromeDriver if available in PATH...")
                    # Fallback if webdriver_manager fails (e.g. network issue, or specific OS issue)
                    self.driver = webdriver.Chrome(service=ChromeService(), options=chrome_options)

                self.driver.set_page_load_timeout(45) # Increased timeout for Eroski
                print("WebDriver initialized successfully.")
            except WebDriverException as e:
                print(f"WebDriverException on init: {e}")
                self.driver = None
            except Exception as e: # Catch any other exception during init
                print(f"An unexpected error occurred during WebDriver init: {e}")
                self.driver = None
        return self.driver

    def _fetch_page_data(self, url, **kwargs):
        driver = self._init_driver()
        if not driver:
            print(f"Skipping URL due to driver init failure: {url}")
            return None

        print(f"Fetching page with Selenium: {url}")
        try:
            driver.get(url)
            # Eroski might have cookie banners or popups. A generic delay might help.
            time.sleep(kwargs.get('initial_delay', 7)) # Increased initial delay for Eroski

            # Scroll to bottom to trigger dynamic content loading
            last_height = driver.execute_script("return document.body.scrollHeight")
            scroll_attempts = 0
            # Max attempts if height doesn't change, Eroski might load a lot.
            max_scroll_attempts = kwargs.get('max_scroll_attempts', 5)
            scroll_count = 0

            while scroll_count < kwargs.get('total_scrolls', 10): # Limit total scrolls
                print(f"Scrolling... Attempt {scroll_count + 1}/{kwargs.get('total_scrolls', 10)}")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(kwargs.get('scroll_delay', 4)) # Increased scroll delay

                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    scroll_attempts += 1
                    if scroll_attempts >= max_scroll_attempts:
                        print(f"Page height did not change after {max_scroll_attempts} scrolls. Assuming all content loaded for {url}")
                        break
                else:
                    last_height = new_height
                    scroll_attempts = 0
                scroll_count += 1

            print(f"Finished scrolling for {url}. Getting page source.")
            return driver.page_source
        except TimeoutException:
            print(f"Timeout loading page: {url}")
            return None
        except WebDriverException as e:
            print(f"WebDriverException during page fetch {url}: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error fetching page {url}: {e}")
            return None

    def _parse_products_from_page(self, page_content, category_name, subcategory_name=None, url=None):
        if not page_content:
            print(f"No page content to parse for {url if url else category_name}")
            return []

        products_list = []
        soup = BeautifulSoup(page_content, 'html.parser')

        # Main container for product cards (adjust based on Eroski's actual structure)
        # Common patterns: 'product-item', 'product-card', 'tile-product'
        product_cards = soup.find_all('div', class_=re.compile(r"product-item-line|product-description-hover"))

        if not product_cards:
            # Fallback if the above doesn't work. Looking for items with product titles.
            product_cards = soup.select('div.product-item, article.product-item, li.product-item') # More generic
            print(f"Using fallback product card selector. Found {len(product_cards)} cards for {url}.")


        print(f"Found {len(product_cards)} potential product cards on {url if url else category_name}.")

        for idx, card in enumerate(product_cards):
            name = "Sin nombre"
            product_code = None
            price = 0.0

            # Name extraction
            name_tag = card.select_one(".product-title a, .product-name a, .productTitle a, .name-product a")
            if name_tag:
                name = name_tag.get_text(strip=True)
                if not name and name_tag.has_attr('title'): # Fallback to title attribute
                    name = name_tag['title'].strip()

            # Product code extraction (often from the product URL)
            if name_tag and name_tag.has_attr('href'):
                href = name_tag['href']
                # Regex for /productdetail/CODE- or /p/CODE
                match = re.search(r'/(?:productdetail/|p/|producto/)(\d+)', href)
                if match:
                    product_code = match.group(1)
                else: # Fallback: try to get it from a data attribute or last part of URL if numeric
                    parts = href.strip("/").split("/")
                    if parts and parts[-1].isdigit():
                        product_code = parts[-1]

            if not product_code: # Try to find code in data attributes on the card
                code_attr = card.get('data-product-id') or card.get('data-sku') or card.get('id')
                if code_attr and code_attr.isdigit(): # Check if it looks like a code
                    product_code = code_attr
                elif code_attr: # If not purely digits, maybe it's like "prod_12345"
                    num_match = re.search(r'(\d+)', code_attr)
                    if num_match: product_code = num_match.group(1)


            # Price extraction
            # Eroski often has prices in 'price-offer-now', 'price-product', 'priceSale'
            price_tag = card.select_one(".price-offer-now, .price-product-price, .priceAmount, .price, .current-price")
            if price_tag:
                price_text = price_tag.get_text(strip=True)
                # Handle complex price formats (e.g., "1,23 €/Kg\n0,99 €") - take the main unit price
                price_text = price_text.split('\n')[0] # Take first line if multiple
                price_text = price_text.replace("€", "").replace(",", ".").replace(" ", "").strip()
                try:
                    price = float(price_text)
                except ValueError:
                    # print(f"Warning: Could not parse price for '{name}' from text '{price_text_original}'. Using 0.0.")
                    price = 0.0

            if name and name != "Sin nombre" and product_code and price > 0:
                product_info = {
                    "product_code": str(product_code).strip(),
                    "name": name,
                    "price": price,
                }
                products_list.append(product_info)
            # else:
            #     print(f"Skipped product on {url}: Name='{name}', Code='{product_code}', Price='{price}'")

        print(f"Parsed {len(products_list)} products from {url if url else category_name}.")
        return products_list

    def close_driver(self):
        if self.driver:
            print("Closing Selenium WebDriver for Eroski.")
            try:
                self.driver.quit()
            except WebDriverException as e:
                print(f"Error closing driver: {e}")
            finally:
                self.driver = None
                print("WebDriver closed.")

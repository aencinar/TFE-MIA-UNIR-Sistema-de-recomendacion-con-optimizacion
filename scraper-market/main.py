from scrapers.alcampo_scraper import AlcampoScraper
from urls.alcampo_urls import alcampo_scrape_list
from scrapers.eroski_scraper import EroskiScraper
from urls.eroski_urls import eroski_scrape_list
from scrapers.mercadona_scraper import MercadonaScraper
from urls.mercadona_urls import mercadona_scrape_list
import os
import sys

def run_alcampo():
    test_urls = alcampo_scrape_list[:2]
    if not test_urls:
        print("No URLs found in alcampo_scrape_list for testing.")
        return

    data_dir = "scraper-market/data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"Created data directory: {data_dir}")

    expected_output_file = os.path.join(data_dir, "productos_alcampo.csv")
    if os.path.exists(expected_output_file):
        os.remove(expected_output_file)
        print(f"Removed existing {expected_output_file} for a fresh Alcampo test run.")

    print(f"\n--- Starting Alcampo Scraper Test ---")
    print(f"Testing Alcampo scraper with {len(test_urls)} URLs...")
    scraper = AlcampoScraper()
    scraper.scrape_category_urls(test_urls)
    print(f"--- Alcampo Scraping Test Finished ---")
    if os.path.exists(expected_output_file):
        print(f"Alcampo: Output file at {expected_output_file}. Check its contents.")
    else:
        print(f"Warning: Alcampo: Output file {expected_output_file} was not created.")

def run_eroski():
    test_urls = eroski_scrape_list[:1]
    if not test_urls:
        print("No URLs found in eroski_scrape_list for testing.")
        return

    data_dir = "scraper-market/data"
    if not os.path.exists(data_dir): # Should be created by Alcampo run if it runs first
        os.makedirs(data_dir)
        print(f"Created data directory: {data_dir}")

    expected_output_file = os.path.join(data_dir, "productos_eroski.csv")
    if os.path.exists(expected_output_file):
        os.remove(expected_output_file)
        print(f"Removed existing {expected_output_file} for a fresh Eroski test run.")

    print(f"\n--- Starting Eroski Scraper Test ---")
    print(f"Testing Eroski scraper with {len(test_urls)} URL(s)...")
    scraper = EroskiScraper()
    try:
        scraper.scrape_category_urls(test_urls)
    except Exception as e:
        print(f"An error occurred during Eroski scraping: {e}")
    finally:
        scraper.close_driver()
    print(f"--- Eroski Scraping Test Finished ---")
    if os.path.exists(expected_output_file):
        print(f"Eroski: Output file at {expected_output_file}. Check its contents.")
    else:
        print(f"Warning: Eroski: Output file {expected_output_file} was not created.")

def run_mercadona():
    test_categories = mercadona_scrape_list[:1]
    if not test_categories:
        print("No categories found in mercadona_scrape_list for testing.")
        return

    data_dir = "scraper-market/data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"Created data directory: {data_dir}")

    expected_output_file = os.path.join(data_dir, "productos_mercadona.csv")
    if os.path.exists(expected_output_file):
        os.remove(expected_output_file)
        print(f"Removed existing {expected_output_file} for a fresh Mercadona test run.")

    print(f"\n--- Starting Mercadona Scraper Test ---")
    print(f"Testing Mercadona scraper with {len(test_categories)} category ID(s)...")
    scraper = MercadonaScraper()
    scraper.scrape_category_urls(test_categories)
    print(f"--- Mercadona Scraping Test Finished ---")
    if os.path.exists(expected_output_file):
        print(f"Mercadona: Output file at {expected_output_file}. Check its contents.")
    else:
        print(f"Warning: Mercadona: Output file {expected_output_file} was not created.")


if __name__ == "__main__":
    # When running 'python scraper-market/main.py' from '/app',
    # '/app/scraper-market' (the directory containing main.py) is automatically added to sys.path by Python.
    # Imports like 'from scrapers...' (referring to '/app/scraper-market/scrapers') will then work directly.
    print("Starting all scraper tests...")

    run_alcampo()
    print("\n---------------------------------------\n")
    run_eroski()
    print("\n---------------------------------------\n")
    run_mercadona()

    print("\nAll scraper tests finished.")

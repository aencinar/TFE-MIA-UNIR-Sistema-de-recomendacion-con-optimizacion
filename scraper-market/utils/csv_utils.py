import csv
import os
import datetime

DEFAULT_HEADERS = ["supermarket", "product_code", "category_code", "category_name", "name", "price", "lastUpdate", "subcategory"]

def save_products_to_csv(products_list, output_filename, headers=DEFAULT_HEADERS):
    if not products_list:
        print(f"No products to save to {output_filename}.")
        return

    # Construct the full path for the output file, placing it in the scraper-market/data directory
    base_data_dir = "scraper-market/data"
    if not os.path.exists(base_data_dir):
        os.makedirs(base_data_dir)
        print(f"Created data directory: {base_data_dir}")

    full_output_path = os.path.join(base_data_dir, output_filename)

    write_header = not os.path.exists(full_output_path) or os.stat(full_output_path).st_size == 0

    processed_products = []
    for product_data in products_list:
        processed_product = {header: product_data.get(header) for header in headers}
        if 'lastUpdate' not in product_data or product_data['lastUpdate'] is None:
             processed_product['lastUpdate'] = datetime.datetime.now().timestamp()
        processed_products.append(processed_product)

    try:
        with open(full_output_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            if write_header:
                writer.writeheader()
            writer.writerows(processed_products)
        print(f"Saved {len(processed_products)} products to {full_output_path}")
    except IOError as e:
        print(f"Error saving to CSV {full_output_path}: {e}")

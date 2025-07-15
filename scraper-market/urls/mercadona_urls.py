# This file lists category IDs and their corresponding names for Mercadona's API.
# The 'name' field is crucial: it must match a key in `scraper-market/config/categories.json`
# to ensure correct `category_code` mapping in the output CSV.
# The 'id' is Mercadona's internal API category ID.

# Discovering these IDs typically involves:
# 1. Navigating tienda.mercadona.es with browser developer tools open.
# 2. Observing network requests to find API calls (usually to /api/categories/<ID>/).
# 3. Correlating these IDs with the displayed category names.

# The examples below are illustrative. Actual, comprehensive mapping requires research.
# If Mercadona's API category (e.g., ID 79 "Aceite, especias y salsas") is broad,
# you map it to the most relevant primary category from your `categories.json` (e.g., "Aceite").
# The scraper will then use Mercadona's internal sub-group names (like "Aceites de oliva")
# as the 'subcategory' in the CSV.

mercadona_scrape_list = [
    # Example based on the original script's hardcoded ID 79.
    # Assuming ID 79 ("Aceite, especias y salsas" in Mercadona's system) should primarily map
    # to our "Aceite" category. Other products like "Especias" or "Salsas" from this same API call
    # will also be categorized under "Aceite" but will have their specific Mercadona subcategory name.
    # This is a simplification. A more granular approach would require finding specific API IDs
    # for "Especias", "Salsas" if they exist and are preferred.
    {"id": "79", "name": "Aceite"}, # Maps to "Aceite" (code 1) in categories.json

    # Hypothetical examples for other categories (IDs are placeholders):
    # To make these work, you'd replace "ID_AGUA_Y_REFRESCOS" etc. with actual Mercadona API IDs,
    # and ensure the "name" matches a key in your categories.json.

    # {"id": "ID_AGUA_Y_REFRESCOS", "name": "Bebidas sin alcohol"}, # Maps to "Bebidas sin alcohol" (code 6)
    # {"id": "ID_APERITIVOS", "name": "Aperitivos"},                # Maps to "Aperitivos" (code 8)
    # {"id": "ID_ARROZ", "name": "Arroz"},                          # Maps to "Arroz" (code 9)
    # {"id": "ID_LEGUMBRES", "name": "Legumbre"},                    # Maps to "Legumbre" (code 10)
    # {"id": "ID_PASTA", "name": "Pasta"},                          # Maps to "Pasta" (code 11)
    # {"id": "ID_CARNE_FRESCA", "name": "Carne"},                   # Maps to "Carne" (code 15)
    # {"id": "ID_PESCADO_FRESCO", "name": "Pescado"},                 # Maps to "Pescado" (code 16)
    # {"id": "ID_FRUTA", "name": "Fruta"},                          # Maps to "Fruta" (code 25)
    # {"id": "ID_VERDURAS", "name": "Verduras"},                    # Maps to "Verduras" (code 26)
    # {"id": "ID_HUEVOS", "name": "Huevos"},                        # Maps to "Huevos" (code 28)
    # {"id": "ID_LACTEOS", "name": "Lacteos"},                      # Maps to "Lacteos" (code 29)
    # {"id": "ID_PAN", "name": "Panaderia"},                        # Maps to "Panaderia" (code 30)
    # {"id": "ID_PIZZAS_REFRIGERADAS", "name": "Pizzas"},            # Maps to "Pizzas" (code 31)
    # {"id": "ID_ZUMOS_AMBIENTE", "name": "Zumos"},                 # Maps to "Zumos" (code 32)

    # For the purpose of this refactoring and testing, only the first entry for "Aceite" will be used by main.py.
    # A real implementation would require populating this list thoroughly.
]

# To make the test runnable with the current main.py which picks the first entry:
if not mercadona_scrape_list:
    print("Warning: mercadona_scrape_list is empty. Adding a default test entry for 'Aceite' using ID 79.")
    mercadona_scrape_list.append({"id": "79", "name": "Aceite"})
elif mercadona_scrape_list[0]["name"] != "Aceite" or mercadona_scrape_list[0]["id"] != "79":
    print("Warning: The first entry in mercadona_scrape_list is not the default Aceite/79. Test might behave unexpectedly or target a different category.")

# Add a few more known valid IDs for slightly broader testing if desired,
# ensuring their 'name' matches a key in categories.json.
# Example: Category 112 for "Agua y refrescos"
# mercadona_scrape_list.append({"id": "112", "name": "Bebidas sin alcohol"})
# Example: Category 100 for "Aperitivos"
# mercadona_scrape_list.append({"id": "100", "name": "Aperitivos"})
# Example: Category 16 for "Pizzas y platos preparados"
# mercadona_scrape_list.append({"id": "16", "name": "Comida preparada"})
# Example: Category 2 for "Fruta"
# mercadona_scrape_list.append({"id": "2", "name": "Fruta"})
# Example: Category 3 for "Verdura"
# mercadona_scrape_list.append({"id": "3", "name": "Verduras"})
# Example: Category 7 for "Carne"
# mercadona_scrape_list.append({"id": "7", "name": "Carne"})
# Example: Category 8 for "Pescado"
# mercadona_scrape_list.append({"id": "8", "name": "Pescado"})

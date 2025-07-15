def individual_serial(product) -> dict:
    return {
        "id": str(product["_id"]),
        "product_code": str(product["product_code"]),
        "supermarket": str(product["supermarket"]),
        "name": str(product["name"]),
        "category": str(product["category"]),
        "description": str(product["description"]),
        "price": float(product["price"]),
        "lastUpdate": int(product["lastUpdate"])
    }

def list_serial(products) -> list:
    return [individual_serial(product) for product in products]
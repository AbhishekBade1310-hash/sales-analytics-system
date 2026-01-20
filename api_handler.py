import os
import requests

# =========================
# PATH SETUP (PORTABLE)
# =========================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

# Ensure data folder exists
os.makedirs(DATA_DIR, exist_ok=True)

ENRICHED_DATA_FILE = os.path.join(DATA_DIR, "enriched_sales_data.txt")

# =========================
# API CONFIG
# =========================

API_URL = "https://dummyjson.com/products"


def fetch_all_products():
    """
    Fetches all products from DummyJSON API
    """
    try:
        response = requests.get(API_URL, params={"limit": 100}, timeout=10)
        response.raise_for_status()

        data = response.json()
        products = data.get("products", [])

        print(f" Successfully fetched {len(products)} products from API")
        return products

    except requests.exceptions.RequestException as e:
        print(f" API fetch failed: {e}")
        return []


def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product info
    """
    product_mapping = {}

    for product in api_products:
        try:
            product_mapping[product["id"]] = {
                "title": product.get("title"),
                "category": product.get("category"),
                "brand": product.get("brand"),
                "rating": product.get("rating"),
            }
        except KeyError:
            continue

    return product_mapping


def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with API product information
    """
    enriched_transactions = []

    for tx in transactions:
        enriched_tx = tx.copy()

        enriched_tx["API_Category"] = None
        enriched_tx["API_Brand"] = None
        enriched_tx["API_Rating"] = None
        enriched_tx["API_Match"] = False

        try:
            # Extract numeric ID from ProductID (P101 -> 101)
            product_id_str = "".join(filter(str.isdigit, tx.get("ProductID", "")))
            product_id = int(product_id_str)

            if product_id in product_mapping:
                api_data = product_mapping[product_id]

                enriched_tx["API_Category"] = api_data.get("category")
                enriched_tx["API_Brand"] = api_data.get("brand")
                enriched_tx["API_Rating"] = api_data.get("rating")
                enriched_tx["API_Match"] = True

        except Exception:
            pass  # Gracefully ignore enrichment errors

        enriched_transactions.append(enriched_tx)

    # Save enriched data to file
    save_enriched_data(enriched_transactions)

    return enriched_transactions


def save_enriched_data(enriched_transactions, filename=ENRICHED_DATA_FILE):
    """
    Saves enriched transactions back to file
    """
    header = (
        "TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|"
        "CustomerID|Region|API_Category|API_Brand|API_Rating|API_Match\n"
    )

    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(header)

            for tx in enriched_transactions:
                row = [
                    str(tx.get("TransactionID", "")),
                    str(tx.get("Date", "")),
                    str(tx.get("ProductID", "")),
                    str(tx.get("ProductName", "")),
                    str(tx.get("Quantity", "")),
                    str(tx.get("UnitPrice", "")),
                    str(tx.get("CustomerID", "")),
                    str(tx.get("Region", "")),
                    str(tx.get("API_Category", "")) if tx.get("API_Category") else "",
                    str(tx.get("API_Brand", "")) if tx.get("API_Brand") else "",
                    str(tx.get("API_Rating", "")) if tx.get("API_Rating") else "",
                    str(tx.get("API_Match", False)),
                ]

                file.write("|".join(row) + "\n")

        print(f" Enriched data saved to {filename}")

    except IOError as e:
        print(f" Failed to write enriched data file: {e}")

from collections import defaultdict
from datetime import datetime


def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions
    """
    total_revenue = 0.0

    for tx in transactions:
        total_revenue += tx["Quantity"] * tx["UnitPrice"]

    return round(total_revenue, 2)


def region_wise_sales(transactions):
    """
    Analyzes sales by region
    """
    region_data = defaultdict(lambda: {"total_sales": 0.0, "transaction_count": 0})

    total_revenue = calculate_total_revenue(transactions)

    for tx in transactions:
        revenue = tx["Quantity"] * tx["UnitPrice"]
        region = tx["Region"]

        region_data[region]["total_sales"] += revenue
        region_data[region]["transaction_count"] += 1

    # Build final output with percentage
    result = {}
    for region, data in region_data.items():
        percentage = (data["total_sales"] / total_revenue * 100) if total_revenue else 0

        result[region] = {
            "total_sales": round(data["total_sales"], 2),
            "transaction_count": data["transaction_count"],
            "percentage": round(percentage, 2),
        }

    # Sort by total_sales descending
    result = dict(
        sorted(result.items(), key=lambda x: x[1]["total_sales"], reverse=True)
    )

    return result


def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold
    """
    product_data = defaultdict(lambda: {"quantity": 0, "revenue": 0.0})

    for tx in transactions:
        name = tx["ProductName"]
        qty = tx["Quantity"]
        revenue = qty * tx["UnitPrice"]

        product_data[name]["quantity"] += qty
        product_data[name]["revenue"] += revenue

    # Convert to list of tuples
    products = [
        (name, data["quantity"], round(data["revenue"], 2))
        for name, data in product_data.items()
    ]

    # Sort by total quantity descending
    products.sort(key=lambda x: x[1], reverse=True)

    return products[:n]


def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns
    """
    customer_data = defaultdict(
        lambda: {
            "total_spent": 0.0,
            "purchase_count": 0,
            "products_bought": set(),
        }
    )

    for tx in transactions:
        customer = tx["CustomerID"]
        amount = tx["Quantity"] * tx["UnitPrice"]

        customer_data[customer]["total_spent"] += amount
        customer_data[customer]["purchase_count"] += 1
        customer_data[customer]["products_bought"].add(tx["ProductName"])

    # Build final output
    result = {}
    for customer, data in customer_data.items():
        avg_order_value = (
            data["total_spent"] / data["purchase_count"]
            if data["purchase_count"]
            else 0
        )

        result[customer] = {
            "total_spent": round(data["total_spent"], 2),
            "purchase_count": data["purchase_count"],
            "avg_order_value": round(avg_order_value, 2),
            "products_bought": sorted(list(data["products_bought"])),
        }

    # Sort by total_spent descending
    result = dict(
        sorted(result.items(), key=lambda x: x[1]["total_spent"], reverse=True)
    )

    return result


def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date
    """
    daily_data = defaultdict(
        lambda: {"revenue": 0.0, "transaction_count": 0, "customers": set()}
    )

    for tx in transactions:
        date = tx["Date"]
        revenue = tx["Quantity"] * tx["UnitPrice"]

        daily_data[date]["revenue"] += revenue
        daily_data[date]["transaction_count"] += 1
        daily_data[date]["customers"].add(tx["CustomerID"])

    # Sort chronologically
    sorted_dates = sorted(
        daily_data.keys(), key=lambda d: datetime.strptime(d, "%Y-%m-%d")
    )

    result = {}
    for date in sorted_dates:
        data = daily_data[date]
        result[date] = {
            "revenue": round(data["revenue"], 2),
            "transaction_count": data["transaction_count"],
            "unique_customers": len(data["customers"]),
        }

    return result


def find_peak_sales_day(transactions):
    """
    Identifies the date with highest revenue
    """
    daily_trend = daily_sales_trend(transactions)

    peak_date = None
    peak_revenue = 0.0
    peak_transactions = 0

    for date, data in daily_trend.items():
        if data["revenue"] > peak_revenue:
            peak_revenue = data["revenue"]
            peak_transactions = data["transaction_count"]
            peak_date = date

    return peak_date, peak_revenue, peak_transactions


def low_performing_products(transactions, threshold=10):
    """
    Identifies products with low sales
    """
    product_data = defaultdict(lambda: {"quantity": 0, "revenue": 0.0})

    for tx in transactions:
        name = tx["ProductName"]
        qty = tx["Quantity"]
        revenue = qty * tx["UnitPrice"]

        product_data[name]["quantity"] += qty
        product_data[name]["revenue"] += revenue

    low_products = [
        (name, data["quantity"], round(data["revenue"], 2))
        for name, data in product_data.items()
        if data["quantity"] < threshold
    ]

    # Sort by quantity ascending
    low_products.sort(key=lambda x: x[1])

    return low_products

from utils.file_handler import (
    read_sales_data,
    parse_transactions,
    validate_and_filter,
)
from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products,
)
from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data,
)
from datetime import datetime


def generate_sales_report(transactions, enriched_transactions, output_file="C:/Users/xcite/Documents/sales-analytics-system/output/sales_report.txt"):
    from utils.data_processor import (
        region_wise_sales,
        top_selling_products,
        customer_analysis,
        daily_sales_trend,
        find_peak_sales_day,
        low_performing_products,
    )

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    total_revenue = calculate_total_revenue(transactions)
    total_txn = len(transactions)
    avg_order = total_revenue / total_txn if total_txn else 0

    dates = sorted(tx["Date"] for tx in transactions)
    date_range = f"{dates[0]} to {dates[-1]}" if dates else "N/A"

    region_stats = region_wise_sales(transactions)
    top_products = top_selling_products(transactions)
    customers = customer_analysis(transactions)
    top_customers = list(customers.items())[:5]
    daily_trend = daily_sales_trend(transactions)

    peak_day, peak_rev, peak_cnt = find_peak_sales_day(transactions)
    low_products = low_performing_products(transactions)

    enriched_ok = [tx for tx in enriched_transactions if tx["API_Match"]]
    enriched_fail = [tx for tx in enriched_transactions if not tx["API_Match"]]

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("=" * 44 + "\n")
        f.write("           SALES ANALYTICS REPORT\n")
        f.write(f"     Generated: {now}\n")
        f.write(f"     Records Processed: {len(transactions)}\n")
        f.write("=" * 44 + "\n\n")

        f.write("OVERALL SUMMARY\n")
        f.write("-" * 44 + "\n")
        f.write(f"Total Revenue:        ₹{total_revenue:,.2f}\n")
        f.write(f"Total Transactions:   {total_txn}\n")
        f.write(f"Average Order Value:  ₹{avg_order:,.2f}\n")
        f.write(f"Date Range:           {date_range}\n\n")

        f.write("REGION-WISE PERFORMANCE\n")
        f.write("-" * 44 + "\n")
        for r, d in region_stats.items():
            f.write(f"{r}: ₹{d['total_sales']:,.2f} ({d['percentage']}%) | Txn: {d['transaction_count']}\n")
        f.write("\n")

        f.write("TOP 5 PRODUCTS\n")
        f.write("-" * 44 + "\n")
        for i, (n, q, rev) in enumerate(top_products, 1):
            f.write(f"{i}. {n} | Qty: {q} | ₹{rev:,.2f}\n")
        f.write("\n")

        f.write("TOP 5 CUSTOMERS\n")
        f.write("-" * 44 + "\n")
        for i, (cid, d) in enumerate(top_customers, 1):
            f.write(f"{i}. {cid} | ₹{d['total_spent']:,.2f} | Orders: {d['purchase_count']}\n")
        f.write("\n")

        f.write("DAILY SALES TREND\n")
        f.write("-" * 44 + "\n")
        for date, d in daily_trend.items():
            f.write(f"{date}: ₹{d['revenue']:,.2f} | Txn: {d['transaction_count']} | Customers: {d['unique_customers']}\n")
        f.write("\n")

        f.write("API ENRICHMENT SUMMARY\n")
        f.write("-" * 44 + "\n")
        f.write(f"Enriched Records: {len(enriched_ok)}\n")
        f.write(f"Failed Enrichment: {len(enriched_fail)}\n")


def main():
    try:
        print("=" * 40)
        print("SALES ANALYTICS SYSTEM")
        print("=" * 40)

        print("[1/10] Reading sales data...")
        raw = read_sales_data("data/sales_data.txt")
        print(f"✓ Successfully read {len(raw)} transactions\n")

        print("[2/10] Parsing and cleaning data...")
        parsed = parse_transactions(raw)
        print(f"✓ Parsed {len(parsed)} records\n")

        print("[3/10] Filter Options Available:")
        regions = sorted(set(tx["Region"] for tx in parsed))
        amounts = [tx["Quantity"] * tx["UnitPrice"] for tx in parsed]
        print("Regions:", ", ".join(regions))
        print(f"Amount Range: ₹{min(amounts):,.0f} - ₹{max(amounts):,.0f}")

        apply = input("Do you want to filter data? (y/n): ").lower()
        region = min_amt = max_amt = None

        if apply == "y":
            region = input("Region: ").strip() or None
            min_amt = input("Min Amount: ").strip()
            max_amt = input("Max Amount: ").strip()

        print("\n[4/10] Validating transactions...")
        valid, invalid, _ = validate_and_filter(
            parsed,
            region=region,
            min_amount=float(min_amt) if min_amt else None,
            max_amount=float(max_amt) if max_amt else None,
        )
        print(f" Valid: {len(valid)} | Invalid: {invalid}\n")

        print("[5/10] Analyzing sales data...")
        print(" Analysis complete\n")

        print("[6/10] Fetching product data from API...")
        products = fetch_all_products()
        print(f" Fetched {len(products)} products\n")

        print("[7/10] Enriching sales data...")
        mapping = create_product_mapping(products)
        enriched = enrich_sales_data(valid, mapping)
        print(" Enrichment complete\n")

        print("[9/10] Generating report...")
        generate_sales_report(valid, enriched)
        print(" Report saved to: output/sales_report.txt\n")

        print("[10/10] Process Complete!")
        print("=" * 40)

    except Exception as e:
        print(" Error occurred:", e)


if __name__ == "__main__":
    main()

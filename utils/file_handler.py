def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues
    Returns: list of raw lines (strings)
    """
    encodings = ["utf-8", "latin-1", "cp1252"]
    lines = []

    for enc in encodings:
        try:
            with open(filename, "r", encoding=enc) as file:
                lines = file.readlines()
            break
        except UnicodeDecodeError:
            continue
        except FileNotFoundError:
            print(f" File not found: {filename}")
            return []

    if not lines:
        print(" Unable to read file with supported encodings")
        return []

    # Remove header and empty lines
    cleaned_lines = []
    for line in lines[1:]:  # skip header
        line = line.strip()
        if line:
            cleaned_lines.append(line)

    return cleaned_lines


def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries
    """
    transactions = []

    for line in raw_lines:
        parts = line.split("|")

        # Skip rows with incorrect field count
        if len(parts) != 8:
            continue

        try:
            transaction = {
                "TransactionID": parts[0].strip(),
                "Date": parts[1].strip(),
                "ProductID": parts[2].strip(),
                "ProductName": parts[3].replace(",", "").strip(),
                "Quantity": int(parts[4].replace(",", "").strip()),
                "UnitPrice": float(parts[5].replace(",", "").strip()),
                "CustomerID": parts[6].strip(),
                "Region": parts[7].strip()
            }

            transactions.append(transaction)

        except ValueError:
            # Skip rows with conversion issues
            continue

    return transactions


def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters
    """
    valid_transactions = []
    invalid_count = 0

    # Validation
    for tx in transactions:
        try:
            if (
                tx["Quantity"] <= 0
                or tx["UnitPrice"] <= 0
                or not tx["TransactionID"].startswith("T")
                or not tx["ProductID"].startswith("P")
                or not tx["CustomerID"].startswith("C")
                or not tx["Region"]
            ):
                invalid_count += 1
                continue

            valid_transactions.append(tx)

        except KeyError:
            invalid_count += 1

    total_input = len(transactions)

    # Display available regions
    regions = sorted(set(tx["Region"] for tx in valid_transactions))
    print(" Available Regions:", regions)

    # Display transaction amount range
    amounts = [tx["Quantity"] * tx["UnitPrice"] for tx in valid_transactions]
    if amounts:
        print(f" Transaction Amount Range: {min(amounts)} - {max(amounts)}")

    filtered_by_region = 0
    filtered_by_amount = 0

    # Apply region filter
    if region:
        before = len(valid_transactions)
        valid_transactions = [
            tx for tx in valid_transactions if tx["Region"] == region
        ]
        filtered_by_region = before - len(valid_transactions)
        print(f" Records after region filter: {len(valid_transactions)}")

    # Apply amount filter
    if min_amount is not None or max_amount is not None:
        before = len(valid_transactions)
        filtered = []

        for tx in valid_transactions:
            amount = tx["Quantity"] * tx["UnitPrice"]

            if min_amount is not None and amount < min_amount:
                continue
            if max_amount is not None and amount > max_amount:
                continue

            filtered.append(tx)

        valid_transactions = filtered
        filtered_by_amount = before - len(valid_transactions)
        print(f" Records after amount filter: {len(valid_transactions)}")

    filter_summary = {
        "total_input": total_input,
        "invalid": invalid_count,
        "filtered_by_region": filtered_by_region,
        "filtered_by_amount": filtered_by_amount,
        "final_count": len(valid_transactions),
    }

    return valid_transactions, invalid_count, filter_summary

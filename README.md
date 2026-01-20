# Sales Analytics System

## 📌 Project Overview

The **Sales Analytics System** is a Python-based data processing and analytics project that reads raw sales data, cleans and validates it, performs detailed analytics, enriches the data using an external API, and generates a comprehensive sales report.

This project demonstrates:

* File handling with encoding issues
* Data cleaning and validation
* Aggregation and analytics
* API integration
* Report generation
* Modular Python project structure

---

##  Project Structure

```
sales-analytics-system/
├── README.md
├── main.py
├── requirements.txt
├── data/
│   ├── sales_data.txt
│   └── enriched_sales_data.txt
├── output/
│   └── sales_report.txt
└── utils/
    ├── file_handler.py
    ├── data_processor.py
    └── api_handler.py
```

---

##  Technologies Used

* Python 3.x
* Requests library (API integration)
* Standard Python libraries (`datetime`, `collections`)

---

##  Setup Instructions

### 1️ Clone the Repository

```bash
git clone <your-github-repo-url>
cd sales-analytics-system
```

### 2️ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️ Run the Project

```bash
python main.py
```

---

##  Application Workflow

1. Reads `sales_data.txt` (handles encoding issues)
2. Parses and cleans raw sales records
3. Allows optional user filtering (region & amount)
4. Validates transactions
5. Performs sales analytics
6. Fetches product data from DummyJSON API
7. Enriches sales data with API information
8. Saves enriched data to file
9. Generates a formatted sales analytics report

---

##  Key Analytics Performed

* Total revenue
* Region-wise sales performance
* Top selling products
* Customer purchase analysis
* Daily sales trends
* Peak sales day
* Low-performing products

---

##  API Used

**DummyJSON Products API**

```
https://dummyjson.com/products
```

Used to enrich sales data with:

* Category
* Brand
* Rating

---

##  Output Files

* `data/enriched_sales_data.txt` → Enriched transaction data
* `output/sales_report.txt` → Final sales analytics report

---

##  Error Handling

* Graceful handling of file errors
* API failures handled safely
* Invalid data filtered without crashing

---

##  Author

Abhishek Bade

---

##  Notes

* Ensure `sales_data.txt` exists in the `data/` folder
* Internet connection required for API enrichment

---


import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

csv_path = r"C:\Users\sarthak\Desktop\Task-7\sales_data.csv"

try:
    df_csv = pd.read_csv(csv_path, encoding="utf-8")
except UnicodeDecodeError:
    try:
        df_csv = pd.read_csv(csv_path, encoding="latin1")
    except UnicodeDecodeError:
        df_csv = pd.read_csv(csv_path, encoding="cp1252")

print("CSV Loaded Successfully")
print(df_csv.head())

df_sales = df_csv[["PRODUCTCODE", "QUANTITYORDERED", "PRICEEACH"]].copy()
df_sales.rename(columns={
    "PRODUCTCODE": "product",
    "QUANTITYORDERED": "quantity",
    "PRICEEACH": "price"
}, inplace=True)

print("\nFiltered Data (First 5 rows):")
print(df_sales.head())

conn = sqlite3.connect("sales_data.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS sales")
cursor.execute("""
CREATE TABLE sales (
    product TEXT,
    quantity INTEGER,
    price REAL
)
""")

df_sales.to_sql("sales", conn, if_exists="append", index=False)

query = """
SELECT 
    product, 
    SUM(quantity) AS total_qty, 
    SUM(quantity * price) AS revenue
FROM sales
GROUP BY product
"""

df_summary = pd.read_sql_query(query, conn)

print("\nSales Summary:")
print(df_summary)

df_summary.plot(kind='bar', x='product', y='revenue', legend=False)
plt.title("Revenue by Product")
plt.xlabel("Product")
plt.ylabel("Revenue")
plt.tight_layout()
plt.savefig("sales_chart.png")
plt.show()

conn.close()
input("\nScript finished. Press Enter to exit...")

import os
import sqlite3

import pandas as pd

# Create the SQLite DB file
conn = sqlite3.connect("sales_analysis.db")
cursor = conn.cursor()

# Load CSVs from the 'dataset' folder
data_dir = "dataset"

# Load Eligibility Table
eligibility_df = pd.read_csv(os.path.join(data_dir, "Eligibility_Table.csv"))
eligibility_df.to_sql("Eligibility", conn, if_exists="replace", index=False)

# Load Ad Sales Table
ad_sales_df = pd.read_csv(os.path.join(data_dir, "AD_Sales.csv"))
ad_sales_df.to_sql("AD_Sales", conn, if_exists="replace", index=False)

# Load Total Sales Table
total_sales_df = pd.read_csv(os.path.join(data_dir, "Total_Sales.csv"))
total_sales_df.to_sql("Total_Sales", conn, if_exists="replace", index=False)

print("✅ All tables loaded into sales_analysis.db successfully.")

## Display all the records
# print("The inserted records are")
# data=cursor.execute('''Select * from Total_Sales''')
# for row in data:
#     print(row)

conn.commit()
conn.close()

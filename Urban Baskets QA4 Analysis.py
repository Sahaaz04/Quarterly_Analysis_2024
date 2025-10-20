import pandas as pd
from datetime import datetime

df = pd.read_csv(r"C:\Program Files\Analysis\Urban Basket Sales 2024 (Clean).csv")

start_date = "2024-01 -01"
end_date = "2024-3-31"

mask = (df["transaction_date"] >= start_date) & (df["transaction_date"] <= end_date)
quarter_df = df.loc[mask] #selects only the rows in the DataFrame where the mask is True.


# Volume & Value Metrics
total_sales = quarter_df["total_spent"].sum()
number_of_transactions = quarter_df["transaction_id"].nunique()
average_order_value = total_sales / number_of_transactions
total_quantity = quarter_df["quantity"].sum()

#Customer Metrics
unique_customers = quarter_df["customer_id"].nunique()
repeat_customers = quarter_df.groupby("customer_id")["transaction_id"].nunique()
no_of_repeat_customers = (repeat_customers > 1).sum()
repeat_rate = (no_of_repeat_customers / unique_customers) * 100 if unique_customers else 0

#Discount related metrics
quarter_df["discount_applied"] = quarter_df["discount_applied"].map({"t": True, "f": False})
discounted_sales = quarter_df[quarter_df["discount_applied"] == True]["total_spent"].sum()
non_discounted_sales = quarter_df[quarter_df["discount_applied"] == False]["total_spent"].sum()
discount_uptake_rate = quarter_df["discount_applied"].astype(float).mean(skipna=True) * 100

#Catergory Performence
top_categories = quarter_df.groupby("category")["total_spent"].sum().sort_values(ascending=False)
top_items = quarter_df.groupby("item")["quantity"].sum().sort_values(ascending=False)

#Sales by Payment method and Location
sales_by_payment = quarter_df.groupby("payment_method")["total_spent"].sum().sort_values(ascending=False)
sales_by_location = quarter_df.groupby("location")["total_spent"].sum().sort_values(ascending=False)

#Weekly Sales
quarter_df["transaction_date"] = pd.to_datetime(quarter_df["transaction_date"])
custom_start = pd.to_datetime("2024-01-01")
quarter_df.loc[:, "custom_week"] = ((quarter_df["transaction_date"] - custom_start).dt.days // 7) + 1
weekly_sales = quarter_df.groupby("custom_week")["total_spent"].sum().reset_index().sort_values("custom_week")

# Sales by day of week
quarter_df.loc[:, "day_of_week"] = quarter_df["transaction_date"].dt.day_of_week
weekday_sales = quarter_df.groupby("day_of_week")["total_spent"].mean().sort_index()

#Items per Transaction
items_per_txn = quarter_df.groupby("transaction_id")["quantity"].sum()
avg_items_per_txn = items_per_txn.mean()



print("Total Sales:", round(total_sales, 2))
print("Average Order Value (AOV):", round(average_order_value, 2))
print("Discounted Sales:", round(discounted_sales, 2))
print("Non-Discounted Sales:", round(non_discounted_sales, 2))
print("Number of Transactions:", number_of_transactions)
print("Average Items per Transaction:", round(avg_items_per_txn, 2))
print("Discount Uptake Rate:", f"{round(discount_uptake_rate, 2)}%")
print("Total Quantity Sold:", total_quantity)
print("Unique Customers:", unique_customers)
print("Repeat Customers:", no_of_repeat_customers)
print("Repeat Purchase Rate:", f"{round(repeat_rate, 2)}%")
print("Top Categories by Sales:", top_categories)
print("Top Items by Quantity Sold:", top_items)
print("Sales by Payment Method:", sales_by_payment)
print("Sales by Location:", sales_by_location)
print("weekly sales:", weekly_sales)
print("weekday sales:", round(weekday_sales, 2))






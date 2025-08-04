import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF
import os
from collections import Counter

df = pd.read_csv('Dataset.csv')
print(df.describe())

df['Transaction_date'] = pd.to_datetime(df['Transaction_date'], errors='coerce')
df['Expiration'] = pd.to_datetime(df['Expiration'], errors='coerce')
if df['Transaction_date'].isnull().any() or df['Expiration'].isnull().any():
    print("Warning: Some dates could not be parsed and are set to NaT.")
df['Days_to_expiration'] = (df['Expiration'] - df['Transaction_date']).dt.days
fast_selling =df[['Transaction_date', 'Expiration', 'Days_to_expiration']].head(5)

if df['Transaction_date'].isnull().any():
    print("Warning: Some dates could not be parsed and are set to NaT.")

df['Year'] = df['Transaction_date'].dt.year
df['Quarter'] = df['Transaction_date'].dt.quarter
df['Month'] = df['Transaction_date'].dt.month
df['Days_to_expiration'] = (df['Expiration'] - df['Transaction_date']).dt.days

product_sales = df['Product_name'].value_counts()
country_performance = df.groupby(['Country', 'Product_name'])['Feedback'].mean().unstack()
product_review = df.groupby(['Comments','Product_name'])['Feedback'].count().unstack()
product_review = product_review.fillna(0)
top_products_by_price = df.groupby('Product_name')['Total_price'].sum().sort_values(ascending=False).head(5)
top_products_by_quantity = df.groupby('Product_name')['Quantity_purchased'].sum().sort_values(ascending=False).head(5)
top_products_by_orders = df['Product_name'].value_counts().head(5)
country_with_most_sales = df.groupby('Country')['Total_price'].sum().sort_values(ascending=False).head(1)
countrywise_top_products = df.groupby(['Country', 'Product_name'])['Total_price'].sum().reset_index()
countrywise_top_products = countrywise_top_products.loc[
    countrywise_top_products.groupby('Country')['Total_price'].idxmax()
].set_index('Country')
annual_sales_report = df.groupby('Year')['Total_price'].sum()
quarterly_sales_report = df.groupby(['Year', 'Quarter'])['Total_price'].sum().unstack()
monthly_sales_report = df.groupby(['Year', 'Month'])['Total_price'].sum().unstack()
all_crops = [crop for sublist in df['Crop_name'] for crop in (sublist if isinstance(sublist, tuple) else [sublist])]
crop_usage = Counter(all_crops)
most_used_crop = max(crop_usage, key=crop_usage.get)
price_variation = df.groupby(['Country', 'Product_name'])['Price'].agg("max").reset_index()
top_best_reviewed = df.groupby('Product_name')['Feedback'].mean().sort_values(ascending=False).head(5)
bottom_reviewed = df.groupby('Product_name')['Feedback'].mean().sort_values(ascending=True).head(3)
quality_analysis = df.groupby(['Year', 'Product_name'])['Feedback'].mean().unstack()
highest_total_price_product = df.groupby('Product_name')['Total_price'].sum().idxmax()
lowest_total_price_product = df.groupby('Product_name')['Total_price'].sum().idxmin()
most_stock_purchasing_country = df.groupby('Country')['Quantity_purchased'].sum().idxmax()
countrywise_most_expensive_product = df.loc[df.groupby('Country')['Total_price'].idxmax(), ['Country', 'Product_name', 'Total_price']]

#can print the result if not required in pdf form 

# print(product_sales)
# print(country_performance)
# print(product_review)
# print(top_products_by_price)
# print(top_products_by_quantity)
# print(top_products_by_orders)
# print(countrywise_top_products)
# print(annual_sales_report)
# print(quarterly_sales_report)
# print(monthly_sales_report)
# print(most_used_crop)
# print(price_variation)
# print(top_best_reviewed)
# print(bottom_reviewed)
# print(quality_analysis)
# print(highest_total_price_product)
# print(lowest_total_price_product)
# print(most_stock_purchasing_country)
# print(countrywise_most_expensive_product)

# Graph analysis:

sns.lineplot(data=df, x="Price", y="Feedback", linewidth=2)
plt.title("Price vs.Feedback")
plt.xlabel("Price")
plt.ylabel("Feedback")
lineplot_path = "lineplot.png"
plt.savefig(lineplot_path)
plt.close()

product_popul= df['Product_name'].value_counts()
product_popul.plot(kind='bar', color=['pink', 'lightblue', 'lightgreen','yellow','lavender','orange','red','grey','black','cyan'])
for i, value in enumerate(product_popul):
    plt.text(i, value + 0.1, str(value), ha='center', fontsize=12)
plt.title('Product Popularity')
plt.xlabel('Product Name')
plt.ylabel('Count of Purchases')
plt.xticks(rotation=90)
barplot_path = "barplot.png"
plt.savefig(barplot_path)
plt.close()

df['Transaction_date'] = pd.to_datetime(df['Transaction_date'])  
df['YearMonth'] = df['Transaction_date'].dt.to_period('M')  
monthly_sales_by_product = df.groupby(['YearMonth', 'Product_name'])['Quantity_purchased'].sum().unstack()
total_sales_by_product = monthly_sales_by_product.sum(axis=0)
top_5_products = total_sales_by_product.nlargest(5).index
monthly_sales_by_top_5 = monthly_sales_by_product[top_5_products]
monthly_sales_by_top_5.plot(kind='line', figsize=(20, 8), marker='o', color=['brown', 'pink', 'blue', 'green', 'purple'])
plt.title('Seasonal Purchase Patterns by Product')
plt.xlabel('Year-Month')
plt.ylabel('Quantity Purchased')
plt.legend(title='Product Name')
seasonal_plot_path = "seasonal_plot.png"
plt.savefig(seasonal_plot_path)
plt.close()

plt.figure(figsize=(10, 6))
product_sales.plot(kind='bar', color="Darkblue")
for i, value in enumerate(product_sales):
    plt.text(i, value + 0.1, str(value), ha='center', fontsize=12)
plt.title("Product Sales Frequency", fontsize=14)
plt.xlabel("Product Name", fontsize=10)
plt.ylabel("Number of Orders", fontsize=10)
plt.xticks(rotation=45)
plt.tight_layout()
barplot3_path="salesfrequency.png"
plt.savefig(barplot3_path)
plt.close()

# Country Performance
plt.figure(figsize=(10, 6))
sns.heatmap(country_performance, annot=True, fmt=".2f", cmap="YlGnBu", cbar_kws={'label': 'Average Feedback'})
plt.title("Country Performance by Product", fontsize=14)
plt.xlabel("Product Name", fontsize=10)
plt.ylabel("Country", fontsize=10)
plt.tight_layout()
heatmap2_path = "couper.png"
plt.savefig(heatmap2_path)
plt.close()

# Product Review
plt.figure(figsize=(10, 6))
sns.heatmap(product_review, annot=True, fmt=".0f", cmap="Blues", cbar_kws={'label': 'Feedback Count'})
plt.title("Product Review Count by Comments", fontsize=14)
plt.xlabel("Product Name", fontsize=10)
plt.ylabel("Comments", fontsize=10)
plt.tight_layout()
heatmap1_path = "prorev.png"
plt.savefig(heatmap1_path)
plt.close()

# Top 5 Products by Price
plt.figure(figsize=(10, 6))
top_products_by_price.plot(kind='bar', color="Purple")
for i, value in enumerate(top_products_by_price):
    plt.text(i, value + 0.1, str(value), ha='center', fontsize=12)
plt.title("Top 5 Products by Total Price", fontsize=14)
plt.xlabel("Product Name", fontsize=10)
plt.ylabel("Total Price", fontsize=10)
plt.tight_layout()
barplot2_path="top5price.png"
plt.savefig(barplot2_path)
plt.close()

# Top 5 Products by Quantity
plt.figure(figsize=(10, 6))
top_products_by_quantity.plot(kind='bar', color="red")
for i, value in enumerate(top_products_by_quantity):
    plt.text(i, value + 0.1, str(value), ha='center', fontsize=12)
plt.title("Top 5 Products by Quantity Purchased", fontsize=14)
plt.xlabel("Product Name", fontsize=10)
plt.ylabel("Total Quantity", fontsize=10)
plt.tight_layout()
barplot1_path="top5quan.png"
plt.savefig(barplot1_path)
plt.close()

# Top 5 Products by Orders
plt.figure(figsize=(10, 6))
top_products_by_orders.plot(kind='bar', color="blue")
for i, value in enumerate(top_products_by_orders):
    plt.text(i, value + 0.1, str(value), ha='center', fontsize=12)
plt.title("Top 5 Products by Order Frequency", fontsize=14)
plt.xlabel("Product Name", fontsize=10)
plt.ylabel("Order Count", fontsize=10)
plt.tight_layout()
barplot4_path = "orderstop5.png"
plt.savefig(barplot4_path)
plt.close()

# Annual Sales Report
plt.figure(figsize=(10, 6))
annual_sales_report.plot(kind='bar', color="green")
for i, value in enumerate(annual_sales_report):
    plt.text(i, value + 0.1, str(value), ha='center', fontsize=12)
plt.title("Annual Sales Report", fontsize=14)
plt.xlabel("Year", fontsize=10)
plt.ylabel("Total Sales (Price)", fontsize=10)
plt.tight_layout()
barplot5_path = "Annual sales report.png"
plt.savefig(barplot5_path)
plt.close()

# Quarterly Sales Report
plt.figure(figsize=(10, 6))
sns.heatmap(quarterly_sales_report, annot=True, fmt=".0f", cmap="Greens", cbar_kws={'label': 'Total Sales'})
plt.title("Quarterly Sales Report", fontsize=14)
plt.xlabel("Quarter", fontsize=10)
plt.ylabel("Year", fontsize=10)
plt.tight_layout()
heatmap3_path = "quaterly.png"
plt.savefig(heatmap3_path)
plt.close()

# Monthly Sales Report
plt.figure(figsize=(10, 6))
sns.heatmap(monthly_sales_report, annot=True, fmt=".0f", cmap="coolwarm", cbar_kws={'label': 'Total Sales'})
plt.title("Monthly Sales Report", fontsize=14)
plt.xlabel("Month", fontsize=10)
plt.ylabel("Year", fontsize=10)
plt.tight_layout()
heatmap4_path = "monthly.png"
plt.savefig(heatmap4_path)
plt.close()

# Crop Usage
plt.figure(figsize=(10, 6))
pd.Series(crop_usage).sort_values(ascending=False).plot(kind='bar', color="pink")
plt.title("Crop Usage Frequency", fontsize=14)
plt.xlabel("Crop Name", fontsize=10)
plt.ylabel("Usage Count", fontsize=10)
plt.tight_layout()
barplot6_path = "cropusage.png"
plt.savefig(barplot6_path)
plt.close()

# Countrywise Top Products
plt.figure(figsize=(12, 6))
sns.barplot(data=countrywise_top_products.reset_index(), x='Country', y='Total_price', hue='Product_name', dodge=False)
plt.title('Top-Selling Products by Country')
plt.ylabel('Total Sales')
plt.xlabel('Country')
plt.legend(title='Product Name', loc='upper right')
plt.tight_layout()
tpcobar_path = "cou_top.png"
plt.savefig(tpcobar_path)
plt.close()

pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()
pdf.set_font("Arial", size=20, style="B")
pdf.cell(200, 10, "Feedback Data Analysis Report", ln=True, align="C")

pdf.set_font("Arial", size=12)
pdf.ln(10)
pdf.cell(200, 10, "Summary Statistics", ln=True, align="L")
pdf.set_font("Arial", size=10)
pdf.multi_cell(0, 10, str(df.describe()))
pdf.set_font("Courier", size=10) 

pdf.ln(5)
pdf.cell(180, 10, "Sales Data of Each Product", ln=True, align="L")
pdf.multi_cell(0, 10, product_sales.to_string())

pdf.ln(5)
pdf.cell(200, 10, "Mean Feedback of Each Country/Product", ln=True, align="L")
pdf.multi_cell(0, 10, country_performance.to_string())

pdf.ln(5)
pdf.cell(180, 10, "Product Review Overview", ln=True, align="L")
pdf.multi_cell(0, 10, product_review.to_string())

pdf.ln(5)
pdf.cell(200, 10, "Top product based on price:", ln=True, align="L")
pdf.multi_cell(0, 10, top_products_by_price.to_string())

pdf.ln(5)
pdf.cell(200, 10, "Top product based on Quantity:", ln=True, align="L")
pdf.multi_cell(0, 10, top_products_by_quantity.to_string())

pdf.ln(5)
pdf.cell(200, 10, "Top product based on orders:", ln=True, align="L")
pdf.multi_cell(0, 10, top_products_by_orders.to_string())

pdf.ln(5)
pdf.cell(200, 10, "Performance of each country:", ln=True, align="L")
pdf.multi_cell(0, 10, country_performance.to_string())

pdf.ln(5)
pdf.cell(200, 10, "Country with most sales:", ln=True, align="L")
pdf.multi_cell(0, 10, country_with_most_sales.to_string())

pdf.ln(5)
pdf.cell(200, 10, "Countrywise top products:", ln=True, align="L")
pdf.multi_cell(0, 10, countrywise_top_products.to_string())

pdf.ln(5)
pdf.cell(200, 10, "Annual Sales report:", ln=True, align="L")
pdf.multi_cell(0, 10, annual_sales_report.to_string())

pdf.ln(5)
pdf.cell(200, 10, "Quarterly sales report:", ln=True, align="L")
pdf.multi_cell(0, 10, quarterly_sales_report.to_string())

pdf.ln(5)
pdf.cell(200, 10, "Monthly sales report:", ln=True, align="L")
pdf.multi_cell(0, 10, monthly_sales_report.to_string())

pdf.ln(5)
pdf.cell(200, 10, "Fast selling products:", ln=True, align="L")
pdf.multi_cell(0, 10,fast_selling.to_string())

pdf.ln(6)
pdf.cell(200, 10, "Price variation in products in each country:", ln=True, align="L")
pdf.multi_cell(0, 10, price_variation.to_string(index=False))

pdf.ln(5)
pdf.cell(200, 10, "Top five products on basis of feedback:", ln=True, align="L")
pdf.multi_cell(0, 10, top_best_reviewed.to_string())

pdf.ln(5)
pdf.cell(200, 10, "Bottom three countries on basis of Feedback:", ln=True, align="L")
pdf.multi_cell(0, 10, bottom_reviewed.to_string())

pdf.ln(5)
pdf.cell(200, 10, "Quality analysis:", ln=True, align="L")
pdf.multi_cell(0, 10, quality_analysis.to_string())

pdf.ln(5)
pdf.cell(200, 10, "Highest total price:", ln=True, align="L")
pdf.multi_cell(0, 10, highest_total_price_product)

pdf.ln(5)
pdf.cell(200, 10, "Lowest total price:", ln=True, align="L")
pdf.multi_cell(0, 10, lowest_total_price_product)

pdf.ln(5)
pdf.cell(200,10, "Most stock purchasing country:",ln=True, align="L")
pdf.multi_cell(0,10, most_stock_purchasing_country)

# pdf.ln(5)
# pdf.cell(200,10, "Countrywise most expensive product:",ln=True, align="L")
# pdf.multi_cell(0,10, countrywise_most_expensive_product)

pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.image(lineplot_path, x=10, y=10, w=190)

pdf.set_font("Arial", size=12)
pdf.image(barplot_path, x=10, y=150, w=190)

pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.image(seasonal_plot_path, x=10, y=30, w=190)

pdf.set_font("Arial", size=12)
pdf.image(barplot3_path, x=10, y=150, w=190)

pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.image(barplot1_path, x=10, y=30, w=190)

pdf.set_font("Arial", size=12)
pdf.image(barplot2_path, x=10, y=150, w=190)

pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.image(barplot4_path, x=10, y=30, w=190)

pdf.set_font("Arial", size=12)
pdf.image(heatmap1_path, x=10, y=150, w=190)

pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.image(heatmap2_path, x=10, y=30, w=190)

pdf.set_font("Arial", size=12)
pdf.image(barplot5_path,x=10, y=150, w=190)

pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.image(heatmap3_path, x=10, y=30, w=190)

pdf.set_font("Arial", size=12)
pdf.image(heatmap4_path,x=10, y=150, w=190)

pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.image(barplot6_path,x=10, y=30, w=190)

pdf.set_font("Arial", size=12)
pdf.image(tpcobar_path,x=10, y=30, w=190)

output_pdf_path = "report.pdf"
pdf.output(output_pdf_path)
print(f"PDF report saved as {output_pdf_path}")

os.remove(lineplot_path)
os.remove(barplot_path)
os.remove(seasonal_plot_path)
os.remove(barplot1_path)
os.remove(barplot2_path)
os.remove(barplot3_path)
os.remove(barplot4_path)
os.remove(barplot5_path)
os.remove(barplot6_path)
os.remove(heatmap1_path)
os.remove(heatmap2_path)
os.remove(heatmap3_path)
os.remove(tpcobar_path)
os.remove(heatmap4_path)

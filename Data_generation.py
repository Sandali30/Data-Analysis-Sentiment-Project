import pandas as pd  # Import pandas library for data manipulation
import numpy as np  # Import numpy for numerical operations
import random  # Import random for generating random choices

# Step 1: Generate random data for countries, products, and quantities purchased
# Create a random selection of countries
Country = np.random.choice(['India', 'Pakistan', 'Bangladesh', 'Sri-Lanka', 'Nepal', 'Bhutan'], size=10000)

# Create a random selection of product names
Product_name = np.random.choice([
    'Biscuit', 'Pie', 'Cookie', 'Khari', 'Nachos', 'Toffee', 'Banana Chips', 'Ketchup', 'Maggi', 'Pasta'
], size=10000)

# Generate random quantities purchased (between 10 and 100)
Quantity_purchased = np.random.randint(10, 100, size=10000)

# Step 2: Define crop mapping function
# Map products to the crops used in their production
def crop_product(product):
    product_to_crops = {
        'Biscuit': ['Wheat', 'Sugar', 'Barley'],
        'Pie': ['Sugar'],
        'Cookie': ['Barley', 'Sugar'],
        'Khari': ['Cumin'],
        'Nachos': ['Maize'],
        'Toffee': ['Sugar'],
        'Banana Chips': ['Banana'],
        'Ketchup': ['Tomato'],
        'Maggi': ['Wheat'],
        'Pasta': ['Wheat', 'Barley']
    }
    return product_to_crops.get(product, [])  # Return crops or an empty list if product is not found

# Step 3: Generate feedback scores and map them to comments
# Create random feedback scores (0 to 5)
Feedback = np.random.randint(0, 6, size=10000)

# Function to map feedback scores to comments
def feedback_to_comments(feedback):
    if feedback == 5:
        return 'Excellent'
    elif feedback == 4:
        return 'Good'
    elif feedback == 3:
        return 'Average'
    elif feedback == 2:
        return 'Poor'
    elif feedback == 1:
        return 'Very Poor'
    else:  # feedback == 0
        return 'No Feedback'

# Apply the feedback mapping to create comments
Comments = [feedback_to_comments(fb) for fb in Feedback]

# Step 4: Define product price mapping by country
# Function to get the price of a product for a specific country
def product_to_price(product, country):
    country = country.strip().title()  # Standardize country name formatting
    prices = {
        'Biscuit': {'India': 20, 'Pakistan': 15, 'Bangladesh': 18, 'Sri-Lanka': 22, 'Nepal': 24, 'Bhutan': 25},
        'Pie': {'India': 50, 'Pakistan': 25, 'Bangladesh': 30, 'Sri-Lanka': 35, 'Nepal': 45, 'Bhutan': 55},
        'Cookie': {'India': 100, 'Pakistan': 75, 'Bangladesh': 80, 'Sri-Lanka': 85, 'Nepal': 95, 'Bhutan': 105},
        'Khari': {'India': 40, 'Pakistan': 25, 'Bangladesh': 20, 'Sri-Lanka': 35, 'Nepal': 35, 'Bhutan': 45},
        'Nachos': {'India': 65, 'Pakistan': 60, 'Bangladesh': 35, 'Sri-Lanka': 45, 'Nepal': 55, 'Bhutan': 75},
        'Toffee': {'India': 20, 'Pakistan': 12, 'Bangladesh': 10, 'Sri-Lanka': 10, 'Nepal': 15, 'Bhutan': 15},
        'Banana Chips': {'India': 40, 'Pakistan': 30, 'Bangladesh': 35, 'Sri-Lanka': 25, 'Nepal': 45, 'Bhutan': 45},
        'Ketchup': {'India': 60, 'Pakistan': 55, 'Bangladesh': 45, 'Sri-Lanka': 50, 'Nepal': 55, 'Bhutan': 65},
        'Maggi': {'India': 25, 'Pakistan': 15, 'Bangladesh': 35, 'Sri-Lanka': 30, 'Nepal': 25, 'Bhutan': 25},
        'Pasta': {'India': 120, 'Pakistan': 75, 'Bangladesh': 95, 'Sri-Lanka': 100, 'Nepal': 100, 'Bhutan': 105}
    }
    product_prices = prices.get(product, {})  # Get the price mapping for the product
    return product_prices.get(country, 0)  # Get the price for the country, default to 0

# Calculate prices and total prices for each transaction
Price = np.array([product_to_price(pr, cn) for pr, cn in zip(Product_name, Country)])
Total_price = Price * Quantity_purchased

# Step 5: Generate random manufacturing and expiration dates
# Create a date range for manufacturing dates
date_range = pd.date_range(start='2020-01-11', end='2025-07-31', freq='D')

# Randomly select manufacturing dates
Manufacturing = np.random.choice(date_range, size=10000)

# Calculate expiration dates (90 days after manufacturing)
Expiration = Manufacturing + pd.Timedelta(days=90)

# Step 6: Generate random transaction dates within a valid range
Transaction_date = []  # Initialize list for transaction dates

# Generate transaction dates based on manufacturing and expiration dates
for manuf_date, exp_date in zip(Manufacturing, Expiration):
    min_transaction_date = manuf_date + pd.Timedelta(days=10)
    max_transaction_date = exp_date - pd.Timedelta(days=5)
    if min_transaction_date > max_transaction_date:  # If the range is invalid, use the minimum date
        random_date = min_transaction_date
    else:
        random_date = pd.Timestamp(np.random.choice(pd.date_range(start=min_transaction_date, end=max_transaction_date)))
    Transaction_date.append(random_date)

Transaction_date = pd.Series(Transaction_date)  # Convert to pandas Series

# Step 7: Create the DataFrame with random reviews
# Function to generate a random review based on feedback
def generate_random_review(feedback):
    review_options = {
        5: ['Outstanding product quality!', 'Exceeded my expectations!', 'Absolutely loved it!'],
        4: ['Good product, no issues.', 'Satisfactory purchase.', 'Quite happy with the product.'],
        3: ['Average product, nothing special.', 'Okay for the price.', 'Decent product overall.'],
        2: ['Below average product.', 'Not what I expected.', 'Not great, needs improvement.'],
        1: ['Very poor quality.', 'Disappointed with the product.', 'Would not recommend.']
    }
    return random.choice(review_options.get(feedback, ['No feedback']))  # Return random review or "No feedback"

# Generate random reviews for each feedback score
Reviews = [generate_random_review(fb) for fb in Feedback]

# Combine all the generated data into a DataFrame
df = pd.DataFrame({
    'Country': Country,
    'Product_name': Product_name,
    'Quantity_purchased': Quantity_purchased,
    'Crop_name': [crop_product(pr) for pr in Product_name],
    'Feedback': Feedback,
    'Comments': Comments,
    'Price': Price,
    'Total_price': Total_price,
    'Manufacturing': Manufacturing,
    'Transaction_date': Transaction_date,
    'Expiration': Expiration,
    'Review': Reviews
})

# Save the DataFrame to a CSV file
df.to_csv('Dataset.csv', index=False)  # Export the data to a CSV file

print("Data saved to Dataset.csv.")  # Print confirmation message
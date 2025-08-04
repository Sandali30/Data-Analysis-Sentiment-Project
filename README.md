# Data Science Project: Random Dataset Generation, EDA, and Sentiment Analysis

### 📌 Project Overview  
This project explores data science techniques by generating and analyzing a synthetic dataset, followed by sentiment analysis. It revolves around analyzing product-related data across multiple countries, focusing on crop-based products and associated business details like manufacturing, transactions, and pricing.

---

### 📂 Project Details  

#### 🌍 Scope and Dataset  
- **Countries**: India, Pakistan, Bangladesh, Sri Lanka, Nepal, Bhutan  
- **Products**: Biscuit, Pie, Cookie, Khari, Nachos, Toffee, Banana Chips, Ketchup, Maggi, Pasta  
- **Attributes**:
  - **Dates**: Manufacturing, Transaction, Expiration  
  - **Pricing**: Base Price, Total Price (after tax/discount)  
  - **Quantity**: Units per transaction

---

#### 🔧 Steps Involved

1. **🗃️ Random Dataset Generation**  
   - Simulate realistic product data using `numpy` and `pandas`
   - Random assignment of product details to countries

2. **📊 Exploratory Data Analysis (EDA)**  
   - Handle missing values, detect outliers, visualize trends  
   - Use `matplotlib`, `seaborn`, and `pandas` to create:
     - Histograms for price distributions  
     - Line charts for sales trends  
     - Heatmaps for country-product correlation  

3. **💬 Sentiment Analysis on Comments**  
   - Generate random customer feedback  
   - Use `nltk` or `TextBlob` to classify sentiments  
   - Visualize results with `wordcloud`  

---

### ✅ Expected Outcomes
- A full dataset simulating real business scenarios  
- EDA insights into sales trends and pricing strategies  
- Sentiment analysis of product reviews for customer satisfaction analysis

---

### 🛠️ Technology Stack
- **Python Libraries**:
  - `numpy`, `pandas` – Dataset generation  
  - `matplotlib`, `seaborn` – EDA & visualization  
  - `nltk`, `TextBlob`, `wordcloud` – Sentiment analysis  

---

### ⚠️ Note  
Dataset is randomly generated and will change on every execution.

---

### ✅ Instructions
You can clone the repo and run the notebook/scripts to regenerate the dataset, perform EDA, and run sentiment analysis.


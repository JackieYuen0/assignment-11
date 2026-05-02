# Module 11 Assignment: Data Visualization with Matplotlib
# SunCoast Retail Visual Analysis

# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Welcome message
print("=" * 60)
print("SUNCOAST RETAIL VISUAL ANALYSIS")
print("=" * 60)

# ----- USE THE FOLLOWING CODE TO CREATE SAMPLE DATA (DO NOT MODIFY) -----
# Create a seed for reproducibility
np.random.seed(42)

# Generate dates for 8 quarters (Q1 2022 - Q4 2023)
quarters = pd.date_range(start='2022-01-01', periods=8, freq='Q')
quarter_labels = ['Q1 2022', 'Q2 2022', 'Q3 2022', 'Q4 2022', 
                 'Q1 2023', 'Q2 2023', 'Q3 2023', 'Q4 2023']

# Store locations
locations = ['Tampa', 'Miami', 'Orlando', 'Jacksonville']

# Product categories
categories = ['Electronics', 'Clothing', 'Home Goods', 'Sporting Goods', 'Beauty']

# Generate quarterly sales data for each location and category
quarterly_data = []

for quarter_idx, quarter in enumerate(quarters):
    for location in locations:
        for category in categories:
            # Base sales with seasonal pattern (Q4 higher, Q1 lower)
            base_sales = np.random.normal(loc=100000, scale=20000)
            seasonal_factor = 1.0
            if quarter.quarter == 4:  # Q4 (holiday boost)
                seasonal_factor = 1.3
            elif quarter.quarter == 1:  # Q1 (post-holiday dip)
                seasonal_factor = 0.8
            
            # Location effect
            location_factor = {
                'Tampa': 1.0,
                'Miami': 1.2,
                'Orlando': 0.9,
                'Jacksonville': 0.8
            }[location]
            
            # Category effect
            category_factor = {
                'Electronics': 1.5,
                'Clothing': 1.0,
                'Home Goods': 0.8,
                'Sporting Goods': 0.7,
                'Beauty': 0.9
            }[category]
            
            # Growth trend over time (5% per year, quarterly compounded)
            growth_factor = (1 + 0.05/4) ** quarter_idx
            
            # Calculate sales with some randomness
            sales = base_sales * seasonal_factor * location_factor * category_factor * growth_factor
            sales = sales * np.random.normal(loc=1.0, scale=0.1)  # Add noise
            
            # Advertising spend (correlated with sales but with diminishing returns)
            ad_spend = (sales ** 0.7) * 0.05 * np.random.normal(loc=1.0, scale=0.2)
            
            # Record
            quarterly_data.append({
                'Quarter': quarter,
                'QuarterLabel': quarter_labels[quarter_idx],
                'Location': location,
                'Category': category,
                'Sales': round(sales, 2),
                'AdSpend': round(ad_spend, 2),
                'Year': quarter.year
            })

# Create customer data
customer_data = []
total_customers = 2000

# Age distribution parameters for each location
age_params = {
    'Tampa': (45, 15),      # Older demographic
    'Miami': (35, 12),      # Younger demographic
    'Orlando': (38, 14),    # Mixed demographic
    'Jacksonville': (42, 13)  # Middle-aged demographic
}

for location in locations:
    # Generate ages based on location demographics
    mean_age, std_age = age_params[location]
    customer_count = int(total_customers * {
        'Tampa': 0.3,
        'Miami': 0.35,
        'Orlando': 0.2,
        'Jacksonville': 0.15
    }[location])
    
    ages = np.random.normal(loc=mean_age, scale=std_age, size=customer_count)
    ages = np.clip(ages, 18, 80).astype(int)  # Ensure ages are between 18-80
    
    # Generate purchase amounts
    for age in ages:
        # Younger and older customers spend differently across categories
        if age < 30:
            category_preference = np.random.choice(categories, p=[0.3, 0.3, 0.1, 0.2, 0.1])
        elif age < 50:
            category_preference = np.random.choice(categories, p=[0.25, 0.2, 0.25, 0.15, 0.15])
        else:
            category_preference = np.random.choice(categories, p=[0.15, 0.1, 0.35, 0.1, 0.3])
        
        # Purchase amount based on age and category
        base_amount = np.random.gamma(shape=5, scale=20)
        
        # Product tier (budget, mid-range, premium)
        price_tier = np.random.choice(['Budget', 'Mid-range', 'Premium'], 
                                     p=[0.3, 0.5, 0.2])
        
        tier_factor = {'Budget': 0.7, 'Mid-range': 1.0, 'Premium': 1.8}[price_tier]
        
        purchase_amount = base_amount * tier_factor
        
        customer_data.append({
            'Location': location,
            'Age': age,
            'Category': category_preference,
            'PurchaseAmount': round(purchase_amount, 2),
            'PriceTier': price_tier
        })

# Create DataFrames
sales_df = pd.DataFrame(quarterly_data)
customer_df = pd.DataFrame(customer_data)

# Add some calculated columns
sales_df['Quarter_Num'] = sales_df['Quarter'].dt.quarter
sales_df['SalesPerDollarSpent'] = sales_df['Sales'] / sales_df['AdSpend']

# Print data info
print("\nSales Data Sample:")
print(sales_df.head())
print("\nCustomer Data Sample:")
print(customer_df.head())
print("\nDataFrames created successfully. Ready for visualization!")
# ----- END OF DATA CREATION -----


# TODO 1: Time Series Visualization - Sales Trends
# 1.1 Create a line chart showing overall quarterly sales trends
# REQUIRED: Function must create and return a matplotlib figure
def plot_quarterly_sales_trend():
    """
    Create a line chart showing total sales for each quarter.
    REQUIRED: Return the figure object
    """
    # Your code here
    sales_data = sales_df.groupby('QuarterLabel')['Sales'].sum()
    fig = plt.figure(figsize=(8,5))
    plt.plot(sales_data.index,sales_data.values)
    plt.title('Quarterly Sales')
    plt.xlabel('Quarters')
    plt.ylabel('Sales')
    return fig

# 1.2 Create a multi-line chart comparing sales trends across locations
# REQUIRED: Function must create and return a matplotlib figure
print(sales_df.groupby('Location')['Sales'].sum())
def plot_location_sales_comparison():
    """
    Create a multi-line chart comparing quarterly sales across different locations.
    REQUIRED: Return the figure object
    """
    # Your code here
    fig = plt.figure(figsize=(8,5))
    sales_data_Miami = sales_df[sales_df['Location'] == 'Miami']
    sales_data_Miami = sales_data_Miami.groupby('QuarterLabel')['Sales'].sum()
    sales_data_Tampa = sales_df[sales_df['Location'] == 'Tampa']
    sales_data_Tampa = sales_data_Tampa.groupby('QuarterLabel')['Sales'].sum()
    sales_data_Jacksonville = sales_df[sales_df['Location'] == 'Jacksonville']
    sales_data_Jacksonville = sales_data_Jacksonville.groupby('QuarterLabel')['Sales'].sum()
    sales_data_Orlando = sales_df[sales_df['Location'] == 'Orlando']
    sales_data_Orlando = sales_data_Orlando.groupby('QuarterLabel')['Sales'].sum()
    plt.plot(sales_data_Miami.index,sales_data_Miami.values, label='Miami')
    plt.plot(sales_data_Tampa.index,sales_data_Tampa.values, label='Tampa')
    plt.plot(sales_data_Jacksonville.index,sales_data_Jacksonville.values, label='Jacksonville')
    plt.plot(sales_data_Orlando.index,sales_data_Orlando.values, label='Orlando')
    plt.legend(fontsize=10)
    plt.title('Quarterly Sales by Location')
    plt.xlabel('Quarters')
    plt.ylabel('Sales')
    return fig


# TODO 2: Categorical Comparison - Product Performance by Location
# 2.1 Create a grouped bar chart comparing category performance by location
# REQUIRED: Function must create and return a matplotlib figure
def plot_category_performance_by_location():
    """
    Create a grouped bar chart showing how each product category performs in different locations.
    REQUIRED: Return the figure object
    """
    # Your code here
    sales_data_1 = sales_df[sales_df['Category'] == 'Beauty']
    sales_data_1 = sales_data_1.groupby('Location')['Sales'].sum()
    sales_data_1 = sales_data_1.to_list()
    sales_data_2 = sales_df[sales_df['Category'] == 'Clothing']
    sales_data_2 = sales_data_2.groupby('Location')['Sales'].sum()
    sales_data_2 = sales_data_2.to_list()
    sales_data_3 = sales_df[sales_df['Category'] == 'Electronics']
    sales_data_3 = sales_data_3.groupby('Location')['Sales'].sum()
    sales_data_3 = sales_data_3.to_list()
    sales_data_4 = sales_df[sales_df['Category'] == 'Home Goods']
    sales_data_4 = sales_data_4.groupby('Location')['Sales'].sum()
    sales_data_4 = sales_data_4.to_list()
    sales_data_5 = sales_df[sales_df['Category'] == 'Sporting Goods']
    sales_data_5 = sales_data_5.groupby('Location')['Sales'].sum()
    sales_data_5 = sales_data_5.to_list()
    fig = plt.figure(figsize=(8,5))
    x = np.arange(4)
    plt.bar(x, sales_data_1, 0.1, color='red', label='Beauty')
    plt.bar(x + 0.1, sales_data_2, 0.1, color='green', label='Clothing')
    plt.bar(x + 0.2, sales_data_3, 0.1, color='blue', label='Electronics')
    plt.bar(x + 0.3, sales_data_4, 0.1, color='pink', label='Home Goods')
    plt.bar(x + 0.4, sales_data_5, 0.1, color='orange', label='Sporting Goods')
    plt.xticks(x, ['Jacksonville', 'Miami', 'Orlando', 'Tampa'])
    plt.legend(fontsize=10)
    plt.title('Quarterly Sales by Location')
    plt.xlabel('Locations')
    plt.ylabel('Sales')
    return fig

# 2.2 Create a stacked bar chart showing the composition of sales in each location
# REQUIRED: Function must create and return a matplotlib figure
def plot_sales_composition_by_location():
    """
    Create a stacked bar chart showing the composition of sales across categories for each location.
    REQUIRED: Return the figure object
    """
    # Your code here
    sales_data_1 = sales_df[sales_df['Category'] == 'Beauty']
    sales_data_1 = sales_data_1.groupby('Location')['Sales'].sum()
    sales_data_1 = np.array(sales_data_1)
    sales_data_2 = sales_df[sales_df['Category'] == 'Clothing']
    sales_data_2 = sales_data_2.groupby('Location')['Sales'].sum()
    sales_data_2 = np.array(sales_data_2)
    sales_data_3 = sales_df[sales_df['Category'] == 'Electronics']
    sales_data_3 = sales_data_3.groupby('Location')['Sales'].sum()
    sales_data_3 = np.array(sales_data_3)
    sales_data_4 = sales_df[sales_df['Category'] == 'Home Goods']
    sales_data_4 = sales_data_4.groupby('Location')['Sales'].sum()
    sales_data_4 = np.array(sales_data_4)
    sales_data_5 = sales_df[sales_df['Category'] == 'Sporting Goods']
    sales_data_5 = sales_data_5.groupby('Location')['Sales'].sum()
    sales_data_5 = np.array(sales_data_5)
    fig = plt.figure(figsize=(8,5))
    x = np.arange(4)
    plt.bar(x, sales_data_1, color='red', label='Beauty')
    plt.bar(x, sales_data_2, bottom=sales_data_1, color='green', label='Clothing')
    plt.bar(x, sales_data_3, bottom=sales_data_1+sales_data_2, color='blue', label='Electronics')
    plt.bar(x, sales_data_4, bottom=sales_data_1+sales_data_2+sales_data_3, color='green', label='Home Goods')
    plt.bar(x, sales_data_5, bottom=sales_data_1+sales_data_2+sales_data_4, color='pink', label='Sporting Goods')
    plt.legend(fontsize=10)
    plt.title('Sales by category by Location')
    plt.xlabel('Locations')
    plt.ylabel('Sales')
    return fig


# TODO 3: Relationship Analysis - Advertising and Sales
# 3.1 Create a scatter plot to examine the relationship between ad spend and sales
# REQUIRED: Function must create and return a matplotlib figure
print(sales_df.columns)
def plot_ad_spend_vs_sales():
    """
    Create a scatter plot to visualize the relationship between advertising spend and sales.
    REQUIRED: Return the figure object
    """
    # Your code here
    fig = plt.figure(figsize=(8,5))
    plt.scatter(sales_df['AdSpend'], sales_df['Sales'])
    plt.title('Ad spend vs Sales')
    plt.xlabel('Ad spending')
    plt.ylabel('Sales')
    return fig

# 3.2 Create a line chart showing sales per dollar spent on advertising over time
# REQUIRED: Function must create and return a matplotlib figure
def plot_ad_efficiency_over_time():
    """
    Create a line chart showing how efficient advertising spend has been over time.
    REQUIRED: Return the figure object
    """
    # Your code here
    sales_data = sales_df.groupby('AdSpend')['SalesPerDollarSpent'].sum()
    fig = plt.figure(figsize=(8,5))
    plt.plot(sales_data.index,sales_data.values)
    plt.title('Ad efficiency line')
    plt.xlabel('AdSpend')
    plt.ylabel('SalesPerDollar')
    return fig



# TODO 4: Distribution Analysis - Customer Demographics
# 4.1 Create histograms of customer age distribution
# REQUIRED: Function must create and return a matplotlib figure with subplots
def plot_customer_age_distribution():
    """
    Create histograms showing the age distribution of customers, both overall and by location.
    REQUIRED: Return the figure object
    """
    # Your code here
    customer_data_1 = customer_df.groupby('Age')['PurchaseAmount'].sum()
    customer_data_2 = customer_df.groupby('Location')['Age'].mean()
    fig = plt.figure(figsize=(8,5))
    plt.subplots(2)
    plt.hist(customer_data_1.index, bins=50, edgecolor='black')
    plt.hist(customer_data_2.values, bins=50, edgecolor='black', color='gray')
    plt.title('Age distribution')
    plt.xlabel('Age')
    plt.ylabel('Quantity')
    return fig

# 4.2 Create box plots comparing purchase amounts by age groups
# REQUIRED: Function must create and return a matplotlib figure
def plot_purchase_by_age_group():
    """
    Create box plots showing purchase amounts across different age groups.
    REQUIRED: Return the figure object
    """
    # Your code here
    pass


# TODO 5: Sales Distribution - Pricing Tiers
# 5.1 Create a histogram of purchase amounts
# REQUIRED: Function must create and return a matplotlib figure
def plot_purchase_amount_distribution():
    """
    Create a histogram showing the distribution of purchase amounts.
    REQUIRED: Return the figure object
    """
    # Your code here
    customer_data_1 = customer_df['PurchaseAmount']
    fig = plt.figure(figsize=(8,5))
    plt.hist(customer_data_1.index, bins=50, edgecolor='black')
    plt.title('Purchase Amounts')
    plt.xlabel('Purchases')
    plt.ylabel('Quantity')
    return fig

# 5.2 Create a pie chart showing sales breakdown by price tier
# REQUIRED: Function must create and return a matplotlib figure
def plot_sales_by_price_tier():
    """
    Create a pie chart showing the breakdown of sales by price tier.
    REQUIRED: Return the figure object
    """
    # Your code here
    customer_data_1 = customer_df.groupby('PriceTier')['PurchaseAmount'].sum()
    fig = plt.figure(figsize=(8,5))
    plt.pie(customer_data_1.values, labels= customer_data_1.index)
    plt.title('Purchase Amounts by Price Tier')
    return fig

# TODO 6: Market Share Analysis
# 6.1 Create a pie chart showing sales breakdown by category
# REQUIRED: Function must create and return a matplotlib figure
def plot_category_market_share():
    """
    Create a pie chart showing the market share of each product category.
    REQUIRED: Return the figure object
    """
    # Your code here
    customer_data = customer_df.groupby('Category')['PurchaseAmount'].sum()
    fig = plt.figure(figsize=(8,5))
    plt.pie(customer_data.values, labels= customer_data.index)
    plt.title('Purchase Amounts by Category')
    return fig

# 6.2 Create a pie chart showing sales breakdown by location
# REQUIRED: Function must create and return a matplotlib figure
def plot_location_sales_distribution():
    """
    Create a pie chart showing the distribution of sales across different store locations.
    REQUIRED: Return the figure object
    """
    # Your code here
    customer_data = customer_df.groupby('Location')['PurchaseAmount'].sum()
    fig = plt.figure(figsize=(8,5))
    plt.pie(customer_data.values, labels= customer_data.index)
    plt.title('Purchase Amounts by Category')
    return fig


# TODO 7: Comprehensive Dashboard
# REQUIRED: Function must create and return a matplotlib figure with at least 4 subplots
def create_business_dashboard():
    """
    Create a comprehensive dashboard with multiple subplots highlighting key business insights.
    REQUIRED: Return the figure object with at least 4 subplots
    """
    # Your code here
    pass


# Main function to execute all visualizations
# REQUIRED: Do not modify this function name
def main():
    print("\n" + "=" * 60)
    print("SUNCOAST RETAIL VISUAL ANALYSIS RESULTS")
    print("=" * 60)
    
    # REQUIRED: Call all visualization functions and store figures
    # Store each figure in a variable for potential saving/display
    
    # Time Series Analysis
    fig1 = plot_quarterly_sales_trend()
    fig2 = plot_location_sales_comparison()
    
    # Categorical Comparison
    fig3 = plot_category_performance_by_location()
    fig4 = plot_sales_composition_by_location()
    
    # Relationship Analysis
    fig5 = plot_ad_spend_vs_sales()
    fig6 = plot_ad_efficiency_over_time()
    
    # Distribution Analysis
    fig7 = plot_customer_age_distribution()
    fig8 = plot_purchase_by_age_group()
    
    # Sales Distribution
    fig9 = plot_purchase_amount_distribution()
    fig10 = plot_sales_by_price_tier()
    
    # Market Share Analysis
    fig11 = plot_category_market_share()
    fig12 = plot_location_sales_distribution()
    
    # Comprehensive Dashboard
    fig13 = create_business_dashboard()
    
    # REQUIRED: Add business insights summary
    print("\nKEY BUSINESS INSIGHTS:")
    # Your insights here based on the visualizations
    
    # Display all figures
    plt.show()

# Run the main function
if __name__ == "__main__":
    main()
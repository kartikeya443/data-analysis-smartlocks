import pandas as pd

# Load the CSV file containing the scraped data
df = pd.read_csv('amazon_smart_locks_detailed.csv')

# Normalize the 'Brand Name' to lowercase to merge similar brands
df['Brand Name'] = df['Brand Name'].str.lower()

# 1. Number of Brands in the Segment
num_brands = df['Brand Name'].nunique()

# 2. Count of SKUs Per Brand
sku_count_per_brand = df['Brand Name'].value_counts()

# 3. Relative Ranking Calculation
# Calculate the average rank for each brand
relative_ranking = df.groupby('Brand Name')['Ranking'].mean().sort_values()

# 4. Relative Rating Calculation
# Calculate the average rating for each brand
relative_rating = df.groupby('Brand Name')['Rating'].mean().sort_values(ascending=False)

# 5. Price Distribution of SKUs
price_bins = [0, 4999, 9999, 14999, 19999, float('inf')]
price_labels = ['<INR 4999', 'INR 5000-9999', 'INR 10000-14999', 'INR 15000-19999', 'Greater than 20000']
df['Price Band'] = pd.cut(df['Price'], bins=price_bins, labels=price_labels)
price_distribution = df['Price Band'].value_counts().reindex(price_labels)

# Output the results
print(f"Number of Brands in the Segment: {num_brands}")
print("\nCount of SKUs Per Brand:")
print(sku_count_per_brand)

print("\nRelative Ranking of Brands (lower is better):")
print(relative_ranking)

print("\nRelative Rating of Brands (higher is better):")
print(relative_rating)

print("\nPrice Distribution of SKUs:")
print(price_distribution)

# Optionally, save the results to a CSV file
analysis_result = {
    'Brand': sku_count_per_brand.index,
    'SKU Count': sku_count_per_brand.values,
    'Relative Ranking': relative_ranking.reindex(sku_count_per_brand.index).values,
    'Relative Rating': relative_rating.reindex(sku_count_per_brand.index).values
}
result_df = pd.DataFrame(analysis_result)
result_df.to_csv('brand_analysis_results.csv', index=False)

price_distribution.to_csv('price_distribution.csv')

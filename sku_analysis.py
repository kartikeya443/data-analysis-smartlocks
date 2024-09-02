import pandas as pd

# Load the CSV file containing the scraped data
df = pd.read_csv('amazon_smart_locks_detailed.csv')

# Normalize the 'Brand Name' to lowercase to merge similar brands
df['Brand Name'] = df['Brand Name'].str.lower()

# Sort the DataFrame by 'Brand Name' and 'Ranking' to make it easier to group SKUs under each brand
df = df.sort_values(by=['Brand Name', 'Ranking'])

# Group the data by 'Brand Name' and create a dictionary with lists of SKUs and their ranks
brand_sku_ranking = df.groupby('Brand Name', group_keys=False).apply(lambda x: list(x['Ranking'])).to_dict()

# Create a DataFrame from the dictionary for better visualization
brand_analysis_df = pd.DataFrame(dict([(k, pd.Series([f'SKU {i+1}: Rank {rank}' for i, rank in enumerate(v)])) for k, v in brand_sku_ranking.items()]))

# Save the DataFrame to a CSV file
brand_analysis_df.to_csv('brand_and_sku.csv', index=False)

print(f"Brand analysis results saved to 'brand_and_sku.csv'")

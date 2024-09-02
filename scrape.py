import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
import time

# Rotating user-agents to avoid detection
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.2 Safari/605.1.15',
    # Add more if needed
]

# Function to extract required data fields
def extract_data(soup, page_number):
    data = []
    search_results = soup.find_all('div', {'data-component-type': 's-search-result'})
    
    for index, item in enumerate(search_results):
        try:
            # Extracting brand name
            product_name = item.h2.text.strip()
            brand_name = product_name.split()[0]
            
            # Extracting product URL
            product_url = 'https://www.amazon.in' + item.h2.a['href']
            
            # Extracting price
            try:
                price = item.find('span', 'a-price-whole').text.replace(',', '').strip()
                price = int(price)
            except:
                price = None
            
            # Extracting rating
            try:
                rating = item.find('span', {'class': 'a-icon-alt'}).text.split()[0]
                rating = float(rating)
            except:
                rating = None
            
            # Extracting rating count
            try:
                rating_count = item.find('span', {'class': 'a-size-base'}).text.replace(',', '').strip()
                rating_count = int(rating_count)
            except:
                rating_count = None
            
            # Extracting review count (assuming same as rating count)
            review_count = rating_count
            
            # Calculating the ranking (position in search results)
            ranking = (page_number - 1) * len(search_results) + (index + 1)
            
            # Append the data to the list
            data.append({
                'Brand Name': brand_name,
                'Price': price,
                'Rating': rating,
                'Rating Count': rating_count,
                'Review Count': review_count,
                'Ranking': ranking,
                'URL': product_url
            })
        except AttributeError:
            continue
    return data

# Scrape multiple pages of Amazon search results
def scrape_amazon(search_query, pages=20):
    all_data = []
    
    for page in range(1, pages + 1):
        try:
            headers = {'User-Agent': random.choice(user_agents)}
            url = f'https://www.amazon.in/s?k={search_query}&page={page}'
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            page_data = extract_data(soup, page)
            all_data.extend(page_data)
            
            print(f"Scraped page {page}/{pages}")
            
            time.sleep(random.uniform(2, 5))
        except Exception as e:
            print(f"Failed to scrape page {page}: {e}")
    
    return all_data

# Search query
search_query = "smart lock"

# Scrape the data
data = scrape_amazon(search_query, pages=20)

# Convert data to DataFrame
df = pd.DataFrame(data)

# Save data to CSV
df.to_csv('amazon_smart_locks_detailed.csv', index=False)

print(f"Scraped {len(data)} products and saved to amazon_smart_locks_detailed.csv")

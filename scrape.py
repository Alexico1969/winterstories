import pandas as pd
import requests
from bs4 import BeautifulSoup

# Load the CSV file
df = pd.read_csv('Winter story - Sheet4.csv')

for index, row in df.iterrows():
    name = row['Name']
    group = row['Group']
    url = row['URL']
    
    # Format the filename: Group-Name.txt
    filename = f"{group}-{name}.txt"
    
    try:
        # Fetch the website content
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Parse the HTML and extract visible text
        soup = BeautifulSoup(response.content, 'html.parser')
        text_content = soup.get_text(separator='\n', strip=True)
        
        # Save to a text file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(text_content)
        print(f"Successfully saved: {filename}")
        
    except Exception as e:
        print(f"Error scraping {url}: {e}")
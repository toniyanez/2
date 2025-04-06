import requests
from bs4 import BeautifulSoup

# URL of the website to scrape
url = 'https://example.com/tariffs'

# Send a GET request to the website
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the table or data section containing the tariffs information
    # This may vary depending on the structure of the website
    tariffs_table = soup.find('table', {'id': 'tariffs-table'})
    
    if tariffs_table:
        # Extract the headers
        headers = [header.text for header in tariffs_table.find_all('th')]
        
        # Extract the rows
        rows = tariffs_table.find_all('tr')
        
        # Process each row
        for row in rows:
            columns = row.find_all('td')
            country_tariffs = {headers[i]: columns[i].text for i in range(len(columns))}
            print(country_tariffs)
    else:
        print('Tariffs table not found on the page.')
else:
    print(f'Failed to retrieve the webpage. Status code: {response.status_code}')

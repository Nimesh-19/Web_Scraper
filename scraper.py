import requests
import sqlite3
from bs4 import BeautifulSoup

def scrape_data(url):
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to retrieve the webpage")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    
    quotes = soup.find_all('div', class_='quote')

    data = []
    for quote in quotes:
        text = quote.find('span', class_='text').get_text()
        author = quote.find('small', class_='author').get_text()
        data.append((text, author))

    return data

def save_to_database(data, db_name="scraper.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT,
            author TEXT
        )
    ''')

    cursor.executemany("INSERT INTO quotes (text, author) VALUES (?, ?)", data)

    conn.commit()
    conn.close()
    print(f"Data saved to {db_name}")

# Run the scraper
url = "https://quotes.toscrape.com"
scraped_data = scrape_data(url)

if scraped_data:
    save_to_database(scraped_data)
    
else:
    print("No data scraped.")

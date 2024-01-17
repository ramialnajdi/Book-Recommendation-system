import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys 

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

def get_data():
    number_of_pages = 50
    titles, prices, urls, description = [], [], [], []
    for page_number in range(1, number_of_pages + 1):
        print('page_number: ', page_number)
        url = f"https://books.toscrape.com/catalogue/page-{page_number}.html"
        doc = get_doc(url)
        titles += get_book_title(doc)
        prices += get_book_price(doc)
        URLS = get_book_url(doc)
        urls += URLS
        for URL in URLS:
            description.append(get_book_description(URL))

    data = {
        "titles": titles,
        "prices": prices,
        "urls": urls,
        "description": description,
    }

    return data    
        

def get_doc(url):
    # Get the response from the URL
    response = requests.get(url)
    # Create a soup object to parse the html content
    doc = BeautifulSoup(response.text,'html.parser') # Parse the HTML
    # Check if the request was successful
    if response.status_code != 200:
        raise Exception('Failed to load page {}'.format(response))
    return doc


# to get books' titles for each page
def get_book_title(doc):
    book_title_tags = doc.find_all('h3')
    book_titles = [tags.text for tags in book_title_tags]
    return book_titles

# to get books' prices for each page
def get_book_price(doc):
    book_price_tags = doc.find_all('p', class_ = 'price_color')
    book_prices = [tags.text.replace('Â','') for tags in book_price_tags]
    return book_prices

# to get books' URLs for each page
def get_book_url(doc):
    book_urls = []
    for article in doc.find_all('h3'):
        for link in article.find_all('a', href = True):
            url = link['href']
            links = 'https://books.toscrape.com/catalogue/' + url 
            if links not in book_urls:
                book_urls.append(links)      
    return book_urls

# to get book's descriptions 
def get_book_description(url):
    doc = BeautifulSoup(requests.get(url).text, "html.parser").find_all('p')
    description = None
    max_length = 0
    for item in doc:
        if len(item) == 1:
            if len(item.text) > max_length:
                max_length = len(item.text) 
                description = item.text
    return description


if __name__=="__main__":
    print("**********************let's begin**********************")
    data = get_data()
    df = pd.DataFrame(data)
    df.to_csv('./book_recommendation_ai/data.csv', index = False, encoding='utf-8') 
    print(df.head())



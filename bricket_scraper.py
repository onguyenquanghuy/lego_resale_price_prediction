import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

HEADERS = {
'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'sec-fetch-site': 'none',
'sec-fetch-mode': 'navigate',
'sec-fetch-user': '?1',
'sec-fetch-dest': 'document',
'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
}

def get_data(url):
    r = requests.get(url, headers=HEADERS)
    if not r.ok:
        print(f"Server status: {r.status_code}")
    else:
        soup = BeautifulSoup(r.text, 'lxml')
    return soup

def parse(soup):
    products_list = []
    results = soup.find_all('article', {'class': 'set'})
    for item in results:
        try:
            title = item.find('div', {'class': 'meta'}).find('a').text
        except:
            title = None

        try:
            sub_theme = item.select('div > a', {'class': 'tags'})[1].text
        except:
            sub_theme = None

        product = {
            'title': title,
            'sub_theme': sub_theme
        }
        products_list.append(product)
    print(products_list)
    
def output(data):
    return

def main():
    url = 'https://brickset.com/sets/year-2022/page-1'
    soup = get_data(url)
    parse(soup)

if __name__ == '__main__':
    main()


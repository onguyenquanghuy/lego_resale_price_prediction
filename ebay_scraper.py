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
    # Check server connection
    if not r.ok:
        print('Server responded:', r.status_code)
    else:
        soup = BeautifulSoup(r.text, 'lxml')
    return soup

def parse(soup):
    products_list = []
    results = soup.find_all('div', {'class': 's-item__info clearfix'})
    for item in results[1:]:
        try:
            title = item.find('div', {'class': 's-item__title s-item__title--has-tags'}).text
        except:
            title = None

        try:
            p = item.find('span', {'class': 's-item__price'}).text.replace(',','').strip()
            currency, sold_price = p[0], float(p[1:])
        except:
            sold_price = None
            currency = None

        try:
            sold_date = item.find('div', {'class': 's-item__title--tagblock'}).find('span', {'class': 'POSITIVE'}).text.replace('Sold','').strip()
        except:
            sold_date = None

        product = {
            'title': title,
            'currency': currency,
            'sold_price': sold_price,
            'sold_date': sold_date,
            # 'link': item.find('a', {'class': 's-item__link'})['href'],
            }
        products_list.append(product)
    return products_list

def output(products_list, search_term):
    products_df = pd.DataFrame(products_list)
    products_df.to_csv(search_term + '_ebay_sold_price.csv', index=False, mode='a')
    return
    

# def write_csv(product_list):
#     with open('lego_sold_price_ebay.csv', 'a') as csvfile:
#         writer = csv.writer(csvfile)
#         row = [product_list['title'], product_list['currency'], product_list['sold_price'], product_list['sold_date']]
#         writer.writerow(row)

def main():
    # products_list = []
    search_term = 'lego'
    for x in range(1,56):
        url = f'https://www.ebay.co.uk/sch/i.html?_from=R40&_nkw={search_term}&_sacat=0&LH_Sold=1&LH_Complete=1&rt=nc&LH_ItemCondition=1000&_pgn={str(x)}'
        soup = get_data(url)
        products_list = parse(soup)
        time.sleep(3)
        output(products_list, search_term)
        # write_csv(products_list)
    print('Saved to CSV')

if __name__ == '__main__':
    main()


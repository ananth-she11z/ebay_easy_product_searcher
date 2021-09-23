import re
import os
import csv
import sys
import requests
from bs4 import BeautifulSoup

if len(sys.argv) < 4:
    print('\nUsage: ' + sys.argv[0] + ' <Product name> <No. of pages to scrap> <Budget price>\n')
    print('Example: ' + sys.argv[0] + ' "Mens watches" 1 50')
    print('Example: ' + sys.argv[0] + ' Laptops 3 500\n')
    sys.exit()

product = str(sys.argv[1]).strip()
product_name = product.replace(' ', '+').strip()
page_number = int(sys.argv[2])
budget_price = int(sys.argv[3])
filename = product_name.replace('+','_') + '.csv'
location = os.getcwd()

csv_file = open(filename, 'w', encoding='utf8')
csv_writer = csv.writer(csv_file)

csv_writer.writerow(['Product Title', 'Product Cost', 'Product Sold', 'Product Available', 'Product Offer time left', \
    'Estimated Product Delivery', 'No. of Watchers', 'Product Seller Name', 'Seller Feedback Score', 'Seller Feedback', \
    'Product URL'])

print('\n----------------------------------------------------------')
print('ebay Web Scrapper by Ananth aka she11z')
print('LinkedIn: https://www.linkedin.com/in/ananth-she11z/')
print('GitHub: https://github.com/ananth-she11z')
print('-----------------------------------------------------------')
print('Product Name: ' + product + '\nNo. of pages to search: ' + str(page_number) + '\nYour Budget Price: ' + str(budget_price))
print('-----------------------------------------------------------')
print('Please wait untill I scrap your search...\n')

def page_index():
    for page in range(1,page_number+1):
        print('Scrapping your product on page ' + str(page) + '/' + str(page_number) + '\n')
        product_search_url = 'https://www.ebay.com/sch/i.html?_nkw=' + product_name + '&_pgn=' + str(page)
        page_soup(product_search_url)

def page_soup(url):
    page_response = requests.get(url)
    if page_response.ok:
        page_soup = BeautifulSoup(page_response.text, 'html.parser')
        products_on_page = page_soup.find_all('a', class_='s-item__link')
        for product in products_on_page:
            product_soup = get_product_soup(product.get('href'))
            get_product_details(product_soup, product.get('href'))
    else:
        sys.exit()

def get_product_soup(p_url):
    p_response = requests.get(p_url)
    return BeautifulSoup(p_response.text, 'html.parser')

def get_product_details(product_soup, p_href):
    try:
        p_cost = product_soup.find('div', id='prcIsumConv')
        p_cost_alpha_numeric = p_cost.text.strip()
        p_cost_numeric_search = re.sub('\W+','', p_cost_alpha_numeric)
        p_cost_numeric_search2 = re.findall('\d+', p_cost_numeric_search)[0]
        p_cost_numeric = int(p_cost_numeric_search2[:-2])

        if p_cost_numeric > budget_price:
            return

        else:
            try:
                p_title = product_soup.find('h1', class_='it-ttl')
                title = p_title.text.replace('Details about', '').strip()

            except:
                title = 'None'

            cost = p_cost.text.strip()

            try:
                p_sold = product_soup.find('a', class_='vi-txt-underline')
                sold = p_sold.text.strip()

            except:
                sold = 'None'

            try:
                p_availibility = product_soup.find('span', id='qtySubTxt')
                availibility = p_availibility.text.strip()

            except:
                availibility = 'None'

            try:
                p_time_left = product_soup.find('span', id='vi-cdown_timeLeft')
                time_left = p_time_left.text.strip()

            except:
                time_left = 'None'

            try:
                p_delivery = product_soup.find('span', class_='vi-acc-del-range')
                delivery = p_delivery.text.strip()

            except:
                delivery = 'None'

            try:
                p_watchers = product_soup.find('span', class_='w2b-head')
                watchers = p_watchers.text.strip()

            except:
                watchers = 'None'

            try:
                p_seller = product_soup.find('span', class_='mbg-nw')
                seller = p_seller.text.strip()

            except:
                seller = 'None'

            try:
                p_seller_score = product_soup.find('span', class_='vi-mbgds3-bkImg')
                seller_score = p_seller_score.get('title').strip()

            except:
                seller_score = 'None'

            try:
                p_seller_feedback = product_soup.find('div', id='si-fb')
                seller_feedback = p_seller_feedback.text.strip()

            except:
                seller_feedback = 'None'

            csv_writer.writerow([title.strip(), cost.strip(), sold.strip(), \
                availibility.strip(), time_left.strip(), delivery.strip(), \
                watchers.strip(), seller.strip(), seller_score.strip(), \
                seller_feedback.strip(), p_href.strip()])

    except:
        return

def main():
    try:
        page_index()
        csv_file.close()
        print('Fantastic!! the scrap completed successfully.\n')
        print('-----------------------------------------------------------')
        print('Output file name: ' + filename)
        print('Output file location: ' + location + '\n')
        print('-----------------------------------------------------------')

    except KeyboardInterrupt:
        print('\nTool stopped. Please delete the incomplete file (' + filename + ') created at location: (' + location + ')\n')

if __name__ == '__main__':
    main()


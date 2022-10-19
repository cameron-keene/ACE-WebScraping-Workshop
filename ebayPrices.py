# 1. make sure you have pip installed

# 2. install packages
# pip install requests-html
from operator import index
from requests_html import HTMLSession
# pip install beautifulsoup4
from bs4 import BeautifulSoup
# pip install pandas
import pandas as pd
# pip install matplotlib
import matplotlib.pyplot as plt

# 3. item that we want to search for
term = 'rtx+3090'
# beginning url
url = f'https://www.ebay.com/sch/i.html?_from=R40&_nkw={term}&_sacat=0&LH_Sold=1&LH_Complete=1&rt=nc&LH_ItemCondition=3000&_ipg=240'

# global variable to put all the data into
soldPrices = []

# 4. get the raw html data from the web page
def get_data(url):
    s = HTMLSession()
    r = s.get(url)
    r.html.render(sleep=1)
    data = BeautifulSoup(r.text, 'html.parser')
    # print("data: ", data)

    return data

# 5. parse the raw html data that we are searching for
def parse_data(data):
    # get each individual listing "widget"
    results = data.find_all('div',{'class':'s-item__detail s-item__detail--primary'})
    # iterate through all items and get the price
    for items in results:
        # find all items in the POSITIVE SPAN, contains price.
        price = items.find('span',{'class':'POSITIVE'})
        # issue with returning none for items, we need to check that item exits
        if price:
            # if item exists we can parse it for the text value ($Price)
            price = float(price.text.replace('$','').replace(',','').strip())
            soldPrices.append(price)

# 6. get multiple pages, we don't want to just get one page of results. 
def next_page(data):
    # get the pagination strip at bottom of page
    pages = data.find('div',{'class':'s-pagination'})
    if pages:
        # extract the URL from the webpage. 
        url = pages.find('a',{'class':'pagination__next icon-link'})['href']
        return url
    else:
        print("pages-none", pages)


# 7. loop through all the pages of sold items and get all the prices
while True:
    # get the data for the webpage
    webpage_data = get_data(url)
    # get the next url
    next_url = next_page(webpage_data)
    # check if old url == next url
    if (url == next_url):
        break
    else:
        url = next_url
    # if does not match then parse
    parse_data(webpage_data)
    # print("new url: ", new_url)

# 8. Main functionallity

# convert the array to a pandas df
df = pd.DataFrame(soldPrices, columns=['prices'])
# insert new column with index numbers
index_column = list(range(0,len(soldPrices)))
# add to the existing df
df.insert(loc=0, column='idx', value=index_column)
# plot the df
df.plot(x='idx',y='prices')
# show the df
plt.show()
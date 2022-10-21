# 2. install packages
# pip install requests-html
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
url = f'https://www.ebay.com/sch/i.html?_nkw={term}&_sop=13&LH_Sold=1&LH_Complete=1&rt=nc&LH_ItemCondition=1000&_ipg=240'

# global variable to put all the data into
soldPrices = []

# 4. get the raw html data from the web page
def get_data(url):
    session = HTMLSession()
    response=session.get(url)
    response.html.render(sleep=2)
    data = BeautifulSoup(response.text, 'html.parser')
    return data

# 5. parse the raw html data that we are searching for
def parse_data(data):
    results = data.find_all('div', {'class':'s-item__detail s-item__detail--primary'})
    for items in results:
        price = items.find('span',{'class':'POSITIVE'})

        if price:
            stringprice = price.text.replace('$','').replace(',','').strip
            price = float(stringprice)
            soldPrices.append(price)


# 6. get multiple pages, we don't want to just get one page of results. 
def next_page(data):
    pages = data.find('div',{'class':'s-pagination'})
    if pages:
        url = pages.find('a',{'class':'pagination__next icon-link'})['href']
        return url
    else:
        return "no more urls"




# 7. loop through all the pages of sold items and get all the prices
while True:
    webpage_data = get_data(url)
    next_url = next_page(webpage_data)
    if(url==next_url):
        break
    else:
        url = next_url
    parse_data(webpage_data)


# 8. Main functionality
df = pd.DataFrame(soldPrices, columns=['prices'])
index_column = list(range(0,len(soldPrices)))
df.insert(loc=0,column='index',value=index_column)
df.plot(x='index',y='prices')
plt.show()
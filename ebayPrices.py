# 1. install packages
# pip install requests-html
from requests_html import HTMLSession
# pip install beautifulsoup4
from bs4 import BeautifulSoup
# pip install pandas
import pandas as pd
# pip install matplotlib
import matplotlib.pyplot as plt

# 2. item that we want to search for
term = 'rtx+3090'
# beginning url
url = f'https://www.ebay.com/sch/i.html?_nkw={term}&_sop=13&LH_Sold=1&LH_Complete=1&rt=nc&LH_ItemCondition=1000&_ipg=240'

# global variable to put all the data into
soldPrices = []

# 3. get the raw html data from the web page
def get_data(url):
    s = HTMLSession()
    r = s.get(url)
    r.html.render(sleep=2)
    data = BeautifulSoup(r.text, 'html.parser')
    return data

# 4. parse the raw html data that we are searching for
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
            try:
                price = float(price.text.replace('$','').replace(',','').strip())
                soldPrices.append(price)
            except:
                print("no price found, append 0")
                soldPrices.append(0)


# 5. get multiple pages, we don't want to just get one page of results. 
def next_page(data):
    # get the pagination strip at bottom of page
    pages = data.find('div',{'class':'s-pagination'})
    # print("pages: ",pages)       
    if pages:
        # extract the URL from the webpage. 
        url = pages.find('a',{'class':'pagination__next icon-link'})
        if url:
            url = url['href']
            print("URL: ", url)
            return url
        else:
            print("no more urls")
            return "no more urls"



# 6. loop through all the pages of sold items and get all the prices
while True:
    # get the data for the webpage
    webpage_data = get_data(url)
    # get the next url
    next_url = next_page(webpage_data)
    # check if old url == next url
    if (url == next_url):
        break
    elif (next_url == "no more urls"):
        break
    else:
        url = next_url
    # if does not match then parse
    parse_data(webpage_data)


# 7. Main functionallity
# convert the array to a pandas df
df = pd.DataFrame(soldPrices, columns=['prices'])
# insert new column with index numbers
index_column = list(range(0,len(soldPrices)))
# add to the existing df
df.insert(loc=0, column='idx', value=index_column)
print(df.dtypes)
# export the data to csv, incase you get blocked
df.to_csv('ebay_data.csv', index = True)
# plot the df
df.plot(x='idx',y='prices')
# show the df
plt.show()
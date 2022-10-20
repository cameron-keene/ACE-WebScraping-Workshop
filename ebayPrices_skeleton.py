# 1. make sure you have pip installed

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
    

# 5. parse the raw html data that we are searching for
def parse_data(data):
    


# 6. get multiple pages, we don't want to just get one page of results. 
def next_page(data):
    



# 7. loop through all the pages of sold items and get all the prices
while True:
    # do something


# 8. Main functionallity

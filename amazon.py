__author__ = 'srizvi'
import requests
from bs4 import BeautifulSoup
import time
import webbrowser
import html5lib


url = 'http://www.amazon.in/Lenovo-U41-70-80JV007GIN-i5-5200U-Graphics/dp/B00YDX0WLW'
aukat=47000
r = requests.get(url)


soup = BeautifulSoup(r.content, "html5lib")

titles = soup.find_all('span',
                       {'id': 'priceblock_saleprice'
                        })
print "Starting..",titles
for title in titles:
    product = title.text.strip().encode('ascii', 'ignore')
    print "Fetched Price", product
    product=product.replace(",","").replace(".00","")
    if int(product) <= aukat:
        print "Yes"
        webbrowser.open(url)
    else:
        print "No"
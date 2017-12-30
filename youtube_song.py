from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import lxml
import requests
import urllib
from bs4 import BeautifulSoup
import sys,os
import json
import re

arg = len(sys.argv)
search = ""
display = ""
for x in range(1, arg):
	search += sys.argv[x]
	display += sys.argv[x]
	display += " "
	if (x == arg-1):
		break
	search += "+"

print display + "!"
print "\nThat's a nice song! Playing right away!"

browser = webdriver.Chrome(executable_path="C:\\Python27\\Scripts\\chromedriver.exe")

url = "https://www.youtube.com/results?search_query=" 
url += search

browser.get(url)
print "Sleeping..."
time.sleep(5)
print "Awake..."


url = browser.current_url
print "URL: "+url

if url=="data:,":
    print "Waiting more.."
    time.sleep(5)
#request = urllib.urlopen(url).read()
regex = re.compile("window[\"ytInitialData\"] = \{.*?\};", re.S)
responser = requests.get(url, 
                  headers={'Content-type': 'text/plain; charset=utf-8'})
regex = re.compile("window[\"ytInitialData\"] = \{.*?\};", re.S)
print responser.text
match = re.search(regex, responser.text)
match2 = match.group()
print match2
soup = BeautifulSoup(request,"lxml")
#searchdiv = soup.find_all("div", class_="yt-lockup-dismissable yt-uix-tile") #This is the div class of the search results in YouTube
#print searchdiv.__len__()
script = soup.find_all('script', text=re.compile('window'))

if script:
	print script.text



prefix = "http://youtube.com"
prefix = prefix + searchdiv[0].a["href"] #Get the url of the first search result
browser.get(prefix)
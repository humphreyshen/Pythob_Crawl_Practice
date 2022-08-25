import string
import urllib.request as req
import pandas as pd

url="https://travel.ettoday.net/category/%E6%A1%83%E5%9C%92/"

request=req.Request(url,headers={
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36"
})
with req.urlopen(request) as response:
    data=response.read().decode('utf-8')

import bs4
root=bs4.BeautifulSoup(data,"html.parser")
titles=root.find_all("h3",itemprop='headline')

for title in titles:
    if title.a != None:
     print(title.a.string)
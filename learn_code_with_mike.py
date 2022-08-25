import urllib.request as req
import string

url="https://www.learncodewithmike.com/"

request=req.Request(url,headers={
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36"
})

with req.urlopen(request) as response:
    data=response.read().decode('utf-8')

import bs4 
root=bs4.BeautifulSoup(data,'html.parser')
titles=root.find_all("h3", class_="post-title entry-title")

import pandas as pd

df=[]

for title in titles:
    if title.a  != None:
        df.append(title.a.string)

df1=pd.DataFrame(df)

print(df1)
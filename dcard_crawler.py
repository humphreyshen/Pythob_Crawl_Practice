import string
import urllib.request as req
import pandas as pd

url="https://www.dcard.tw/f/girl"

request=req.Request(url,headers={
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36"
})
with req.urlopen(request) as response:
    data=response.read().decode("utf-8")
    
import bs4
root=bs4.BeautifulSoup(data,"html.parser")
titles=root.find_all("a",class_="tgn9uw-3 bJQtxM")

df=[]
for title in titles:
   df.append(title.string)
   
df1=(pd.DataFrame(df))
df1.to_csv('123',encoding='utf-8')
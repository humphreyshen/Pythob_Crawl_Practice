import string
import urllib.request as req
url="https://www.ptt.cc/bbs/index.html"

#建立一個request物件，附加 Request Headers的資訊
request=req.Request(url,headers={
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36"
})
with req.urlopen(request) as response:
    data=response.read().decode("utf-8")
#解析原始碼，取得每篇文章的標題
import bs4
root=bs4.BeautifulSoup(data,"html.parser")
titles=root.find_all("div", class_="board-title") #尋找class="board-title"的div標籤
for title in titles:
    print(title.string)
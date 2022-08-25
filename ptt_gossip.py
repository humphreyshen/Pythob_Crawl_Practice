import string
import urllib.request as req

def getData(url):
    #建立一個request物件，附加 Request Headers的資訊
    request=req.Request(url,headers={
        "cookie":"over18=1",
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36"
    })
    with req.urlopen(request) as response:
        data=response.read().decode("utf-8")
    #解析原始碼，取得每篇文章的標題

    import bs4
    root=bs4.BeautifulSoup(data,"html.parser")
    titles=root.find_all("div", class_="title")
    for title in titles:
        if title.a != None:
            print(title.a.string)

    #抓取上一頁的連結
    nextLink=root.find("a",string="‹ 上頁") #找到內文是‹ 上頁的a標籤
    return nextLink["href"]
# 主程序：抓取多個頁面的標題
pageURL="https://www.ptt.cc/bbs/Gossiping/index.html"
count=0
while count<5:
    pageURL="https://www.ptt.cc"+getData(pageURL)
    count+=1
print(pageURL)
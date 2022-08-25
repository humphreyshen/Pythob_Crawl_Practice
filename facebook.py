import pandas as pd
import re, time, requests
from selenium import webdriver
from bs4 import BeautifulSoup



def FindLinks(url, n):
    Links = []
    driver.get(url)
    username = 'h5534668@yahoo.com.tw'
    password = 'Hh5534668$'
    driver.get(url)
    for i in range(n):
        time.sleep(2)
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    driver.find_element_by_name("email").send_keys(username)
    driver.find_element_by_name("pass").send_keys(password)
    driver.find_element_by_css_selector("[aria-label=Accessible login button]").click()        
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source)
    posts = soup.findAll('div', {'class':'clearfix y_c3pyo2ta3'})
    for i in posts:
        Links.append('https://www.facebook.com' + i.find('a',{'class':'_5pcq'}).attrs['href'].split('?',2)[0])
    return Links

def expand(url):
    driver.get(url)
    try:
        driver.find_element_by_xpath('//a[@lang="en_US"]').click()
    except:
        print("Now is in EN_US")
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    # 點擊「comments」，藉以展開留言
    try:
        driver.find_element_by_xpath('//div[@class="_5pcr userContentWrapper"]//a[@data-testid="UFI2CommentsCount/root"]').click()
        time.sleep(1)
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(1)
        driver.find_element_by_id('expanding_cta_close_button').click() 
    except:
        print('There is no comment!')
    k = 1
    while k != 0:
        k = 0
        for i in driver.find_elements_by_xpath('//div[@class="_5pcr userContentWrapper"]//div[@data-testid="UFI2CommentsList/root_depth_0"]//a[@role="button"]'): 
            # 反覆偵測是否有「看更多留言」、「看更多回覆」與「看完整貼文內容」等按鈕，若有擇點擊
            if bool(re.search('comment|More|Repl',i.text)) == True :
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                time.sleep(2)
                try:
                    driver.find_element_by_xpath('//div[@style="display: block;"]//a[@id="expanding_cta_close_button"]').click()
                except:
                    print('No pupup!')
                try:
                    i.click()
                except:
                    print('Nothing')
                time.sleep(2)
                k += 1

# 文章內容與互動摘要
def PostContent(soup):
    # po文區塊
    userContent = soup.find('div', {'class':'_5pcr userContentWrapper'})
    # po文人資訊區塊
    PosterInfo = userContent.find('div', {'class':'l_c3pyo2v0u i_c3pynyi2f clearfix'})
    # 互動摘要區(讚、留言與分享)
    feedback = soup.find('form', {'class':'commentable_item collapsed_comments'})
    # 名稱
    Name = PosterInfo.find('img').attrs['aria-label']
    # ID
    ID = PosterInfo.find('a', {'class':'_5pb8 o_c3pynyi2g _8o _8s lfloat _ohe'}).attrs['href'].split('/?',2)[0].split('/',-1)[-1]
    # 網址
    Link = driver.current_url
    # 發文時間
    try:
        Time = PosterInfo.find('abbr').attrs['title']
    except:
        Time = PosterInfo.find('div', {'class':'_1atc fsm fwn fcg'}).text
    # 文章內容
    try:
        Content = userContent.find('div', {'class':'_5pbx userContent _3576'}).text
    except:
        Content = ""
    # Like
    try:
        Like = feedback.find('span', {'data-testid':'UFI2TopReactions/tooltip_LIKE'}).find('a').attrs['aria-label']
    except:
        Like = '0' 
    # Angry
    try:
        ANGER = feedback.find('span', {'data-testid':'UFI2TopReactions/tooltip_ANGER'}).find('a').attrs['aria-label']
    except:
        ANGER = '0'
    # HAHA
    try:
        HAHA = feedback.find('span', {'data-testid':'UFI2TopReactions/tooltip_HAHA'}).find('a').attrs['aria-label']
    except:
        HAHA = '0'
    # 留言
    try:
        commentcount = feedback.find('a', {'data-testid':'UFI2CommentsCount/root'}).text
    except:
        commentcount = '0' 
    # 分享
    try:
        share = feedback.find('span', {'class':'_355t _4vn2'}).text
    except:
        share = '0' 
    return pd.DataFrame(
        data = [{'Name':Name,
                 'ID':ID,
                 'Link':Link,
                 'Time':Time,
                 'Content':Content,
                 'Like':Like,
                 'ANGER':ANGER,
                 "HAHA":HAHA,
                 'commentcount':commentcount,
                 'share':share}],
        columns = ['Name', 'ID', 'Time', 'Content', 'Like', 'ANGER', 'HAHA', 'commentcount', 'share', 'Link'])

# 留言
def CrawlComment(soup):
    Comments = pd.DataFrame()
    # po文區塊
    userContent = soup.find('div', {'class':'_5pcr userContentWrapper'})
    # 用戶留言區
    userContent = soup.find('div', {'class':'_5pcr userContentWrapper'})
    # 回應貼文的留言
    for i in userContent.findAll('div', {'data-testid':'UFI2Comment/root_depth_0'}):
        try:
            CommentContent = i.find('span', {'dir':'ltr'}).text
        except:
            CommentContent = 'Sticker'
        Comment = pd.DataFrame(data = [{'CommentID':i.find('a', {'class':' _3mf5 _3mg0'}).attrs['data-hovercard'].split('id=',2)[1],
                                 'CommentName':i.find('img').attrs['alt'],
                                 'CommentTime':i.find('abbr',{'class':'livetimestamp'}).attrs['data-tooltip-content'],
                                 'CommentContent':CommentContent,
                                 'Link':driver.current_url}],
                        columns = ['CommentID', 'CommentName', 'CommentTime', 'CommentContent', 'Link'])
        Comments = pd.concat([Comments, Comment], ignore_index=True)
    
    # 回應留言的留言
    for i in userContent.findAll('div', {'data-testid':'UFI2Comment/root_depth_1'}):
        try:
            CommentContent = i.find('span', {'dir':'ltr'}).text
        except:
            CommentContent = 'Sticker'
        Comment = pd.DataFrame(data = [{'CommentID':i.find('a', {'class':' _3mf5 _3mg1'}).attrs['data-hovercard'].split('id=',2)[1],
                                 'CommentName':i.find('img').attrs['alt'],
                                 'CommentTime':i.find('abbr',{'class':'livetimestamp'}).attrs['data-tooltip-content'],
                                 'CommentContent':CommentContent,
                                 'Link':driver.current_url}],
                        columns = ['CommentID', 'CommentName', 'CommentTime', 'CommentContent', 'Link'])
        Comments = pd.concat([Comments, Comment], ignore_index=True)        
    return Comments

driver = webdriver.Chrome('/Users/humphreyshen/Desktop/Visual Code/Facebook_Crawler/chromedriver 2')
Links = FindLinks(url = 'https://www.facebook.com/scuaa.tw',
                  n = 3)
Links

# 抓下來所有留言
PostsInformation = pd.DataFrame()
PostsComments = pd.DataFrame()
for i in Links:
    print('Dealing with: ' + i)
    try:
        expand(i)
        soup = BeautifulSoup(driver.page_source)
        PostsInformation = pd.concat([PostsInformation, PostContent(soup)],ignore_index=True)
        PostsComments = pd.concat([PostsComments, CrawlComment(soup)],ignore_index=True)
    except:
        print('Load Failed: ' + i)

PostsInformation
PostsComments

PostsInformation.to_excel('C:/Users/TLYu0419/Desktop/PostsInformation.xlsx')
PostsComments.to_excel('C:/Users/TLYu0419/Desktop/PostsComments.xlsx')
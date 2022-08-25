from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import time, re
import csv
import datetime as dt
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

################################################################################################################################

#print('即將取得近 %d 天的貼文，欲取得的粉專共有 %d 個'%(dt_num, len(page_list)))
#print('\n>> 請注意，程式執行完畢後會自動關閉 Chrome 瀏覽器，請勿手動關閉以免程式錯誤。\n若出現防火牆訊息，可點選關閉或接受。')


print('>> 正在開啟瀏覽器...')
driver = webdriver.Chrome('/Users/humphreyshen/Desktop/Visual Code/Facebook_Crawler/chromedriver 2')
print('>> 開啟網頁中...')
driver.get('https://irs.thsrc.com.tw/IMINT/')
WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "btn-confirm"))
    )
driver.find_element_by_id('btn-confirm').click()
WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "selectStartStation"))
    )
driver.find_element_by_name('selectStartStation').click()
driver.find_element_by_xpath('//*[@id="content"]/tbody/tr[1]/td[2]/span/select/option[3]').click()
driver.find_element_by_name('selectDestinationStation').click()
driver.find_element_by_xpath('//*[@id="content"]/tbody/tr[1]/td[2]/select/option[8]').click()
driver.find_element_by_id('bookingMethod_1').click()

startdate = '2022-01-21'
driver.find_element_by_id('toTimeInputField').send_keys(startdate)
trainid='1327'
driver.find_element_by_name('toTrainIDInputField').send_keys(trainid)
catpchatext=input('請輸入驗證碼')
driver.find_element_by_id('securityCode').send_keys(catpchatext)
driver.find_element_by_id('SubmitButton').click()
idnumber='J122746040'
driver.find_element_by_id('idNumber').send_keys(idnumber)


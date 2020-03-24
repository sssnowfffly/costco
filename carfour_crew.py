from bs4 import BeautifulSoup
import urllib.parse,json,requests,time,sys,csv,os,cx_Oracle,urllib,re
import numpy as np
import pandas as pd
from urllib import request
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

def traceback(err):
    '''
    紀錄錯誤資訊。
    包含時間點(now)，錯誤內容(traceback)，以及行數。
    '''
    now = time.strftime('%H:%M:%S', time.localtime(time.time()))
    traceback = sys.exc_info()[2]
    print (str(now)+' '+str(err)+'\n'+'exception in line '+str(traceback.tb_lineno))

def execute_times(times):
    '''
    利用selenium來做到滾輪下滑的動作，TIMES指的是滑動次數
    '''
    for i in range(times + 1):
        web.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5)    
    
url='https://online.carrefour.com.tw/tw/'
resp = requests.get(url)
resp.encoding = 'utf-8'
soup = BeautifulSoup(resp.text, 'html.parser')
NoneType=None

tags=pd.DataFrame(columns=['BIG_TAG','MED_TAG','SMA_TAG','HREF'])

for i in soup.select('.nav-bar')[0].select('a'):
    try:
        print(i)
        if i['href']=="javascript:;":
            navname=i.text.replace('\n','')
            print(navname)
        
        elif i.find(class_='two-cate'):
            twocate=i.find(class_='two-cate').text
            print(twocate)
        else:
            tags1=pd.DataFrame([[navname,twocate,i.text,'https://online.carrefour.com.tw'+i['href']]],columns=['BIG_TAG','MED_TAG','SMA_TAG','HREF'])
            tags=pd.concat([tags,tags1],axis=0)
            print(tags)
    except Exception as err:
        traceback(err)
    print('-'*100)

web = webdriver.Chrome('chromedriver.exe')
web.maximize_window()

caitem=pd.DataFrame(columns=['BIG_TAG','MED_TAG','SMA_TAG','CA_ITEM_NAME','CA_ITEM_PRICE','HREF','UPDATE_TIME'])

for i in tags['HREF']:
    tStart = time.time()#計時開始
    print(i)
    web.get(i)

    bar=BeautifulSoup(web.find_element_by_class_name('breadcrumb-list').get_attribute('outerHTML'), 'html.parser').find_all('li')
    tag=[]
    for k in bar:
        tag.append(k.text)
    print(tag[1],tag[2],tag[3])
    execute_times(30)
    for j in web.find_elements_by_class_name('item-product'):
        try:
            itemall=BeautifulSoup(j.get_attribute('outerHTML'), 'html.parser')
            name=itemall.find(class_='item-name').text.replace(' ','').replace('\n','').split('/')[0]
            disprice=itemall.find(class_='discount-price').text.replace(' ','').replace('\n','').replace('$','')
            print(name,disprice)
            caitem1=pd.DataFrame([[tag[1],tag[2],tag[3],name,disprice,i,'20181226']],columns=['BIG_TAG','MED_TAG','SMA_TAG','CA_ITEM_NAME','CA_ITEM_PRICE','HREF','UPDATE_TIME'])
            caitem=pd.concat([caitem,caitem1],axis=0)
        except Exception as err:
            traceback(err)  
    tEnd = time.time()#計時結束
    print (round((tEnd - tStart)/60,2))

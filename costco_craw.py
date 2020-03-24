from bs4 import BeautifulSoup
import pandas as pd
import requests, time, re

#爬取COSTCO商品資料
url='https://www.costco.com.tw/'
a=requests.get(url)
soup=BeautifulSoup(a.text,'lxml')

#找尋型錄連結
link=[]

for i in soup.select('li'):
    try:
        aa=i.a['href']
        if len(aa.split('/')) == 5 :
            link.append('https://www.costco.com.tw'+aa)
            print('https://www.costco.com.tw'+aa)
    except:
        continue

#製作商品的DATAFRAME，欄位為：商品名稱、價格、商品編號
item=pd.DataFrame(columns=['NAME','PRICE','ITEMNO'])

#開始抓取
for j in link:
    r = requests.get(j)
    soupin=BeautifulSoup(r.text,'lxml')
    itemqty=int(soupin.find_all(class_='search-pagination-container hidden-xs')[0].text.replace(' ','').split('之')[1])
    print(j)
    #當數量小於100時，代表頁數已經到底
    if itemqty<=100:
            for i in soupin.find_all(class_='product-info-wrapper'):
                #商品名稱
                chname=i.find_all(class_="product-name-container")[0].text.split('\n')[1]
                #商品編號
                itemno=i.find_all(class_="product-name-container")[0].a['href'].split('/p/')[1]
                try:
                    #商品價格
                    price=i.find_all(class_="price-panel")[0].text.replace('\n','').replace('$','').replace('含運','')
                except:
                    try:
                        price=i.find_all(class_="price-panel-login")[0].text.replace('\n','').replace('$','').replace('含運','')
                    except:
                        print("price error")
                item1=pd.DataFrame([[chname,price,itemno]],columns=['NAME','PRICE','ITEMNO'])
                item=pd.concat([item,item1],axis=0)
                print(chname,itemno,price,'\n','-'*30)
    else:
        #計算頁數以便翻頁
        page=itemqty//100+1
        print('total page = '+str(page))
        
        #抓取商品
        for k in range(page):
            linkin=j+('?page={}').format(str(k))
            r = requests.get(linkin)
            soupin=BeautifulSoup(r.text,'lxml')
            print(linkin)
            print('now page = '+str(k))
            for i in soupin.find_all(class_='product-info-wrapper'):
                chname=i.find_all(class_="product-name-container")[0].text.split('\n')[1]
                itemno=i.find_all(class_="product-name-container")[0].a['href'].split('/p/')[1]
                try:
                    price=i.find_all(class_="price-panel")[0].text.replace('\n','').replace('$','').replace('含運','')
                except:
                    try:
                        price=i.find_all(class_="price-panel-login")[0].text.replace('\n','').replace('$','').replace('含運','')
                    except:
                        print("price error")
                
                item1=pd.DataFrame([[chname,price,itemno]],columns=['NAME','PRICE','ITEMNO'])
                item=pd.concat([item,item1],axis=0)
                print(chname,itemno,price,'\n','-'*30)
        
            time.sleep(5)
    time.sleep(5)

#輸出成CSV
item.to_csv('costcoitem.csv',index=None)

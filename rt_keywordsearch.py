 # -*- coding: utf-8 -*-
import urllib.parse
import requests,time,json,sys,csv,re
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

query_enc=urllib.parse.quote('綠茶')
url = "https://www.rt-mart.com.tw/mobile/index.php?action=product_search_mobile&prod_keyword=" + query_enc
headers = {'User-Agent': 'mozilla/5.0 (Linux; Android 6.0.1; '
           'Nexus 5x build/mtc19t applewebkit/537.36 (KHTML, like Gecko) '
           'Chrome/51.0.2702.81 Mobile Safari/537.36'}
resp = requests.get(url, headers=headers)
if not resp:
    print('no')
resp.encoding = 'utf-8'
soup = BeautifulSoup(resp.text, 'html.parser')
items = []
for elem in soup.find_all(class_='index_prolistbox'):
    item_name = elem.find('h3').text
    item_no =elem.find('a')['href'].split('prod_no=P')[1].split('&prod_sort_uid=')[0]
    item = {
        'name': item_name,
        'item_no': item_no,
    }
    items.append(item)
print(items)

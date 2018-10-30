# -*- coding: utf8 -*-
#author :- Jabed

import bs4, requests, sys, csv, #int()
import time
#base_url = sys.argv[1] or pyperclip.paste()
base_url = " "
arr = []
info = []
file = open('info.txt', 'w')
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36', 'cookie':'inweb'}
res = requests.get(base_url, headers=headers)
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, "html.parser")
elems = soup.select("li['data-href']")
title = soup.select('.input-control')[0].get('value')
#print (elems)
#time.sleep(100000)
mycsvfile = open(title + '.csv','a')
csv.writer(mycsvfile).writerow(['Name','Address','Contact','Rating'])
counter = 2
while len(elems) > 0:
    for j in range(len(elems)):
        url = elems[j].get('data-href')
        print (url)
        time.sleep(100000)
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text,"html.parser")
        print("Saving data for: %s" %(soup.select('span[itemprop="name"]')[0].getText()))
        arr.append(soup.select('span[itemprop="name"]')[0].getText())
        arr.append(soup.select('span[itemprop="streetAddress"]')[0].getText())
        rating = soup.select('.value-titles')[0].getText() if len(soup.select('.value-titles')) > 0 else 'NA'
        if (len(soup.select('.tel'))) != 0:
            contact = (soup.select('.tel b')[0].getText() if ((len(soup.select('.tel b'))) > 0) else soup.select('.tel')[0].getText())
        else:
            contact = 'NA'
        arr.append(contact)
        arr.append(rating)
        csv.writer(mycsvfile).writerow(arr)
        arr = []
    res = requests.get(base_url + '/page-' + str(counter), headers=headers)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    elems = soup.select("li['data-href']")
    counter += 1

        
    
    

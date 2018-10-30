# -*- coding: utf8 -*-
#author :- jabed

from bs4 import BeautifulSoup
from urllib.request import urlopen

def Data():
    baseUrl = '%s'


    cityState = [('', '')]

    bedroom = ['_1', '_', '_']

    citys = []
    prices = []
    addressList = []
    type = []
    zipcode = []
    numBed = []
    numBath = []
    for city in cityState:
        for bed in bedroom:
            URL = baseUrl % (city[0], city[1], bed)
            #request = urllib.request(URL, headers={'User-Agent': "Resistance is futile"})
            response = urlopen(URL)
            html = BeautifulSoup(response, 'html.parser')
            totalCount = int(html.find('span', {'class': 'total-listings-count'}).get_text())
            if totalCount >= 20:
                #pageTotal = int(html.find('span', {'class': 'total-listings-count'}).get_text())
            else:
                pageTotal = 1
            for i in range(5):
                newURL = URL + '?page=' + str(i + 1)
                #newReq = urllib2.Request(newURL, headers={'User-Agent': "Resistance is futile"})
                response = urlopen(newURL)
                html = BeautifulSoup(response, 'html.parser')
                items = html.find_all('div', {'class': 'prop li-srp'})
                for item in items:
                    price = str(item.find('p', {'class': 'prop-rent bullet-separator strong'}).get_text()).replace(',', '')
                    if price != 'Contact for Pricing':
                        if 'From' in price:
                            prices.append(int(price[6:]))
                        elif ' ' not in price:
                            prices.append(int(price[1:]))
                        else:
                            prices.append(int(price[1:price.index(' ')]))
                        citys.append(city[1])
                        type.append('Rent')
                        link = item.a['href']
                        res = urlopen('' + link)
                        ht = BeautifulSoup(res, 'html.parser')
                        address = str(ht.find('span', {'itemprop': 'streetAddress'}).get_text())
                        addressList.append(address)
                        postal = str(ht.find('span', {'itemprop': 'postalCode'}).get_text())
                        zipcode.append(postal)
                        numOfBed = str(item.find('span', {'class': 'prop-beds bullet-separator'}).get_text())
                        numBed.append(int(numOfBed[0]))
                        numOfBath = str(item.find('span', {'class': 'prop-baths bullet-separator'}).get_text())
                        numBath.append(int(numOfBath[0]))
    output = zip(addressList, zipcode, prices, type, citys, numBed, numBath)
    #return output
if __name__ == "__main__":
    Data()
    with open('rent_com.csv', 'wb') as f:
        writer = csv.writer(f)
        for row in output:
            writer.writerow(row)

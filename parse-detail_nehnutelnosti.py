#!/usr/bin/python
# coding=utf-8

## time-spent: 1
import re
import sys
import reality
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')

soup = BeautifulSoup(sys.stdin, 'html.parser')

columns = ["url", "title", "text", "agency", "agency_person", "price", "price_currency", "street", "city", "district", "price", "offer", "category", "condition", "area_usable"]

info = {}

info["title"] = unicode(soup.find('h1')).replace("\n", " ").replace("\r", " ").strip()
info["agency"] = soup.find('div', class_='brokerContacts').find('a').string.strip()
if soup.find_all('div', class_='brokerContacts')[1].find('p').string:
    info["agency_person"] = soup.find_all('div', class_='brokerContacts')[1].find('p').string.strip()
info["text"] = unicode(soup.find('p', class_='popis')).replace("\n", " ").replace("\r", " ")

for item in soup.find('div', id='params').find_all('p', {'class':['paramNo0', 'paramNo1']}):
    prop = item.find('span').string.strip()

    if prop == 'Lokalita:':
        if item.find('strong', class_='street'):
            info["street"] = item.find('strong', class_='street').string.strip()
    
        try:
            info["city"] = item.find('strong', class_='location').contents[1][2:]
        except:
            pass
        info["district"] =  item.find('span', class_='left150').string[6:]
    else:
        info[prop] = unicode(item.find('strong').string).strip()

    if prop == 'Cena:':
        info[prop] = re.sub(r"\s+", "", info[prop], flags=re.UNICODE)[:-1]
    elif prop == u'Úžitková plocha:':
        info[prop] = info[prop][:-3]

## unification
reality.renameKey(info, 'Cena:', 'price')
reality.renameKey(info, 'Typ:', 'offer')
reality.renameKey(info, 'Druh:', 'category')
reality.renameKey(info, 'Stav:', 'condition')
reality.renameKey(info, u'Úžitková plocha:', 'area_usable')

info['price_currency'] = u'EUR'
info.pop(u'Dátum aktualizácie:')

info["url"] = sys.argv[1]

reality.printAdv([info], 'csv', columns)


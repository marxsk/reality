#!/usr/bin/python
# coding=utf-8

## time-spent: 1.5 + 1
import re
import sys
import reality
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')

soup = BeautifulSoup(sys.stdin, 'html.parser')

info = {}

columns = ["url", "title", "text", "agency", "agency_person", "price", "price_currency", "type", "offer", "floor", "floor_max", "area_usable", "street", "id_estate", "condition", "attr_elevator", "attr_balcony", "attr_cellar"]

info["title"] = soup.find('h1').string.strip()

if soup.find('div', class_='contact'):
    info["agency"] = soup.find('div', class_='contact').find('strong').string.strip()
    info["agency_person"] = soup.find('div', class_='contactBox').find('strong').string.strip()

for item in soup.find('div', class_='properties').find('ul').find_all('li'):
    prop = item.find('span').string.strip()

    if prop == '':
        continue

    if prop in [u'Cena vrátane provízie', u'Cena']:
        info["price"] = item.find('meta', itemprop='price').attrs['content']
        info["price_currency"] = item.find('meta', itemprop='currency').attrs['content']
    elif prop == u'Kategória':
        info["type"] = item.find('strong').find('span').string
        info["offer"] = item.find('strong').contents[1].strip()[2:]
    elif prop == u'Poschodie':
        value = item.find('strong').string
        (current, max) = value.split(' / ')
        info["floor"] = current
        if max:
            info["floor_max"] = max
    elif u'plocha' in prop:
        info['area_usable'] = item.find('strong').contents[0][:-2]
    else:
        info[prop] = item.find('strong').string

info["text"] = unicode(soup.find('p', itemprop='description')).replace("\n", " ").replace("\r", " ")
info["url"] = sys.argv[1]

## unification
reality.renameKey(info, u'Úžitková plocha', 'area_usable')
reality.renameKey(info, u'Ulica', 'street')
reality.renameKey(info, u'Identifikačné číslo:', 'id_estate')
reality.renameKey(info, u'Stav nehnuteľnosti:', 'condition')
reality.renameKey(info, u'Výťah', 'attr_elevator')
reality.renameKey(info, u'Balkón / loggia', 'attr_balcony')
reality.renameKey(info, u'Pivnica', 'attr_cellar')


info.pop(u'Aktualizácia')

reality.printAdv([info], 'csv', columns)
